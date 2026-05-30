#!/usr/bin/env python3

import numpy as np
import cv2
import os
from glob import glob

# ------------------------------------------------------------
# CONFIGURAÇÕES DO TABULEIRO
# ------------------------------------------------------------

# Número de cantos internos (8 colunas x 5 linhas)
pattern_size = (8, 5)

# Cada quadrado vale "1 unidade" (não importa, só afeta escala extrínseca)
square_size = 1.0


# ------------------------------------------------------------
# FUNÇÃO PRINCIPAL
# ------------------------------------------------------------

def main():
    # pega todas as imagens .jpg
    img_names = glob("fotos/*.jpg")

    if len(img_names) == 0:
        print("Nenhuma imagem encontrada em fotos/*.jpg")
        return

    print("Encontradas %d imagens" % len(img_names))

    # cria pasta de debug
    debug_dir = "./output"
    if not os.path.isdir(debug_dir):
        os.mkdir(debug_dir)

    # gera grid de pontos 3D do tabuleiro
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []  # coordenadas 3D do tabuleiro
    img_points = []  # coordenadas 2D no pixel

    # lê primeira imagem para pegar resolução
    h, w = cv2.imread(img_names[0], cv2.IMREAD_GRAYSCALE).shape[:2]

    # processa cada imagem
    for fn in img_names:
        print("Processando:", fn)
        img = cv2.imread(fn, cv2.IMREAD_GRAYSCALE)

        if img is None:
            print("Falha ao abrir:", fn)
            continue

        if img.shape[0] != h or img.shape[1] != w:
            print("Imagem com resolução diferente! Pulando:", fn)
            continue

        found, corners = cv2.findChessboardCorners(img, pattern_size)

        if found:
            # melhora precisão dos cantos
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

            img_points.append(corners.reshape(-1, 2))
            obj_points.append(pattern_points)

            # salva imagem marcada
            vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawChessboardCorners(vis, pattern_size, corners, found)
            outname = os.path.join(debug_dir, os.path.basename(fn) + "_corners.png")
            cv2.imwrite(outname, vis)

        else:
            print("Tabuleiro NAO encontrado em:", fn)

    # calibrar
    print("\nCalibrando a câmera...")
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(
        obj_points, img_points, (w, h), None, None
    )

    print("\n----------------------------------------")
    print("RMS error:", rms)
    print("\nCamera Matrix (intrínsecos):")
    print(camera_matrix)
    print("\nCoeficientes de Distorção:")
    print(dist_coefs.ravel())
    print("----------------------------------------")

    print("\nImagens detectadas salvas em ./output/")



# ------------------------------------------------------------
# RODAR SCRIPT
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
