import os
import sys

# --- 1. Configurações de Ambiente (Otimização de VRAM) ---
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import torch
import numpy as np
import torch.nn.functional as F

# --- 2. Importação Segura ---
try:
    from mapanything.models import MapAnything
except ImportError:
    print("\nERRO CRÍTICO: Biblioteca 'MapAnything' não encontrada.")
    sys.exit(1)

class MapAnythingNode(Node):
    def __init__(self):
        super().__init__('map_anything_node')
        
        self.get_logger().info('--- Inicializando MapAnything ROS 2 (Versão Final: Resize Fix) ---')

        # Configuração do Dispositivo
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.get_logger().info(f'Usando dispositivo: {self.device}')
        
        # Carrega o modelo
        try:
            self.model = MapAnything.from_pretrained("facebook/map-anything").to(self.device)
            self.model.eval()
        except Exception as e:
            self.get_logger().error(f'Falha ao carregar modelo: {e}')
            sys.exit(1)

        # Configuração ROS
        self.sub = self.create_subscription(Image, '/image_raw', self.image_callback, 10)
        self.pub_depth = self.create_publisher(Image, '/camera/depth_registered', 10)
        
        self.get_logger().info('Nó pronto! Aguardando imagens...')

    def manual_imgmsg_to_cv2(self, msg):
        """ Converte sensor_msgs/Image para NumPy manualmente """
        dtype = np.uint8
        n_channels = 3
        img = np.frombuffer(msg.data, dtype=dtype)
        try:
            img = img.reshape((msg.height, msg.width, n_channels))
        except ValueError:
            return None
        return img

    def manual_cv2_to_imgmsg(self, cv_image, original_header):
        """ Converte NumPy (Float32) para sensor_msgs/Image (32FC1) """
        msg = Image()
        msg.header = original_header
        msg.height = cv_image.shape[0]
        msg.width = cv_image.shape[1]
        msg.encoding = "32FC1"
        msg.is_bigendian = 0
        msg.step = msg.width * 4
        msg.data = cv_image.astype(np.float32).tobytes()
        return msg

    def preprocess_image(self, cv_image, encoding):
        """ 
        Prepara a imagem: Cor -> Resize (Múltiplo de 14) -> Tensor 
        """
        # 1. Ajuste de Cor
        if encoding == 'bgr8':
            img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        elif encoding == 'rgb8':
            img = cv_image
        else:
            img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

        # --- FIX: OBRIGATÓRIO SER MÚLTIPLO DE 14 ---
        h, w = img.shape[:2]
        patch_size = 14
        
        # Calcula nova altura/largura que sejam múltiplos de 14
        new_h = int(round(h / patch_size) * patch_size)
        new_w = int(round(w / patch_size) * patch_size)
        
        # Se necessário, redimensiona
        if new_h != h or new_w != w:
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
        # -------------------------------------------

        # 2. Normalização (0.0 a 1.0)
        img = img.astype(np.float32) / 255.0
        
        # 3. Transforma em Tensor e adiciona Batch
        img_tensor = torch.from_numpy(img).permute(2, 0, 1).unsqueeze(0)
        
        return img_tensor.to(self.device)

    def image_callback(self, msg):
        try:
            # 1. Conversão ROS
            cv_image = self.manual_imgmsg_to_cv2(msg)
            if cv_image is None: return
            original_h, original_w = cv_image.shape[:2]

            # 2. Pré-processamento (Já inclui o resize p/ múltiplo de 14)
            input_tensor = self.preprocess_image(cv_image, msg.encoding)
            
            # 3. Definição da View (Com correções de lista e strings)
            views = [{
                "img": input_tensor,
                "data_norm_type": ["dinov2"], # Lista obrigatória
                "idx": 0,
                "instance": "camera_0"
            }]

            # 4. Inferência
            with torch.no_grad():
                predictions = self.model.infer(
                    views,
                    memory_efficient_inference=False, 
                    use_amp=True,
                    amp_dtype="bf16", # Se der erro, mude para "fp16"
                    apply_mask=True,
                    mask_edges=True
                )

            # 5. Processamento da Saída
            pred = predictions[0]
            depth_map = pred["depth_z"] 

            # Redimensionamento Reverso
            # (A IA processou no tamanho múltiplo de 14, mas o ROS quer o tamanho original)
            if depth_map.shape[1] != original_h or depth_map.shape[2] != original_w:
                depth_map = F.interpolate(
                    depth_map.permute(0, 3, 1, 2),
                    size=(original_h, original_w), 
                    mode="nearest" # Nearest é mais rápido, Bicubic é mais suave
                ).permute(0, 2, 3, 1)

            # Conversão final
            depth_meters = depth_map.squeeze().cpu().numpy()
            
            # Limpa valores inválidos
            depth_meters = np.nan_to_num(depth_meters, nan=0.0, posinf=0.0, neginf=0.0)

            # 6. Publicação
            depth_msg = self.manual_cv2_to_imgmsg(depth_meters, msg.header)
            self.pub_depth.publish(depth_msg)

        except Exception as e:
            # Mostra o erro mas tenta não crashar o nó
            self.get_logger().error(f'Erro no ciclo: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = MapAnythingNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()
