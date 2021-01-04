from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


def herokudb():
    Host = 'ec2-79-125-64-18.eu-west-1.compute.amazonaws.com'
    Database = 'ddl4kr8rvkoscg'
    User = 'xmvkgmqtcfbplx'
    Password = '80b8fb5bd23fdcf122a4270230b9daa963e6398c70eb13dc4e17d3b31b4b29a4'
    return psycopg2.connect(host=Host, database=Database, user=User, password=Password, sslmode='require')


def gravar(v1, v2, v3):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (nome text,email text, passe text)")
    db.execute("INSERT INTO usr VALUES (%s, %s, %s)", (v1, v2, v3))
    ficheiro.commit()
    ficheiro.close()


def existe(v1):
    try:
        ficheiro = herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE nome = %s", (v1,))
        valor = db.fetchone()
        ficheiro.close()
    except:
        valor = None
    return valor


def log(v1, v2):
    ficheiro = herokudb()
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome = %s and passe = %s", (v1, v2,))
    valor = db.fetchone()
    ficheiro.close()
    return valor


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/piano')
def piano():
    return render_template('piano.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            erro = 'Bem-Vindo.'
    return render_template('login.html', erro=erro)

@app.route('/registo', methods=['GET', 'POST'])
def registo():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['email']
        v3 = request.form['passe']
        v4 = request.form['cpasse']
        if existe(v1):
            erro = 'O Utilizador já existe.'
        elif v3 != v4:
            erro = 'A palavra passe não coincide.'
        else:
            gravar(v1, v2, v3)
    return render_template('registo.html', erro=erro)


@app.route('/guitarraacustica')
def guitarraacustica():
    return render_template('guitarraacustica.html')


@app.route('/bateria')
def bateria():
    return render_template('bateria.html')


@app.route('/canto')
def canto():
    return render_template('canto.html')


@app.route('/guitarra')
def guitarra():
    return render_template('guitarra.html')


@app.route('/guitarraeletrica')
def guitarraeletrica():
    return render_template('guitarraeletrica.html')


@app.route('/cavaquinho')
def cavaquinho():
    return render_template('cavaquinho.html')


@app.route('/saxofone')
def saxofone():
    return render_template('saxofone.html')


@app.route('/violino')
def violino():
    return render_template('violino.html')


if __name__ == '__main__':
    app.run(debug=True)
