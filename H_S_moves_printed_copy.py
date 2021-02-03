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
#def getScore(state):
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



def getScore(state):
    score = 0
    hypScoreTotal = 0
    minscore = 0
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
                        hypScoreTotal -= max([0, (boardWidth - homeWidth - ax)]) + max([0, (boardHeight - homeHeight - by)])
                        print("\n\Max's Score: "+ str(hypScoreTotal))
                        break
                    score -= max([0, boardWidth - homeWidth - x]) + max([0, boardHeight - homeHeight - y])
                    #print("\n")

            else:
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
                    if ((xStar == x and yStar == y) and [((xEn - x) > maxix) or ((yEn - y) > maxiy)]):
                        maxix = xEn - x
                        maxiy = yEn - y
                        maxix = -maxix
                        maxiy = -maxiy
                        print("max x jump for red piece is: " +str(maxix))
                        print("max y jump for red piece is: " +str(maxiy))
                    print("\n<<<<<<<<<<<<<<<<<<<<<FOR MAX>>>>>>>>>>>>>>>>>>>>>>>>>>")
                    # print("\nRed piece at: (" + str(x) + ", "+ str(y)+")    x: " + str(x) + "   y: "+ str(y)+"")
                    # print("\n               hw: "+str(homeWidth) + ",   hh: "+str(homeHeight)+ ",   y: " + str(y))

                    # print("\n(x - hw + 1) =  " + str( x - homeWidth + 1) +"     +      (y - hh + 1) =  "+ str( y - homeHeight + 1)+ "    ===> " + str(max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])))

                    # #because this starts at five five
                    # print("\nscore before: " + str(score), end=" ")
                    minscore += max([0, x - homeWidth + maxix]) + max([0, y - homeHeight + maxiy])
                    # print("\nscore after: " + str(score), end=" ")
                    # print("\n")
                    print("Mins Score"+str(minscore))




















                  #  score += max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])
    #print("\n")
    print("score:"+str(score))
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
    while count < 5:
        print("The count is: "+ str(count))
        count = count + 1

    #NextBestMoveSoFar3 = NextMoveList3[NextscoreList3.index(max(NextscoreList3))]
        if state.playerToMove == 0: 
            #TODO have counter, show both for x and y, return bestMoveSar everytime in while, break in while loop, smaller board, manually switch Players.move to 1?, put the loop in both executions?
            print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            print("Last BLUE move: "+str(state.playerToMove)+ "'s turn, which is Blue")
            #print("\nLast Move List:")
            #print(moveList)
            #print("\nScorelist") 
            #print(scoreList)
            #print("\nMax score: "+str(max(scoreList))+",  Index: " + str(scoreList.index(max(scoreList))))
            for (xs, ys, xe, ye) in [bestMoveSoFar]:
                print("\nThe player: "+str(state.playerToMove) +" moved from: ("+ str(xs)+", " +str(ys) + ") to: ("+str(xe)+", "+str(ye)+")")
                break
            bestMoveSoFar = moveList[scoreList.index(max(scoreList))] 
            #print(bestMoveSoFar)
            print("\n\n\n") 
            NewprojectedState = makeMove(projectedState, bestMoveSoFar) 
            moveTotry = getMove(NewprojectedState,homeWidth,homeHeight, timeLimit) 
            TryState =  makeMove(NewprojectedState, moveTotry) 
            if (TryState.winner != -1):
                print("\n\n___WWWWWWWoooooooooooooooooNNNNNNNNNNNNNNNNNNN____________WOOOOOOOOOOOOOONNNNNNNNNNNNNNNNNN_____________:"+str(TryState.winner))
            elif TryState.winner == -1:

                print("\n\nTHIS IS THE BEFORE_-------------------------------------___:"+str(TryState.winner))
            #if moveTotry 
            return bestMoveSoFar

            if count == 1:
                #time.sleep(10)
                bestMoveSoFar = bestMoveSoFar
                return bestMoveSoFar
                break 
            break    
           
        #break
            #print("WINNER STATE"+str(state.winner))

            #while depth <= 3:
        #     if len(moveList) > 0:
        # #          depth += 1
        # #         print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv") 
        #         #Nmove = getMove(projectedState,homeWidth,homeHeight, timeLimit) 
        #        # NewprojectedState = makeMove(projectedState, bestMoveSoFar)  
        #         # print("\nNext Depth: "+str(depth))
        #         #print("Sleeping....")
        #         #time.sleep(15)                      
        #         #bestMoveSoFar =

        #         #return bestMoveSoFar
        #         break
        #         #print("\n\n\nIN HEREERERERERERER \n\n\n" )
        #         #time.sleep(1)
        #         #print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            # else: 
            #     return bestMoveSoFar
            #     break
        elif state.playerToMove == 1:
            print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            # print("\nMax score: "+str(max(scoreList))+",  Index: " + str(scoreList.index(min(scoreList))))

            print("Last RED move: "+str(state.playerToMove)+ "'s turn, which is Red")
          #  print("\nLast Move List:")
           # print(moveList)
           # print("\nScorelist") 
           # print(scoreList)
           # print("\nMax score: "+str(max(scoreList))+",  Index: " + str(scoreList.index(min(scoreList))))
            for (xs, ys, xe, ye) in [bestMoveSoFar]:
                print("\nThe player: "+str(state.playerToMove) +" moved from: ("+ str(xs)+", " +str(ys) + ") to: ("+str(xe)+", "+str(ye)+")")
                break
            #bestMoveSoFar = moveList[scoreList.index(min(scoreList))] 
            print(bestMoveSoFar)
            print("\n\n\n") 
            #time.sleep(1)
    #     print("\nOpponetMoveList:")
    #     print(NextMoveList2)
    #     print("\nScorelist") 
    #     print(NextscoreList2)
    #     print("\nMax score: "+str(max(NextscoreList2))+",  Index: " + str(NextscoreList2.index(max(NextscoreList2))))
    #     print("\nMove:")
    #     bestMoveSoFar = NextMoveList2[NextscoreList2.index(min(NextscoreList2))]
    #     print(bestMoveSoFar)
    #     print("\n\n\n") 
    #     time.sleep(6)

    # elif state.playerToMove == 0:
    #     print("GOTHHHHHHHHHHHHHHHHHHHHHHHHHHHEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRRRREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

    #     print("Next move is "+str(state.playerToMove)+ "'s turn, which is Blue")
    #     print("\nNext Move List:")
    #     print(NextMoveList3)
    #     print("\nScorelist") 
    #     print(NextscoreList3)
    #     print("\nMax score: "+str(max(NextscoreList3))+",  Index: " + str(NextscoreList3.index(max(NextscoreList3))))
    #     print("\nMove:")
    #     print(NextBestMoveSoFar3)
    #     print("\n\n\n") 

    #     print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    print("sleeping...")
    time.sleep(40)
    return bestMoveSoFar












    #print("lIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
           # ... and call the evaluation function on the resulting GameState

    
    #if state.playerToMove == 0:  
     


        #TODO next next state so its blue again
    

    # else:
    #     bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score

    # print("###########################################################################################################################")

# return bestMoveSoFar







































"""     
    print(state.board[0,0])
    print("\nLast Move List:")
    print(moveList)
    print("Last Move:")
    print(bestMoveSoFar)
    print("score of last move & its index")
    print("blue guy by himself can have a score 0 to 8. 0to4 for xmoves. 0to4 for ymoves")
    print(max(scoreList))
    print(scoreList.index(max(scoreList)))
 

    #next next state
   
    print("\nNext Move List:")
    print(NextNextMoveList)
    print("Next Move:")
    print(NextBestMoveSoFar)
    print("score of next move & its index")
    print(max(NextscoreList))
    print(NextscoreList.index(max(NextscoreList)))





        print("\nscorelist") 
        print(scoreList)

        print("Max score of last move & its index")
        print(max(scoreList))
        print(scoreList.index(max(scoreList)))

        print("the move at that index")
        print(bestMoveSoFar)
        print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        print("\n\n")

        print("\nNextscorelist") 
        print(scoreList)

        print("Max score of last move & its index")
        print(max(scoreList))
        print(scoreList.index(max(scoreList)))

        print("the move at that index")
        print(nextbestMove)
        print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
        print("\n\n")
 """
