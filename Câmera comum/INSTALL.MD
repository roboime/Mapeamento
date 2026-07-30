sudo apt install ros-jazzy-usb-cam


ros2 run usb_cam usb_cam_node_exe --ros-args \
    -p video_device:=/dev/video0 \
    -p pixel_format:=mjpeg2rgb \
    -p camera_info_url:=file:///caminho/valido/camera.yaml \
    -p frame_id:=default_cam
