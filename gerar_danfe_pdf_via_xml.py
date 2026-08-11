#!/usr/bin/env python3
# gerar_danfe_tkinter.py
# Interface Tkinter para gerar DANFE PDF a partir de XML autorizado de NF-e.
# Permite gerar um único PDF ou gerar PDFs em lote a partir de uma pasta.

import os
import sys
import threading
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from brazilfiscalreport.danfe import Danfe, DanfeConfig
except ImportError:
    Danfe = None
    DanfeConfig = None


def ler_xml(caminho: Path) -> str:
    dados = caminho.read_bytes()

    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return dados.decode(encoding)
        except UnicodeDecodeError:
            continue

    return dados.decode("utf-8", errors="replace")


def nome_tag(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def buscar_texto(root: ET.Element, tag_local: str) -> str | None:
    for elemento in root.iter():
        if nome_tag(elemento.tag) == tag_local:
            return (elemento.text or "").strip()
    return None


def buscar_chave_nfe(root: ET.Element) -> str | None:
    for elemento in root.iter():
        if nome_tag(elemento.tag) == "infNFe":
            chave = elemento.attrib.get("Id", "")
            chave = chave.replace("NFe", "").strip()
            if len(chave) == 44 and chave.isdigit():
                return chave
    return None


def validar_xml_nfe(xml_texto: str) -> tuple[str | None, str | None, str | None]:
    root = ET.fromstring(xml_texto)

    modelo = buscar_texto(root, "mod")
    cstat = buscar_texto(root, "cStat")
    chave = buscar_chave_nfe(root)

    return modelo, cstat, chave


def nome_pdf_para_xml(xml_path: Path, pasta_saida: Path, xml_texto: str) -> Path:
    try:
        root = ET.fromstring(xml_texto)
        chave = buscar_chave_nfe(root)
    except Exception:
        chave = None

    if chave:
        nome = f"{chave}.pdf"
    else:
        nome = f"{xml_path.stem}.pdf"

    return pasta_saida / nome


def evitar_sobrescrever(caminho: Path) -> Path:
    if not caminho.exists():
        return caminho

    base = caminho.stem
    sufixo = caminho.suffix
    pasta = caminho.parent

    contador = 2

    while True:
        candidato = pasta / f"{base}_{contador}{sufixo}"
        if not candidato.exists():
            return candidato
        contador += 1


def listar_xmls(pasta: Path, incluir_subpastas: bool) -> list[Path]:
    if incluir_subpastas:
        arquivos = list(pasta.rglob("*.xml"))
    else:
        arquivos = list(pasta.glob("*.xml"))

    return sorted([arquivo for arquivo in arquivos if arquivo.is_file()])


def criar_danfe(xml_texto: str, pdf_saida: Path, logo: Path | None) -> None:
    if Danfe is None or DanfeConfig is None:
        raise RuntimeError(
            "A biblioteca 'brazilfiscalreport' não está instalada.\n\n"
            "Instale com:\n"
            "python -m pip install --upgrade brazilfiscalreport"
        )

    pdf_saida.parent.mkdir(parents=True, exist_ok=True)

    if logo:
        config = DanfeConfig()
        config.logo = str(logo)
        danfe = Danfe(xml=xml_texto, config=config)
    else:
        danfe = Danfe(xml=xml_texto)

    danfe.output(str(pdf_saida))


def gerar_danfe_pdf(
    xml_entrada: Path,
    pdf_saida: Path,
    logo: Path | None = None,
    sobrescrever: bool = True,
) -> tuple[Path, list[str]]:
    if not xml_entrada.exists():
        raise FileNotFoundError(f"Arquivo XML não encontrado: {xml_entrada}")

    if logo and not logo.exists():
        raise FileNotFoundError(f"Arquivo de logo não encontrado: {logo}")

    xml_texto = ler_xml(xml_entrada)
    avisos = []

    modelo, cstat, _ = validar_xml_nfe(xml_texto)

    if modelo and modelo != "55":
        avisos.append(
            f"Modelo encontrado: {modelo}. Para DANFE tradicional, o esperado é NF-e modelo 55."
        )

    if cstat and cstat != "100":
        avisos.append(
            f"cStat encontrado: {cstat}. Normalmente o esperado para XML autorizado é cStat=100."
        )

    if not cstat:
        avisos.append(
            "Não foi encontrado cStat. Verifique se é o XML autorizado completo da NF-e."
        )

    if not sobrescrever:
        pdf_saida = evitar_sobrescrever(pdf_saida)

    criar_danfe(xml_texto, pdf_saida, logo)

    if not pdf_saida.exists():
        avisos.append("A geração terminou, mas o arquivo PDF não foi encontrado no destino.")

    return pdf_saida, avisos


def gerar_lote_pasta(
    pasta_xml: Path,
    pasta_saida: Path,
    logo: Path | None = None,
    incluir_subpastas: bool = False,
    sobrescrever: bool = True,
    callback_progresso=None,
) -> dict:
    if not pasta_xml.exists() or not pasta_xml.is_dir():
        raise NotADirectoryError(f"Pasta de XML não encontrada: {pasta_xml}")

    if logo and not logo.exists():
        raise FileNotFoundError(f"Arquivo de logo não encontrado: {logo}")

    xmls = listar_xmls(pasta_xml, incluir_subpastas)

    resultado = {
        "total": len(xmls),
        "sucesso": [],
        "falha": [],
    }

    for indice, xml_path in enumerate(xmls, start=1):
        try:
            xml_texto = ler_xml(xml_path)
            validar_xml_nfe(xml_texto)

            pdf_saida = nome_pdf_para_xml(xml_path, pasta_saida, xml_texto)

            if not sobrescrever:
                pdf_saida = evitar_sobrescrever(pdf_saida)

            criar_danfe(xml_texto, pdf_saida, logo)

            resultado["sucesso"].append((xml_path, pdf_saida))

        except Exception as e:
            resultado["falha"].append((xml_path, str(e)))

        if callback_progresso:
            callback_progresso(indice, len(xmls), xml_path.name)

    return resultado


def abrir_arquivo(caminho: Path) -> None:
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(caminho))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(caminho)])
        else:
            subprocess.Popen(["xdg-open", str(caminho)])
    except Exception:
        pass


