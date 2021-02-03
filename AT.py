# Player Abdelrahman Obyat
#Please note this implements iterative deepneing and minimax correctly, with individually correct GetScoreMix(), getScoreMax()
#Meaning both functions accurately return the number of moves left to make while accounting for jumps.

#however, I am stuck on the issue where Player1 significantly improves using iterative deepening minimax, while player2 does not benifit. It was suggested on piazza 
#that getScore could bet the reason, but it deosn't seem to be through tests. Just uncomment print() statements to see control flow, both getScore() functions and getMove() behave as expected, just not for player 2
import random as rnd
import numpy as np
from datetime import datetime
import time

class GameState(object):
    __slots__ = ['board', 'playerToMove', 'winner']

# Global variables
boardWidth = 0
boardHeight = 0
homeWidth = 0
homeHeight = 0
timeLimit = 0



# For a given GameState and move to be executed, return the GameState that results from the move
def makeMove(state, move):
    (xStart, yStart, xEnd, yEnd) = move
    newState = GameState()

    newState.playerToMove = 1 - state.playerToMove          # After the move, it's the other player's turn
    newState.board = np.copy(state.board)
    newState.board[xStart, yStart] = -1                     # Remove the piece at the start position
    if (state.playerToMove == 0 and (xEnd < boardWidth - homeWidth or yEnd < boardHeight - homeHeight)) or \
       (state.playerToMove == 1 and (xEnd >= homeWidth or yEnd >= homeHeight)):
        newState.board[xEnd, yEnd] = state.playerToMove     # Unless the move ends in the opponent's home, place piece at end position
    
    for xStart in range(boardWidth):
        for yStart in range(boardHeight):
            if newState.board[xStart, yStart] == state.playerToMove:
                newState.winner = -1                        # If the player still has pieces on the board, then there is no winner yet...
                return newState
    
    newState.winner = state.playerToMove                    # Otherwise, the current player has won!
    return newState

# Compute list of legal moves for a given GameState for the player moving next 
def getMoveOptions(state):
    direction = [[(1, 0), (0, 1)], [(-1, 0), (0, -1)]]              # Possible (dx, dy) moving directions for each player
    moves = []
    for xStart in range(boardWidth):                                # Search board for player's pieces
        for yStart in range(boardHeight):
            if state.board[xStart, yStart] == state.playerToMove:   # Found a piece!
                for (dx, dy) in direction[state.playerToMove]:      # Check horizontal and vertical moving directions
                    (xEnd, yEnd) = (xStart + dx, yStart + dy)
                    while xEnd >= 0 and xEnd < boardWidth and yEnd >= 0 and yEnd < boardHeight:
                        if state.board[xEnd, yEnd] == -1:
                            moves.append((xStart, yStart, xEnd, yEnd))      # If square is free, we have a legal move...
                            break
                        xEnd += dx                                          # Otherwise, check for larger step
                        yEnd += dy
    return moves



def getScoreMin(state):
    score = 0
    hypMaxScoreTotal = 0
    hypMinScoreTotal = 0
    direction = [[(1, 0), (0, 1)], [(-1, 0), (0, -1)]] 
    moves = []
    for x in range(boardWidth):                            
        for y in range(boardHeight):
            if state.board[x, y] == 1:  
                for (dx, dy) in direction[state.board[x, y]]:
                    (xEnd, yEnd) = (x + dx, y + dy)
                    while xEnd >= 0 and xEnd < boardWidth and yEnd >= 0 and yEnd < boardHeight:
                        if state.board[xEnd, yEnd] == -1:
                            moves.append((x, y, xEnd, yEnd))      
                            break
                        xEnd += dx                                          
                        yEnd += dy
                maxix = 0
                maxiy = 0
                for i in range(0, len(moves)):
                    (xStar, yStar, xEn, yEn) =  moves[i]
                    if ((xStar == x and yStar == y) and [((xEn - x) < maxix) or ((yEn - y) < maxiy)]):   
                        maxix = xEn - x
                        maxix = -maxix
                        maxiy = yEn - y
                        maxiy = -maxiy
                        ax = max(0, ((x + 1) - maxix))
                        by = max(0, ((y + 1) - maxiy))
                        if boardWidth - homeWidth == 0:
                            ax = 0
                        else:
                            ax = ax
                        if boardHeight - homeHeight == 0 :
                            by = 0
                        else:
                            by = by
                        hypMinScoreTotal -= (ax - homeWidth + 1 ) + (by - homeHeight + 1)
                        #hypMaxScoreTotal = -hypMaxScoreTotal
                        #print("\n\hypMinScoreTotal: "+ str(hypMinScoreTotal))
                        moves = []
                        break

    return hypMinScoreTotal

