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



def destination(move):
    destL = [move]
    for (xs, ys, xe, ye) in destL:
        dest = (xe, ye)
    return dest

def startingLocation(move):
    destL = [move]
    for (xs, ys, xe, ye) in destL:
        dest = (xs, ys)
    return dest


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
def getMove_old(state, hWidth, hHeight, timeLimit):
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
        iterateMove(projectedState, hWidth, hHeight, timeLimit)     
        time.sleep(30)

    if state.playerToMove == 0:                                      # Finally, pick the move with the best score
        bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
    else:
        bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score

    return bestMoveSoFar


""# Compute the next move to be played; keep updating <bestMoveSoFar> until computation finished or time limit reached
def getMove____THE_LAST_WORKING(state, hWidth, hHeight, timeLimit):
    # Set global variables
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight
    scoreList = []
    scoreList.append(getScore(state))  
    









    OgmoveList = getMoveOptions(state)         
    bestMoveSoFar = OgmoveList[0] if len(OgmoveList) > 0  else bestMoveSoFar        #todo| Just choose first move from the list for now, in case we run out of time 

    print("The bestMoveSofar from outside whileloop: "+str(bestMoveSoFar))
    print("\nSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsPurmutation of MoveList: "+str(OgmoveList))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXIT\n")

    OgmoveList = getMoveOptions(state)         


    #maybe put inside of for
    Keepgoing = True;
    for originalMove in OgmoveList:
        while ((state.winner == -1) and (Keepgoing == True)):

            print("The last/ORIGINAL move: "+str(originalMove))                            #todo| For each move, play it on a separate board...
            print("\n\n\nIteratedMove from while loop" + str(originalMove))

            #possibly two state, to avoid opponent???                      
            Newstate = makeMove(state, originalMove)                                    #todo| make a new state with our move from the initial moveList
            if (Newstate.winner == -1):
                getMove(Newstate, hWidth, hHeight, timeLimit)  
            else:
                print("\n\n\n\n\n\n_____win\n\n\n\n\n\n")
                print("\n\n\n\n\n\nwinning_____move:"+str(originalMove)+"\n\n\n\n\n\n")
                Keepgoing = False
                time.sleep(2)
                break
            break
        break

    # for originalMove in OgmoveList:
    #    # print("The last/ORIGINAL move: "+str(originalMove))                         #todo| For each move, play it on a separate board...

    #     #possibly two state, to avoid opponent???                      
    #     newState = makeMove(state, originalMove)                                    #todo| make a new state with our move from the initial moveList
    #     resultingmovesList = getMoveOptions(newState)                               #todo| for the new created state, get the LIST of next possible moves


    #     for IteratedMove in resultingmovesList:                                     #todo| for each possible move FROM THE NEW MOVE LIST...
    #         while (newState.winner == -1):                                          #todo| if at somepoint our next move could win, then stop playing
               
    #             print("\n\n\nIteratedMove from while loop" + str(IteratedMove))
    #                                                                                 #todo| Actual TODO if the CURRENT move from FIRSTTTT list won the game, then it is our bmsf


    #             makeAnotherMoveWithState =  makeMove(newState, IteratedMove)        #todo| for each IteratedMove you make get the resulting state
    #             #RECURSE
    #             getMove(makeAnotherMoveWithState, hWidth, hHeight, timeLimit)       #TODO| recurively get the next possible bmsf could be max or min >:)



























                # if state.playerToMove == 0:                                      # Finally, pick the move with the best score
                #     bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
                # else:
                #     bestMoveSoFar = moveList[scoreList.index(min(scoreList))]                
        
                         # ... and call the evaluation function on the resulting GameState
        #returns
        
        
        if (state.winner != -1):
            print("______________________________________________________________________________________________________THE Last lookahead Move THAT WON"+str(originalMove))
            bestMoveSoFar = originalMove
            time.sleep(20)
            break  
        break
    if state.playerToMove == 0:  
        #bestMoveSoFar = bestMoveSoFar                                    # Finally, pick the move with the best score
        bestMoveSoFar = OgmoveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
    else:
        #bestMoveSoFar = bestMoveSoFar
        bestMoveSoFar = OgmoveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score

    return bestMoveSoFar


