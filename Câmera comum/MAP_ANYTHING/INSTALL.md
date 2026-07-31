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

ros2 launch rtabmap_launch rtabmap.launch.py     rtabmap_args:="--delete_db_on_start --Vis/MinInliers 10 --Mem/IncrementalMemory true"     rgb_topic:=/camera/rgb_local     depth_topic:=/camera/depth_registered     camera_info_topic:=/camera_info     frame_id:=camera_optical_frame     approx_sync:=true     approx_sync_max_interval:=0.2     wait_imu_to_init:=false     qos:=1     visual_odometry:=true
