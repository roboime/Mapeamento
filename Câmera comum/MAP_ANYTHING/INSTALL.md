Cria o ambiente virtual 
sudo apt install python3-venv python3 -m venv ~/mapeamento/midas_ws/venv --system-site-packages source ~/mapeamento/midas_ws/venv/bin/activate

python3 -m venv ~/mapeamento/mapanything_ws/venv --system-site-packages
source ~/mapeamento/mapanything_ws/venv/bin/activate

git clone https://github.com/facebookresearch/map-anything.git
cd map-anything
pip install -e .
pip install torch torchvision numpy