def abrir_pasta(caminho: Path) -> None:
    abrir_arquivo(caminho)


class DanfeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gerador de DANFE - XML NF-e para PDF")
        self.geometry("880x610")
        self.minsize(820, 560)

        self.modo_var = tk.StringVar(value="arquivo")

        self.xml_var = tk.StringVar()
        self.pdf_var = tk.StringVar()

        self.pasta_xml_var = tk.StringVar()
        self.pasta_saida_var = tk.StringVar()

        self.logo_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Selecione uma opção e informe os arquivos.")

        self.abrir_resultado_var = tk.BooleanVar(value=True)
        self.incluir_subpastas_var = tk.BooleanVar(value=False)
        self.sobrescrever_var = tk.BooleanVar(value=True)

        self._montar_interface()
        self._atualizar_modo()

        if Danfe is None:
            messagebox.showwarning(
                "Biblioteca não instalada",
                "A biblioteca 'brazilfiscalreport' não foi encontrada.\n\n"
                "Instale com:\n"
                "python -m pip install --upgrade brazilfiscalreport"
            )

    def _montar_interface(self):
        container = ttk.Frame(self, padding=18)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Gerador de DANFE em PDF",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")

        ttk.Label(
            container,
            text="Gere o DANFE de um XML específico ou processe todos os XMLs de uma pasta.",
        ).pack(anchor="w", pady=(4, 16))

        modo_frame = ttk.LabelFrame(container, text="Modo de geração", padding=10)
        modo_frame.pack(fill="x")

        ttk.Radiobutton(
            modo_frame,
            text="Gerar PDF de um único XML",
            variable=self.modo_var,
            value="arquivo",
            command=self._atualizar_modo,
        ).pack(side="left", padx=(0, 24))

        ttk.Radiobutton(
            modo_frame,
            text="Gerar PDFs de todos os XMLs de uma pasta",
            variable=self.modo_var,
            value="pasta",
            command=self._atualizar_modo,
        ).pack(side="left")

        self.frame_arquivo = ttk.LabelFrame(container, text="XML único", padding=10)
        self.frame_arquivo.pack(fill="x", pady=(14, 0))

        self._linha_arquivo(
            self.frame_arquivo,
            linha=0,
            rotulo="XML da NF-e:",
            variavel=self.xml_var,
            comando=self.selecionar_xml,
            texto_botao="Selecionar XML",
        )

        self._linha_arquivo(
            self.frame_arquivo,
            linha=1,
            rotulo="PDF de saída:",
            variavel=self.pdf_var,
            comando=self.selecionar_pdf_saida,
            texto_botao="Salvar como",
        )

        self.frame_arquivo.columnconfigure(1, weight=1)

        self.frame_pasta = ttk.LabelFrame(container, text="Geração em lote", padding=10)
        self.frame_pasta.pack(fill="x", pady=(14, 0))

        self._linha_arquivo(
            self.frame_pasta,
            linha=0,
            rotulo="Pasta dos XMLs:",
            variavel=self.pasta_xml_var,
            comando=self.selecionar_pasta_xml,
            texto_botao="Selecionar pasta",
        )

        self._linha_arquivo(
            self.frame_pasta,
            linha=1,
            rotulo="Pasta de saída:",
            variavel=self.pasta_saida_var,
            comando=self.selecionar_pasta_saida,
            texto_botao="Selecionar saída",
        )

        opcoes_lote = ttk.Frame(self.frame_pasta)
        opcoes_lote.grid(row=2, column=1, columnspan=2, sticky="w", pady=(6, 0))

        ttk.Checkbutton(
            opcoes_lote,
            text="Incluir XMLs de subpastas",
            variable=self.incluir_subpastas_var,
        ).pack(side="left", padx=(0, 18))

        self.frame_pasta.columnconfigure(1, weight=1)

        frame_opcoes = ttk.LabelFrame(container, text="Opções gerais", padding=10)
        frame_opcoes.pack(fill="x", pady=(14, 0))

        self._linha_arquivo(
            frame_opcoes,
            linha=0,
            rotulo="Logo opcional:",
            variavel=self.logo_var,
            comando=self.selecionar_logo,
            texto_botao="Selecionar logo",
        )

        ttk.Button(frame_opcoes, text="Limpar logo", command=self.limpar_logo).grid(
            row=0,
            column=3,
            padx=(8, 0),
            sticky="w",
        )

        checks = ttk.Frame(frame_opcoes)
        checks.grid(row=1, column=1, columnspan=3, sticky="w", pady=(8, 0))

        ttk.Checkbutton(
            checks,
            text="Abrir resultado após gerar",
            variable=self.abrir_resultado_var,
        ).pack(side="left", padx=(0, 18))

        ttk.Checkbutton(
            checks,
            text="Sobrescrever PDFs existentes",
            variable=self.sobrescrever_var,
        ).pack(side="left")

        frame_opcoes.columnconfigure(1, weight=1)

        botoes = ttk.Frame(container)
        botoes.pack(fill="x", pady=(14, 8))

        self.botao_gerar = ttk.Button(
            botoes,
            text="Gerar DANFE",
            command=self.iniciar_geracao,
        )
        self.botao_gerar.pack(side="left")

        self.botao_limpar = ttk.Button(
            botoes,
            text="Limpar campos",
            command=self.limpar_campos,
        )
        self.botao_limpar.pack(side="left", padx=(10, 0))

        self.progress = ttk.Progressbar(container, mode="determinate")
        self.progress.pack(fill="x", pady=(8, 8))

        status_frame = ttk.LabelFrame(container, text="Status", padding=10)
        status_frame.pack(fill="both", expand=True, pady=(8, 0))

        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            wraplength=800,
            justify="left",
        )
        self.status_label.pack(anchor="w", fill="x")

    def _linha_arquivo(self, parent, linha, rotulo, variavel, comando, texto_botao):
        ttk.Label(parent, text=rotulo).grid(
            row=linha,
            column=0,
            sticky="w",
            pady=6,
            padx=(0, 8),
        )

        entrada = ttk.Entry(parent, textvariable=variavel)
        entrada.grid(row=linha, column=1, sticky="ew", pady=6)

        botao = ttk.Button(parent, text=texto_botao, command=comando)
        botao.grid(row=linha, column=2, sticky="w", pady=6, padx=(8, 0))

    def _set_frame_enabled(self, frame: ttk.LabelFrame, enabled: bool):
        estado = "normal" if enabled else "disabled"

        def alterar(widget):
            try:
                widget.configure(state=estado)
            except tk.TclError:
                pass

            for filho in widget.winfo_children():
                alterar(filho)

        alterar(frame)

    def _atualizar_modo(self):
        modo = self.modo_var.get()

        self._set_frame_enabled(self.frame_arquivo, modo == "arquivo")
        self._set_frame_enabled(self.frame_pasta, modo == "pasta")

        if modo == "arquivo":
            self.status_var.set("Modo XML único selecionado.")
        else:
            self.status_var.set(
                "Modo pasta selecionado. Todos os XMLs da pasta serão lidos e convertidos."
            )

    def selecionar_xml(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o XML autorizado da NF-e",
            filetypes=[
                ("Arquivos XML", "*.xml"),
                ("Todos os arquivos", "*.*"),
            ],
        )

        if not caminho:
            return

        xml_path = Path(caminho)
        self.xml_var.set(str(xml_path))

        try:
            xml_texto = ler_xml(xml_path)
            _, _, chave = validar_xml_nfe(xml_texto)

            if chave:
                pdf_sugerido = xml_path.with_name(f"{chave}.pdf")
            else:
                pdf_sugerido = xml_path.with_suffix(".pdf")

            self.pdf_var.set(str(pdf_sugerido))
            self.status_var.set(
                "XML selecionado. Confira o local de saída e clique em Gerar DANFE."
            )

        except Exception as e:
            self.pdf_var.set(str(xml_path.with_suffix(".pdf")))
            self.status_var.set(
                "XML selecionado, mas não foi possível validar previamente.\n"
                f"Detalhe: {e}"
            )

    def selecionar_pdf_saida(self):
        nome_inicial = "danfe.pdf"

        if self.xml_var.get():
            nome_inicial = Path(self.xml_var.get()).with_suffix(".pdf").name

        caminho = filedialog.asksaveasfilename(
            title="Escolha onde salvar o DANFE PDF",
            defaultextension=".pdf",
            initialfile=nome_inicial,
            filetypes=[
                ("PDF", "*.pdf"),
                ("Todos os arquivos", "*.*"),
            ],
        )

        if caminho:
            pdf_path = Path(caminho)

            if pdf_path.suffix.lower() != ".pdf":
                pdf_path = pdf_path.with_suffix(".pdf")

            self.pdf_var.set(str(pdf_path))

    def selecionar_pasta_xml(self):
        caminho = filedialog.askdirectory(
            title="Selecione a pasta que contém os XMLs"
        )

        if not caminho:
            return

        pasta = Path(caminho)
        self.pasta_xml_var.set(str(pasta))

        if not self.pasta_saida_var.get().strip():
            self.pasta_saida_var.set(str(pasta / "danfes_pdf"))

        qtd = len(listar_xmls(pasta, self.incluir_subpastas_var.get()))
        self.status_var.set(f"Pasta selecionada. XMLs encontrados: {qtd}.")

    def selecionar_pasta_saida(self):
        caminho = filedialog.askdirectory(
            title="Selecione a pasta onde os PDFs serão salvos"
        )

        if caminho:
            self.pasta_saida_var.set(caminho)

    def selecionar_logo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione a logo do emitente",
            filetypes=[
                ("Imagens", "*.png *.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Todos os arquivos", "*.*"),
            ],
        )

        if caminho:
            self.logo_var.set(caminho)

    def limpar_logo(self):
        self.logo_var.set("")

    def limpar_campos(self):
        self.xml_var.set("")
        self.pdf_var.set("")
        self.pasta_xml_var.set("")
        self.pasta_saida_var.set("")
        self.logo_var.set("")
        self.progress["value"] = 0
        self.status_var.set("Selecione uma opção e informe os arquivos.")

    def iniciar_geracao(self):
        modo = self.modo_var.get()
        logo_texto = self.logo_var.get().strip()
        logo_path = Path(logo_texto) if logo_texto else None

        if modo == "arquivo":
            self._iniciar_geracao_arquivo(logo_path)
        else:
            self._iniciar_geracao_pasta(logo_path)

    def _bloquear_interface(self):
        self.botao_gerar.config(state="disabled")
        self.botao_limpar.config(state="disabled")

    def _liberar_interface(self):
        self.botao_gerar.config(state="normal")
        self.botao_limpar.config(state="normal")
        self._atualizar_modo()

    def _iniciar_geracao_arquivo(self, logo_path: Path | None):
        xml_texto = self.xml_var.get().strip()
        pdf_texto = self.pdf_var.get().strip()

        if not xml_texto:
            messagebox.showwarning("XML obrigatório", "Selecione o arquivo XML da NF-e.")
            return

        if not pdf_texto:
            messagebox.showwarning("PDF obrigatório", "Escolha onde salvar o PDF.")
            return

        xml_path = Path(xml_texto)
        pdf_path = Path(pdf_texto)

        if pdf_path.suffix.lower() != ".pdf":
            pdf_path = pdf_path.with_suffix(".pdf")
            self.pdf_var.set(str(pdf_path))

        self._bloquear_interface()
        self.progress["mode"] = "indeterminate"
        self.progress.start(10)
        self.status_var.set("Gerando DANFE PDF...")

        thread = threading.Thread(
            target=self._gerar_arquivo_thread,
            args=(xml_path, pdf_path, logo_path, self.sobrescrever_var.get()),
            daemon=True,
        )
        thread.start()

    def _iniciar_geracao_pasta(self, logo_path: Path | None):
        pasta_xml_texto = self.pasta_xml_var.get().strip()
        pasta_saida_texto = self.pasta_saida_var.get().strip()

        if not pasta_xml_texto:
            messagebox.showwarning(
                "Pasta obrigatória",
                "Selecione a pasta que contém os XMLs.",
            )
            return

        if not pasta_saida_texto:
            messagebox.showwarning(
                "Saída obrigatória",
                "Selecione a pasta onde os PDFs serão salvos.",
            )
            return

        pasta_xml = Path(pasta_xml_texto)
        pasta_saida = Path(pasta_saida_texto)
        incluir_subpastas = self.incluir_subpastas_var.get()

        qtd = len(listar_xmls(pasta_xml, incluir_subpastas)) if pasta_xml.exists() else 0

        if qtd == 0:
            messagebox.showwarning(
                "Nenhum XML encontrado",
                "Não encontrei arquivos .xml na pasta selecionada.",
            )
            return

        self._bloquear_interface()
        self.progress.stop()
        self.progress["mode"] = "determinate"
        self.progress["maximum"] = qtd
        self.progress["value"] = 0
        self.status_var.set(f"Iniciando geração em lote. Total de XMLs: {qtd}.")

        thread = threading.Thread(
            target=self._gerar_pasta_thread,
            args=(
                pasta_xml,
                pasta_saida,
                logo_path,
                incluir_subpastas,
                self.sobrescrever_var.get(),
            ),
            daemon=True,
        )
        thread.start()

    def _gerar_arquivo_thread(
        self,
        xml_path: Path,
        pdf_path: Path,
        logo_path: Path | None,
        sobrescrever: bool,
    ):
        try:
            pdf_final, avisos = gerar_danfe_pdf(
                xml_path,
                pdf_path,
                logo_path,
                sobrescrever,
            )
            self.after(0, self._geracao_arquivo_sucesso, pdf_final, avisos)

        except ET.ParseError as e:
            self.after(
                0,
                self._geracao_erro,
                f"XML inválido ou malformado.\n\nDetalhe:\n{e}",
            )

        except Exception as e:
            self.after(0, self._geracao_erro, str(e))

    def _gerar_pasta_thread(
        self,
        pasta_xml: Path,
        pasta_saida: Path,
        logo_path: Path | None,
        incluir_subpastas: bool,
        sobrescrever: bool,
    ):
        def progresso(atual: int, total: int, nome_arquivo: str):
            self.after(0, self._atualizar_progresso_lote, atual, total, nome_arquivo)

        try:
            resultado = gerar_lote_pasta(
                pasta_xml=pasta_xml,
                pasta_saida=pasta_saida,
                logo=logo_path,
                incluir_subpastas=incluir_subpastas,
                sobrescrever=sobrescrever,
                callback_progresso=progresso,
            )

            self.after(0, self._geracao_pasta_sucesso, pasta_saida, resultado)

        except Exception as e:
            self.after(0, self._geracao_erro, str(e))

    def _atualizar_progresso_lote(self, atual: int, total: int, nome_arquivo: str):
        self.progress["value"] = atual
        self.status_var.set(f"Processando {atual}/{total}: {nome_arquivo}")

    def _geracao_arquivo_sucesso(self, pdf_path: Path, avisos: list[str]):
        self.progress.stop()
        self.progress["mode"] = "determinate"
        self.progress["value"] = 100
        self._liberar_interface()

        mensagem = f"DANFE gerado com sucesso:\n{pdf_path}"

        if avisos:
            mensagem += "\n\nAvisos:\n- " + "\n- ".join(avisos)

        self.status_var.set(mensagem)
        messagebox.showinfo("DANFE gerado", mensagem)

        if self.abrir_resultado_var.get():
            abrir_arquivo(pdf_path)

    def _geracao_pasta_sucesso(self, pasta_saida: Path, resultado: dict):
        self._liberar_interface()

        total = resultado["total"]
        sucesso = len(resultado["sucesso"])
        falha = len(resultado["falha"])

        resumo = (
            f"Geração em lote concluída.\n\n"
            f"XMLs encontrados: {total}\n"
            f"PDFs gerados: {sucesso}\n"
            f"Falhas: {falha}\n"
            f"Pasta de saída:\n{pasta_saida}"
        )

        if falha:
            resumo += "\n\nArquivos com falha:"

            for xml_path, erro in resultado["falha"][:10]:
                resumo += f"\n- {xml_path.name}: {erro}"

            if falha > 10:
                resumo += f"\n- ... e mais {falha - 10} arquivo(s)."

        self.status_var.set(resumo)
        messagebox.showinfo("Geração em lote concluída", resumo)

        if self.abrir_resultado_var.get():
            abrir_pasta(pasta_saida)

    def _geracao_erro(self, erro: str):
        self.progress.stop()
        self.progress["mode"] = "determinate"
        self.progress["value"] = 0
        self._liberar_interface()

        mensagem = f"Não foi possível gerar o DANFE.\n\n{erro}"
        self.status_var.set(mensagem)
        messagebox.showerror("Erro ao gerar DANFE", mensagem)


def main():
    app = DanfeApp()
    app.mainloop()


if __name__ == "__main__":
    main()
