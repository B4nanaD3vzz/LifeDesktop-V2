# LifeDesktop-V2
<img src="https://share.creavite.co/68054be48bd3b02a647afaa1.gifautoplay=1">

<details>
  <summary>Versão em português - BR </summary>

  ```markdown
# 🎯 LifeDesktop — Sistema de Monitoramento Avançado (Overlay + Logs)

> Monitoramento em tempo real de **CPU, GPU, RAM, Rede, FPS**, temperatura e muito mais — com overlay transparente, logging em CSV e análise de métricas.

---

## 🧩 Sobre o Projeto

O **Life Desktop** é uma aplicação desenvolvida em Python com uma interface leve e sobreposta (`overlay`) que coleta dados em tempo real do sistema e jogos. Ideal para análise de desempenho, amostragem técnica, testes de stress ou uso pessoal.

O sistema inclui:

- Monitoramento ao vivo de hardware
- Gravação de logs em `.csv`
- Interface gráfica com `customtkinter`
- Overlay transparente que permanece acima de todas as janelas
- Geração de métricas de uso ao final da sessão

---

## 📊 O que a aplicação monitora

| Recurso              | Detalhes coletados                                        |
|----------------------|-----------------------------------------------------------|
| **CPU**              | Uso (%) e temperatura                                     |
| **RAM**              | Uso (%), usada e livre em MB                              |
| **GPU (NVIDIA)**     | Uso (%) e temperatura                                     |
| **Internet**         | Upload e download em KB/s                                 |
| **FPS**              | FPS atual em programas e jogos                            |


---

## 🧰 Tecnologias e Bibliotecas Utilizadas

| Biblioteca           | Função principal                                  |
|----------------------|---------------------------------------------------|
| `psutil`             | Coleta dados de CPU, RAM, disco e rede            |
| `GPUtil`             | Coleta dados da GPU (NVIDIA)                      |
| `customtkinter`      | Interface gráfica moderna e personalizável        |
| `tkinter`            | Base para a GUI e overlay                         |
| `pandas`             | Geração de métricas com base nos logs             |
| `datetime` / `os`    | Manipulação de arquivos, diretórios e tempo       |

---

## 🖥️ Interface (Overlay)

- Caixa flutuante sobre todas as janelas
- Transparente com borda verde fina
- Texto em **verde limão** sobre fundo escuro (estilo HUD)
- Pode ser arrastada pela tela
- Exibe: CPU, RAM, GPU, Net e agora FPS.

---

## 📁 Estrutura de Arquivos

LifeDesktop/
├── main.py               # Inicia a aplicação e gera métricas finais
├── monitor.py            # Coleta e grava dados em tempo real
├── overlay.py            # Interface HUD sobreposta com informações ao vivo
├── logs/                 # Pasta onde os arquivos CSV são salvos
├── README.md             # Este documento
└── requirements.txt      # Bibliotecas necessárias

```

 INSTALAÇÃO:
- 1 Clone o repositório:
  ```bash
  git clone https://github.com/B4nanaD3vzz/LifeDesktop-V2.git
  cd LifeDesktop
  ```

-2 Instale as Dependencias:
 ```bash
 pip install -r requirements.txt
 ```

-3 Execute a aplicação:
 ```bash
 python main.py
 ```

<h1 align="center">COMO USAR</h1>
 - Interface HUD será aberta
 <img src="https://i.postimg.cc/J7K5rrQB/Captura-de-Tela-28.png">
 Observe que possui 3 botões no lado esquerdo:
 
 ```markdown
 > Home - Principal
 > Dados - Grafico em tempo real
 > Configurações - Configurações do software (ainda em desenvolvimento)
```
 - Os dados começam a ser coletados automaticamente.
```markdown
> Use o botão "Iniciar monitoramento" para começar a aparecer as métricas em sua tela.
> Use o botâo "Parar e exibir métricas" para exibir a log de captura de dados.
```

<h2>Como será exibido o overlay:</h2>
<img src="https://i.postimg.cc/Mp8sXWL0/Captura-de-Tela-32.png">

# Contribuições:
 Se você quer contribuir mas não quer ou não sabe programar, saiba que idéias são válidas e ajudam muito, a sua idéia poderá está na próxima versão do LifeDesktop.

 ## 🧠 Autor

Desenvolvido por **[B4nanaD3vzz]**  
Se curtir, ⭐ no repo é sempre bem-vindo!


</details>


