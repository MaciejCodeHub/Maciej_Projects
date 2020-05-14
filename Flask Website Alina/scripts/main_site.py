# http://127.0.0.1:5000/

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home_page():
    return render_template("home.html", title=' EL Sklep Zielarski')

@app.route('/produkty')
def products_page():
    return render_template("products.html", title=' EL Produkty')

@app.route('/uzdrawianie')
def healing_page():
    return render_template("uzdrawianie.html", title=' EL Uzdrawianie')

@app.route('/theta_healing')
def theta_page():
    return render_template("theta.html", title=' EL Theta Healing')

@app.route('/konchowanie')
def candle_page():
    return render_template("konchowanie.html", title=' EL Konchowanie')

@app.route('/kontakt')
def contact_page():
    return render_template("kontakt.html", title=' EL Kontakt')


if __name__ == '__main__':
    app.run(debug=True)


