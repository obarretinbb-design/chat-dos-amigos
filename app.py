from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "chave_secreta_aqui" # Pode ser qualquer texto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)

# Modelo do Banco de Dados para salvar mensagens
class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    texto = db.Column(db.String(500))
    data = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        nome = request.form.get('nome')
        if senha == "SALVEM US": # <--- COLOQUE SUA SENHA AQUI
            session['usuario'] = nome
            return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        novo_texto = request.form.get('mensagem')
        if novo_texto:
            nova_msg = Mensagem(usuario=session['usuario'], texto=novo_texto)
            db.session.add(nova_msg)
            db.session.commit()
            
    mensagens = Mensagem.query.order_by(Mensagem.data.asc()).all()
    return render_template('chat.html', mensagens=mensagens, nome_usuario=session['usuario'])

if __name__ == "__main__":
    app.run(debug=True)