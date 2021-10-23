import requests
import json
import numpy as np

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
    #method to grab best possible moves
    #used for building the model of the user
    def getBestMoves():
        print("hi")
        #blah

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

        return (np.mean(moveScores), np.std(moveScores))

#print(Connect_4_API.rateOppMoves("444447123311215666611673322237657452355775"))