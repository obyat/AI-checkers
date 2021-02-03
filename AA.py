# Player Alan_Turing

import random as rnd
import numpy as np
from datetime import datetime

class GameState(object):
    __slots__ = ['board', 'playerToMove', 'winner']

# Global variables
boardWidth = 0
boardHeight = 0
homeWidth = 0
homeHeight = 0
timeLimit = 0

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

# Return the evaluation score for a given GameState; higher score indicates a better situation for Player 1
# Alan_Turing's evaluation function is based on the (non-jump) moves each player would need to win the game. 
def getScore_old(state):
   # print("\n\n_________________________________DURING ______THIS____ EXECUTION__________________________________________________")
    minscore = 0
    score = 0
    for x in range(boardWidth):                             # Search board for any pieces
        for y in range(boardHeight):
            if state.board[x, y] == 0:   
                # print("\n\n======================MIN BLue==========================")
                # print("\nx is: " + str(x) + "             y is: "+ str(y))
                # print("\n\nboardWidth is: "+str(boardWidth) + ",   homewidth is: "+str(homeWidth)+ ",   x is: " + str(x))
                # print("boardWidth - homeWidth - x =>   ("  +str(boardWidth)+ " - " +str(homeWidth)+ " - " + str(x)+ ") = " +str(boardWidth - homeWidth - x) +" <--this is the score for x") 
                # print("boardHeight - homeHeight - y =>   ("  +str(boardHeight)+ " - " +str(homeHeight)+ " - " + str(y)+ ") = " +str(boardHeight - homeHeight - y) +" <--this is the score for y")              
                # print("\nx-dir is:  " + str(boardWidth - homeWidth - x) +"   +  y-direc is: "+ str(boardHeight - homeHeight - y)+ "   =" + str(max([0, boardWidth - homeWidth - x]) + max([0, boardHeight - homeHeight - y])), end=" ")
                
                
                # print("\nscore before: " + str(score))
                score -= max([0, boardWidth - homeWidth - x]) + max([0, boardHeight - homeHeight - y])
                # print("\nscore after: " + str(score), end=" ")
            else:
                if state.board[x, y] == 1:                  # Add the number of moves (non-jumps) for Player 2's piece to reach Player 1's home area
                    print("\n\n\n<<<<<<<<<<<<<<<<<<<<<FOR MAX>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    print("\nx is: " + str(x) + "             y is: "+ str(y))
                    print("\nhomeWidth is: "+str(homeWidth) + ",   homeHeight is: "+str(homeHeight)+ ",   y is: " + str(y))

                    print("\nx - homeWidth + 1 is:  " + str( x - homeWidth + 1) +"   +  y - homeHeight + 1. From the current board, # of moves min needs: "+ str( y - homeHeight + 1)+ "   =" + str(max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])), end=" ")

#                    because this starts at five five
                    print("\n\nscore before: " + str(minscore))
                    minscore += max([0, x - homeWidth + 1]) #+ max([0, y - homeHeight + 1])
                    print("\nsminscore after: " + str(minscore), end=" ")
    #print("\nreturned Score: " + str(score), end=" ")
    #print("\n")
    return score





