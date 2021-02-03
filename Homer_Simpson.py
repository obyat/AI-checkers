# Player Homer_Simpson

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
depth = 0

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
def getScore(state):
   # print("\n\n_________________________________DURING ______THIS____ EXECUTION__________________________________________________")

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
                    # print("\n\n\n<<<<<<<<<<<<<<<<<<<<<FOR MAX>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    # print("\nx is: " + str(x) + "             y is: "+ str(y))
                    # print("\nhomeWidth is: "+str(homeWidth) + ",   homeHeight is: "+str(homeHeight)+ ",   y is: " + str(y))

                    # print("\nx - homeWidth + 1 is:  " + str( x - homeWidth + 1) +"   +  y - homeHeight + 1  which is: "+ str( y - homeHeight + 1)+ "   =" + str(max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])), end=" ")

                    #because this starts at five five
                    # print("\n\nscore before: " + str(score))
                    score += max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])
                    # print("\nscore after: " + str(score), end=" ")
    #print("\nreturned Score: " + str(score), end=" ")
    #print("\n")
    return score



#def WorkingMaxgetScore(state):
    score = 0
    hypScoreTotal = 0
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
                        #print("\n\n=TTTTTTTTTTTTTTTTTTTTTTTTTT==MIN BLue==TTTTTTTTTTTTTTTTTTTTTTTT==")
                        #print("\nBlue piece at: (" + str(x) + ", "+ str(y)+")    x: " + str(x) + "   y: "+ str(y)+"")
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
                        #print("\n\nTotal Score: "+ str(hypScoreTotal))
                        break
                    score -= max([0, boardWidth - homeWidth - x]) + max([0, boardHeight - homeHeight - y])
                    #print("\n")

            else:
                if state.board[x, y] == 1:
                    # print("\n<<<<<<<<<<<<<<<<<<<<<FOR MAX>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    # print("\nRed piece at: (" + str(x) + ", "+ str(y)+")    x: " + str(x) + "   y: "+ str(y)+"")
                    # print("\n               hw: "+str(homeWidth) + ",   hh: "+str(homeHeight)+ ",   y: " + str(y))

                    # print("\n(x - hw + 1) =  " + str( x - homeWidth + 1) +"     +      (y - hh + 1) =  "+ str( y - homeHeight + 1)+ "    ===> " + str(max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])))

                    # #because this starts at five five
                    # print("\nscore before: " + str(score), end=" ")
                    score += max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])
                    # print("\nscore after: " + str(score), end=" ")
                    # print("\n")


                  #  score += max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])
    #print("\n")
    return score

# Check whether time limit has been reached
def timeOut(startTime, timeLimit):
    duration = datetime.now() - startTime
    return duration.seconds + duration.microseconds * 1e-6 >= timeLimit

    
# Compute the next move to be played; keep updating <bestMoveSoFar> until computation finished or time limit reached
def getMove(state, hWidth, hHeight, timeLimit):
    depth = 0
    # Set global variables
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight

    startTime = datetime.now()                                       # Remember computation start time
