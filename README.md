# UnfollowersCheck

Programa simples que compara os arquivos `following.js` e `follower.js` do seu arquivo de dados do X (Twitter) e gera uma lista de contas que você segue mas que não te seguem de volta.

Tudo roda localmente, no seu computador. O programa não acessa a internet nem a API do X — ele só lê os arquivos que você mesmo baixou.

Tem duas formas de usar:

- **Interface gráfica** (`gui.py` ou o executável da [página de Releases](../../releases)): selecione os arquivos em janelas de "Abrir arquivo", clique em Verificar e veja o resultado na tela.
- **Linha de comando** (`checar_unfollowers.py`): para quem prefere terminal ou quer automatizar.

## Baixando um executável pronto (sem instalar Python)

Na [página de Releases](../../releases) do repositório há executáveis prontos para Windows, macOS e Linux. Baixe o arquivo correspondente ao seu sistema, execute-o e use a interface gráfica normalmente — não é necessário instalar Python.

> No macOS/Linux pode ser preciso marcar o arquivo como executável (`chmod +x UnfollowersCheck-linux`) antes de rodar. No Windows, o SmartScreen pode avisar que o executável não é reconhecido (comum em programas sem assinatura digital) — escolha "Mais informações → Executar assim mesmo".

## Rodando a partir do código-fonte

### Requisitos

- Python 3.7 ou superior.
- Para a interface gráfica, o módulo `tkinter` (já vem com o instalador oficial do Python no Windows e macOS; no Linux, se necessário, instale com `sudo apt install python3-tk` ou equivalente da sua distro).
- Nenhuma biblioteca externa é necessária — o projeto usa só a biblioteca padrão do Python.

### Como conseguir os arquivos `following.js` e `follower.js`

1. No X, acesse **Configurações e privacidade → Sua conta → Baixar um arquivo de dados**.
2. Confirme sua senha e solicite o arquivo. O X pode levar de alguns minutos a alguns dias para preparar o download (você recebe um e-mail e uma notificação quando estiver pronto).
3. Baixe e extraia o `.zip` recebido.
4. Dentro da pasta extraída, procure em `data/`:
   - `following.js`
   - `follower.js`
5. Copie esses dois arquivos para a pasta deste projeto (ou anote o caminho completo até eles).

### Usando a interface gráfica

```bash
python gui.py
```

Uma janela abre com dois campos: um para selecionar o `following.js` e outro para o `follower.js`. Clique em **Selecionar...** em cada um, escolha os arquivos, depois clique em **Verificar**. O resultado aparece na caixa de texto, e o botão **Salvar lista (.txt)** deixa escolher onde salvar o arquivo com a lista de quem não te segue de volta.

### Usando a linha de comando

```bash
python checar_unfollowers.py following.js follower.js
```

Se os arquivos estiverem em outro lugar, informe o caminho completo:

```bash
python checar_unfollowers.py /caminho/para/following.js /caminho/para/follower.js
```

#### Saída

O script imprime no terminal:

- Quantas contas você segue
- Quantas contas te seguem
- Quantas não te seguem de volta, com a lista de `accountId` + link do perfil

Exemplo (com IDs fictícios, apenas para ilustrar o formato):

```
Você segue: 350 contas
Te seguem: 320 contas
Não te seguem de volta: 3 contas

Lista de quem não te segue de volta (accountId + link):
- 1000000000000000001 -> https://twitter.com/intent/user?user_id=1000000000000000001
- 1000000000000000002 -> https://twitter.com/intent/user?user_id=1000000000000000002
- 1000000000000000003 -> https://twitter.com/intent/user?user_id=1000000000000000003

Lista salva em: /caminho/completo/nao_seguem_de_volta.txt
```

Além de imprimir no terminal, o resultado também é salvo em `nao_seguem_de_volta.txt`, no formato `accountId<TAB>link`.

### Descobrindo o @ (username) de cada conta

O arquivo de dados do X só traz o `accountId` numérico, não o `@usuario`. Para saber quem é a conta, basta abrir o link `userLink` de cada linha (`https://twitter.com/intent/user?user_id=...`) no navegador — ele redireciona para o perfil correspondente.

## Gerando um executável você mesmo

O projeto usa [PyInstaller](https://pyinstaller.org/) para gerar os executáveis publicados nas Releases. Para gerar localmente:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name UnfollowersCheck gui.py
```

O executável fica em `dist/UnfollowersCheck`.

## Estrutura do projeto

```
UnfollowersCheck/
├── checar_unfollowers.py         # lógica principal + versão em linha de comando
├── gui.py                        # interface gráfica (tkinter)
├── .github/workflows/release.yml # build automático dos executáveis ao criar uma tag
├── README.md
└── .gitignore
```

Os arquivos `following.js`, `follower.js` e `nao_seguem_de_volta.txt` **não são versionados** (veja `.gitignore`), pois contêm dados pessoais da sua conta do X.

## Privacidade

Os arquivos `following.js` e `follower.js` contêm dados da sua rede no X. Evite compartilhar ou commitar esses arquivos em repositórios públicos.
