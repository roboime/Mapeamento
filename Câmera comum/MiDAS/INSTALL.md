Cria o ambiente virtual
sudo apt install python3-venv
python3 -m venv ~/mapeamento/midas_ws/venv --system-site-packages
source ~/mapeamento/midas_ws/venv/bin/activate

Baixa dependencias
pip install torch torchvision opencv-python numpy timm

source /opt/ros/jazzy/setup.bash
source ~/mapeamento/midas_ws/venv/bin/activate (só precisa rodar isso se o env não tiver ativado)
python3 midas_ros2.py

