from copy import copy
from curses import window
from datetime import datetime
from hashlib import new
import numbers
from os import pread
from unicodedata import name
from xmlrpc.client import DateTime
import random
from click import style
from flask import Flask, redirect, render_template, json, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from utils.db import db
from models.user import User
from models.game import Game
from models.plays import Play_number

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ideaas@localhost/gamedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLAlchemy(app)

with app.app_context():
    db.create_all()

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# si la palabra es una cadena vacia, retorna false
def isValid(word):
    return word.strip() != ""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form["name"]
        password = request.form["password"]
        email = request.form["email"]
        isValidName = isValid(name)
        isValidPassword = isValid(password)
        isValidEmail = isValid(email)
        # if user is not valid, redirect to index with error message
        if isValidName and isValidPassword and isValidEmail:
            user = User.query.filter_by(name=name).first()
        else:
            return render_template('index.html', error="enter a valid name, password and email")

        # if user don't exist, create a new user
        if user is None:
            user = User(name, email, password)
            db.session.add(user)
            session["name"] = name
            db.session.commit()
            return redirect(url_for('options'))
        # if user already exists return error
        else:
            return render_template('index.html', error="El usuario ya existe")
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form["nameOrmail"]
        password = request.form["password"]
        user = User.query.filter_by(name=name).first()
        if user:
            if user.password == password:
                session["name"] = user.name
                session["id"] = user.id
                session["idGame"] = 0
                session["logged_in"] = True
                return redirect(url_for('options'))
            else:
                print("Password incorrecto")
                return render_template('login.html', error="Password incorrecto")
        else:
            print("Usuario no encontrado")
            return render_template('login.html', error="Usuario no encontrado")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))


def ramdomGame():
    randoms = []
    for i in range(5):
        randoms.append(random.randint(0, 50))
    return randoms


@app.route('/options')
def options():
    randoms = ramdomGame()
    print(randoms)
    session['numbers'] = randoms
    return render_template('options.html')


@app.route('/game', methods=['GET', 'POST'])
def game():
    clase = ["", "", "", "", ""]
    userNumbers = request.form
    if request.method == 'POST':
        userNumbersSave = []
        corrects = 0
        for positionUserNumber in userNumbers.keys():
            userNumbersSave.append(userNumbers[positionUserNumber])
            for positionRandom in range(len(session['numbers'])):
                if int(userNumbers[positionUserNumber]) == int(session['numbers'][positionRandom]):
                    if int(positionRandom) == int(positionUserNumber):
                        clase[int(positionUserNumber)] = "green"
                        corrects = corrects + 1
                        break
                    else:
                        clase[int(positionUserNumber)] = "yellow"
                elif(clase[int(positionUserNumber)] != "yellow" and clase[int(positionUserNumber)] != "green"):
                    clase[int(positionUserNumber)] = "red"
        session["userNumbers"] = userNumbersSave
        if(corrects == 5):
            session["isWinner"] = "true"
            randoms = ramdomGame()
            session['numbers'] = randoms
            session["endGame"] = datetime.now()
            print("ganoo")
        else:
            session["isWinner"] = "false"
            session["attempts"] = session["attempts"] + 1

        game = Game.query.filter_by(id=session['idGame']).first()
        if game is None:
            game = Game(session["id"], 0, False, datetime.now(),
                        datetime.now(), 0, session["attempts"])
            db.session.add(game)
            db.session.commit()
            session['idGame'] = game.id
        else:
            game.end = datetime.now()
            duration = (datetime.now() - game.start).total_seconds()
            durationsMinutes = duration / 60
            game.duration = durationsMinutes
            game.attemps = session['attempts']
            game.is_winner = session['isWinner'] == "true"
            db.session.commit()
        # game_id, attemp, is_winner, numbers , date
        playNumber = Play_number(session["idGame"], session["attempts"], session["isWinner"] == 'true', str(
            session["userNumbers"]), datetime.now())
        db.session.add(playNumber)
        db.session.commit()
        return render_template('game.html', clase=clase)
    else:
        session["attempts"] = 0
        session["isWinner"] = "false"
        session["startGame"] = datetime.now()
        session["idGame"] = 0
        randoms = ramdomGame()
        print(randoms)
        session['numbers'] = randoms
        return render_template('game.html', clase=clase)


def getAllGamesByUser(id):
    games = Game.query.filter_by(user_id=id).all()
    return games


def getAllPlaysByUser(id):
    plays = Play_number.query.filter_by(user_id=id).all()
    return plays


def getAllPlaysByGame(id):
    plays = Play_number.query.filter_by(game_id=id).all()
    return plays


def getStatistics(id):
    games = getAllGamesByUser(id)
    gamesWon = 0
    gamesLost = 0
    gamesDuration = 0
    gamesAttempts = 0
    for game in games:
        if game.is_winner:
            gamesWon = gamesWon + 1
        else:
            gamesLost = gamesLost + 1
        gamesDuration = gamesDuration + game.duration
        gamesAttempts = gamesAttempts + game.attemps
    return gamesWon, gamesLost, gamesDuration, gamesAttempts


def getAllUsers():
    users = User.query.all()
    return users


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
    gamesByUser = []
    print(request.method)
    if request.method == 'POST':
        userIdForData = request.form["user"]
        # if filter by user
        # filter by period and user_id
        fromDate = request.form["from"]
        toDate = request.form["to"]
        if fromDate != "" and toDate != "":
            if userIdForData != "all":
                gamesByUser = Game.query.filter(
                    Game.user_id == userIdForData, 
                    Game.start >= fromDate, 
                    Game.start <= toDate
                    ).all()
            else:
                gamesByUser = Game.query.filter(
                    Game.start >= fromDate, 
                    Game.start <= toDate
                    ).all()
        else:
            if userIdForData != "all":
                gamesByUser = Game.query.filter(
                    Game.user_id == userIdForData
                    ).all()
            else:
                gamesByUser = Game.query.all()
    else:
        gamesByUser = Game.query.all()

    statistics = {}
    resume = {}
    wins = 0
    losses = 0
    played = 0
    for game in gamesByUser:
        played = played + 1
        if game.is_winner:
            wins = wins + 1
        else:
            losses = losses + 1
        statistics[game.id] = {}
        statistics[game.id]["attempts"] = game.attemps
        statistics[game.id]["duration"] = game.duration
        statistics[game.id]["is_winner"] = game.is_winner
        statistics[game.id]["date"] = game.start
        statistics[game.id]["user"] = game.user.name
    resume["wins"] = wins
    resume["losses"] = losses
    resume["played"] = played
    users = getAllUsers()

    return render_template('statistics.html', statistics=statistics, resume=resume, users=users)


def queryString():
    print(request)
    print(request.args)
    print(request.args.get('nombre'))
    return "OK"


def pagina_no_encontrada(error):
    return redirect(url_for('index')), 404


if __name__ == "app":
    app.add_url_rule('/queryString', 'queryString', view_func=queryString)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
