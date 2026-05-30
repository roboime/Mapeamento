# Manual - NUVEM_DE_PONTOS_DENSA versão 1.0

## NÓ - CÂMERA

```python
ros2 run usb_cam usb_cam_node_exe --ros-args     -p video_device:=/dev/video0     -p pixel_format:="mjpeg2rgb"     -p camera_info_url:="file:///home/roboime/dev/rtab/camera.yaml"     -p frame_id:=default_cam
```
Obs: verifique o caminho do .yaml e se a câmera está configurada como video0!

## NÓ - Midas

```python
python3 midas_ros2.py
```
Obs: verifique se está na pasta do projeto!


## NÓ - RTAB

```python
ros2 launch rtabmap_launch rtabmap.launch.py     rtabmap_args:="--delete_db_on_start --Vis/MinInliers 10 --Mem/IncrementalMemory true"     rgb_topic:=/image_raw     depth_topic:=/camera/depth_registered     camera_info_topic:=/camera_info     frame_id:=default_cam     approx_sync:=true     approx_sync_max_interval:=0.7     wait_imu_to_init:=false     qos:=1    visual_odometry:=true
```
(base) roboime@roboime-kubuntu:~/dev/rtab$ python3 midas_ros2.py

A module that was compiled using NumPy 1.x cannot be run in
NumPy 2.2.6 as it may crash. To support both 1.x and 2.x
versions of NumPy, modules must be compiled with NumPy 2.0.
Some module may need to rebuild instead e.g. with 'pybind11>=2.12'.

If you are a user of the module, the easiest solution will be to
downgrade to 'numpy<2' or try to upgrade the affected module.
We expect that some modules will need time to support NumPy 2.

Traceback (most recent call last):  File "/home/roboime/dev/rtab/midas_ros2.py", line 4, in <module>
    from cv_bridge import CvBridge
  File "/opt/ros/jazzy/lib/python3.12/site-packages/cv_bridge/__init__.py", line 6, in <module>
    from cv_bridge.boost.cv_bridge_boost import cvtColorForDisplay, getCvType
Traceback (most recent call last):
  File "/home/roboime/miniforge3/li
# Dependências
## ROS JAZZY
Passo a passo:
1. Configurar o Local:
O ROS 2 requer que o seu ambiente utilize codificação UTF-8.
```python
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

2. Configurar Repositórios
Adicione o repositório ROS 2 para que o sistema saiba onde encontrar os pacotes.
* Habilitar o Repositório Universe do Ubuntu:
```python
sudo apt install software-properties-common
sudo add-apt-repository universe
```

* Adicionar a Chave GPG do Repositório ROS 2:
```
sudo apt update && sudo apt install curl
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
```

Adicionar o Repositório ROS 2:
```python
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

3. Instalar o ROS 2

```python
sudo apt update
sudo apt upgrade
sudo apt install ros-jazzy-desktop
sudo apt install ros-jazzy-ros-base
```

4. Configurar o Ambiente
   
