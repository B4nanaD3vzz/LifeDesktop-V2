import customtkinter as ctk
import threading
import time
import pandas as pd
from monitor import iniciar_monitoramento, log_file
from overlay import Overlay
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import psutil

# Configurações padrão (podem ser salvas em um arquivo)
configuracoes = {
    "mostrar_temp_cpu": True,
    "mostrar_uso_gpu": True,
    "grafico_intervalo": 1000,  # milissegundos
    "tema_claro": False,  # Dark mode
    "salvar_logs": True
}

executando = {"executando": False}
thread_monitor = None
overlay = None

ctk.set_appearance_mode("dark" if not configuracoes["tema_claro"] else "light")
ctk.set_default_color_theme("dark-blue")


class LifeDesktopApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LifeDesktop V2 - Monitoramento de Sistema")
        self.geometry("1000x600")
        self.resizable(False, False)

        self.sidebar = ctk.CTkFrame(self, width=80, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.main_content = ctk.CTkFrame(self, corner_radius=15)
        self.main_content.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.frames = {}
        self.create_sidebar()
        self.create_main_content()

    def create_sidebar(self):
        self.home_btn = ctk.CTkButton(self.sidebar, text="🏠", width=60, height=60, corner_radius=15,
                                      command=lambda: self.mostrar_frame("monitoramento"))
        self.home_btn.pack(pady=20)

        self.graph_btn = ctk.CTkButton(self.sidebar, text="⚙️", width=60, height=60, corner_radius=15,
                                       command=lambda: self.mostrar_frame("grafico"))
        self.graph_btn.pack(pady=20)

        self.config_btn = ctk.CTkButton(self.sidebar, text="🌐", width=60, height=60, corner_radius=15,
                                        command=lambda: self.mostrar_frame("config"))
        self.config_btn.pack(pady=20)

    def create_main_content(self):
        # FRAME MONITORAMENTO
        frame_monitor = ctk.CTkFrame(self.main_content, corner_radius=15)
        self.frames["monitoramento"] = frame_monitor
        frame_monitor.pack(fill="both", expand=True)

        self.clock_label = ctk.CTkLabel(frame_monitor, text="", font=("Helvetica", 48))
        self.clock_label.pack(pady=(40, 10))

        self.start_btn = ctk.CTkButton(frame_monitor, text="Iniciar Monitoramento", command=self.iniciar)
        self.start_btn.pack(pady=10)

        self.stop_btn = ctk.CTkButton(frame_monitor, text="Parar e Exibir Métricas", command=self.parar)
        self.stop_btn.pack(pady=10)

        self.resultado = ctk.CTkLabel(frame_monitor, text="", wraplength=600, justify="left")
        self.resultado.pack(pady=20)

        # FRAME GRÁFICO
        frame_graph = ctk.CTkFrame(self.main_content, corner_radius=15)
        self.frames["grafico"] = frame_graph

        self.cpu_data = []
        self.ram_data = []
        self.time_data = []

        self.fig, self.ax = plt.subplots(figsize=(6, 3), dpi=100)
        self.ax.set_title("Uso de CPU e RAM (%)")
        self.ax.set_ylim(0, 100)

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_graph)
        self.canvas.get_tk_widget().pack(pady=20)

        self.update_grafico()

        # FRAME CONFIGURAÇÕES
        frame_config = ctk.CTkFrame(self.main_content, corner_radius=15)
        self.frames["config"] = frame_config

        config_label = ctk.CTkLabel(frame_config, text="Configurações do LifeDesktop", font=("Arial", 22))
        config_label.pack(pady=20)

        self.temp_cpu_check = ctk.CTkCheckBox(frame_config, text="Mostrar Temperatura da CPU no Overlay",
                                              variable=ctk.BooleanVar(value=configuracoes["mostrar_temp_cpu"]))
        self.temp_cpu_check.pack(pady=10)

        self.gpu_usage_check = ctk.CTkCheckBox(frame_config, text="Mostrar Uso da GPU no Overlay",
                                               variable=ctk.BooleanVar(value=configuracoes["mostrar_uso_gpu"]))
        self.gpu_usage_check.pack(pady=10)

        self.graph_interval_label = ctk.CTkLabel(frame_config, text="Intervalo de Atualização do Gráfico (ms):")
        self.graph_interval_label.pack(pady=10)
        self.graph_interval_entry = ctk.CTkEntry(frame_config, width=200)
        self.graph_interval_entry.insert(0, str(configuracoes["grafico_intervalo"]))
        self.graph_interval_entry.pack(pady=10)

        self.light_mode_check = ctk.CTkCheckBox(frame_config, text="Modo Claro",
                                                 variable=ctk.BooleanVar(value=configuracoes["tema_claro"]))
        self.light_mode_check.pack(pady=10)

        self.save_logs_check = ctk.CTkCheckBox(frame_config, text="Salvar Logs de Monitoramento",
                                                variable=ctk.BooleanVar(value=configuracoes["salvar_logs"]))
        self.save_logs_check.pack(pady=10)

        self.save_config_btn = ctk.CTkButton(frame_config, text="Salvar Configurações", command=self.salvar_configuracoes)
        self.save_config_btn.pack(pady=20)

        self.mostrar_frame("monitoramento")
        self.update_clock()

    def mostrar_frame(self, nome):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[nome].pack(fill="both", expand=True)

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.configure(text=current_time)
        self.after(1000, self.update_clock)

    def update_grafico(self):
        if len(self.cpu_data) > 50:
            self.cpu_data.pop(0)
            self.ram_data.pop(0)
            self.time_data.pop(0)

        self.cpu_data.append(psutil.cpu_percent())
        self.ram_data.append(psutil.virtual_memory().percent)
        self.time_data.append(len(self.cpu_data))

        self.ax.clear()
        self.ax.plot(self.time_data, self.cpu_data, label="CPU", color="cyan")
        self.ax.plot(self.time_data, self.ram_data, label="RAM", color="magenta")
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Uso de CPU e RAM (%)")
        self.ax.legend()
        self.canvas.draw()

        self.after(configuracoes["grafico_intervalo"], self.update_grafico)

    def iniciar(self):
        global overlay, thread_monitor
        if not executando["executando"]:
            executando["executando"] = True
            self.resultado.configure(text="Monitoramento em execução...")
            thread_monitor = threading.Thread(target=iniciar_monitoramento, args=(executando,))
            thread_monitor.start()
            overlay = Overlay(self)

    def parar(self):
        global overlay
        if executando["executando"]:
            executando["executando"] = False
            self.resultado.configure(text="Monitoramento finalizado.")
            self.gerar_metricas()
            if overlay:
                overlay.fechar()
                overlay = None

    def gerar_metricas(self):
        df = pd.read_csv(log_file)
        metricas = {
            "CPU (%) média": df["cpu_percent"].mean(),
            "Temp. CPU (°C) média": df["cpu_temp"].dropna().mean(),
            "RAM usada (MB) média": df["ram_used_mb"].mean(),
            "RAM livre (MB) média": df["ram_free_mb"].mean(),
            "RAM (%) média": df["ram_percent"].mean(),
            "GPU (%) média": df["gpu_load"].dropna().mean(),
            "Temp. GPU (°C) média": df["gpu_temp"].dropna().mean()
        }

        texto = "\n".join([f"{k}: {round(v, 2)}" for k, v in metricas.items() if not pd.isna(v)])
        self.resultado.configure(text="Métricas:\n" + texto)

    def salvar_configuracoes(self):
        configuracoes["mostrar_temp_cpu"] = self.temp_cpu_check.get()
        configuracoes["mostrar_uso_gpu"] = self.gpu_usage_check.get()
        configuracoes["grafico_intervalo"] = int(self.graph_interval_entry.get())
        configuracoes["tema_claro"] = self.light_mode_check.get()
        configuracoes["salvar_logs"] = self.save_logs_check.get()

        # Salva as configurações em um arquivo ou banco de dados, se necessário.
        ctk.set_appearance_mode("light" if configuracoes["tema_claro"] else "dark")
        print("Configurações salvas com sucesso!")

if __name__ == "__main__":
    app = LifeDesktopApp()
    app.mainloop()
