# Player Homer_Simpson

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
# Homer_Simpson's evaluation function is based on the (non-jump) moves each player would need to win the game. 
#def getScore(state):
    print("\n\n_________________________________DURING ______THIS____ EXECUTION__________________________________________________")

    score = 0
    for x in range(boardWidth):                             # Search board for any pieces
        for y in range(boardHeight):
            if state.board[x, y] == 0:   
                print("\n\n======================MIN BLue==========================")
                print("\nx is: " + str(x) + "             y is: "+ str(y))
                print("\n\nboardWidth is: "+str(boardWidth) + ",   homewidth is: "+str(homeWidth)+ ",   x is: " + str(x))
                print("boardWidth - homeWidth - x =>   ("  +str(boardWidth)+ " - " +str(homeWidth)+ " - " + str(x)+ ") = " +str(boardWidth - homeWidth - x) +" <--this is the score for x") 
                print("boardHeight - homeHeight - y =>   ("  +str(boardHeight)+ " - " +str(homeHeight)+ " - " + str(y)+ ") = " +str(boardHeight - homeHeight - y) +" <--this is the score for y")              
                print("\nx-dir is:  " + str(boardWidth - homeWidth - x) +"   +  y-direc is: "+ str(boardHeight - homeHeight - y)+ "   =" + str(max([0, boardWidth - homeWidth - x]) + max([0, boardHeight - homeHeight - y])), end=" ")
                
                
                print("\nscore before: " + str(score))
                score -= max([0, boardWidth - homeWidth - x]) + max([0, boardHeight - homeHeight - y])
                print("\nscore after: " + str(score), end=" ")
            else:
                if state.board[x, y] == 1:                  # Add the number of moves (non-jumps) for Player 2's piece to reach Player 1's home area
                    # print("\n\n\n<<<<<<<<<<<<<<<<<<<<<FOR MAX>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    # print("\nx is: " + str(x) + "             y is: "+ str(y))
                    # print("\nhomeWidth is: "+str(homeWidth) + ",   homeHeight is: "+str(homeHeight)+ ",   y is: " + str(y))

                    # print("\nx - homeWidth + 1 is:  " + str( x - homeWidth + 1) +"   +  y - homeHeight + 1  which is: "+ str( y - homeHeight + 1)+ "   =" + str(max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])), end=" ")

                    #because this starts at five five
                    # print("\n\nscore before: " + str(score))
                    score += max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])
                    # print("\nscore after: " + str(score), end=" ")
    print("\nreturned Score: " + str(score), end=" ")
    print("\n")
    return score



def getScore(state):
    score = 0
    hypScoreTotal = 0
    direction = [[(1, 0), (0, 1)], [(-1, 0), (0, -1)]] 
    moves = []
    #print("\n\n___________________________________________________________DURING ______THIS____ EXECUTION__________________________________________________")

    
    for x in range(boardWidth):                             # Search board for any pieces
        for y in range(boardHeight):
            #DIFFERENT
            if state.board[x, y] == 0:  


                      # Subtract the number of moves (non-jumps) for Player 1's piece to reach Player 2's home area
               
               
               
               
               
                for (dx, dy) in direction[state.board[x, y]]:      # Check horizontal and vertical moving directions
                    (xEnd, yEnd) = (x + dx, y + dy)
                    while xEnd >= 0 and xEnd < boardWidth and yEnd >= 0 and yEnd < boardHeight:
                        if state.board[xEnd, yEnd] == -1:
                            moves.append((x, y, xEnd, yEnd))      # If square is free, we have a legal move...
                            break
                        xEnd += dx                                          # Otherwise, check for larger step
                        yEnd += dy

                maxix = 0
                maxiy = 0

                #CODE CAN BE SIMPLIFIED BUT THIS LOGIC  WORKS. JUST SIMPLIFY IT. TECHNICALLY DONT NEED XSTART WHATEVER
                for i in range(0, len(moves)):
                    (xStar, yStar, xEn, yEn) =  moves[i]
                    if ((xStar == x and yStar == y) and [((xEn - x) > maxiy) or ((yEn - y) > maxiy)]):                     # ((yEn - y) > maxiy)):
                        #print("\n\n=TTTTTTTTTTTTTTTTTTTTTTTTTT==MIN BLue==TTTTTTTTTTTTTTTTTTTTTTTT==")
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
                        hypScoreTotal -= max([0, (boardWidth - homeWidth - ax)]) + max([0, (boardHeight - homeHeight - by)])
                        print("Total Score: "+ str(hypScoreTotal))
                        break

#maxi = (1 - 1) + 2 = 2
#maxiy = (0 -1) + 1 = 0 = 0
#AT X = 1


#ax = (1 -1) + max = 0 + 2 = 2

#AT Y = 0
#by = (Y - 1) + maxy = -1 + 1 = 0

#4 - 2 = (2 - ax) = 2 - 2 = 0 
#+
#4 - 1 = (3 - by) = 3 - 0 = 3
# = 4
                    # else:
                    #     if ((xStar == x and yStar == y) and [((yEn - y) > maxiy) or ((yEn - y) > maxiy)]):
                    #         # ((yEn - y) > maxiy)):
                    #         print("\n\n=TTTTTTTTTTTTTTTTTTTTTTTTTT==MIN BLue==TTTTTTTTTTTTTTTTTTTTTTTT==")
                    #         print("\nBlue piece at: (" + str(x) + ", "+ str(y)+")    x: " + str(x) + "   y: "+ str(y)+"")
                    #         maxix = xEn - x
                    #         maxiy = yEn - y
                    #         ax = max(0, ((x-1) + maxix))
                    #         by = max(0, ((y-1) + maxiy))

                    #         if maxix == 0:
                    #             ax = x
                    #         else:
                    #             ax = ax
                    #         if maxiy == 0:
                    #             by = y
                    #         else:
                    #             by = by
                    #         hypScoreTotal -= max([0, (boardWidth - homeWidth - ax)]) + max([0, (boardHeight - homeHeight - by)])
                    #         print("Total Score: "+ str(hypScoreTotal))


                    score -= max([0, boardWidth - homeWidth - x]) + max([0, boardHeight - homeHeight - y])
                    # print("\n\n[Score is: "+ str(score) +", Hypothetical Score after everything: " + str(hypScoreTotal)+"]")
                    
                    #print("\nscore  after: " + str(score), end=" ")
                    print("\n")

            else:
                if state.board[x, y] == 1:
                    score += max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])


    #print("\nreturned  Score: " + str(score), end=" ")
    print("\n")
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
        print(" = = = = =  = = =  = = =  = = =  = = =  = = =  = = = = = = = = NEXT DIRECTION= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = ")
        scoreList.append(getScore(projectedState))                   # ... and call the evaluation function on the resulting GameState
        
        if timeOut(startTime, timeLimit):                            # Check for timeout and return current best move if time limit is reached
            return bestMoveSoFar                                     # It is not necessary for Homer_Simpson, but you need to include this check in
                                                                     # all time-consuming loops in your code so that you will not exceed the time limit
    if state.playerToMove == 0:                                      # Finally, pick the move with the worst score (Homer_Simpson's strategy)
        bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the minimum score
    else:
        bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the maximum score
    print("#########################################################################################################################################################################################################################")

    return bestMoveSoFar