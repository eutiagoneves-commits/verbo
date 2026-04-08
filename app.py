from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "segredo"

palavras = ["canto", "vento", "livro", "pedra", "nuvem", "carta"]

def verificar(chute, palavra):
    resultado = []
    for i in range(5):
        if chute[i] == palavra[i]:
            resultado.append((chute[i], "green"))
        elif chute[i] in palavra:
            resultado.append((chute[i], "gold"))
        else:
            resultado.append((chute[i], "gray"))
    return resultado

@app.route("/", methods=["GET", "POST"])
def index():
    if "palavra" not in session:
        session["palavra"] = random.choice(palavras)
        session["tentativas"] = []
        session["fim"] = False
        session["mensagem"] = ""

    if request.method == "POST" and not session["fim"]:
        chute = request.form.get("chute", "").lower()

        if len(chute) == 5:
            resultado = verificar(chute, session["palavra"])

            tentativas = session.get("tentativas", [])
            tentativas.append(resultado)
            session["tentativas"] = tentativas

            if chute == session["palavra"]:
                session["fim"] = True
                session["mensagem"] = "🎉 Você venceu!"

            elif len(tentativas) >= 6:
                session["fim"] = True
                session["mensagem"] = f"😢 Você perdeu! Palavra: {session['palavra']}"

    return render_template(
        "index.html",
        tentativas=session.get("tentativas", []),
        mensagem=session.get("mensagem", ""),
        fim=session.get("fim", False)
    )

@app.route("/reset")
def reset():
    session.clear()
    return "<h2>Jogo reiniciado!</h2><a href='/'>Voltar</a>"

import os

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))