# UnfollowersCheck

Script simples em Python que compara os arquivos `following.js` e `follower.js` do seu arquivo de dados do X (Twitter) e gera uma lista de contas que você segue mas que não te seguem de volta.

Tudo roda localmente, no seu computador. O script não acessa a internet nem a API do X — ele só lê os arquivos que você mesmo baixou.

## Requisitos

- Python 3.7 ou superior (não precisa instalar nenhuma biblioteca extra, o script usa só a biblioteca padrão do Python).

## Como conseguir os arquivos `following.js` e `follower.js`

1. No X, acesse **Configurações e privacidade → Sua conta → Baixar um arquivo de dados**.
2. Confirme sua senha e solicite o arquivo. O X pode levar de alguns minutos a alguns dias para preparar o download (você recebe um e-mail e uma notificação quando estiver pronto).
3. Baixe e extraia o `.zip` recebido.
4. Dentro da pasta extraída, procure em `data/`:
   - `following.js`
   - `follower.js`
5. Copie esses dois arquivos para a pasta deste projeto (ou anote o caminho completo até eles).

## Como usar

Pelo terminal, na pasta do projeto:

```bash
python checar_unfollowers.py following.js follower.js
```

Se os arquivos estiverem em outro lugar, informe o caminho completo:

```bash
python checar_unfollowers.py /caminho/para/following.js /caminho/para/follower.js
```

### Saída

O script imprime no terminal:

- Quantas contas você segue
- Quantas contas te seguem
- Quantas não te seguem de volta, com a lista de `accountId` + link do perfil

Exemplo:

```
Você segue: 350 contas
Te seguem: 320 contas
Não te seguem de volta: 33 contas

Lista de quem não te segue de volta (accountId + link):
- 1075921659947827200 -> https://twitter.com/intent/user?user_id=1075921659947827200
- 1167260493540745216 -> https://twitter.com/intent/user?user_id=1167260493540745216
...

Lista salva em: /caminho/completo/nao_seguem_de_volta.txt
```

Além de imprimir no terminal, o resultado também é salvo em `nao_seguem_de_volta.txt`, no formato `accountId<TAB>link`.

### Descobrindo o @ (username) de cada conta

O arquivo de dados do X só traz o `accountId` numérico, não o `@usuario`. Para saber quem é a conta, basta abrir o link `userLink` de cada linha (`https://twitter.com/intent/user?user_id=...`) no navegador — ele redireciona para o perfil correspondente.

## Estrutura do projeto

```
UnfollowersCheck/
├── checar_unfollowers.py     # script principal
├── README.md
└── .gitignore
```

Os arquivos `following.js`, `follower.js` e `nao_seguem_de_volta.txt` **não são versionados** (veja `.gitignore`), pois contêm dados pessoais da sua conta do X.

## Privacidade

Os arquivos `following.js` e `follower.js` contêm dados da sua rede no X. Evite compartilhar ou commitar esses arquivos em repositórios públicos.
