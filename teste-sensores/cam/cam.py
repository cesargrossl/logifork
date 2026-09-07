import pyrealsense2 as rs
import numpy as np
import cv2

# ============================================================
# TESTE SIMPLES - INTEL REALSENSE D435i
# Exibe a câmera RGB em 640x480 @ 30 FPS
#
# Teclas:
#   Q ou ESC = sair
# ============================================================

LARGURA = 640
ALTURA = 480
FPS = 30

pipeline = rs.pipeline()
config = rs.config()

try:
    # Verifica se existe uma RealSense conectada
    contexto = rs.context()
    dispositivos = contexto.query_devices()

    if len(dispositivos) == 0:
        raise RuntimeError("Nenhuma câmera Intel RealSense foi encontrada.")

    dispositivo = dispositivos[0]
    nome = dispositivo.get_info(rs.camera_info.name)
    serial = dispositivo.get_info(rs.camera_info.serial_number)

    print("=" * 60)
    print("Câmera encontrada!")
    print(f"Modelo : {nome}")
    print(f"Serial : {serial}")
    print(f"RGB    : {LARGURA}x{ALTURA} @ {FPS} FPS")
    print("=" * 60)

    # Configura somente o stream RGB
    config.enable_stream(
        rs.stream.color,
        LARGURA,
        ALTURA,
        rs.format.bgr8,
        FPS
    )

    pipeline.start(config)

    print("\nCâmera iniciada.")
    print("Pressione Q ou ESC para sair.\n")

    while True:
        frames = pipeline.wait_for_frames()
        frame_cor = frames.get_color_frame()

        if not frame_cor:
            continue

        imagem = np.asanyarray(frame_cor.get_data())

        # Mostra resolução e FPS configurados na tela
        cv2.putText(
            imagem,
            f"D435i RGB - {LARGURA}x{ALTURA} @ {FPS} FPS",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2
        )

        cv2.imshow("Teste Intel RealSense D435i", imagem)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord("q") or tecla == 27:
            break

except Exception as erro:
    print("\nERRO:")
    print(erro)

finally:
    try:
        pipeline.stop()
    except Exception:
        pass

    cv2.destroyAllWindows()
    print("\nPrograma finalizado.")
