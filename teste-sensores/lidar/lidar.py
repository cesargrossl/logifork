import asyncio
from rplidarc1.scanner import RPLidar


PORTA = "/dev/ttyUSB0"
BAUDRATE = 460800


lidar = RPLidar(
    PORTA,
    BAUDRATE
)


async def mostrar_dados():
    print("=" * 60)
    print("RPLIDAR C1 - TESTE DE VARREDURA")
    print("=" * 60)
    print(f"Porta: {PORTA}")
    print(f"Baudrate: {BAUDRATE}")
    print()
    print("Pressione CTRL+C para encerrar.")
    print()

    async def scanner():
        await lidar.simple_scan(
            make_return_dict=True
        )

    async def visualizar():
        while True:
            await asyncio.sleep(0.5)

            dados = lidar.output_dict.copy()

            if not dados:
                print("Aguardando pontos do LiDAR...")
                continue

            print()
            print("-" * 60)
            print(f"Pontos recebidos: {len(dados)}")
            print("-" * 60)

            # ==================================================
            # DISTÂNCIA FRONTAL
            # ==================================================

            frente = []

            for angulo, distancia in dados.items():

                if distancia is None:
                    continue

                try:
                    angulo = float(angulo)
                    distancia = float(distancia)
                except (TypeError, ValueError):
                    continue

                if distancia <= 0:
                    continue

                if angulo <= 5 or angulo >= 355:
                    frente.append(distancia)

            if frente:
                menor = min(frente)

                print(
                    f"FRENTE: {menor / 1000:.3f} m"
                )
            else:
                print("FRENTE: sem leitura válida")

            # ==================================================
            # ÂNGULOS DE REFERÊNCIA
            # ==================================================

            referencias = [
                0,
                45,
                90,
                135,
                180,
                225,
                270,
                315
            ]

            for ref in referencias:

                mais_proximo = None
                menor_diferenca = 999

                for angulo, distancia in dados.items():

                    if distancia is None:
                        continue

                    try:
                        angulo_float = float(angulo)
                        distancia_float = float(distancia)
                    except (TypeError, ValueError):
                        continue

                    if distancia_float <= 0:
                        continue

                    diferenca = abs(
                        angulo_float - ref
                    )

                    if diferenca > 180:
                        diferenca = 360 - diferenca

                    if diferenca < menor_diferenca:

                        menor_diferenca = diferenca

                        mais_proximo = (
                            angulo_float,
                            distancia_float
                        )

                if mais_proximo:

                    angulo, distancia = mais_proximo

                    print(
                        f"{angulo:7.2f}° : "
                        f"{distancia / 1000:6.3f} m"
                    )

                else:

                    print(
                        f"{ref:7.2f}° : "
                        f"sem leitura"
                    )

    try:

        async with asyncio.TaskGroup() as tg:

            tg.create_task(scanner())

            tg.create_task(visualizar())

    finally:

        try:
            lidar.stop_event.set()
        except Exception:
            pass


def encerrar():

    print()
    print("Encerrando RPLIDAR C1...")

    try:
        lidar.stop_event.set()
    except Exception:
        pass

    try:
        lidar.reset()
    except Exception:
        pass

    try:
        lidar.shutdown()
    except Exception:
        pass

    print("RPLIDAR C1 desconectado.")


try:

    asyncio.run(
        mostrar_dados()
    )

except KeyboardInterrupt:

    print()
    print("CTRL+C detectado.")

finally:

    encerrar()