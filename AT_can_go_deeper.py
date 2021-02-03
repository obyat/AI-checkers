# Player Alan_Turing

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
def getScore(state):
    score = 0
    for x in range(boardWidth):                             # Search board for any pieces
        for y in range(boardHeight):
            if state.board[x, y] == 0:                      # Subtract the number of moves (non-jumps) for Player 1's piece to reach Player 2's home area
                score -= max([0, boardWidth - homeWidth - x]) + max([0, boardHeight - homeHeight - y])
            else:
                if state.board[x, y] == 1:                  # Add the number of moves (non-jumps) for Player 2's piece to reach Player 1's home area
                    score += max([0, x - homeWidth + 1]) + max([0, y - homeHeight + 1])
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
    

    moveList = getMoveOptions(state)                                 # Get the list of possible moves
    if len(moveList) > 0:
        bestMoveSoFar = moveList[0]
    else: 
        return bestMoveSoFar  
                                       # Just choose first move from the list for now, in case we run out of time 
    print("Actual Move to make/bestMove: "+str(bestMoveSoFar))
    print("\nPurmutation of MoveList: "+str(moveList))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXIT\n")


    scoreList = []
    for move in moveList:
        print("The last move: "+str(move))
        projectedState = makeMove(state, move)                       # For each move, play it on a separate board...
        scoreList.append(getScore(projectedState))                   # ... and call the evaluation function on the resulting GameState
        #returns
        getMove(projectedState, hWidth, hHeight, timeLimit)     
        time.sleep(30)

    if state.playerToMove == 0:                                      # Finally, pick the move with the best score
        bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
    else:
        bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score

    return bestMoveSoFar




""# Compute the next move to be played; keep updating <bestMoveSoFar> until computation finished or time limit reached
def getMove(state, hWidth, hHeight, timeLimit):
    # Set global variables
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight
    

    moveList = getMoveOptions(state)                                 # Get the list of possible moves
    if len(moveList) > 0:
        bestMoveSoFar = moveList[0]
    else: 
        return bestMoveSoFar  
                                       # Just choose first move from the list for now, in case we run out of time 
    print("Actual Move to make/bestMove: "+str(bestMoveSoFar))
    print("\nPurmutation of MoveList: "+str(moveList))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXIT\n")


    scoreList = []
    for move in moveList:
        print("The last move: "+str(move))



        #possibly two state, to avoid opponent???
        
        newState = makeMove(state, move)                        #todo For each move, play it on a separate board...
                                                                #todo make a new state with our initial move
        resultingmovesList = getMoveOptions(newState)           #todo for the new created state, get the LIST of next possible moves
        for move in resultingmovesList:                     #todo for each possible move...
            while (newState.winner == -1):                #todo if at somepoint our next move could win, then stop playing

                #todo if the CURRENT move from FIRSTTTT list won the game, then it is our bmsf
                makeAnotherMoveWithState =  makeMove(newState, move)            #todo for each move you make get the resulting state
                getMove(makeAnotherMoveWithState, hWidth, hHeight, timeLimit)       #TODO recurively get the next possible bmsf could be max or min >:)
                if (newState.winner != -1):                                 #Todo if we won it??? stop recursing, and return our FIRST INITAL BMSF
                    print("THIS WON IT=================================")                            #todo maybe change this to anotherstate?
                    return bestMoveSoFar
                break
 
            break
        
        scoreList.append(getScore(newState))                   # ... and call the evaluation function on the resulting GameState
        #returns
        
        
        if (newState.winner != -1):
            print("THIS WON IT=================================")
            time.sleep(2)
            break  
        break
    if state.playerToMove == 0:                                      # Finally, pick the move with the best score
        bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
    else:
        bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score

    return bestMoveSoFar







#WORKING??????????
# "# Compute the next move to be played; keep updating <bestMoveSoFar> until computation finished or time limit reached
# def getMove(state, hWidth, hHeight, timeLimit):
#     # Set global variables
#     global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
#     boardWidth = state.board.shape[0]
#     boardHeight = state.board.shape[1]
#     homeWidth = hWidth
#     homeHeight = hHeight
    

#     moveList = getMoveOptions(state)                                 # Get the list of possible moves
#     if len(moveList) > 0:
#         bestMoveSoFar = moveList[0]
#     else: 
#         return bestMoveSoFar  
#                                        # Just choose first move from the list for now, in case we run out of time 
#     print("Actual Move to make/bestMove: "+str(bestMoveSoFar))
#     print("\nPurmutation of MoveList: "+str(moveList))
#     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXIT\n")


#     scoreList = []
#     for move in moveList:
#         print("The last move: "+str(move))



#         newState = makeMove(state, move)                       # For each move, play it on a separate board...
#         resultingmovesList = getMoveOptions(newState)
#         for move in resultingmovesList:
#                                             #todo maybe change this to anotherstate?
#             makeAnotherState =  makeMove(newState, move)   
#             getMove(makeAnotherState, hWidth, hHeight, timeLimit)     
#         scoreList.append(getScore(newState))                   # ... and call the evaluation function on the resulting GameState
#         #returns
        
#         time.sleep(50)

#     if state.playerToMove == 0:                                      # Finally, pick the move with the best score
#         bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
#     else:
#         bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score

#     return bestMoveSoFar














































# Compute the next move to be played; keep updating <bestMoveSoFar> until computation finished or time limit reached
# def getMove(state, hWidth, hHeight, timeLimit):
#     # Set global variables
#     global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
#     boardWidth = state.board.shape[0]
#     boardHeight = state.board.shape[1]
#     homeWidth = hWidth
#     homeHeight = hHeight
    

#     moveList = getMoveOptions(state)                                 # Get the list of possible moves
#     if len(moveList) > 0:
#         bestMoveSoFar = moveList[0]
#     else: 
#         return bestMoveSoFar  
#                                        # Just choose first move from the list for now, in case we run out of time 
#     print("Actual Move to make/bestMove: "+str(bestMoveSoFar))
#     print("\nPurmutation of MoveList: "+str(moveList))
#     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXIT\n")


#     scoreList = []
#     for move in moveList:
#         print("The last move: "+str(move))
#         projectedState = makeMove(state, move)                       # For each move, play it on a separate board...
#         scoreList.append(getScore(projectedState))                   # ... and call the evaluation function on the resulting GameState
#         #returns
#         getMove(projectedState, hWidth, hHeight, timeLimit)     
#         time.sleep(30)

#     if state.playerToMove == 0:                                      # Finally, pick the move with the best score
#         bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
#     else:
#         bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score

#     return bestMoveSoFar













def iterateMove(state, hWidth, hHeight, timeLimit):
    # Set global variables
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMove
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight



    moveList = getMoveOptions(state)                                 # Get the list of possible moves
    bestMove = moveList[0]                                      # Just choose first move from the list for now, in case we run out of time 


    scoreList = []
    for move in moveList:
        projectedState = makeMove(state, move)                       # For each move, play it on a separate board...
        iteratedMoveList = getMoveOptions(projectedState)
        scoreList.append(getScore(projectedState))                   # ... and call the evaluation function on the resulting GameState
    if state.playerToMove == 0:                                      # Finally, pick the move with the best score
        bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
    else:
        bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score
    return bestMove