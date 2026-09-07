import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time

PASTA = "dataset_pallet"
os.makedirs(PASTA, exist_ok=True)

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(
    rs.stream.color,
    640,
    480,
    rs.format.bgr8,
    30
)

pipeline.start(config)

contador = 0

print("D435i iniciada")
print("ESPAÇO = salvar foto")
print("Q = sair")

try:
    while True:

        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            continue

        imagem = np.asanyarray(color_frame.get_data())

        cv2.putText(
            imagem,
            f"Fotos: {contador}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow("Dataset D435i", imagem)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord(" "):

            nome = os.path.join(
                PASTA,
                f"pallet_{int(time.time()*1000)}.jpg"
            )

            # Salva frame original, sem texto
            frame_original = np.asanyarray(
                color_frame.get_data()
            ).copy()

            cv2.imwrite(nome, frame_original)

            contador += 1
            print(f"Salva: {nome}")

        elif tecla == ord("q"):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