```python
source /opt/ros/jazzy/setup.bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```
* SE APARECER UM ERRO COMO?
  ```python
  E: Conflicting values set for option Signed-By regarding source http://packages.ros.org/ros2/ubuntu/ noble: /usr/share/keyrings/ros-archive-keyring.gpg != -----BEGIN PGP PUBLIC KEY BLOCK-----

   mQINBFzvJpYBEADY8l1YvO7iYW5gUESyzsTGnMvVUmlV3XarBaJz9bGRmgPXh7jc

   VFrQhE0L/HV7LOfoLI9H2GWYyHBqN5ERBlcA8XxG3ZvX7t9nAZPQT2Xxe3GT3tro

   u5oCR+SyHN9xPnUwDuqUSvJ2eqMYb9B/Hph3OmtjG30jSNq9kOF5bBTk1hOTGPH4

   K/AY0jzT6OpHfXU6ytlFsI47ZKsnTUhipGsKucQ1CXlyirndZ3V3k70YaooZ55rG

   aIoAWlx2H0J7sAHmqS29N9jV9mo135d+d+TdLBXI0PXtiHzE9IPaX+ctdSUrPnp+

   TwR99lxglpIG6hLuvOMAaxiqFBB/Jf3XJ8OBakfS6nHrWH2WqQxRbiITl0irkQoz

   pwNEF2Bv0+Jvs1UFEdVGz5a8xexQHst/RmKrtHLct3iOCvBNqoAQRbvWvBhPjO/p

   V5cYeUljZ5wpHyFkaEViClaVWqa6PIsyLqmyjsruPCWlURLsQoQxABcL8bwxX7UT

   hM6CtH6tGlYZ85RIzRifIm2oudzV5l+8oRgFr9yVcwyOFT6JCioqkwldW52P1pk/

   /SnuexC6LYqqDuHUs5NnokzzpfS6QaWfTY5P5tz4KHJfsjDIktly3mKVfY0fSPVV

   okdGpcUzvz2hq1fqjxB6MlB/1vtk0bImfcsoxBmF7H+4E9ZN1sX/tSb0KQARAQAB

   tCZPcGVuIFJvYm90aWNzIDxpbmZvQG9zcmZvdW5kYXRpb24ub3JnPokCVAQTAQgA

   PgIbAwULCQgHAgYVCgkICwIEFgIDAQIeAQIXgBYhBMHPbjHmut6IaLFytPQu1vur

   F8ZUBQJoEhoGBQkUtHZwAAoJEPQu1vurF8ZUv1AP/2gID+uw7pw3WpPevny3pliZ

   JeDx4Y+ut+5c2nCfkpUc3lG50v9ly4ZpNQTWKIm9yB6dxgary7EKpAlGVmiU75JA

   LyftVtjeyQcre2f7Z00u2lXw8Red52AsWHkh/dtctgLSGQiJdTd0donO6cszZFVa

   sCiFdRKlizGvBkE8uFdKYMGixOgnvQZrb9OLqRsoj10aDzN0X3NJk1LTxiS3+udY

   poOk2Bm9VGyrNmgIrYiNqbYPBHYkWGHBqJxvAK92lJ2I/n6X4U8r6sMdDE7QDw4j

   FMdrxC0XmCL4cFPkkR1qadtJy9FiCtpKyqiKuUsCG6AUi5EOY+7Y3oSpKn8Wp1K5

   VMbv12JRIatDIeaAnwa2qyBQVAVC1F/OqWUFKluPjKyMR3DXKwjxpt1P+HUmda0w

   HcnhFIu2th/egmGKH5e3atcVxjAxYfm+f92MN7fFEuFQsMZhI/gt3IgESWrgdaAz

   opRInrMz7yEtz3VaaehwmUUR2gevPQMzBRaA+NIqMLDUvV5jujvFe8c1VUtBLTYc

   /alBiM/Mo1niy3aUfDahzhTr6zz+ur6BFRnNFWv56M3NOVlreNm3NIbNX2kTKh0Z

   QJSSCklJuDUqnPmAzT2BZWUpwfe7QYRwvQhF0YB2N1LavyNwiyfinCQlAh+Q9eme

   2jqGsxvQym3sAPnWvA68

   =xH9H

   -----END PGP PUBLIC KEY BLOCK-----

E: The list of sources could not be read.
```
PARA RESOLVER:
Você precisa limpar a configuração antiga e garantir que apenas a nova e correta chave e o formato de arquivo de lista sejam usados.
Passo 1: Limpar todas as chaves e listas do ROS

```python
sudo rm -f /etc/apt/sources.list.d/ros2.list
```

Remova a Chave GPG do Local Padrão: Remove a chave que você baixou.
```python
sudo rm -f /usr/share/keyrings/ros-archive-keyring.gpg
```
Verifique o Arquivo Principal de Fontes (/etc/apt/sources.list): É muito raro, mas pode haver uma linha de ROS aqui.

```python
grep "ros2" /etc/apt/sources.list
```

Se retornar alguma linha, você precisará editá-la manualmente (ex: sudo nano /etc/apt/sources.list) e removê-la.
Verifique Fontes Antigas no Diretório sources.list.d: Liste todos os arquivos de configuração de fontes para garantir que não haja outro arquivo ROS de uma tentativa anterior (ex: ros.list, ros
-ubuntu.list).
```python
    ls -l /etc/apt/sources.list.d/
```
Se você vir algum arquivo relacionado a ROS 2, remova-o.

