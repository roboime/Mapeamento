Cria o ambiente virtual
sudo apt install python3-venv
python3 -m venv ~/mapeamento/midas_ws/venv --system-site-packages
source ~/mapeamento/midas_ws/venv/bin/activate

Baixa dependencias
pip install torch torchvision opencv-python numpy timm

source /opt/ros/jazzy/setup.bash
source ~/mapeamento/midas_ws/venv/bin/activate (só precisa rodar isso se o env não tiver ativado)

NÓ - CÂMERA
ros2 run usb_cam usb_cam_node_exe --ros-args     -p video_device:=/dev/video0     -p pixel_format:="mjpeg2rgb"     -p camera_info_url:="file:///home/roboime/dev/rtab/camera.yaml"     -p frame_id:=default_cam
Obs: verifique o caminho do .yaml e se a câmera está configurada como video0!

NÓ - Midas
python3 midas_ros2.py
Obs: verifique se está na pasta do projeto!

NÓ - RTAB
ros2 launch rtabmap_launch rtabmap.launch.py     rtabmap_args:="--delete_db_on_start --Vis/MinInliers 10 --Mem/IncrementalMemory true"     rgb_topic:=/image_raw     depth_topic:=/camera/depth_registered     camera_info_topic:=/camera_info     frame_id:=default_cam     approx_sync:=true     approx_sync_max_interval:=0.7     wait_imu_to_init:=false     qos:=1    visual_odometry:=true
