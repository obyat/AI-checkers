# Player Abdelrahman Obyat
#Please note this implements iterative deepneing and minimax correctly, with individually correct GetScoreMix(), getScoreMax()
#Meaning both functions accurately return the number of moves left to make while accounting for jumps.

#however, I am stuck on the issue where Player1 significantly improves using iterative deepening minimax, while player2 does not benifit. It was suggested on piazza 
#that getScore could bet the reason, but it deosn't seem to be through tests.
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
                        hypMinScoreTotal = (ax - homeWidth + 1 ) + (by - homeHeight + 1)
                        print("\n\hypMinScoreTotal: "+ str(hypMinScoreTotal))
                        moves = []
                        break
                        #hypMinScoreTotal -= max([0, boardWidth - homeWidth - (x - maxix)]) + max([0, boardHeight - homeHeight - y])
                        # print("\n\nTotal min Score: "+ str(hypMinScoreTotal))             



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

    print("\n\Max Score: "+ str(hypMaxScoreTotal))
    return hypMaxScoreTotal



# Check whether time limit has been reached
def timeOut(startTime, timeLimit):
    duration = datetime.now() - startTime
    return duration.seconds + duration.microseconds * 1e-6 >= timeLimit

def getBestMoveSoFar(move, state):
    return move

def getState(move, state):
    return state








#         while not timeOut(startTime, timeLimit) and keepgoing:
#             depthlimit += 1

#             bestMoveSoFar, iteratedToGoal, scoreAtDepth = iterateMove(projectedState, hWidth, hHeight, timeLimit, move, 0,  depthlimit)
#             scoreList.append(scoreAtDepth)
#             print("this is the scoreList" + str(scoreList))
#             print("the move with that scorelist"+str(bestMoveSoFar))
#             if iteratedToGoal == True or projectedState.winner == 0:
#                 keepgoing = False
#                 break             



#     if state.playerToMove == 0:  
#         bestMoveSoFar = bestMoveSoFar                                    # Finally, pick the move with the best score
#         #bestMoveSoFar = GivenMoveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
#     else:
#         bestMoveSoFar = bestMoveSoFar
#         #bestMoveSoFar = GivenMoveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score


#     return bestMoveSoFar



# def iterateMove(state, hWidth, hHeight, timeLimit, currentbestMove, startdepth, depthlimit):
#     global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
#     boardWidth = state.board.shape[0]
#     boardHeight = state.board.shape[1]
#     homeWidth = hWidth
#     homeHeight = hHeight
#     bestMoveSoFar = currentbestMove
#     scoreList = []
#     scoreList.append(getScore(state))  
#     GivenMoveList = getMoveOptions(state) 
#     winningState = -1
#     checkMyState = state
#     iteratedToGoal = False
#     scoreAtDepth = 0
#     for givenMove in GivenMoveList:
#         if ((state.winner == -1) and (startdepth < depthlimit)):
#             if state.playerToMove == 0:  
#                 startdepth += 1
#                 print("\n\nI can only look ahead to depth: "+str(depthlimit) +"!")
#                 print("I am now looking ahead to depth: "+str(startdepth))  
#                 print("The possible moves from this " +str(startingLocation(givenMove)) + " *lookahead* depth: "+str(GivenMoveList))
#                 print("The move Im lookingahead from in the *Next* depth: "+str(destination(givenMove)))                          

#                 if (startdepth == depthlimit):
#                     print("\n\n I finally reached the current given depthlimit: "+str(depthlimit) +", Im gonna compute the score and return it with the bestmove for max___")
#                     scoreAtDepth = getScore(state)
#                  #   print("ScoreAtDepthLimit"+str(scoreAtDepth))

                  
            
                     
#             state = makeMove(state, givenMove)
#             nextmove = getMoveOptions(state)
#             #print("next set of moves: "+str(nextmove))
#             if (state.winner != -1):
#              #   print("\nThe *original* move "+str(bestMoveSoFar)+" needed depth "+str(depthlimit) +" to win!\n\n\n\n\n\n")
#               #  print("The last move which WON the game: "+str(destination(givenMove)))     
#                 iteratedToGoal = True
#                 scoreATDepth = 100000000000000000
#                 print(iteratedToGoal)
#                 bestMoveSoFar = givenMove
#                 return bestMoveSoFar, iteratedToGoal, scoreAtDepth
#                 break
#             else:    
#                 bestMoveSoFar, iteratedToGoal, scoreAtDepth = iterateMove(state, hWidth, hHeight, timeLimit, bestMoveSoFar, startdepth, depthlimit)  
   