Passo 2: Reinstalar o Repositório do ROS 2 do Zero

Agora que limpamos o sistema de referências conflitantes, vamos refazer os passos de configuração.

    Baixar a Chave GPG Novamente:
```python
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
```    

Adicionar o Repositório ROS 2 com a Sintaxe Correta para Noble (24.04) e atualizar o apt:
```python
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu noble main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
    sudo apt update
```

Se o sudo apt update finalmente rodar sem erros, você pode prosseguir para a instalação do ROS Jazzy:
```python
    sudo apt install ros-jazzy-desktop
```
Limpeza Final
Remova o link simbólico ros2.sources:
```python
    sudo rm -f /etc/apt/sources.list.d/ros2.sources
```

Remova o arquivo de fontes original (Se existir, pois foi para onde o link apontava):
```python
    sudo rm -f /usr/share/ros-apt-source/ros2.sources
```
    
Configurar ROS 2 Jazzy (Método ros2.sources para Ubuntu 24.04)
Vamos configurar o repositório ROS 2 usando o método mais robusto e moderno que o ROS Foundation fornece, que usa a ferramenta apt-key (para compatibilidade) e o novo formato .sources. Além disso, adicionar a Chave GPG:
```python
    sudo apt update

    sudo apt install curl gnupg lsb-release -y
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
```

Configurar o Repositório ROS 2 (Usando o formato .sources moderno): Este comando utiliza o nome do seu sistema operacional (noble) para garantir a configuração correta do ROS Jazzy.
```python
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```
Obs: Embora o .sources seja o preferido, a criação de ros2.list com signed-by é o método canônico do tutorial do ROS e deve funcionar perfeitamente após a limpeza.

Atualização e Instalação

Agora, execute a atualização do apt. Se tudo estiver limpo, desta vez deve funcionar. Se o comando acima for bem-sucedido (sem erros E: Conflicting values), você pode finalmente instalar o ROS 2 Jazzy:
Bash
```python
    sudo apt update
    sudo apt install ros-jazzy-desktop
```

Para saber se o ROS 2 Jazzy Jalisco foi baixado e instalado corretamente, você precisa executar o teste básico e verificar se os comandos do ROS 2 estão disponíveis no seu terminal.
1. Configurar o Ambiente
Você precisa garantir que o terminal saiba onde procurar os comandos do ROS 2. Execute o comando de source para carregar o ambiente do ROS Jazzy:
```python
    source /opt/ros/jazzy/setup.bash
```

2. Teste Básico: Comando ros2

O teste mais rápido é verificar se o comando principal do ROS 2 funciona.Execute:
```python
    ros2 -h
```
        Sucesso: Se a instalação foi bem-sucedida, o terminal exibirá a mensagem de ajuda do comando ros2, listando todos os subcomandos disponíveis (run, topic, node, etc.).

        Falha: Se o terminal retornar command not found, o ambiente ROS não foi carregado (veja o passo 1) ou a instalação falhou.

## Dependências do Midas(Não foi testado essa forma de baixar)
OBS: tem que ter o pip instalado.
```python
pip3 install torch torchvision opencv-python numpy timm
sudo apt update
sudo apt install ros-jazzy-cv-bridge ros-jazzy-vision-opencv ros-jazzy-sensor-msgs
wget https://github.com/intel-isl/MiDaS/releases/download/v3_1/dpt_beit_large_512.pt
```
## Dependências do RTAB_MAP
```python
sudo apt update
sudo apt install ros-jazzy-rtabmap-ros
sudo apt install ros-jazzy-rtabmap-viz
ros2 pkg list | grep rtabmap
```
Se aparecer rtabmap_ros e rtabmap_msgs, a instalação foi um sucesso.

## Dependências da Câmera
```python
sudo apt update
sudo apt install ros-jazzy-usb-cam
```
## Vizualizar os mapas
```python
sudo apt install meshlab
```
E para abrir:
```python
meshlab /caminho/do/arquivo.ply
```


rqt_graph



rqt_graph


conda deactivate
