from flask import Flask
import json
import random
import requests
import numpy as np

app = Flask(__name__)


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
                
                return random.choice(move_and_vals[scores[i]])
        return str(random.choice(move_and_vals[scores[-1]]))

    
    #method to grab best possible moves
    #used for building the model of the user
    def getBestMoves():
        pass

    
    @app.route("/<state>")
    #returns tuple of normalized average optimality score and the std dev of optimal moves made by opponent
    def rateOppMoves(state):
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


if __name__ == '__main__':
    obj = {"board": "1121", "player": "id"}
    jsonStr = json.dumps(obj)
    print(jsonStr)
    app.run()