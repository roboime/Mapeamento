
git clone https://github.com/UZ-SLAMLab/ORB_SLAM3.git ORB_SLAM3

O CMakeLists.txt do repositorio oficial está desatualizado, é necessário trocar ele pelo nosso cmakelists que está na pasta orbslam3

Após isso, colar o arquivo mono_cam.cc no diretório ORB_SLAM3/Examples/Monocular/

cd ORB_SLAM3
chmod +x build.sh
./build.sh

Outro comando

./Examples/Monocular/mono_cam Vocabulary/ORBvoc.txt ./Examples/Monocular/camera.yaml
