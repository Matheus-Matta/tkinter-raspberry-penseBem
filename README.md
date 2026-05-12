# Pense Bem - Emulador Python

Este projeto é uma recriação em Python do clássico brinquedo "Pense Bem", otimizado para ser executado em ambientes leves, como um Raspberry Pi. O aplicativo utiliza a biblioteca `customtkinter` para fornecer uma interface moderna e responsiva.

## Pré-requisitos

Para rodar este projeto, você precisará ter o **Python 3** instalado em sua máquina ou no seu emulador Raspberry Pi.

Além disso, é necessário possuir uma interface gráfica no sistema (X11, Wayland ou similar), pois o aplicativo abrirá uma janela.

## Como instalar

1. Acesse o diretório do projeto Python:
   ```bash
   cd projeto_python
   ```

2. Recomenda-se criar um ambiente virtual (opcional, mas recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Instalação em Raspberry Pi (Offline)

Se o seu Raspberry Pi não tiver acesso à internet, siga estes passos para levar as dependências:

1. **Em um computador com internet**, baixe as bibliotecas (Wheels) para uma pasta chamada `vendor`:
   ```bash
   mkdir vendor
   pip download -d vendor -r requirements.txt
   ```

2. **Copie a pasta do projeto + a pasta `vendor`** para um pendrive e passe para o Raspberry Pi.

3. **No Raspberry Pi**, instale as bibliotecas localmente:
   ```bash
   pip install --no-index --find-links=./vendor -r requirements.txt
   ```

> [!IMPORTANT]
> O `customtkinter` depende do `tkinter` do sistema. No Raspberry Pi OS (Linux), você **precisa** garantir que o pacote `python3-tk` esteja instalado. Como ele é um pacote do sistema, se você não tiver internet no Pi, precisará baixar o arquivo `.deb` correspondente à sua versão do OS em outro PC ou instalar enquanto o Pi ainda tiver internet uma única vez: `sudo apt install python3-tk`.

## Criando Executável Único (Linux)

Se você quiser transformar o projeto em um único arquivo executável (para facilitar a distribuição), utilizaremos o **PyInstaller**.

> [!CAUTION]
> **Arquitetura (PC vs Raspberry Pi):** Se você gerar o executável no seu computador Windows ou Linux (x86), ele **NÃO** funcionará no Raspberry Pi (ARM). Para gerar um executável para o Raspberry, você deve rodar os comandos abaixo **dentro do próprio Raspberry Pi**.

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Gere o arquivo único:
   ```bash
   pyinstaller --noconfirm --onefile --windowed --name "PenseBem" main.py
   ```

3. O arquivo executável será gerado dentro da pasta `dist/PenseBem`.

---

## Como executar


Com as dependências instaladas, basta executar o arquivo principal:

```bash
python main.py
```

## Como jogar

Ao iniciar o programa, siga estes passos:
1. **Escolha o Livro**: Digite o código de um dos livros disponíveis (por exemplo: `021`, `081` ou `131`) e pressione **Enter**.
2. **Responda às Perguntas**: O programa mostrará o número do programa (1 a 5 regulares, mais o programa final 6) e o número da questão.
3. **Controles**: Utilize o teclado para navegar e responder (mais rápido para emuladores):
   - **Menu (Home):** `Q` (Sobe), `W` (Seleciona/Inicia), `E` (Desce), `ESC` (Sai do jogo)
   - **No Jogo:** 
     - `Q` -> Opção A
     - `W` -> Opção B
     - `E` -> Opção C
     - `R` -> Opção D
     - `ESC` -> Voltar ao Menu
4. **Tentativas e Pontuação**: Você tem até 3 tentativas por pergunta. Se acertar de primeira, ganha 3 pontos. Na segunda, 2 pontos. Na terceira, 1 ponto. Ao final de cada programa e do livro, um resumo detalhado de acertos e erros (%) será exibido.


Divirta-se relembrando este clássico!
