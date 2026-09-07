# README — Guia de Coleta de Imagens para um Modelo YOLO Sólido de Detecção de Pallets

## 1. Objetivo

Criar um dataset robusto para que o YOLO consiga identificar o pallet miniatura nas condições reais de operação da miniempilhadeira.

O princípio mais importante é:

> O dataset deve representar o que a câmera realmente verá quando o robô estiver funcionando.

Para este projeto, priorize imagens obtidas pela Intel RealSense D435i instalada na posição definitiva do robô.

---

## 2. Quantidade inicial recomendada

Meta inicial: **1.000 a 1.500 imagens**.

Não é necessário atingir esse número antes do primeiro treinamento. Uma estratégia melhor é:

1. Coletar aproximadamente 600–800 imagens variadas.
2. Treinar uma primeira versão.
3. Testar no robô.
4. Identificar situações em que o modelo falha.
5. Fotografar mais dessas situações.
6. Treinar novamente.

**Qualidade e diversidade são mais importantes do que simplesmente ter milhares de imagens.**

---

## 3. Câmera e resolução

### Câmera recomendada
- Intel RealSense D435i.
- Instalada no próprio robô.
- Mesma altura e inclinação que serão utilizadas durante a operação.

### Captura
Recomendação inicial:

- RGB: **640 × 480**
- 30 FPS

Mesmo que o YOLO seja executado posteriormente com uma entrada menor, mantenha as imagens originais em 640 × 480.

Não reduza permanentemente as imagens antes de montar o dataset. É fácil gerar uma versão menor depois, mas detalhes perdidos não podem ser recuperados.

---

## 4. O que deve variar nas imagens

### 4.1 Distância

Fotografe o pallet em várias distâncias dentro da faixa real de operação.

Exemplo:

- 0,4 m
- 0,5 m
- 0,6 m
- 0,8 m
- 1,0 m
- 1,2 m
- 1,5 m
- 2,0 m
- 2,5 m, se fizer sentido para o ambiente

Não deixe o dataset concentrado apenas em uma distância.

---

### 4.2 Ângulo

O pallet não estará sempre perfeitamente frontal.

Inclua aproximadamente:

- -45°
- -30°
- -20°
- -10°
- 0°
- +10°
- +20°
- +30°
- +45°

Dê maior quantidade de imagens aos ângulos que realmente ocorrerão durante a operação.

---

### 4.3 Posição na imagem

O pallet deve aparecer:

- centralizado;
- deslocado para a esquerda;
- deslocado para a direita;
- mais acima;
- mais abaixo;
- próximo das bordas.

Inclua também casos em que parte do pallet esteja fora do campo de visão.

Isso é especialmente importante para permitir que o sistema reconheça o pallet antes de executar uma manobra de recentralização.

---

### 4.4 Iluminação

Repita as capturas com:

- iluminação normal;
- iluminação mais fraca;
- iluminação forte;
- luz lateral;
- sombras;
- iluminação artificial;
- diferentes horários, quando possível.

Evite criar um dataset em que todas as imagens tenham exatamente a mesma iluminação.

---

### 4.5 Fundo e ambiente

Varie o que existe atrás e ao redor do pallet:

- parede;
- caixas;
- estruturas;
- objetos;
- corredor;
- equipamentos;
- pessoas ao fundo;
- outros pallets, se isso puder ocorrer.

O objetivo é impedir que o modelo aprenda o **cenário** em vez de aprender o **pallet**.

---

### 4.6 Oclusão

Inclua situações realistas em que o pallet esteja parcialmente escondido:

- caixa na frente;
- objeto lateral;
- pessoa passando;
- garfo ou estrutura cobrindo uma pequena parte;
- pallet parcialmente fora da imagem.

Não exagere em situações impossíveis de reconhecer. O objetivo é representar condições reais.

---

## 5. Imagens negativas

Inclua aproximadamente **10% a 15% de imagens sem pallet**.

Exemplos:

- corredor vazio;
- caixas;
- parede;
- estantes;
- pessoas;
- cadeira;
- robô;
- objetos com formato semelhante ao pallet;
- ambiente de operação sem pallet.

Essas imagens devem permanecer **sem bounding box de pallet**.

Elas são importantes para reduzir falsos positivos.

---

## 6. Não tire centenas de imagens praticamente iguais

Evite:

1. deixar o robô e o pallet parados;
2. gravar vários segundos;
3. extrair todos os frames;
4. usar centenas de imagens quase idênticas.

Exemplo ruim:

- pallet a 1 m;
- mesma posição;
- mesma iluminação;
- mesma câmera;
- 300 frames consecutivos.

Isso aumenta o número de arquivos sem aumentar significativamente a diversidade do dataset.

Se utilizar vídeo, extraia frames espaçados e selecione apenas imagens que realmente acrescentem variação.

---

## 7. Plano prático de coleta

Uma sessão pode seguir este padrão:

### Etapa A — Pallet frontal
Fotografar em várias distâncias.

### Etapa B — Pallet à esquerda
Repetir as distâncias principais.

### Etapa C — Pallet à direita
Repetir as distâncias principais.

### Etapa D — Pallet inclinado
Variar ângulos positivos e negativos.

### Etapa E — Iluminação
Repetir parte das situações com luz diferente.

### Etapa F — Cenário difícil
Adicionar caixas, objetos, oclusões e pallet parcialmente cortado.

### Etapa G — Negativas
Percorrer o ambiente fotografando situações sem pallet.

---

## 8. Exemplo de distribuição para 1.200 imagens