#             break
#         break







#     return bestMoveSoFar, iteratedToGoal, scoreAtDepth



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
                bestMoveSoFar = moveList[0] #moveList[scoreList.index(max(scoreList))]   
            else:
                bestMoveSoFar = moveList[0] #moveList[scoreList.index(min(scoreList))]    



        projectedState = makeMove(state, move)    

        while not timeOut(startTime, timeLimit) and keepgoing:
            depthlimit += 1

            bestMoveSoFar, iteratedToGoal, scoreAtDepth = iterateMove(projectedState, hWidth, hHeight, timeLimit, move, 0,  depthlimit)
            scoreList.append(scoreAtDepth)
            bestMoveList.append(bestMoveSoFar)
            if iteratedToGoal == True or projectedState.winner == 0:
                keepgoing = False
                break             

    if state.playerToMove == 0:                                      # Finally, pick the move with the best score
        bestMoveSoFar = bestMoveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
        returnedScore = scoreList[scoreList.index(max(scoreList))]
       # print("The max score if we are blue: "+str(returnedScore))
        # print("The bestMoveList so far"+str(bestMoveList))
        # print ("\n\nThe score Which was returned: " + str(returnedScore))
        # print ("\n\nThe move Which was returned with it: " + str(bestMoveSoFar))
    else:
        bestMoveSoFar = bestMoveList[scoreList.index(min(scoreList))]  
        returnedScore = scoreList[scoreList.index(min(scoreList))]
        print("The min score if we are red: "+str(returnedScore))
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
                # print("The possible moves from this " +str(startingLocation(givenMove)) + " *lookahead* depth: "+str(GivenMoveList))
                # print("The move Im lookingahead from in the *Next* depth: "+str(destination(givenMove)))                          

                if (startdepth == depthlimit):
                    #print("\n\n I finally reached the current given depthlimit: "+str(depthlimit) +", Im gonna compute the score and return it with the bestmove for max___")
                    scoreAtDepth = getScoreMax(state)
                    #print("score at min's depth "+str(scoreAtDepth))
                    return bestMoveSoFar, iteratedToGoal, scoreAtDepth




            # The work is done for both but only printing for max, uncommment below to also print for min
                  


            #     print("\n\nI can only look ahead to depth: "+str(depthlimit) +"!")
            #     print("I am now looking ahead to depth: "+str(startdepth))  
            #     print("The possible moves from this " +str(startingLocation(givenMove)) + " *lookahead* depth: "+str(GivenMoveList))
            #     print("The move Im lookingahead from in the *Next* depth: "+str(destination(givenMove)))                          
            if (state.winner == -1):
                       
                if (startdepth == depthlimit):
             #    print("\n\n I finally reached the current given depthlimit: "+str(depthlimit) +", Im gonna compute the score and return it with the bestmove for min___")
                    
                    scoreAtDepth = getScoreMax(state)
                   # print("score at min's depth "+str(scoreAtDepth))
                    return bestMoveSoFar, iteratedToGoal, scoreAtDepth

            state = makeMove(state, givenMove)
            if  state.winner == 1:
                scoreAtDepth = minWins
                return bestMoveSoFar, iteratedToGoal, scoreAtDepth
                break
            elif state.playerToMove == 1:  
                 if state.winner == 0:
                    scoreAtDepth = maxWins
                    return bestMoveSoFar, iteratedToGoal, scoreAtDepth
                    break
            #note the if state.winner == -1 check should terminate this work on its own but it cant
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





# def getMove(state, hWidth, hHeight, timeLimit):
#     global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
#     boardWidth = state.board.shape[0]
#     boardHeight = state.board.shape[1]
#     homeWidth = hWidth
#     homeHeight = hHeight
#     keepgoing = True
#     startTime = datetime.now()                                    
#     moveList = getMoveOptions(state)                                 
#     depthlimit = 1
#     scoreList = []
#     scoreAtDepth = 0
#     iteratedToGoal = False
#     for move in moveList:
#         #scoreList.append(getScore(state))
#         if len(moveList) > 0:                                                                    
#             if state.playerToMove == 0:                                     
#                 bestMoveSoFar = moveList[0]# moveList[scoreList.index(max(scoreList))]   
#             else:
#                 bestMoveSoFar = moveList[0]#moveList[scoreList.index(min(scoreList))]    

