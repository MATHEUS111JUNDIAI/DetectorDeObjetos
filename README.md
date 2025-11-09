# Detector de Objetos em Tempo Real com YOLOv8

Este projeto é uma aplicação de detecção e rastreamento de objetos em tempo real que utiliza o modelo YOLOv8. Ele é capaz de processar feeds de vídeo de múltiplas fontes, como webcams e streams RTSP, identificar objetos em cada frame e rastreá-los de forma consistente.

## Funcionalidades

- **Detecção de Objetos em Tempo Real:** Utiliza o modelo YOLOv8 para identificar uma ampla variedade de objetos.
- **Rastreamento de Objetos:** Atribui um ID único e persistente a cada objeto detectado, permitindo o rastreamento contínuo mesmo que o objeto saia e reapareça no quadro.
- **Suporte a Múltiplas Câmeras:** Permite a configuração de várias fontes de vídeo e a alternância entre elas durante a execução.
- **Gerenciamento de Câmeras Assíncrono:** A leitura dos frames da câmera é feita em uma thread separada para evitar bloqueios e perda de frames, especialmente em streams de rede (RTSP).
- **Configuração Flexível:** As fontes de câmera e as configurações do rastreador são gerenciadas através de um arquivo `config.json`.

## Como Funciona

O sistema é composto por três módulos principais:

1.  **`main.py`**: O ponto de entrada da aplicação. Ele carrega o modelo YOLO, gerencia o loop principal, processa os frames e controla a interação do usuário (troca de câmera e encerramento).
2.  **`camera_manager.py`**: Responsável por abrir e gerenciar as fontes de vídeo. Inclui a classe `ThreadedVideoCapture` para uma captura de vídeo mais robusta e sem bloqueios.
3.  **`tracker_manager.py`**: Gerencia a lógica de rastreamento. Ele mantém um mapeamento entre os IDs de rastreamento brutos do YOLO e IDs "bonitos" e persistentes, garantindo que um objeto seja sempre rotulado com o mesmo número.

## Pré-requisitos

Antes de começar, certifique-se de ter o Python 3.12.6 (ou superior) e o pip instalados.

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    O arquivo `requirements.txt` deve conter:
    ```
    opencv-python
    ultralytics
    ```

## Configuração

1.  Crie um arquivo chamado `config.json` na raiz do projeto.
2.  Adicione as fontes de sua câmera a este arquivo. Você pode usar o índice da webcam (0, 1, ...) ou o URL de um stream RTSP.

**Exemplo de `config.json`:**
```json
{
  "camera_sources": [
    {
      "name": "Webcam Principal",
      "source": 0
    },
    {
      "name": "Câmera do Corredor",
      "source": "rtsp://usuario:senha@192.168.1.100:554/stream1"
    }
  ],
  "tracker_config": "bytetrack.yaml"
}
```
- **`name`**: Um nome amigável para a câmera.
- **`source`**: O índice da webcam ou o URL do stream.
- **`tracker_config`**: (Opcional) O arquivo de configuração do rastreador a ser usado pelo YOLO. O padrão é `bytetrack.yaml`.

## Como Usar

1.  Execute o script principal:
    ```bash
    python main.py
    ```

2.  Uma janela do OpenCV aparecerá mostrando o feed da câmera com os objetos detectados e rastreados.

3.  **Controles:**
    -   Pressione a tecla **`c`** para alternar para a próxima fonte de câmera na lista.
    -   Pressione a tecla **`q`** para fechar a aplicação.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
