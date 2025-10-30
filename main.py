import cv2
from ultralytics import YOLO
import time
import json # Para ler o config.json

# --- IMPORTA NOSSOS MÓDULOS ---
from camera_manager import open_camera
from tracker_manager import TrackerManager

# --- Configuração ---
print("Carregando modelo YOLO...")
model = YOLO('yolov8n.pt')

print("Carregando configurações de 'config.json'...")
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        camera_sources = config['camera_sources']
        tracker_config = config.get('tracker_config', 'bytetrack.yaml') # Padrão para bytetrack.yaml se não for encontrado
except FileNotFoundError:
    print("\n--- ERRO FATAL ---")
    print("Arquivo 'config.json' não encontrado. Crie um com a lista de câmeras.")
    exit()
except (json.JSONDecodeError, KeyError) as e:
    print("\n--- ERRO FATAL ---")
    print(f"Erro ao ler 'config.json': {e}")
    print("Verifique se o arquivo está formatado corretamente e contém a chave 'camera_sources'.")
    exit()

# Cria uma instância do nosso gerenciador de rastreamento
tracker = TrackerManager()

# --- Conexão Inicial ---
current_source_index = 0
cap = None
print("Procurando a primeira câmera funcional...")
for i in range(len(camera_sources)):
    cap = open_camera(camera_sources[current_source_index])
    if cap:
        break 
    current_source_index = (current_source_index + 1) % len(camera_sources)

if not cap:
    print("\n--- ERRO FATAL ---")
    print("Não foi possível abrir NENHUMA câmera da lista.")
    exit()

print('\nPressione "c" na janela para TROCAR de câmera.')
print('Pressione "q" na janela para SAIR.')


# --- Loop Principal (AGORA MUITO MAIS LIMPO) ---
while True:
    ret, frame = cap.read() 
    
    if not ret:
        print("Erro: Frame não recebido. Câmera desconectada.")
        key = ord('c') 
    else:
        # 1. Roda a IA
        results = model.track(frame, persist=True, tracker=tracker_config)
        
        # 2. Deixa o tracker_manager fazer todo o trabalho de lógica e desenho
        frame_anotado = tracker.process_frame(frame, results)
        
        # 3. Mostra o resultado
        cam_name = camera_sources[current_source_index]['name']
        cv2.imshow(f"Rastreador ({cam_name}) - 'c' (trocar) 'q' (sair)", frame_anotado)
        
        key = cv2.waitKey(1) & 0xFF

    # --- Lógica de Controle ---
    if key == ord('q'):
        print("Tecla 'q' pressionada... Finalizando.")
        break
    
    if key == ord('c'):
        print("Tecla 'c' pressionada... Procurando próxima câmera funcional.")
        cap.release() 
        
        # Reseta o estado do rastreador
        tracker.reset() 
        
        found_cam = False
        for _ in range(len(camera_sources)):
            current_source_index = (current_source_index + 1) % len(camera_sources)
            cap = open_camera(camera_sources[current_source_index])
            if cap:
                found_cam = True
                break
        
        if not found_cam:
            print("ERRO: Nenhuma outra câmera funcional foi encontrada. Saindo.")
            break 

# --- Limpeza ---
print("Finalizando o programa...")
if cap:
    cap.release()
cv2.destroyAllWindows()