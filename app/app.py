from copy import copy
from curses import window
from datetime import datetime
from hashlib import new
import numbers
from unicodedata import name
from xmlrpc.client import DateTime
from click import style
from flask import Flask, redirect, render_template, json, request, url_for, session
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/' , methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form["name"]
        session["name"] = name
        return redirect(url_for('options'))
    return render_template('index.html')


@app.route('/options')
def options():
    session['numbers'] = [6, 5, 6, 12, 43 ]
    return render_template('options.html')



@app.route('/game', methods=['GET', 'POST'])
def game():
    styles  = style('Hello World!', fg='red', bg='blue')
    clase = ["" ,"" , "", "", "" ]
    userNumbers = request.form
    if request.method == 'POST':
        session["attempts"] = session["attempts"] + 1 
        userNumbersSave = []
        for positionUserNumber in  userNumbers.keys():
            userNumbersSave.append(userNumbers[positionUserNumber])
            for positionRandom in  range(len(session['numbers'])):
                if int(userNumbers[positionUserNumber]) ==  int(session['numbers'][positionRandom]):
                    if int(positionRandom) == int(positionUserNumber):
                        clase[int(positionUserNumber)] = "green"
                        break
                    else:
                        clase[int(positionUserNumber)] = "yellow"
                elif(clase[int(positionUserNumber)] != "yellow" and clase[int(positionUserNumber)] != "green"):
                    clase[int(positionUserNumber)] = "red"
        session["userNumbers"] = userNumbersSave
        return render_template('game.html', style = styles, clase = clase)
    else:
        session["attempts"] = 0
        session["startGame"] = datetime.now()
        return render_template('game.html',style = styles, clase = clase)   

def check_numbers():
    return "OK"


def queryString():
    print(request)
    print(request.args)
    print(request.args.get('nombre'))
    return "OK"



def pagina_no_encontrada(error):
    return redirect(url_for('index')), 404



if __name__ == "app":
    app.add_url_rule('/queryString', 'queryString', view_func= queryString)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)

