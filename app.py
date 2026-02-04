from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import base64
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "chave_mestra_snoop"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    texto = db.Column(db.String(500))
    imagem = db.Column(db.Text) 
    data = db.Column(db.DateTime, default=datetime.now)
    
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        senha = request.form.get('senha')
        nome = request.form.get('nome')
        if senha == "SALVEM US": # Sua senha
            session['usuario'] = nome
            return redirect(url_for('chat'))
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        texto = request.form.get('mensagem')
        arquivo = request.files.get('foto')
        img_base64 = None
        
        if arquivo and arquivo.filename != '':
            img_base64 = base64.b64encode(arquivo.read()).decode('utf-8')
        
        if texto or img_base64:
            nova_msg = Mensagem(usuario=session['usuario'], texto=texto, imagem=img_base64)
            db.session.add(nova_msg)
            db.session.commit()
            
    mensagens = Mensagem.query.order_by(Mensagem.data.asc()).all()
    return render_template('chat.html', mensagens=mensagens, nome_usuario=session['usuario'])

if __name__ == "__main__":
    app.run(debug=True)
