import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import torch
import numpy as np

class MidasDepthNode(Node):
    def __init__(self):
        super().__init__('midas_depth_node')
        
        # --- Parâmetros Ajustáveis ---
        # MiDaS_small é muito mais rápido e ideal para rodar em tempo real
        self.declare_parameter('model_type', 'MiDaS_small') 
        model_type = self.get_parameter('model_type').value
        
        self.get_logger().info(f'Carregando modelo {model_type}... (Isso pode demorar na primeira vez)')
        
        # --- Configuração da IA (MiDaS) ---
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.midas = torch.hub.load("intel-isl/MiDaS", model_type)
        self.midas.to(self.device)
        self.midas.eval()
        
        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        self.transform = midas_transforms.small_transform if model_type == "MiDaS_small" else midas_transforms.dpt_transform

        # --- Configuração ROS ---
        self.bridge = CvBridge()
        # Inscreve na imagem raw da câmera USB
        self.sub = self.create_subscription(Image, '/image_raw', self.image_callback, 10)
        # Publica no tópico que o RTAB-Map espera
        self.pub_depth = self.create_publisher(Image, '/camera/depth_registered', 10)
        
        self.get_logger().info('MiDaS Node pronto! Aguardando imagens...')

    def image_callback(self, msg):
        try:
            # 1. Converter ROS -> OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
            original_size = cv_image.shape[:2]

            # 2. Prepara imagem para IA
            img_rgb = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            input_batch = self.transform(img_rgb).to(self.device)

            # 3. Inferência (Gerar o mapa de profundidade)
            with torch.no_grad():
                prediction = self.midas(input_batch)
                
                # Redimensionar para o tamanho original da câmera (640x480)
                prediction = torch.nn.functional.interpolate(
                    prediction.unsqueeze(1),
                    size=original_size,
                    mode="bicubic",
                    align_corners=False,
                ).squeeze()

            # Passar para CPU numpy
            depth_map = prediction.cpu().numpy()

            # 4. Conversão Matemática (Disparidade -> Metros)
            # O MiDaS retorna "Disparidade Inversa" (Perto = Valor Alto, Longe = Valor Baixo)
            # Precisamos inverter isso para Metros (Perto = Valor Baixo, Longe = Valor Alto)
            
            # Normaliza os valores brutos para 0 a 1 para estabilidade
            depth_min = depth_map.min()
            depth_max = depth_map.max()
            # Evita divisão por zero se a imagem for sólida
            if (depth_max - depth_min) > 0:
                depth_norm = (depth_map - depth_min) / (depth_max - depth_min)
            else:
                depth_norm = depth_map

            # FÓRMULA MÁGICA: Inversão e Escala
            # "15.0" é um fator de escala arbitrário (ajuste se o mapa parecer muito pequeno/grande)
            # "+ 0.1" evita divisão por zero
            # O resultado é uma estimativa em METROS.
            depth_meters = 15.0 / (depth_norm * 10 + 0.5) 
            
            # CLIP: Cortar valores absurdos. 
            # Dizemos ao ROS que nada está mais perto que 20cm ou mais longe que 10m.
            depth_meters = np.clip(depth_meters, 0.2, 10.0)

            # 5. Publicar ROS (Encoding 32FC1 é obrigatório para precisão float)
            depth_msg = self.bridge.cv2_to_imgmsg(depth_meters.astype(np.float32), encoding="32FC1")
            
            # CRUCIAL: Copiar o timestamp da imagem original para sincronia!
            depth_msg.header = msg.header 
            # Força o frame_id correto caso esteja vindo errado
            # depth_msg.header.frame_id = "default_cam" 
            
            self.pub_depth.publish(depth_msg)

        except Exception as e:
            self.get_logger().error(f'Erro no processamento: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = MidasDepthNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