#TODO BEST WORKING VERSION SO FAR (ACTUALLY LOOKS AHEAD UNTIL GOAL WITHOUT PLAYING IN THE CURRENT GAME, BUT DOES NOT RETURN OG MOVE)
def getMove_backup(state, hWidth, hHeight, timeLimit):
    # Set global variables
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight
    

    OgmoveList = getMoveOptions(state)                                 # Get the list of possible moves
    if len(OgmoveList) > 0:
        bestMoveSoFar = OgmoveList[0]
    else: 
        return bestMoveSoFar  
                                       # Just choose first move from the list for now, in case we run out of time 
    print("The bestMoveSofar from outside whileloop: "+str(bestMoveSoFar))
    print("\nPurmutation of MoveList: "+str(moveList))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXIT\n")


    scoreList = []
    for originalMove in OgmoveList:
        print("The last/ORIGINAL move: "+str(originalMove))                      #todo| For each move, play it on a separate board...

        #possibly two state, to avoid opponent???                      
        newState = makeMove(state, originalMove)                        #todo| make a new state with our move from the initial moveList
        resultingmovesList = getMoveOptions(newState)           #todo| for the new created state, get the LIST of next possible moves


        for IteratedMove in resultingmovesList:                     #todo| for each possible move FROM THE NEW MOVE LIST...
            while (newState.winner == -1):                  #todo| if at somepoint our next move could win, then stop playing
                print("\n\n\nIteratedMove from while loop" + str(IteratedMove))
                #todo| Actual TODO if the CURRENT move from FIRSTTTT list won the game, then it is our bmsf
                makeAnotherMoveWithState =  makeMove(newState, IteratedMove)        #todo| for each IteratedMove you make get the resulting state
                getMove(makeAnotherMoveWithState, hWidth, hHeight, timeLimit)       #TODO| recurively get the next possible bmsf could be max or min >:)
                # if state.playerToMove == 0:                                      # Finally, pick the move with the best score
                #     bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
                # else:
                #     bestMoveSoFar = moveList[scoreList.index(min(scoreList))]                
                
                if (makeAnotherMoveWithState.winner != -1):                                 #Todo| if we won it??? stop recursing, and return our FIRST INITAL BMSF
                    print("THIS WON IT=================================")                            #todo| maybe change this to anotherstate?
                    print("______________________________________________________________________________________________________THE ORIGINAL MOVE THAT WON"+str(originalMove))
                    bestMoveSoFar = originalMove
                break
 
            break
        
        scoreList.append(getScore(newState))                   # ... and call the evaluation function on the resulting GameState
        #returns
        
        
        if (newState.winner != -1):
            print("______________________________________________________________________________________________________THE ORIGINAL MOVE THAT WON"+str(originalMove))
            bestMoveSoFar = originalMove
            time.sleep(2)
            break  
        break
    # if state.playerToMove == 0:                                      # Finally, pick the move with the best score
    #     bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
    # else:
    #     bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score

    return bestMoveSoFar

#WORKING??????????
# Compute the next move to be played; keep updating <bestMoveSoFar> until computation finished or time limit reached
def getMove___idk(state, hWidth, hHeight, timeLimit):
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



        newState = makeMove(state, move)                       # For each move, play it on a separate board...
        resultingmovesList = getMoveOptions(newState)
        for move in resultingmovesList:
                                            #todo maybe change this to anotherstate?
            makeAnotherState =  makeMove(newState, move)   
            getMove(makeAnotherState, hWidth, hHeight, timeLimit)     
        scoreList.append(getScore(newState))                   # ... and call the evaluation function on the resulting GameState
        #returns
        
        time.sleep(50)

    if state.playerToMove == 0:                                      # Finally, pick the move with the best score
        bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
    else:
        bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score

    return bestMoveSoFar








def getBestMoveSoFar(move, state):
    return move

def getState(move, state):
    return state



def getMove(state, hWidth, hHeight, timeLimit):
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight
    keepgoing = True
    startTime = datetime.now()                                       # Remember computation start time
    print("I got the current best score with the best move:___so im gonna sort my scorelist with its corresponding move and exapnd the next most likely to win")
    print("I also need MaxSCORE, MinSCORE to return incase we or opponent win")
    moveList = getMoveOptions(state)                                 # Get the list of possible moves
    #TODO bestMoveSoFar = currentbestMove                                  # Just choose first move from the list for now, in case we run out of time 
    depthlimit = 1
    scoreList = []
    

    for move in moveList:
        scoreList.append(getScore(state))

        if len(moveList) > 0:                                                                    # all time-consuming loops in your code so that you will not exceed the time limit
            if state.playerToMove == 0:                                      # Finally, pick the move with the best score
                bestMoveSoFar = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
            else:
                bestMoveSoFar = moveList[scoreList.index(min(scoreList))]    


        projectedState = makeMove(state, move)                       
        while not timeOut(startTime, timeLimit) and keepgoing:
            depthlimit += 1

            #print("\n\nI want you to return the first move in the second iteration. So the depthlimit is "+str(depthlimit))  
            print("THE move I want next set of moves for is------------------->"+str(move)+",  with the depthlimit: "+str(depthlimit))
#TODO so I can win in 5 max depth for current, since the iterateMove did reach a win state, I should stop looping and just make the damn move
            bestMoveSoFar, winningState = iterateMove(projectedState, hWidth, hHeight, timeLimit, move, 0,  depthlimit)
            # Propstate = iterateMove(projectedState, hWidth, hHeight, timeLimit, move, 0,  depthlimit).[1]
            print("\n\n>>>>>>>><<<<<<<<<<<<><><><><I'm printing my NewState iterateMove" +str(winningState))
            time.sleep(.2)
            #todo change to  !=-1
            if winningState == 0 or projectedState.winner == 0:
                keepgoing = False
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!I PROJECTED A WIN FROM THE LAST ATTEMPTED MOVE!!!!")
                break
            
        else:
                          # Check for timeout and return current best move if time limit is reached
            return bestMoveSoFar                                     # It is not necessary for Alan_Turing, but you need to include this check in
