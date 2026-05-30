#include<iostream>
#include<opencv2/opencv.hpp>
#include<System.h>

int main(int argc, char **argv)
{
    if(argc != 3 && argc != 4)
    {
        std::cout << "Uso: ./mono_cam ORBvoc.txt Camera.yaml [video_file]\n";
        std::cout << "Se video_file não for fornecido, usa câmera padrão\n";
        return 1;
    }

    cv::VideoCapture cap;
    double fps = 30.0;

    if(argc == 4) {
        std::string video_path = argv[3];
        cap.open(video_path);
        std::cout << "Abrindo vídeo: " << video_path << std::endl;

        if(!cap.isOpened()) {
            std::cout << "ERRO: Não consegui abrir o vídeo: " << video_path << std::endl;
            return -1;
        }

        fps = cap.get(cv::CAP_PROP_FPS);
        int total_frames = cap.get(cv::CAP_PROP_FRAME_COUNT);
        std::cout << "Vídeo info - FPS: " << fps << ", Frames: " << total_frames << std::endl;

    } else {
        cap.open(0);
        std::cout << "Abrindo câmera padrão (FPS setado para " << fps << ")" << std::endl;

        if(!cap.isOpened()) {
            std::cout << "ERRO: Não consegui abrir a câmera!\n";
            return -1;
        }

        cap.set(cv::CAP_PROP_FRAME_WIDTH, 640);
        cap.set(cv::CAP_PROP_FRAME_HEIGHT, 480);
        cap.set(cv::CAP_PROP_FPS, fps);
    }

    // Inicializa SLAM COM visualização do Pangolin
    ORB_SLAM3::System SLAM(argv[1], argv[2], ORB_SLAM3::System::MONOCULAR, true);

    std::cout << "Sistema ORB-SLAM3 inicializado!\n";
    std::cout << "Feche a janela do 'Map Viewer' para sair...\n";

    cv::Mat frame;
    double timestamp = 0.0;
    int frame_count = 0;
    bool user_exit = false;

    while(true)
    {
        cap >> frame;
        if(frame.empty()) {
            if(argc == 4) {
                std::cout << "Fim do vídeo atingido!\n";
            } else {
                std::cout << "ERRO: Frame vazio da câmera!\n";
            }
            break;
        }

        // Timestamp correto
        if(argc == 4) {
            timestamp = (double)frame_count / fps;
        } else {
            timestamp = (double)cv::getTickCount() / cv::getTickFrequency();
        }

        frame_count++;

        // Processa frame
        SLAM.TrackMonocular(frame, timestamp);

        // ⚠️ REMOVA completamente o OpenCV imshow/waitKey
        // Para verificar se o usuário quer sair, use um método simples:

        // Mostra progresso a cada 100 frames
        if(frame_count % 100 == 0) {
            std::cout << "Processados " << frame_count << " frames...\n";
            std::cout << "Pressione Ctrl+C no terminal para sair\n";
        }

        // Verificação simples - se processou muitos frames, assume que o vídeo acabou
        if(argc == 4 && frame_count > 10000) {
            std::cout << "Muitos frames processados, assumindo fim...\n";
            break;
        }
    }

    std::cout << "Finalizando SLAM...\n";

    // ⚠️ REMOVA SaveAtlas - é privado!
    // SLAM.SaveAtlas(1); // REMOVA ESTA LINHA

    // Tenta salvar em diferentes formatos
    try {
        SLAM.SaveTrajectoryKITTI("CameraTrajectory_KITTI.txt");
        std::cout << "Trajetória KITTI salva\n";
    } catch(...) {
        std::cout << "Não foi possível salvar trajetória KITTI\n";
    }

    try {
        SLAM.SaveTrajectoryTUM("CameraTrajectory_TUM.txt");
        std::cout << "Trajetória TUM salva\n";
    } catch(...) {
        std::cout << "Não foi possível salvar trajetória TUM\n";
    }

    SLAM.Shutdown();
    std::cout << "Total de frames processados: " << frame_count << std::endl;

    return 0;
}
