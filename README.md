# nuvembrasileira

## Estrutura do projeto

```
nuvembrasileira/
├── servidor/
│   ├── servidor.py
│   └── arquivos/
├── cliente/
│   └── cliente.py
└── README.md
```

## Pré-requisitos 

- Python 3.8 ou superior instalado.

A instalação de nenhuma biblioteca externa se faz necessária, pois o projeto usa apenas módulos da biblioteca padrão do Python.

Para conferir a instalação do python:

**Linux/mac os**

```bash
python3 --version
```

**Windows**

```powershell
python --version
```

ou 

```powershell
py --version
```

## Passo a passo

#### 1. Entre na pasta onde o projeto está

```bash
cd pasta/de/trabalho/nuvembrasileira/
```

#### 2. Inicie o servidor (terminal 1)

**Linux/macOS:**

```bash
python3 servidor/servidor.py
```

**Windows:**

```powershell
python servidor/servidor.py
```

Quando aparecer:

```text
Quantidade de clientes para atender:
```

Digite `1` para testar com um cliente e pressione Enter. O terminal exibirá:

```text
Servidor ouvindo em 127.0.0.1:8080
```

**Não feche o terminal!!!**. O número informado é a quantidade total de conexões que o servidor aceitará nesta execução.

#### 3. Inicie o cliente (terminal 2)

**Linux/macOS:**

```bash
python3 cliente/cliente.py
```

**Windows:**

```powershell
python cliente/cliente.py
```

Saída esperada:

```text
Conectado a 127.0.0.1:8080. Use Upload arquivo, Download arquivo ou LIST ou EXIT
>
```

Agora você pode digitar comandos no terminal do cliente.

#### 4. Envie um arquivo (UPLOAD)

Crie um arquivo de teste na pasta `cliente/`, por exemplo `sonic.webm`.


```text
> UPLOAD cliente/sonic.webm
```

Saída esperada:

```text
OK upload de sonic.webm concluido
```

O arquivo será salvo em `servidor/arquivos/sonic.webm`. 

#### 5. Liste os arquivos (LIST)

```text
> LIST
```

O cliente mostrará o nome, o tamanho em bytes, a data de modificação e o endereço da conexão do cliente que solicitou a listagem.

#### 6. Baixe um arquivo (DOWNLOAD)

```text
> DOWNLOAD sonic.webm
```

O arquivo será salvo na pasta de onde você executou o cliente.

### 7. Encerre a conexão

```text
> EXIT
```

Se você configurou apenas um cliente, o servidor terminará depois dessa conexão. Para iniciar outro teste, execute novamente o servidor antes do cliente.

## Comandos disponíveis

| Comando | Função | Exemplo |
| --- | --- | --- |
| `UPLOAD <caminho>` | Envia um arquivo local ao servidor | `UPLOAD cliente/sonic.webm` |
| `DOWNLOAD <nome>` | Baixa um arquivo do servidor | `DOWNLOAD sonic.webm` |
| `LIST` | Lista os arquivos armazenados | `LIST` |
| `EXIT` | Encerra a sessão do cliente | `EXIT` |

## Configuração de rede

Por padrão, ambos os scripts utilizam:

```python
HOST = "127.0.0.1"
PORTA = 8080
```
 