def getScoreMax(state):
    score = 0
    hypMaxScoreTotal = 0
    hypMinScoreTotal = 0
    direction = [[(1, 0), (0, 1)], [(-1, 0), (0, -1)]] 
    moves = []
    for x in range(boardWidth):                            
        for y in range(boardHeight):
            if state.board[x, y] == 0:  
                for (dx, dy) in direction[state.board[x, y]]:
                    (xEnd, yEnd) = (x + dx, y + dy)
                    while xEnd >= 0 and xEnd < boardWidth and yEnd >= 0 and yEnd < boardHeight:
                        if state.board[xEnd, yEnd] == -1:
                            moves.append((x, y, xEnd, yEnd))      
                            break
                        xEnd += dx                                          
                        yEnd += dy

                maxix = 0
                maxiy = 0
                for i in range(0, len(moves)):
                    (xStar, yStar, xEn, yEn) =  moves[i]
                    if ((xStar == x and yStar == y) and [((xEn - x) > maxix) or ((yEn - y) > maxiy)]): 
                        maxix = xEn - x
                        maxiy = yEn - y
                        ax = max(0, ((x-1) + maxix))
                        by = max(0, ((y-1) + maxiy))

                        if maxix == 0:
                            ax = x
                        else:
                            ax = ax
                        if maxiy == 0:
                            by = y
                        else:
                            by = by
                        hypMaxScoreTotal -= max([0, (boardWidth - homeWidth - ax)]) + max([0, (boardHeight - homeHeight - by)])
                        hypMaxScoreTotal = -hypMaxScoreTotal
                        break

    #print("\n\Max Score: "+ str(hypMaxScoreTotal))
    return hypMaxScoreTotal



# Check whether time limit has been reached
def timeOut(startTime, timeLimit):
    duration = datetime.now() - startTime
    return duration.seconds + duration.microseconds * 1e-6 >= timeLimit


def getMove(state, hWidth, hHeight, timeLimit):
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight
    keepgoing = True
    startTime = datetime.now()                                    
    moveList = getMoveOptions(state)                                 
    depthlimit = 1
    scoreList = []
    scoreAtDepth = 0
    bestMoveList = []
    iteratedToGoal = False

    for move in moveList:
        if len(moveList) > 0:                                                                    
            if state.playerToMove == 0:                                     
                bestMoveSoFar = moveList[0]
            else:
                bestMoveSoFar = moveList[0]

        projectedState = makeMove(state, move)    

        while not timeOut(startTime, timeLimit) and keepgoing:
            depthlimit += 1

            bestMoveSoFar, iteratedToGoal, scoreAtDepth = iterateMove(projectedState, hWidth, hHeight, timeLimit, move, 0,  depthlimit)
            scoreList.append(scoreAtDepth)
            bestMoveList.append(bestMoveSoFar)
            if iteratedToGoal == True or projectedState.winner == 0:
                keepgoing = False
                break             

    if state.playerToMove == 0:                                      
        bestMoveSoFar = bestMoveList[scoreList.index(max(scoreList))]
        #returnedScore = scoreList[scoreList.index(max(scoreList))]
        #print("The max score if we are blue: "+str(returnedScore))
        #print("The bestMoveList so far"+str(bestMoveList))

    else:
        bestMoveSoFar = bestMoveList[scoreList.index(min(scoreList))]  
        # returnedScore = scoreList[scoreList.index(min(scoreList))]
        # print("The min score if we are red: "+str(returnedScore))
    return bestMoveSoFar



def iterateMove(state, hWidth, hHeight, timeLimit, currentbestMove, startdepth, depthlimit):
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight
    bestMoveSoFar = currentbestMove
    GivenMoveList = getMoveOptions(state) 
    winningState = -1
    iteratedToGoal = False
    scoreAtDepth = 0
    minWins = -99999999999999999999999999999999999999999999999999999999999
    maxWins = 9999999999999999999999999999999999999999999999999999999999
    for givenMove in GivenMoveList:
        if ((state.winner == -1) and (startdepth < depthlimit)):
            startdepth += 1
            if state.playerToMove == 0:  
                # print("\n\nI can only look ahead to depth: "+str(depthlimit) +"!")
                # print("I am now looking ahead to depth: "+str(startdepth))  
                if (startdepth == depthlimit):
                    scoreAtDepth = getScoreMax(state)
                    return bestMoveSoFar, iteratedToGoal, scoreAtDepth
            state = makeMove(state, givenMove)
            if  state.winner == 1:
                scoreAtDepth = minWins
                return bestMoveSoFar, iteratedToGoal, scoreAtDepth
                break
            elif state.playerToMove == 1:  
                  # print("\n\nI can only look ahead to depth: "+str(depthlimit) +"!")
                  # print("I am now looking ahead to depth: "+str(startdepth))  
                 if state.winner == 0:
                    scoreAtDepth = maxWins
                    return bestMoveSoFar, iteratedToGoal, scoreAtDepth
            if (state.winner != -1):
                if state.playerToMove == 0:  
                    scoreAtDepth = maxWins
                elif state.playerToMove == 1:
                    scoreAtDepth = minWins
                iteratedToGoal = True
                return bestMoveSoFar, iteratedToGoal, scoreAtDepth
                break
            else:    
                bestMoveSoFar, iteratedToGoal, scoreAtDepth = iterateMove(state, hWidth, hHeight, timeLimit, bestMoveSoFar, startdepth, depthlimit)  
            break
        break
    return bestMoveSoFar, iteratedToGoal, scoreAtDepth