#         projectedState = makeMove(state, move)    







#         while not timeOut(startTime, timeLimit) and keepgoing:
#             depthlimit += 1

#             bestMoveSoFar, iteratedToGoal, scoreAtDepth = iterateMove(projectedState, hWidth, hHeight, timeLimit, move, 0,  depthlimit)
#             scoreList.append(scoreAtDepth)
#             print("this is the scoreList" + str(scoreList))
#             print("the move with that scorelist"+str(bestMoveSoFar))
#             if iteratedToGoal == True or projectedState.winner == 0:
#                 keepgoing = False
#                 break             



#     if state.playerToMove == 0:  
#         bestMoveSoFar = bestMoveSoFar                                    # Finally, pick the move with the best score
#         #bestMoveSoFar = GivenMoveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
#     else:
#         bestMoveSoFar = bestMoveSoFar
#         #bestMoveSoFar = GivenMoveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score


#     return bestMoveSoFar



# def iterateMove(state, hWidth, hHeight, timeLimit, currentbestMove, startdepth, depthlimit):
#     global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
#     boardWidth = state.board.shape[0]
#     boardHeight = state.board.shape[1]
#     homeWidth = hWidth
#     homeHeight = hHeight
#     bestMoveSoFar = currentbestMove
#     scoreList = []
#     scoreList.append(getScore(state))  
#     GivenMoveList = getMoveOptions(state) 
#     winningState = -1
#     checkMyState = state
#     iteratedToGoal = False
#     scoreAtDepth = 0
#     for givenMove in GivenMoveList:
#         if ((state.winner == -1) and (startdepth < depthlimit)):
#             if state.playerToMove == 0:  
#                 startdepth += 1
#                 print("\n\nI can only look ahead to depth: "+str(depthlimit) +"!")
#                 print("I am now looking ahead to depth: "+str(startdepth))  
#                 print("The possible moves from this " +str(startingLocation(givenMove)) + " *lookahead* depth: "+str(GivenMoveList))
#                 print("The move Im lookingahead from in the *Next* depth: "+str(destination(givenMove)))                          

#                 if (startdepth == depthlimit):
#                     print("\n\n I finally reached the current given depthlimit: "+str(depthlimit) +", Im gonna compute the score and return it with the bestmove for max___")
#                     scoreAtDepth = getScore(state)
#                  #   print("ScoreAtDepthLimit"+str(scoreAtDepth))

                  
            
                     
#             state = makeMove(state, givenMove)
#             #print("next set of moves: "+str(nextmove))
#             if (state.winner != -1):
#                 print("\nThe *original* move "+str(bestMoveSoFar)+" needed depth "+str(depthlimit) +" to win!\n\n\n\n\n\n")
#                 print("The last move which WON the game: "+str(destination(givenMove)))     
#                 iteratedToGoal = True
#                 scoreATDepth = 100000000000000000
#                 print(iteratedToGoal)
#                 bestMoveSoFar = givenMove
#                 return bestMoveSoFar, iteratedToGoal, scoreAtDepth
#                 break
#             else:    
#                 bestMoveSoFar, iteratedToGoal, scoreAtDepth = iterateMove(state, hWidth, hHeight, timeLimit, bestMoveSoFar, startdepth, depthlimit)  
   
#             break
#         break







