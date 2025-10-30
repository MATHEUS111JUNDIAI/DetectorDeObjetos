import cv2
from collections import defaultdict

class TrackerManager:
    def __init__(self):
        # Dicionário que armazena os dados de CADA classe
        self.gerenciador_ids_por_classe = defaultdict(lambda: {
            "mapeamento_ids": {},
            "ids_livres": [],
            "proximo_id_bonito": 1
        })

    def reset(self):
        """Limpa todo o estado de rastreamento (usado ao trocar de câmera)."""
        self.gerenciador_ids_por_classe.clear()
        print("Contadores de rastreamento resetados.")

    def process_frame(self, frame, results):
        """Processa os resultados do YOLO e desenha no frame."""
        
        frame_anotado = frame.copy()
        
        # Dicionário para guardar os IDs ('RGs') na tela NESTE frame
        ids_na_tela_por_classe = defaultdict(set)

        # 1. Verifica se o rastreador encontrou IDs
        if results[0].boxes.id is not None:
            
            boxes = results[0].boxes.xyxy.int().cpu().tolist()
            track_ids = results[0].boxes.id.int().cpu().tolist()
            class_ids = results[0].boxes.cls.int().cpu().tolist()
            
            # 2. Itera sobre cada objeto encontrado
            for box, track_id, cls_id in zip(boxes, track_ids, class_ids):
                
                manager = self.gerenciador_ids_por_classe[cls_id]
                ids_na_tela_por_classe[cls_id].add(track_id)
                
                # 3. Lógica de Mapeamento
                if track_id not in manager["mapeamento_ids"]:
                    if manager["ids_livres"]:
                        id_bonito = manager["ids_livres"].pop(0)
                    else:
                        id_bonito = manager["proximo_id_bonito"]
                        manager["proximo_id_bonito"] += 1
                    manager["mapeamento_ids"][track_id] = id_bonito
                
                id_bonito = manager["mapeamento_ids"][track_id]
                
                # 4. CRIA O RÓTULO (em inglês)
                nome_classe = results[0].names[cls_id]
                label_text = f"{nome_classe} {id_bonito}"
                
                # 5. Desenha o retângulo e o texto
                x1, y1, x2, y2 = box
                color = (0, 255, 0) # Verde
                cv2.rectangle(frame_anotado, (x1, y1), (x2, y2), color, 2)
                (w, h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                cv2.rectangle(frame_anotado, (x1, y1 - 20), (x1 + w, y1), color, -1)
                cv2.putText(frame_anotado, label_text, (x1, y1 - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # 6. Limpeza
        for cls_id, manager in list(self.gerenciador_ids_por_classe.items()):
            ids_na_tela_agora = ids_na_tela_por_classe[cls_id]
            ids_para_remover = set(manager["mapeamento_ids"].keys()) - ids_na_tela_agora
            
            for track_id in ids_para_remover:
                id_bonito = manager["mapeamento_ids"][track_id]
                manager["ids_livres"].append(id_bonito)
                del manager["mapeamento_ids"][track_id]
            manager["ids_livres"].sort() 
        
        # 7. Retorna o frame desenhado
        return frame_anotado