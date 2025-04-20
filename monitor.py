import psutil
import GPUtil
import csv
import os
from datetime import datetime
import threading
import time

# Cria pasta de logs se não existir
os.makedirs("logs", exist_ok=True)

# Gera nome do arquivo
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = f"logs/amostragem_{now}.csv"

# Cabeçalho padrão
headers = [
    "timestamp",
    "cpu_percent",
    "cpu_temp",
    "ram_percent",
    "ram_used_mb",
    "ram_free_mb",
    "gpu_load",
    "gpu_temp"
]

# Escreve o cabeçalho no CSV
with open(log_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)

# Função principal de coleta
def iniciar_monitoramento(flag_execucao):
    while flag_execucao["executando"]:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # CPU
        cpu_percent = psutil.cpu_percent()
        try:
            temps = psutil.sensors_temperatures()
            cpu_temp = temps.get('coretemp', [{}])[0].get('current', None)
        except:
            cpu_temp = None

        # RAM
        mem = psutil.virtual_memory()
        ram_percent = mem.percent
        ram_used = round(mem.used / 1024 / 1024, 2)
        ram_free = round(mem.available / 1024 / 1024, 2)

        # GPU
        try:
            gpus = GPUtil.getGPUs()
            gpu_load = round(gpus[0].load * 100, 2)
            gpu_temp = gpus[0].temperature
        except:
            gpu_load = None
            gpu_temp = None

        dados = [
            timestamp,
            cpu_percent,
            cpu_temp,
            ram_percent,
            ram_used,
            ram_free,
            gpu_load,
            gpu_temp
        ]

        # Escreve no CSV
        with open(log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(dados)

        time.sleep(1)  # A cada 1 segundo

    return log_file