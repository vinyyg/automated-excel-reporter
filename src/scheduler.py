import time
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import config

class MonitorPasta(FileSystemEventHandler):
    def __init__(self, job):
        self.job   = job
        self._lock = threading.Lock()

    def on_created(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(".xlsx"):
            return
        print(f"Novo arquivo detectado: {event.src_path}")
        if not self._lock.acquire(blocking=False):
            print("Execução já em andamento, ignorando.")
            return
        threading.Thread(target=self._executar, daemon=True).start()

    def _executar(self):
        try:
            time.sleep(2)
            self.job()
        finally:
            self._lock.release()

def iniciar_monitoramento(job):
    pasta = str(Path(config.PASTA_INPUT)) if config.PASTA_INPUT else str(Path(__file__).parent.parent / "input")
    handler  = MonitorPasta(job)
    observer = Observer()
    observer.schedule(handler, path=pasta, recursive=False)
    observer.start()

    print(f"Monitorando pasta: {pasta}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()