# Player Cookie_Monster

import random as rnd
import numpy as np

class GameState(object):
    __slots__ = ['board', 'playerToMove', 'winner']

# Global variables
boardWidth = 0
boardHeight = 0
homeWidth = 0
homeHeight = 0

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
# Note that Cookie_Monster likes random choices
def getScore(state):
    return rnd.random()

# Compute the next move to be played
def getMove(state, hWidth, hHeight, timeLimit):
    # Set global variables
    global boardWidth, boardHeight, homeWidth, homeHeight
    boardWidth = state.board.shape[0]
    boardHeight = state.board.shape[1]
    homeWidth = hWidth
    homeHeight = hHeight

    moveList = getMoveOptions(state)                            # Get the list of possible moves
    scoreList = []
    for move in moveList:
        projectedState = makeMove(state, move)                  # For each move, play it on a separate board...
        scoreList.append(getScore(projectedState))              # ... and call the evaluation function on the resulting GameState
    
    if state.playerToMove == 0:                                 # Finally, pick the move with the best score
        bestMove = moveList[scoreList.index(max(scoreList))]    # If we are Player 1, we look for the maximum score
    else:
        bestMove = moveList[scoreList.index(min(scoreList))]    # If we are Player 2, we look for the minimum score
    
    return bestMove


