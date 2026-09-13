import sys
import time
import signal
from rplidar import RPLidar, RPLidarException


# ============================================================
# CONFIGURAÇÕES
# ============================================================

PORTA = "/dev/ttyUSB0"

# RPLIDAR C1
BAUDRATE = 460800

TIMEOUT = 3

# Distâncias que serão consideradas válidas
DISTANCIA_MIN_MM = 50
DISTANCIA_MAX_MM = 12000


# ============================================================
# VARIÁVEIS
# ============================================================

lidar = None
executando = True


# ============================================================
# ENCERRAMENTO SEGURO
# ============================================================

def encerrar_lidar():
    global lidar

    if lidar is None:
        return

    print("\nEncerrando LiDAR...")

    try:
        lidar.stop()
    except Exception:
        pass

    try:
        lidar.stop_motor()
    except Exception:
        pass

    try:
        lidar.disconnect()
    except Exception:
        pass

    lidar = None

    print("LiDAR desconectado.")


def sinal_encerramento(signum, frame):
    global executando

    print("\nSolicitação de encerramento recebida...")

    executando = False

    encerrar_lidar()

    sys.exit(0)


signal.signal(signal.SIGINT, sinal_encerramento)
signal.signal(signal.SIGTERM, sinal_encerramento)


# ============================================================
# CONEXÃO
# ============================================================

def conectar_lidar():
    global lidar

    print("=" * 60)
    print("TESTE RPLIDAR C1")
    print("=" * 60)

    print(f"Porta     : {PORTA}")
    print(f"Baudrate  : {BAUDRATE}")
    print()

    print("Conectando ao LiDAR...")

    lidar = RPLidar(
        PORTA,
        baudrate=BAUDRATE,
        timeout=TIMEOUT
    )

    time.sleep(1)

    print("Conexão realizada.")


# ============================================================
# INFORMAÇÕES DO LIDAR
# ============================================================

def mostrar_informacoes():

    print("\n" + "=" * 60)
    print("INFORMAÇÕES DO LIDAR")
    print("=" * 60)

    try:
        info = lidar.get_info()

        print(f"Modelo            : {info.get('model')}")
        print(f"Firmware          : {info.get('firmware')}")
        print(f"Hardware          : {info.get('hardware')}")
        print(f"Número de série   : {info.get('serialnumber')}")

    except Exception as erro:

        print("Não foi possível obter as informações.")
        print(f"Erro: {erro}")


# ============================================================
# SAÚDE DO LIDAR
# ============================================================

def verificar_saude():

    print("\n" + "=" * 60)
    print("STATUS DO LIDAR")
    print("=" * 60)

    try:
        status, codigo = lidar.get_health()

        print(f"Status : {status}")
        print(f"Código : {codigo}")

        if status.lower() == "good":
            print("LiDAR funcionando corretamente.")

        elif status.lower() == "warning":
            print("ATENÇÃO: LiDAR retornou WARNING.")

        elif status.lower() == "error":
            print("ERRO reportado pelo LiDAR.")

    except Exception as erro:

        print("Não foi possível verificar a saúde.")
        print(f"Erro: {erro}")


# ============================================================
# PROCESSAMENTO DA VARREDURA
# ============================================================

def testar_varredura():

    global executando

    print("\n" + "=" * 60)
    print("INICIANDO VARREDURA")
    print("=" * 60)

    print()
    print("Formato:")
    print("Ângulo | Distância | Qualidade")
    print()
    print("Pressione CTRL+C para encerrar.")
    print()

    contador_scan = 0

    try:

        for scan in lidar.iter_scans():

            if not executando:
                break

            contador_scan += 1

            print()
            print("-" * 60)
            print(
                f"SCAN #{contador_scan} | "
                f"Pontos recebidos: {len(scan)}"
            )
            print("-" * 60)

            pontos_validos = []

            for medida in scan:

                qualidade = medida[0]
                angulo = medida[1]
                distancia = medida[2]

                if (
                    DISTANCIA_MIN_MM
                    <= distancia
                    <= DISTANCIA_MAX_MM
                ):

                    pontos_validos.append(
                        (
                            qualidade,
                            angulo,
                            distancia
                        )
                    )

            # Ordenar pelo ângulo
            pontos_validos.sort(
                key=lambda x: x[1]
            )

            # ------------------------------------------------
            # Exibir alguns ângulos
            # ------------------------------------------------

            for qualidade, angulo, distancia in pontos_validos:

                # Mostra aproximadamente a cada 10 graus
                if int(angulo) % 10 == 0:

                    distancia_metros = distancia / 1000

                    print(
                        f"Ângulo: {angulo:7.2f}° | "
                        f"Distância: {distancia_metros:6.3f} m | "
                        f"Qualidade: {qualidade}"
                    )

            # ------------------------------------------------
            # Distância frontal
            # ------------------------------------------------

            frente = []

            for qualidade, angulo, distancia in pontos_validos:

                # Frente do LiDAR
                # região aproximada entre 355° e 5°
                if angulo >= 355 or angulo <= 5:

                    frente.append(distancia)

            if frente:

                distancia_frontal = min(frente)

                print()
                print(
                    ">>> DISTÂNCIA FRONTAL: "
                    f"{distancia_frontal / 1000:.3f} m"
                )

    except KeyboardInterrupt:

        print("\nCTRL+C detectado.")

    except RPLidarException as erro:

        print()
        print("ERRO RPLIDAR:")
        print(erro)

    except Exception as erro:

        print()
        print("ERRO INESPERADO:")
        print(type(erro).__name__)
        print(erro)

    finally:

        encerrar_lidar()


# ============================================================
# MAIN
# ============================================================

def main():

    try:

        conectar_lidar()

        mostrar_informacoes()

        verificar_saude()

        print()
        print("Aguardando estabilização do LiDAR...")
        time.sleep(2)

        testar_varredura()

    except PermissionError:

        print()
        print("=" * 60)
        print("ERRO DE PERMISSÃO")
        print("=" * 60)

        print()
        print(
            f"Sem permissão para acessar {PORTA}"
        )

        print()
        print("Execute:")
        print()
        print("sudo usermod -aG dialout $USER")
        print()
        print("Depois reinicie o Raspberry.")

    except FileNotFoundError:

        print()
        print("=" * 60)
        print("PORTA SERIAL NÃO ENCONTRADA")
        print("=" * 60)

        print()
        print(
            f"A porta {PORTA} não existe."
        )

        print()
        print("Verifique com:")
        print()
        print("ls /dev/ttyUSB*")
        print()
        print("ou")
        print()
        print("ls /dev/ttyACM*")

    except RPLidarException as erro:

        print()
        print("=" * 60)
        print("ERRO DE COMUNICAÇÃO COM O RPLIDAR")
        print("=" * 60)

        print()
        print(erro)

        print()
        print("Possíveis causas:")
        print("- Porta serial incorreta")
        print("- Baudrate incorreto")
        print("- LiDAR sendo utilizado por outro programa")
        print("- Alimentação insuficiente")
        print("- Cabo USB")
        print("- Permissão da porta serial")

    except Exception as erro:

        print()
        print("=" * 60)
        print("ERRO")
        print("=" * 60)

        print()
        print(type(erro).__name__)
        print(erro)

    finally:

        encerrar_lidar()


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    main()