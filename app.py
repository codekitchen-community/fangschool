from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/construction_site')
def construction_site():
    return render_template('construction_site.html')


@app.route('/playground')
def playground():
    return render_template('playground.html')
