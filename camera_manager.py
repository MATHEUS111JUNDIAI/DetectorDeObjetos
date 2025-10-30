import cv2
import os
import threading
import time

# --- CLASSE DE VÍDEO "ASSÍNCRONA" ---
class ThreadedVideoCapture:
    def __init__(self, source):
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
        self.cap = cv2.VideoCapture(source)
        self.status = False
        self.frame = None
        self.stopped = False 
        
        if self.cap.isOpened():
            self.status, self.frame = self.cap.read()
            self.thread = threading.Thread(target=self.update, args=())
            self.thread.daemon = True 
            self.thread.start()
        else:
            self.status = False

    def update(self):
        while True:
            if self.stopped:
                return
            if self.cap.isOpened():
                self.status, self.frame = self.cap.read()
                if not self.status:
                    self.stopped = True
            else:
                self.stopped = True
            time.sleep(0.001) 

    def read(self):
        return self.status, self.frame

    def isOpened(self):
        return self.status

    def release(self):
        self.stopped = True 
        if hasattr(self, 'thread'):
            self.thread.join()  
        if self.cap.isOpened():
            self.cap.release() 
# --- FIM DA CLASSE ---


# --- FUNÇÃO DE ABERTURA ---
# (Certifique-se de que esta linha NÃO está indentada)
def open_camera(source_info):
    """Tenta abrir uma fonte de câmera usando a classe correta."""
    print(f"\nTentando conectar à '{source_info['name']}'...")
    
    source = source_info['source']
    
    if isinstance(source, str) and source.startswith("rtsp"):
        cap = ThreadedVideoCapture(source)
        print("Aguardando buffer RTSP (1.0s)...")
        time.sleep(1.0) 
    else:
        cap = cv2.VideoCapture(source)
        
    if not cap.isOpened():
        print(f"--- FALHA AO ABRIR '{source_info['name']}' ---")
        return None
        
    print(f"Sucesso! Câmera '{source_info['name']}' ativa.")
    return cap