#####################################################################################################################################################################################################################################    

    moveList = getMoveOptions(state)
    if len(moveList) > 0:
        bestMoveSoFar = moveList[0]
    else: 
        return bestMoveSoFar
    
    # getNextState2 = makeMove(state, moveList[0]) 
    # NextMoveList2 = getMoveOptions(getNextState2)      
    # NextBestMoveSoFar2 = NextMoveList2[0]

    # getNextState3 = makeMove(getNextState2, NextMoveList2[0])
    # NextMoveList3 = getMoveOptions(getNextState3)    
    # NextBestMoveSoFar3 = NextMoveList3[0]



                              
    scoreList = []
    for move in moveList:
        projectedState = makeMove(state, move)                      
        scoreList.append(getScore(projectedState))  


    print("\n\n\n\n_________________________________Being called again!__________________________________________________\n\n\n\n")

    
    # NextscoreList2 = []
    # for move in NextMoveList2:
    #     projectedState2 = makeMove(getNextState2, move)  
    #     NextscoreList2.append(getScore(projectedState2))        


    # NextscoreList3 = []
    # for move in NextMoveList3:
    #     projectedState3 = makeMove(getNextState3, move)  
    #     NextscoreList3.append(getScore(projectedState3))        

    count = 0
    while count < 1:
        print("The count is: "+ str(count))
        count = count + 1

    #NextBestMoveSoFar3 = NextMoveList3[NextscoreList3.index(max(NextscoreList3))]
        if state.playerToMove == 0: 
            #TODO have counter, show both for x and y, return bestMoveSar everytime in while, break in while loop, smaller board, manually switch Players.move to 1?, put the loop in both executions?
            print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            print("Last BLUE move: "+str(state.playerToMove)+ "'s turn, which is Blue")
            # for (xs, ys, xe, ye) in [bestMoveSoFar]:
            #     print("\nThe player: "+str(state.playerToMove) +" moved from: ("+ str(xs)+", " +str(ys) + ") to: ("+str(xe)+", "+str(ye)+")")
              


            # moveList = getMoveOptions(NewprojectedState)
            # moveTotry = getMove(NewprojectedState,homeWidth,homeHeight, timeLimit) 

            # for move in moveList:
            #     TryState =  makeMove(NewprojectedState, moveTotry) 












            # print("\nLast Move List:")
            # print(moveList)
            # print("\nScorelist") 
            # print(scoreList)
            # print("\nMax score: "+str(max(scoreList))+",  Index: " + str(scoreList.index(max(scoreList))))
            bestMoveSoFar = moveList[scoreList.index(max(scoreList))] 

            for (xs, ys, xe, ye) in [bestMoveSoFar]:
                print("\nThe player: "+str(state.playerToMove) +" moved from: ("+ str(xs)+", " +str(ys) + ") to: ("+str(xe)+", "+str(ye)+")")
                break



            # getNextState2 = makeMove(state, moveList[0]) 
            # NextMoveList2 = getMoveOptions(getNextState2)      


            # getNextState3 = makeMove(getNextState2, NextMoveList2[0])
            # NextMoveList3 = getMoveOptions(getNextState3)    

            #TODO get the next movelist resulting from this move
            #lookaheadState = makeMove(projectedState, bestMoveSoFar)
            #resultingMoveList = getMoveOptions(lookaheadState)    
           # print("\n\n\nNext Move List: "+str(NextMoveList3))
            #lookaheadMove = getMove(lookaheadState, homeWidth,homeHeight, timeLimit) #TODO depth field
            #NewprojectedState = makeMove(projectedState, bestMoveSoFar) 


            #moveTotry = getMove(NewprojectedState,homeWidth,homeHeight, timeLimit) 
            #TryState =  makeMove(NewprojectedState, moveTotry) 
            depth = 1
            while depth < 7:
               
                NewprojectedState = makeMove(state, bestMoveSoFar) 
                newMove = getMove(NewprojectedState,homeWidth,homeHeight, timeLimit) 
                NextState = makeMove(NewprojectedState, newMove)
                NextMoveList = getMoveOptions(NextState)    

                print("\n\n\n\n\n\n\n\nDepth in iteration:  "+str(depth)+"\n\nNext Move List: "+str(NextMoveList)+"\n\n\n\n\n\n\n\n\n\n")
                depth += 1
















            #print(bestMoveSoFar)
            print("\n\n\n") 

            #getMoveOptions()
            print("\n\n\n") 
           
            if count == 2:
                #bestMoveSoFar = bestMoveSoFar
                #return bestMoveSoFar
                break 
            break   
        else:
            print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            print("Last RED move: "+str(state.playerToMove)+ "'s turn, which is Red")
            bestMoveSoFar = moveList[scoreList.index(min(scoreList))] 
            for (xs, ys, xe, ye) in [bestMoveSoFar]:
                print("\nThe player: "+str(state.playerToMove) +" moved from: ("+ str(xs)+", " +str(ys) + ") to: ("+str(xe)+", "+str(ye)+")")
                break
            print(bestMoveSoFar)
            print("\n\n\n") 
    #print("sleeping...")
    time.sleep(4)
    return bestMoveSoFar


def getMove(state, hWidth, hHeight, timeLimit):
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight

    moveList = getMoveOptions(state)
    if len(moveList) > 0:
        bestMoveSoFar = moveList[0]
    else: 
        return bestMoveSoFar


    scoreList = []
    for move in moveList:
        projectedState = makeMove(state, move)                      
        scoreList.append(getScore(projectedState))  
    
        break

    print("the move list resulting from first move:"+str(moveList))

    if state.playerToMove == 0: 
            print("Last BLUE move: "+str(state.playerToMove)+ "'s turn, which is Blue")
            bestMoveSoFar = moveList[scoreList.index(max(scoreList))] 

            for (xs, ys, xe, ye) in [bestMoveSoFar]:
                print("\nThe player: "+str(state.playerToMove) +" moved from: ("+ str(xs)+", " +str(ys) + ") to: ("+str(xe)+", "+str(ye)+")")
                break

            depth = 1
            while depth < 7:
               
                NewprojectedState = makeMove(state, bestMoveSoFar) 
                newMove = getMove(NewprojectedState,homeWidth,homeHeight, timeLimit) 
                NextState = makeMove(NewprojectedState, newMove)
                NextMoveList = getMoveOptions(NextState)    
                for nextMove in NextMoveList:
                    iteratedState = makeMove(NewprojectedState, newMove)
                    print("\n\n\n\n\n\n\n\nDepth in iteration:  "+str(depth)+"\n\nNext Move List: "+str(getMoveOptions(NextState))+"\n\n\n\n\n\n\n\n\n\n")
                depth += 1
    else:
            print("Last RED move: "+str(state.playerToMove)+ "'s turn, which is Red")
            bestMoveSoFar = moveList[scoreList.index(min(scoreList))] 
            for (xs, ys, xe, ye) in [bestMoveSoFar]:
                print("\nThe player: "+str(state.playerToMove) +" moved from: ("+ str(xs)+", " +str(ys) + ") to: ("+str(xe)+", "+str(ye)+")")
                break
            print(bestMoveSoFar)
            print("\n\n\n") 











    print("sleeping...")
    time.sleep(4)
    return bestMoveSoFar