#     return bestMoveSoFar, iteratedToGoal, scoreAtDepth














    # for givenMove in GivenMoveList:
    #     while ((state.winner == -1) and (startdepth < depthlimit)):
    #         if state.playerToMove == 0:  
    #             startdepth += 1
    #             print("\n\nI can only look ahead to depth: "+str(depthlimit) +"!")
    #             print("I am now looking ahead to depth: "+str(startdepth))  
    #             print("The possible moves from this " +str(startingLocation(givenMove)) + " *lookahead* depth: "+str(GivenMoveList))
    #             print("The move Im lookingahead from in the *Next* depth: "+str(destination(givenMove)))                            #todo| For each move, play it on a separate board...
    #             if (startdepth == depthlimit):
    #                 print("\n\n I finally reached the current given depthlimit: "+str(depthlimit) +", Im gonna compute the score and return it with the bestmove for max___")
                  

                  
    #         state = makeMove(state, givenMove)                                
    #         winningState = state.winner


    #         if (winningState  == -1):
    #             bestMoveSoFar, winningState, bestScoreSoFar = iterateMove(state, hWidth, hHeight, timeLimit, bestMoveSoFar, startdepth, depthlimit)  
    #         else:
    #             print("\n\nThe *original* move "+str(bestMoveSoFar)+" needed depth "+str(depthlimit) +" to win!\n\n\n\n\n\n")
    #             print("The last move which WON the game: "+str(destination(givenMove)))     

    #             winningState = 0
    #             if state.playerToMove == 0:                                    
    #                 bestMoveSoFar = GivenMoveList[scoreList.index(max(scoreList))] 
    #             else:
    #                 bestMoveSoFar = GivenMoveList[scoreList.index(min(scoreList))]    
    #             break
    #         break
    #     break

    # return bestMoveSoFar, winningState, bestScoreSoFar





#fixed the bug where infinit depths
"""

def getMove(state, hWidth, hHeight, timeLimit):
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight
    keepgoing = True
    startTime = datetime.now()                                       # Remember computation start time
    #todoprint("I got the current best score with the best move:___so im gonna sort my scorelist with its corresponding move and exapnd the next most likely to win")
    #todoprint("I also need MaxSCORE, MinSCORE to return incase we or opponent win")
    moveList = getMoveOptions(state)                                 # Get the list of possible moves
    #TODO bestMoveSoFar = currentbestMove                                  # Just choose first move from the list for now, in case we run out of time 
    depthlimit = 1
    scoreList = []



#maybe sort moveList first?
    for move in moveList:
        scoreList.append(getScore(state))

        if len(moveList) > 0:                                                                  
            if state.playerToMove == 0:                                    
                bestMoveSoFar = moveList[scoreList.index(max(scoreList))] 
            else:
                bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    


        projectedState = makeMove(state, move)                       
       
       
        while (not timeOut(startTime, timeLimit)) and keepgoing:
            depthlimit += 1
            bestMoveSoFar, bestScoreSoFar = iterateMove(projectedState, hWidth, hHeight, timeLimit, bestMoveSoFar, 0,  depthlimit)
          
            if (state != -1) or (projectedState.winner != -1):
                keepgoing = False
                break                
    return bestMoveSoFar



def iterateMove(state, hWidth, hHeight, timeLimit, currentbestMove, startdepth, depthlimit):
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight
    bestMoveSoFar = currentbestMove
    scoreList = []
    scoreList.append(getScore(state))  
    GivenMoveList = getMoveOptions(state) 
    winningState = -1
    bestScoreSoFar = 1

    for givenMove in GivenMoveList:
        while ((state.winner == -1) and (startdepth < depthlimit)):
            if state.playerToMove == 0:  
                startdepth += 1
                print("\n\nI can only look ahead to depth: "+str(depthlimit) +"!")
                print("I am now looking ahead to depth: "+str(startdepth))  
                print("The possible moves from this " +str(startingLocation(givenMove)) + " *lookahead* depth: "+str(GivenMoveList))
                print("The move Im lookingahead from in the *Next* depth: "+str(destination(givenMove)))   
                print("The move that won!! "+str(givenMove))                       


                if (startdepth == depthlimit):
                    print("\n\n I finally reached the current given depthlimit: "+str(depthlimit) +", Im gonna compute the score and return it with the bestmove for max___")
                  
            state = makeMove(state, givenMove)                                
            bestMoveSoFar, bestScoreSoFar = iterateMove(state, hWidth, hHeight, timeLimit, bestMoveSoFar, startdepth, depthlimit)  


            
    print("\n\nThe *original* move "+str(bestMoveSoFar)+" needed depth "+str(depthlimit) +" to win!\n\n\n\n\n\n")
    if state.playerToMove == 0:                                    
        bestMoveSoFar = bestMoveSoFar#GivenMoveList[scoreList.index(max(scoreList))] 
    else:
        bestMoveSoFar = bestMoveSoFar #GivenMoveList[scoreList.index(min(scoreList))]    

    return bestMoveSoFar,  bestScoreSoFar










"""