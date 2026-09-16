import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

from checar_unfollowers import carregar_js_como_json, extrair_ids


class UnfollowersCheckApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UnfollowersCheck")
        self.geometry("620x520")
        self.minsize(560, 420)

        self.following_path = tk.StringVar()
        self.follower_path = tk.StringVar()
        self.resultado_linhas = []

        self._montar_layout()

    def _montar_layout(self):
        padding = {"padx": 10, "pady": 6}

        frame_arquivos = ttk.Frame(self)
        frame_arquivos.pack(fill="x", **padding)

        self._linha_selecao(
            frame_arquivos,
            "following.js (quem você segue):",
            self.following_path,
            self._selecionar_following,
        )
        self._linha_selecao(
            frame_arquivos,
            "follower.js (quem te segue):",
            self.follower_path,
            self._selecionar_follower,
        )

        frame_botoes = ttk.Frame(self)
        frame_botoes.pack(fill="x", **padding)

        ttk.Button(
            frame_botoes, text="Verificar", command=self._verificar
        ).pack(side="left")
        self.botao_salvar = ttk.Button(
            frame_botoes,
            text="Salvar lista (.txt)",
            command=self._salvar_resultado,
            state="disabled",
        )
        self.botao_salvar.pack(side="left", padx=8)

        self.texto_resultado = scrolledtext.ScrolledText(self, wrap="word")
        self.texto_resultado.pack(fill="both", expand=True, **padding)
        self.texto_resultado.configure(state="disabled")

    def _linha_selecao(self, container, rotulo, variavel, comando):
        linha = ttk.Frame(container)
        linha.pack(fill="x", pady=4)

        ttk.Label(linha, text=rotulo, width=28).pack(side="left")
        ttk.Entry(linha, textvariable=variavel, state="readonly").pack(
            side="left", fill="x", expand=True, padx=6
        )
        ttk.Button(linha, text="Selecionar...", command=comando).pack(side="left")

    def _selecionar_following(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo following.js",
            filetypes=[("Arquivo following.js", "following.js"), ("Todos os arquivos", "*.*")],
        )
        if caminho:
            self.following_path.set(caminho)

    def _selecionar_follower(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo follower.js",
            filetypes=[("Arquivo follower.js", "follower.js"), ("Todos os arquivos", "*.*")],
        )
        if caminho:
            self.follower_path.set(caminho)

    def _verificar(self):
        caminho_following = self.following_path.get()
        caminho_follower = self.follower_path.get()

        if not caminho_following or not caminho_follower:
            messagebox.showwarning(
                "Arquivos faltando",
                "Selecione os dois arquivos (following.js e follower.js) antes de verificar.",
            )
            return

        try:
            following_data = carregar_js_como_json(caminho_following)
            follower_data = carregar_js_como_json(caminho_follower)
        except Exception as erro:
            messagebox.showerror("Erro ao ler arquivos", str(erro))
            return

        following_ids = extrair_ids(following_data, "following")
        follower_ids = extrair_ids(follower_data, "follower")
        nao_seguem_de_volta = sorted(set(following_ids.keys()) - set(follower_ids.keys()))

        self.resultado_linhas = [
            f"{account_id}\t{following_ids[account_id]}" for account_id in nao_seguem_de_volta
        ]

        linhas_exibicao = [
            f"Você segue: {len(following_ids)} contas",
            f"Te seguem: {len(follower_ids)} contas",
            f"Não te seguem de volta: {len(nao_seguem_de_volta)} contas",
            "",
        ]

        if nao_seguem_de_volta:
            linhas_exibicao.append("Lista de quem não te segue de volta (accountId + link):")
            for account_id in nao_seguem_de_volta:
                linhas_exibicao.append(f"- {account_id} -> {following_ids[account_id]}")
        else:
            linhas_exibicao.append("Todo mundo que você segue te segue de volta! 🎉")

        self._exibir_resultado("\n".join(linhas_exibicao))
        self.botao_salvar.configure(state="normal" if nao_seguem_de_volta else "disabled")

    def _exibir_resultado(self, texto):
        self.texto_resultado.configure(state="normal")
        self.texto_resultado.delete("1.0", "end")
        self.texto_resultado.insert("1.0", texto)
        self.texto_resultado.configure(state="disabled")

    def _salvar_resultado(self):
        if not self.resultado_linhas:
            return

        caminho = filedialog.asksaveasfilename(
            title="Salvar lista de quem não te segue de volta",
            defaultextension=".txt",
            initialfile="nao_seguem_de_volta.txt",
            filetypes=[("Arquivo de texto", "*.txt")],
        )
        if not caminho:
            return

        Path(caminho).write_text("\n".join(self.resultado_linhas) + "\n", encoding="utf-8")
        messagebox.showinfo("Lista salva", f"Lista salva em:\n{caminho}")


def main():
    app = UnfollowersCheckApp()
    app.mainloop()


if __name__ == "__main__":
    main()
