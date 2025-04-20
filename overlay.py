import customtkinter as ctk
import psutil
import GPUtil
import threading
import time
import tkinter as tk

# Monitoramento de FPS
frame_count = 0
last_time = time.time()
fps_global = 0

def calculate_fps():
    global frame_count, last_time, fps_global
    while True:
        current_time = time.time()
        elapsed_time = current_time - last_time
        frame_count += 1

        if elapsed_time >= 1:
            fps_global = frame_count / elapsed_time
            frame_count = 0
            last_time = current_time

        time.sleep(0.01)


class Overlay(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.width = 290
        self.height = 150

        self.geometry(f"{self.width}x{self.height}+20+50")
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        transparent_color = "gray20"
        self.attributes("-transparentcolor", transparent_color)
        self.configure(bg=transparent_color)

        self.canvas = tk.Canvas(self, width=self.width, height=self.height,
                                highlightthickness=1, highlightbackground="lime",
                                bg=transparent_color, bd=0)
        self.canvas.pack(fill="both", expand=True)

        self.info_frame = tk.Frame(self, bg="black")
        self.info_frame.place(x=5, y=5, width=self.width - 10, height=self.height - 10)

        self.texto = tk.Label(self.info_frame, text="Iniciando monitoramento...",
                              font=("Consolas", 11), fg="lime", bg="black", justify="left")
        self.texto.pack(padx=5, pady=5)

        self._drag_data = {"x": 0, "y": 0}
        self.bind("<Button-1>", self._start_drag)
        self.bind("<B1-Motion>", self._do_drag)

        self.rodando = True

        # ⏱️ Inicia thread de atualização do overlay
        self.thread = threading.Thread(target=self.atualizar_dados)
        self.thread.daemon = True
        self.thread.start()

        # 🔁 Inicia thread de cálculo de FPS real
        self.fps_thread = threading.Thread(target=calculate_fps)
        self.fps_thread.daemon = True
        self.fps_thread.start()

    def _start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _do_drag(self, event):
        x = self.winfo_pointerx() - self._drag_data["x"]
        y = self.winfo_pointery() - self._drag_data["y"]
        self.geometry(f"+{x}+{y}")

    def atualizar_dados(self):
        global fps_global
        while self.rodando:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            ram_used = round(ram.used / 1024 / 1024, 1)

            try:
                gpu = GPUtil.getGPUs()[0]
                gpu_load = round(gpu.load * 100, 1)
                gpu_temp = gpu.temperature
            except:
                gpu_load = None
                gpu_temp = None

            net = psutil.net_io_counters()
            if not hasattr(self, 'last_net'):
                self.last_net = net
                net_upload = net_download = 0
            else:
                net_upload = (net.bytes_sent - self.last_net.bytes_sent) / 1024
                net_download = (net.bytes_recv - self.last_net.bytes_recv) / 1024
                self.last_net = net

            texto = (
                f"FPS: {fps_global:.0f}\n"
                f"CPU: {cpu:.1f}%\n"
                f"RAM: {ram_percent:.1f}% ({ram_used} MB)\n"
                f"GPU: {gpu_load if gpu_load is not None else 'N/A'}%\n"
                f"Temp GPU: {gpu_temp if gpu_temp is not None else 'N/A'}°C\n"
                f"Up: {net_upload:.1f} KB/s | Down: {net_download:.1f} KB/s"
            )
            self.texto.configure(text=texto)
            time.sleep(1)

    def fechar(self):
        self.rodando = False
        self.destroy()
