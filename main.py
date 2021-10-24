import json
import random
from numpy.lib.function_base import average
import requests
import numpy as np

from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "PLZWORK"

"""
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    username="SpotifyUnlocked",
    password="SacKings2020",
    hostname="SpotifyUnlocked.mysql.pythonanywhere-services.com",
    databasename="SpotifyUnlocked$vibes",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class Arenas(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    coor_x = db.Column(db.Float())
    coor_y = db.Column(db.Float())
    leaderBoards = 


class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    average = db.Column(db.Float())
    standardDev = db.Column(db.Float())
    
    def __init__(self, username):
        self.username = username
        self.average = average
        self.standardDev = standardDev


    def __repr__(self):
        return f"users('{self.username}') avg({self.average}) std({self.standardDev})"



#app = Flask(__name__)


@app.route("/")
def hello_world():
  return "test"


class Connect_4_API:
    GET_URL = "https://connect4.gamesolver.org/solve?pos="
    GET_HEADER = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Host": "connect4.gamesolver.org",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"

    }
    users = {"id": {"std": 0.1, "avg": 1}}

    @app.route("/generateNextMove/<jsonStr>")
    def generateNextMove(jsonStr):
        obj = json.loads(jsonStr)
        board = obj["board"]
        player = obj["player"]
        #generate random num based on players ability
        avg = Connect_4_API.users[player]["avg"]
        std = Connect_4_API.users[player]["std"]
        rand_num = np.random.normal(loc = avg, scale = std, size = 1)

        #get request 
        r = requests.get(url=Connect_4_API.GET_URL + board, headers=Connect_4_API.GET_HEADER)
        data = r.json()
        move_and_vals = {}#{"score": "moves"}
        scores = []

        for i in range(1, len(data["score"]) + 1):
            score = data["score"][i]
            if score == 100:
                continue
            if score not in move_and_vals.keys():
                scores.append(score)
                move_and_vals[score] = []
            move_and_vals[score].append(i)
        scores.sort(reverse=False)
        sum_of_score = 0
        for i in range(len(scores)):
            sum_of_score += (1 / len(scores))
            if sum_of_score > rand_num:
                
                return str(random.choice(move_and_vals[scores[i]]))
        return str(random.choice(move_and_vals[scores[-1]]))

    
    #method to grab best possible moves
    #used for building the model of the user
    def getBestMoves():
        pass

    @app.route("/createNewUser/<usrID>")
    def createNewUser(usrID):
        #try:
        print("1")
        new_user = Users(username=usrID)
        
        db.session.add(new_user)
        print("3")
        db.session.commit()
        print("4")

        found_user = Users.query.filter_by(username = usrID).first()
        print("5")
        print(found_user)
        print("6")

        return "SUCCESS"
        #except:
        #    return "FAILURE"

    @app.route("/<state>")
    #returns tuple of normalized average optimality score and the std dev of optimal moves made by opponent
    def rateOppMoves(state, userID):
        moveScores = []
        for i in range(0, len(state), 2):
            r = requests.get(Connect_4_API.GET_URL + state[:i], headers=Connect_4_API.GET_HEADER)
            data = r.json()
            colScores = data['score']
            scoreFreq = {}
            numChoices = 0
            for score in colScores:
                if score != 100:
                    scoreFreq[score] = scoreFreq.get(score, 0) + 1
                    numChoices += 1

            scores = [(k, scoreFreq[k]) for k in reversed(scoreFreq.keys())]
            moveScore = colScores[int(state[i]) - 1]
            movesBetterThan = numChoices

            for i in range(len(scores)):
                if scores[i][0] > moveScore:
                    movesBetterThan -= scores[i][1]
                else:
                    moveScores.append(movesBetterThan / numChoices)
        
        userUpdate = Users(userID, np.mean(moveScores), np.std(moveScores))
        found_user = Users.query.filter_by(username = userID).first()
        print(found_user)

        return {"mean": str(np.mean(moveScores)), "std": str(np.std(moveScores))}

    def getArenaLeaderboard(arenaID):
        try:
            userList = LeaderBoards.query.filter_by(arena_id = arenaID).first()
            ranked = []
            for user in LeaderBoards.users:
                ranked.append((user.id, user.average, user.standardDev))
            ranked.sort(key=lambda user : (-user[1], user[2]))
            return [user[0] for user in ranked]
        except:
            return "FAILURE"

db.create_all()

if __name__ == '__main__':
    obj = {"board": "1121", "player": "id"}
    jsonStr = json.dumps(obj)
    print(jsonStr)
    app.run()