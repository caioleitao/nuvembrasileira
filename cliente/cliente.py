import socket
import sys
from pathlib import Path

HOST = "127.0.0.1"
PORTA = 8080

def enviar_linha(conexao, texto):
    conexao.sendall((texto + "\n").encode("utf-8"))

def receber_linha(conexao):
    dados = bytearray()
    while True:
        parte = conexao.recv(1)
        if not parte:
            raise ConnectionError("Servidor encerrou a conexão")
        if parte == b"\n":
            return dados.decode("utf-8").rstrip("\r")
        dados.extend(parte)

def enviar_arquivo(conexao, nome):
    caminho = Path(nome).expanduser()
    if not caminho.is_file():
        print("Arquivo local não encontrado.")
        return
    tamanho = caminho.stat().st_size
    enviar_linha(conexao, f"UPLOAD {tamanho} {caminho.name}")
    with caminho.open("rb") as arquivo:
        while dados := arquivo.read(1024):
            conexao.sendall(dados)
    print(receber_linha(conexao))

def baixar_arquivo(conexao, nome):
    enviar_linha(conexao, f"DOWNLOAD {Path(nome).name}")
    resposta = receber_linha(conexao)
    if resposta.startswith("ERRO "):
        print(resposta[5:])
        return
    tamanho = int(resposta.split()[1])
    destino = Path(nome).name
    with open(destino, "wb") as arquivo:
        while tamanho > 0:
            dados = conexao.recv(min(1024, tamanho))
            if not dados:
                raise ConnectionError("Conexão encerrada durante o download")
            arquivo.write(dados)
            tamanho -= len(dados)
    print("Download salvo em:", Path(destino).resolve())

def listar_arquivos(conexao):
    enviar_linha(conexao, "LIST")
    resposta = receber_linha(conexao).split()
    quantidade = int(resposta[1])
    if quantidade == 0:
        print("Nenhum arquivo no servidor")
        return
    print("Nome\t\tTamanho (bytes)\tModificado\t\tEnviado pelo cliente")
    for _ in range(quantidade):
        print(receber_linha(conexao).replace("\t", "\t"))

def main():
    host = sys.argv[1] if len(sys.argv) > 1 else HOST
    with socket.create_connection((host, PORTA)) as conexao:
        print(f"Conectado a {host}:{PORTA}. Use Upload arquivo, Download arquivo ou LIST ou EXIT")
        while True:
            partes = input("> ").strip().split(maxsplit=1)
            if not partes:
                continue
            comando = partes[0].upper()
            argumento = partes[1] if len(partes) > 1 else ""
            if comando == "UPLOAD" and argumento:
                enviar_arquivo(conexao, argumento)
            elif comando == "DOWNLOAD" and argumento:
                baixar_arquivo(conexao, argumento)
            elif comando == "LIST":
                listar_arquivos(conexao)
            elif comando in ("EXIT", "QUIT"):
                enviar_linha(conexao, "EXIT")
                print(receber_linha(conexao))
                break
            else:
                print("Use Upload <arquivo>, DONWLOAD <arquivo>, LIST ou EXIT")

if __name__ == "__main__":
    main()