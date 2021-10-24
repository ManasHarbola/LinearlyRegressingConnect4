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
    leaderBoards = db.relationship('LeaderBoards', backref='author', lazy=True)

    def __init__(self, id, coor_x, coor_y):
        self.id = id
        self.coor_x = coor_x
        self.coor_y = coor_y
    
    def __init__(self, coor_x, coor_y):
        self.coor_x = coor_x
        self.coor_y = coor_y

class LeaderBoards(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    users = db.relationship('Users', backref='author', lazy=True)
    arena_id = db.Column(db.Integer, db.ForeignKey('Arenas.id'), nullable=False)

    def __init__(self, arena_id):
        self.arena_id = arena_id


class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    average = db.Column(db.Float())
    standardDev = db.Column(db.Float())
    leaderboards_id = db.Column(db.Integer, db.ForeignKey('LeaderBoards.id'), nullable=False)
    
    def __init__(self, id, username, average, standardDev, leaderboards_id):
        self.username = username
        self.average = average
        self.standardDev = standardDev
        self.leaderboards_id = leaderboards_id
    
    def __init__(self, username, average, standardDev, leaderboards_id):
        self.username = username
        self.average = average
        self.standardDev = standardDev
        self.leaderboards_id = leaderboards_id


    def __repr__(self):
        return f"users('{self.username}') avg({self.average}) std({self.standardDev})"



#app = Flask(__name__)


@app.route("/initialize")
def initializeDatabase():
    
    global_arena = Arenas(0, 0, 0)
    initial_leaderBoard = LeaderBoards(global_arena.id)
    perfect_player = Users(username="perfect_player", average=1, standardDev=0.1, leaderboards_id=initial_leaderBoard.id)
    
    db.session.add(global_arena)
    db.session.add(initial_leaderBoard)
    db.session.add(perfect_player)
    db.session.commit()





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

    #usrID
    @app.route("/createNewUser/<usrID>")
    def createNewUser(usrID):
        try:
            global_leaderBoard = LeaderBoards.query.filter_by(arena_id = 0).first()
            new_user = Users(username=usrID, average=0, standardDev=0, leaderboards_id=global_leaderBoard.id)
            
            db.session.add(new_user)
            db.session.commit()

            found_user = Users.query.filter_by(username = usrID).first()

            return "SUCCESS"
        except:
            return "FAILURE"

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
      
    #send move made by AI based on player simulation
    #def postNextMove(move):
        #blah

"""
print("hello")
api = Connect_4_API()

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
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0"
}
r = requests.get("https://connect4.gamesolver.org/solve?pos=1", headers=GET_HEADER)
print(r.text)
api.testGetReq("444447123311")

"""

'''
for i in range(100):
    r = requests.get("https://connect4.gamesolver.org/solve?pos=1", headers=headers)
    print(r.text)
'''
#data = r.json()
#jsonStr = json.dumps(data)
#print(jsonStr)
#print(Connect_4_API.rateOppMoves("44444723333213216275"))

db.create_all()

if __name__ == '__main__':
    obj = {"board": "1121", "player": "id"}
    jsonStr = json.dumps(obj)
    print(jsonStr)
    app.run()