# If we are Player 2, we look for the minimum score
        
    return bestMoveSoFar



def iterateMove(state, hWidth, hHeight, timeLimit, currentbestMove, startdepth, depthlimit):
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight
    bestMoveSoFar = currentbestMove#GivenMoveList[0] if len(GivenMoveList) > 0  else bestMoveSoFar        #todo| Just choose first move from the list for now, in case we run out of time 
    time.sleep(0.2)
    scoreList = []
    scoreList.append(getScore(state))  
    GivenMoveList = getMoveOptions(state) 
    winningState = -1
        
    
    #print("The bestMoveSofar from outside whileloop: "+str(bestMoveSoFar))
    #if state.playerToMove == 0: 
     #   print("\nSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsPurmutation of MoveList: "+str(GivenMoveList))
    #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXIT\n")

    for givenMove in GivenMoveList:
        while ((state.winner == -1) and (startdepth < depthlimit)):
            if state.playerToMove == 0:  
                startdepth += 1
                print("\n\nI can only look ahead to depth: "+str(depthlimit) +"!")
                print("I am now looking ahead to depth: "+str(startdepth))  
                print("The possible moves from this " +str(startingLocation(givenMove)) + " *lookahead* depth: "+str(GivenMoveList))
                print("The move Im lookingahead from in the *Next* depth: "+str(destination(givenMove)))                            #todo| For each move, play it on a separate board...


                if (startdepth == depthlimit):
                    print("\n\n I finally reached the current given depthlimit: "+str(depthlimit) +", Im gonna compute the score and return it with the bestmove for max___")

                #print("\n\n\nIteratedMove from while loop" + str(givenMove))

            #possibly two state, to avoid opponent???                      
            Newstate = makeMove(state, givenMove)                                    #todo| make a new state with our move from the initial moveList
            winningState = Newstate.winner


            if (winningState  == -1):
                bestMoveSoFar, winningState = iterateMove(Newstate, hWidth, hHeight, timeLimit, bestMoveSoFar, startdepth, depthlimit)  
            else:
                print("\n\n\n\n\n\n_____win\n\n\n\n\n\n")
                print("\nThe *original* move "+str(bestMoveSoFar)+" needed depth "+str(depthlimit) +" to win!\n\n\n\n\n\n")
                winningState = 0
                return bestMoveSoFar, winningState
                break
            break
        break

        if (state.winner != -1):
            print("______________________________________________________________________________________________________THE Last lookahead Move THAT WON"+str(originalMove))
            bestMoveSoFar = givenMove
            time.sleep(20)
            break  
        break
    if state.playerToMove == 0:  
        bestMoveSoFar = bestMoveSoFar                                    # Finally, pick the move with the best score
        #bestMoveSoFar = GivenMoveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
    else:
        bestMoveSoFar = bestMoveSoFar
        #bestMoveSoFar = GivenMoveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score

    return bestMoveSoFar, winningState


















def iterateMove_backup(state, hWidth, hHeight, timeLimit, currentbestMove):
    global boardWidth, boardHeight, homeWidth, homeHeight, bestMoveSoFar
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight
    scoreList = []
    scoreList.append(getScore(state))  

    OgmoveList = getMoveOptions(state)         
    bestMoveSoFar = OgmoveList[0] if len(OgmoveList) > 0  else bestMoveSoFar        #todo| Just choose first move from the list for now, in case we run out of time 

    print("The bestMoveSofar from outside whileloop: "+str(bestMoveSoFar))
    print("\nSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsPurmutation of MoveList: "+str(OgmoveList))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXIT\n")

    OgmoveList = getMoveOptions(state)         


    #maybe put inside of for
    Keepgoing = True;
    for originalMove in OgmoveList:
        while ((state.winner == -1) and (Keepgoing == True)):

            print("The last/ORIGINAL move: "+str(originalMove))                            #todo| For each move, play it on a separate board...
            print("\n\n\nIteratedMove from while loop" + str(originalMove))

            #possibly two state, to avoid opponent???                      
            Newstate = makeMove(state, originalMove)                                    #todo| make a new state with our move from the initial moveList
            if (Newstate.winner == -1):
                iterateMove(Newstate, hWidth, hHeight, timeLimit, bestMoveSoFar)  
            else:
                print("\n\n\n\n\n\n_____win\n\n\n\n\n\n")
                print("\n\n\n\n\n\nwinning_____move:"+str(originalMove)+"\n\n\n\n\n\n")
                Keepgoing = False
                time.sleep(2)
                break
            break
        break

        if (state.winner != -1):
            print("______________________________________________________________________________________________________THE Last lookahead Move THAT WON"+str(originalMove))
            bestMoveSoFar = originalMove
            time.sleep(20)
            break  
        break
    if state.playerToMove == 0:  
        #bestMoveSoFar = bestMoveSoFar                                    # Finally, pick the move with the best score
        bestMoveSoFar = OgmoveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
    else:
        #bestMoveSoFar = bestMoveSoFar
        bestMoveSoFar = OgmoveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score

    return bestMoveSoFar






