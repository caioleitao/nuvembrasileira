import socket
from datetime import datetime
from pathlib import Path

HOST = "127.0.0.1"
PORTA = 8080
PASTA_ARQUIVOS = Path(__file__).parent / "arquivos"

def receber_comando(conexao):
    dados = bytearray()
    while True:
        parte = conexao.recv(1)
        if not parte:
            if dados:
                return dados.decode("utf-8").strip()
            raise ConnectionError("Cleinte desconectou")
        if parte == b"\n":
            return dados.decode("utf-8").rstrip("\r")
        dados.extend(parte)

def receber_arquivo(conexao, arquivo, tamanho):
    while tamanho > 0:
        dados = conexao.recv(min(1024, tamanho))
        if not dados:
            raise ConnectionError("Conexão encerrada durante o upload")
        arquivo.write(dados)
        tamanho -= len(dados)

def enviar_arquivo(conexao, caminho):
    with caminho.open("rb") as arquivo:
        while dados := arquivo.read(1024):
            conexao.sendall(dados)

#evita vulnerabilidade do ../
def nome_seguro(nome):
    nome = Path(nome).name
    if nome in ("", ".", ".."):
        raiseValueError("Nome de arquivo inválido")
    return nome

def atender_cliente(conexao, endereco):
    print(f"Cliente conectado: {endereco}")
    with conexao:
        while True:
            linha = receber_comando(conexao)
            partes = linha.split()
            if not partes:
                continue
            comando = partes[0].upper()

            if comando == "UPLOAD" and len(partes) == 3:
                tamanho = int(partes[1])
                nome = nome_seguro(partes[2])
                with (PASTA_ARQUIVOS / nome).open("wb") as arquivo:
                    receber_arquivo(conexao, arquivo, tamanho)
                conexao.sendall(f"OK upload de {nome} concluido\n".encode("utf-8"))
                print("Arquivo recebido", nome)
            elif comando == "DOWNLOAD" and len(partes) >= 2:
                nome = nome_seguro(partes[1])
                caminho = PASTA_ARQUIVOS / nome
                if not caminho.is_file():
                    conexao.sendall(b"Erro arquivo nao encontrado\n")
                    continue
                tamanho = caminho.stat().st_size
                conexao.sendall(f"Ok {tamanho}\n".encode("ascii"))
                enviar_arquivo(conexao, caminho)
            elif comando == "LIST":
                arquivos = [p for p in sorted(PASTA_ARQUIVOS.iterdir()) if p.is_file()]
                conexao.sendall(f"OK {len(arquivos)}\n".encode("ascii"))
                for caminho in arquivos:
                    info = caminho.stat()
                    data = datetime.fromtimestamp(info.st_mtime).isoformat(timespec="seconds")
                    cliente_enviado = str(endereco)
                    linha_arquivo = f"{caminho.name}\t{info.st_size}\t\t{data}\t{cliente_enviado}\n"
                    conexao.sendall(linha_arquivo.encode("utf-8"))
            elif comando in ("EXIT", "QUIT"):
                conexao.sendall("Ok até logo\n".encode("utf-8"))
                break
            else:
                conexao.sendall(b"Error comando invalido\n")

def main():
    total_clientes = int(input("Quantidade de clientes para atender: "))
    if total_clientes < 1:
        print("informe pelo menos um cliente.")
        return

    PASTA_ARQUIVOS.mkdir(exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORTA))
        servidor.listen(total_clientes)

        print(f"Servidor ouvindo em {HOST}:{PORTA}")

        for numero in range(total_clientes):
            conexao, endereco = servidor.accept()
            print(f"Atendendo cliente {numero + 1} de {total_clientes}")
            try:
                atender_cliente(conexao, endereco)
            except(ConnectionError, OSError, ValueError) as erro:
                print(erro)
            print("Todos os clientes foram atendidos")

if __name__ == "__main__":
    main()