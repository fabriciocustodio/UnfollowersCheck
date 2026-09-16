import json
import sys
from pathlib import Path


def carregar_js_como_json(caminho):
    """
    Os arquivos do Twitter/X vêm no formato:
        window.YTD.following.part0 = [ ... ]
    Esta função remove essa parte inicial e faz o parse do JSON.
    """
    texto = Path(caminho).read_text(encoding="utf-8")

    # Remove tudo antes do primeiro "[" (a atribuição window.YTD... = )
    inicio = texto.find("[")
    if inicio == -1:
        raise ValueError(f"Não encontrei um array JSON em {caminho}")

    json_texto = texto[inicio:]
    return json.loads(json_texto)


def extrair_ids(dados, chave):
    """
    Extrai o conjunto de accountIds de uma lista de objetos
    no formato {"following": {...}} ou {"follower": {...}}
    """
    ids = {}
    for item in dados:
        info = item.get(chave, {})
        account_id = info.get("accountId")
        user_link = info.get("userLink")
        if account_id:
            ids[account_id] = user_link
    return ids


def main():
    if len(sys.argv) != 3:
        print("Uso: python checar_unfollowers.py following.js follower.js")
        sys.exit(1)

    caminho_following = sys.argv[1]
    caminho_follower = sys.argv[2]

    following_data = carregar_js_como_json(caminho_following)
    follower_data = carregar_js_como_json(caminho_follower)

    following_ids = extrair_ids(following_data, "following")
    follower_ids = extrair_ids(follower_data, "follower")

    nao_seguem_de_volta = set(following_ids.keys()) - set(follower_ids.keys())

    print(f"Você segue: {len(following_ids)} contas")
    print(f"Te seguem: {len(follower_ids)} contas")
    print(f"Não te seguem de volta: {len(nao_seguem_de_volta)} contas\n")

    if nao_seguem_de_volta:
        print("Lista de quem não te segue de volta (accountId + link):")
        for account_id in sorted(nao_seguem_de_volta):
            link = following_ids[account_id]
            print(f"- {account_id} -> {link}")

        # Salva também em um arquivo de texto
        saida = Path("nao_seguem_de_volta.txt")
        with saida.open("w", encoding="utf-8") as f:
            for account_id in sorted(nao_seguem_de_volta):
                f.write(f"{account_id}\t{following_ids[account_id]}\n")
        print(f"\nLista salva em: {saida.resolve()}")
    else:
        print("Todo mundo que você segue te segue de volta! 🎉")


if __name__ == "__main__":
    main()
