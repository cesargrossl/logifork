# 🤖 LOGIFORK

### Mini Empilhadeira Robótica Autônoma para Operações Logísticas

**LOGIFORK** é uma plataforma robótica móvel desenvolvida para automatizar processos de **movimentação, localização, alinhamento, captura e transporte de pallets em ambientes logísticos**.

O nome **LOGIFORK** combina:

* **LOGI** — Logistics / Logística
* **FORK** — Forklift / Garfo de empilhadeira

O projeto utiliza uma **mini empilhadeira robótica** como plataforma experimental, integrando visão computacional, sensores de distância, navegação e controle de motores.

---

## 🎯 Objetivo

O objetivo do LOGIFORK é desenvolver e validar uma solução capaz de executar operações de movimentação de pallets.

O fluxo básico de operação consiste em:

**Navegar → Localizar → Identificar → Alinhar → Aproximar → Capturar → Transportar**

---

## 🚜 Funcionalidades

O LOGIFORK foi projetado para realizar:

* Navegação em ambientes internos;
* Mapeamento do ambiente;
* Localização do robô;
* Detecção de pallets utilizando visão computacional;
* Identificação da posição do pallet;
* Detecção dos pontos de entrada dos garfos;
* Alinhamento automático com o pallet;
* Aproximação controlada;
* Elevação e descida dos garfos;
* Captura do pallet;
* Transporte do pallet;
* Desvio de obstáculos;
* Monitoramento de sensores durante a operação.

---

## 🧠 Arquitetura

O sistema integra diferentes tecnologias de robótica e visão computacional.

### Hardware

* Raspberry Pi 5;
* Intel RealSense;
* RPLIDAR;
* Motores DC;
* Encoders;
* Sensores ultrassônicos;
* Sensores de fim de curso;
* Sistema motorizado para elevação dos garfos;
* Estrutura de mini empilhadeira.

### Software

* Ubuntu;
* ROS 2;
* Nav2;
* SLAM;
* OpenCV;
* Python;
* YOLO;
* Intel RealSense SDK.

---

## 👁️ Visão Computacional

O sistema de visão computacional permite identificar pallets e determinar sua posição em relação ao robô.

O processamento utiliza imagens da câmera Intel RealSense combinadas com modelos de detecção de objetos e técnicas de processamento de imagens.

O LOGIFORK utiliza essas informações para determinar:

* Presença do pallet;
* Posição do pallet;
* Distância;
* Centro do pallet;
* Posição dos pontos de entrada dos garfos;
* Erro de alinhamento;
* Ângulo em relação ao pallet.

Com essas informações, o robô executa automaticamente as correções necessárias antes da aproximação.


## 🔬 Aplicação

O LOGIFORK é uma plataforma experimental voltada principalmente para estudos relacionados a:

* Robótica móvel;
* Intralogística;
* Indústria 4.0;
* Visão computacional;
* Inteligência artificial;
* Navegação autônoma;
* Sistemas autônomos de movimentação de materiais;
* Automação de processos logísticos.