def getScore(state):
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
                    if ((xStar == x and yStar == y) and [((xEn - x) > maxix) or ((yEn - y) > maxiy)]):                     # ((yEn - y) > maxiy)):
                        print("\n\n=TTTTTTTTTTTTTTTTTTTTTTTTTT==MIN BLue==TTTTTTTTTTTTTTTTTTTTTTTT==")
                        print("\nBlue piece at: (" + str(x) + ", "+ str(y)+")    x: " + str(x) + "   y: "+ str(y)+"")

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
                        # print("the max y-jump for this piece is: "+ str(maxiy))
                        #print("\n___________________________________________________________________________________________________________________________")
                        # print("the max x-jump for this piece is: "+ str(maxix))
                        hypMaxScoreTotal -= max([0, (boardWidth - homeWidth - ax)]) + max([0, (boardHeight - homeHeight - by)])
                        #print("\n\nTotal Score: "+ str(hypScoreTotal))

                        break
                        #hypMinScoreTotal -= max([0, boardWidth - homeWidth - (x - maxix)]) + max([0, boardHeight - homeHeight - y])
                        # print("\n\nTotal min Score: "+ str(hypMinScoreTotal))              
            moves = []  
            if state.board[x, y] == 1:  
                #print("\nBlue piece at: (" + str(x) + ", "+ str(y)+")    x: " + str(x) + "   y: "+ str(y)+"")

                for (dx, dy) in direction[state.board[x, y]]:
                    (xEnd, yEnd) = (x + dx, y + dy)
                    while xEnd >= 0 and xEnd < boardWidth and yEnd >= 0 and yEnd < boardHeight:
                        if state.board[xEnd, yEnd] == -1:
                            moves.append((x, y, xEnd, yEnd))      
                            break
                        xEnd += dx                                          
                        yEnd += dy
                print("moves"+str(moves))

                maxix = 0
                maxiy = 0

                for i in range(0, len(moves)):
                    (xStar, yStar, xEn, yEn) =  moves[i]
                    if ((xStar == x and yStar == y) and [((xEn - x) < maxix) or ((yEn - y) < maxiy)]):                     # ((yEn - y) > maxiy)):
                        # print("\n\n=TTTTTTTTTTTTTTTTTTTTTTTTTT==MIN BLue==TTTTTTTTTTTTTTTTTTTTTTTT==")
                        # print("\nBlue piece at: (" + str(x) + ", "+ str(y)+")    x: " + str(x) + "   y: "+ str(y)+"")

                        maxix = xEn - x
                        maxix = -maxix
                        maxiy = yEn - y
                        maxiy = -maxiy
                        print(" actual max jump maxix" +str(maxix))
                        print("maxiy"+str(maxiy))
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
                        print("by"+str(by))
                        print("ax" +str(ax))
                        # ax - homeWidth + 1 
                        score = (ax - homeWidth + 1 ) + (by - homeHeight + 1)
                        print("\n\hypMinScoreTotal: "+ str(hypMinScoreTotal))
                        moves = []
                        break
                        #hypMinScoreTotal -= max([0, boardWidth - homeWidth - (x - maxix)]) + max([0, boardHeight - homeHeight - y])
                        # print("\n\nTotal min Score: "+ str(hypMinScoreTotal))             


   
                  #  score += max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])
    print("-----------------------------------------------")
    #print("minscore" + str(hypMinScoreTotal))
    print("THE Hyp max"+str(hypMaxScoreTotal))
    # print("THE hyp min"+str(hypMinScoreTotal))
    # score = hypMaxScoreTotal + hypMinScoreTotal
    # print("THE Total SCORE"+str(score))1
    return score
# Check whether time limit has been reached
def timeOut(startTime, timeLimit):
    duration = datetime.now() - startTime
    return duration.seconds + duration.microseconds * 1e-6 >= timeLimit

# Compute the next move to be played; keep updating <bestMoveSoFar> until computation finished or time limit reached
def getMove(state, hWidth, hHeight, timeLimit):
    # Set global variables
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight
    
    startTime = datetime.now()                                       # Remember computation start time

    moveList = getMoveOptions(state)                                 # Get the list of possible moves
    bestMoveSoFar = moveList[0]                                      # Just choose first move from the list for now, in case we run out of time 
    scoreList = []
    for move in moveList:
        projectedState = makeMove(state, move)                       # For each move, play it on a separate board...
        scoreList.append(getScore(projectedState))                   # ... and call the evaluation function on the resulting GameState
    
        if timeOut(startTime, timeLimit):                            # Check for timeout and return current best move if time limit is reached
            return bestMoveSoFar                                     # It is not necessary for Alan_Turing, but you need to include this check in
    if state.winner == 0:
        print("\n\n\n\n\nplayer " + str(state.playerToMove) +" has won\n\n\n\n\n")
                                                                     # all time-consuming loops in your code so that you will not exceed the time limit
    if state.playerToMove == 0:                                      # Finally, pick the move with the best score
        bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
    else:
        bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score
    
    return bestMoveSoFar



                    #        # ax = max(0, ((x-1) + maxix))
                    # #        # by = max(0, ((y-1) + maxiy))
                    #     print("\n\n=TTTTTTTTTTTTTTTTTTTTTTTTTT==Min Red==TTTTTTTTTTTTTTTTTTTTTTTT==")
                    #     print("\nRed piece at: (" + str(x) + ", "+ str(y)+")    x: " + str(x) + "   y: "+ str(y)+"")
                    #     print("the max y-jump for this piece is: "+ str(maxiy))


                    # print("\n               hw: "+str(homeWidth) + ",   hh: "+str(homeHeight)+ ",   y: " + str(y))

                # print("\n(x - hw + 1) =  " + str( x - homeWidth + 1) +"     +      (y - hh + 1) =  "+ str( y - homeHeight + 1)+ "    ===> " + str(max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])))

                # #because this starts at five five
                # print("\nscore before: " + str(hypMinScoreTotal), end=" ")
                      
                        #print("\n ax" + str(ax))
                        #print("\n by" + str(by))
