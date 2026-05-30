# Mapeamento

Repositório do projeto de mapeamento do RoboIME, organizado por tipo de sensor utilizado.

---

## 📷 Câmera Comum

Algoritmos de mapeamento e estimativa de profundidade utilizando câmera monocular padrão (sem sensor de profundidade dedicado).

### Algoritmos

- **ORB-SLAM3** — Sistema de SLAM (Simultaneous Localization and Mapping) baseado em features ORB. Capaz de operar em modo monocular, estéreo e RGB-D, construindo um mapa esparso do ambiente enquanto estima a trajetória da câmera em tempo real.

- **MiDaS** — Rede neural para estimativa de profundidade monocular. A partir de uma única imagem RGB, infere um mapa de profundidade relativo, permitindo que câmeras comuns obtenham informações 3D sem sensor adicional.

- **MapAnything** — Pipeline de mapeamento semântico que combina detecção de objetos com localização espacial, permitindo associar entidades identificadas a posições no mapa do ambiente.

- **RTAB-Map** (Real-Time Appearance-Based Mapping) — Sistema de SLAM com detecção de loop closure baseada em aparência visual. Gera mapas densos e é capaz de gerenciar grafos de poses de grande escala, sendo adequado para operação de longo prazo.

---

## 📷 Câmera com Sensor de Profundidade

Algoritmos de mapeamento utilizando câmeras RGB-D (ex: Intel RealSense, Microsoft Kinect), que fornecem imagem colorida e mapa de profundidade diretamente do hardware.

---

## 📡 Lidar 2D

Algoritmos de mapeamento e navegação utilizando Lidar bidimensional, que realiza varreduras planares do ambiente para construção de mapas de ocupação 2D.

---

## 📡 Lidar 3D

Algoritmos de mapeamento utilizando Lidar tridimensional, que gera nuvens de pontos densas do ambiente para reconstrução 3D e localização de alta precisão.