Não trate as categorias como totalmente independentes; uma mesma imagem pode combinar distância, ângulo e iluminação diferentes.

Sugestão de planejamento:

- ~200 frontais/centrais;
- ~150 deslocadas para a esquerda;
- ~150 deslocadas para a direita;
- ~200 com ângulos variados;
- ~100 com iluminação difícil;
- ~100 com oclusão ou pallet parcialmente cortado;
- ~150 com mudanças importantes de cenário/fundo;
- ~150 negativas sem pallet.

Total aproximado: **1.200 imagens**.

---

## 9. Anotação

Se houver apenas uma classe:

```text
pallet
```

Marque a bounding box envolvendo o pallet de forma consistente.

### Evite:
- caixas muito maiores que o objeto;
- cortar partes visíveis do pallet;
- marcar somente a frente quando a definição da classe é o pallet inteiro;
- alternar critérios de anotação entre imagens.

**Consistência na anotação é fundamental.**

---

## 10. Divisão do dataset

Sugestão:

- **70% treino**
- **20% validação**
- **10% teste**

Para 1.200 imagens:

- treino: 840
- validação: 240
- teste: 120

### Atenção com vídeos

Não coloque frames quase consecutivos do mesmo vídeo em treino e teste.

Exemplo:

```text
frame_100 → treino
frame_101 → teste
frame_102 → validação
```

Isso é ruim porque as imagens são praticamente iguais.

Prefira separar por **sessão de coleta** ou sequência:

```text
Sessões 1–7 → treino
Sessões 8–9 → validação
Sessão 10 → teste
```

Assim o teste mede melhor a capacidade de generalização do modelo.

---

## 11. Dataset de teste deve ser realmente difícil

Reserve imagens que o modelo nunca viu durante o treinamento:

- nova posição do pallet;
- outra iluminação;
- pequenas alterações no cenário;
- ângulos diferentes;
- obstáculos;
- imagens negativas.

Não escolha somente imagens fáceis para o conjunto de teste.

---

## 12. Uso de imagens de pallets reais

É possível adicionar imagens de pallets reais, mas como o sistema será utilizado com uma **miniatura**, elas não devem dominar o dataset.

Priorize imagens do:

- pallet miniatura real;
- ambiente experimental;
- D435i;
- posição real da câmera;
- condições reais do protótipo.

Imagens externas podem ser usadas apenas como complemento de diversidade.

---

## 13. Data augmentation

Depois de coletar boas imagens reais, podem ser utilizadas técnicas de augmentation durante o treinamento, como:

- pequenas mudanças de brilho;
- contraste;
- escala;
- translação;
- pequenas rotações;
- pequenas alterações de cor.

Augmentation **não substitui uma boa coleta real**.

Não use transformações que criem situações fisicamente absurdas para o robô.

---

## 14. Processo recomendado de evolução

Não tente criar o dataset “perfeito” de uma única vez.

Use um processo iterativo:

```text
COLETAR
   ↓
ANOTAR
   ↓
TREINAR YOLO
   ↓
TESTAR NO ROBÔ
   ↓
REGISTRAR FALHAS
   ↓
COLETAR IMAGENS DAS FALHAS
   ↓
ADICIONAR AO DATASET
   ↓
RETREINAR
```

Exemplo:

Se o YOLO funciona frontalmente, mas falha quando o pallet está a +30°, não adicione mais 200 fotos frontais. Adicione imagens próximas de +30°.

Isso é muito mais eficiente para tornar o modelo robusto.

---

## 15. Checklist antes de treinar

Verifique:

- [ ] Há pallets próximos e distantes.
- [ ] Há pallets centralizados.
- [ ] Há pallets à esquerda e à direita.
- [ ] Há ângulos positivos e negativos.
- [ ] Há diferentes iluminações.
- [ ] Há diferentes fundos.
- [ ] Há pallet parcialmente cortado.
- [ ] Há pequenas oclusões.
- [ ] Há imagens sem pallet.
- [ ] As bounding boxes seguem o mesmo padrão.
- [ ] Não existem centenas de imagens duplicadas.
- [ ] Treino, validação e teste foram separados corretamente.
- [ ] O conjunto de teste contém situações realmente novas.

---

## 16. Regra principal para este projeto

Antes de tirar uma foto, pergunte:

> **“Esta situação pode acontecer quando a miniempilhadeira estiver procurando um pallet?”**

Se a resposta for **sim**, é uma situação interessante para o dataset.

A robustez virá principalmente da diversidade de **distância + ângulo + posição + iluminação + fundo + oclusão**, e não apenas da quantidade total de imagens.

---

## 17. Organização sugerida das coletas

Antes de fazer o split final, você pode organizar as imagens brutas por sessão:

```text
dataset_bruto/
├── sessao_01_frontal/
├── sessao_02_angulos/
├── sessao_03_luz_fraca/
├── sessao_04_luz_forte/
├── sessao_05_pallet_cortado/
├── sessao_06_obstaculos/
├── sessao_07_outro_cenario/
└── sessao_08_negativas/
```

Depois de revisar e anotar, faça a divisão final em treino, validação e teste.

---

## 18. O que registrar para artigo/dissertação

Durante a coleta, mantenha uma pequena planilha ou registro contendo:

- data/sessão;
- câmera;
- resolução;
- número de imagens;
- faixa de distância;
- ângulos utilizados;
- condições de iluminação;
- cenário;
- quantidade de imagens negativas;
- divisão treino/validação/teste;
- versão do dataset.

Isso facilita muito a descrição metodológica e permite reproduzir os experimentos posteriormente.
