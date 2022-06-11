from copy import copy
from curses import window
import numbers
from unicodedata import name
from click import style
from flask import Flask, redirect, render_template, json, request, url_for, session
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


# @app.before_request
# def before_request():
#     print("Antes de la peticion")

# @app.after_request
# def after_request(response):
#     name = response
#     print("Despues de la peticion")
#     return response



@app.route('/' , methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form["name"]
        session["name"] = name
        return redirect(url_for('options'))
    return render_template('index.html')




# @app.route('/inicio/<nombre>/<int:edad>')
# def inicio(nombre,edad):
#     data = {
#         'title': 'inicio',
#         'name' : nombre,
#         'edad' : edad,
#     }
#     return render_template('inicio.html', data = data)

@app.route('/options')
def options():
    session['numbers'] = [6, 5, 6, 12, 43 ]
    return render_template('options.html')



@app.route('/game', methods=['GET', 'POST'])
def game():
    # name = request.args.get('name')
    styles  = style('Hello World!', fg='red', bg='blue')
    # print(request.args.get('name'))
    clase = ["" ,"" , "", "", "" ]
    userNumbers = request.form
    if request.method == 'POST':
        userNumbersSave = []
        for positionUserNumber in  userNumbers.keys():
            userNumbersSave.append(userNumbers[positionUserNumber])
            for positionRandom in  range(len(session['numbers'])):
                if int(userNumbers[positionUserNumber]) ==  int(session['numbers'][positionRandom]):
                    if int(positionRandom) == int(positionUserNumber):
                        clase[positionRandom] = "green"
                    elif (clase[positionRandom] != "green"):
                        clase[positionRandom] = "yellow"
                elif(clase[positionRandom] != "yellow" and clase[positionRandom] != "green"):
                    clase[positionRandom] = "red"
        session["userNumbers"] = userNumbersSave
        print(userNumbersSave)
        print(clase)
        return render_template('game.html', style = styles, clase = clase)
    else:
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

