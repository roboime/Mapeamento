# Cria o ambiente virtual:
```bash
sudo apt install python3-venv 
python3 -m venv ~/mapeamento/map_anything_ws/venv --system-site-packages 
source ~/mapeamento/map_anything_ws/venv/bin/activate
```

```bash
python3 -m venv ~/mapeamento/mapanything_ws/venv --system-site-packages
source ~/mapeamento/mapanything_ws/venv/bin/activate
```

```bash
git clone https://github.com/facebookresearch/map-anything.git
cd map-anything
pip install -e .
pip install torch torchvision numpy
```
```bash
python3 map_node.py
```
OBS: Nesse ultimo comando tem que verificar se está na mesma pasta onde está o map_node
