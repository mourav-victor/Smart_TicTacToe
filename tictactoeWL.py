## Development and study of a Tic Tac Toe IA 

#######################################################################
## There will be trheeo IA-based programs to play it:                ##
##  i - Pontuation based of the number of winner positions           ##
##  ii - Pontuation based on a weight of winner and loser positions  ##
##  iii - Pontuation based on a history score of positions           ##
#######################################################################

import random # randrange and choice modules
import numpy as np

print("\n\nWelcome to Tic Tac Toe bot, lets go!")


def convertVector(board_vector):
    X_and_O_vector = []
    for i in range(len(board_vector)):
        if board_vector[i] == 0:
            X_and_O_vector.append(" ")
        elif board_vector[i] == -1:
            X_and_O_vector.append("X")
        elif board_vector[i] == 1:
            X_and_O_vector.append("O")
        
    return X_and_O_vector


def printBoard(board_vector):
    board_symbols = convertVector(board_vector)
    print(f"_{board_symbols[0]}_|_{board_symbols[1]}_|_{board_symbols[2]}_")
    print(f"_{board_symbols[3]}_|_{board_symbols[4]}_|_{board_symbols[5]}_")
    print(f" {board_symbols[6]} | {board_symbols[7]} | {board_symbols[8]} \n")


def checkWinner(board_vector):
    for k in range(3):
        if(board_vector[k]+board_vector[k+3]+board_vector[k+6] == 3):
            return 1 
        if(board_vector[3*k]+board_vector[3*k+1]+board_vector[3*k+2] == 3):
            return 1 
        if(board_vector[k]+board_vector[k+3]+board_vector[k+6] == -3):
            return -1
        if(board_vector[3*k]+board_vector[3*k+1]+board_vector[3*k+2] == -3):
            return -1
        
    if(board_vector[0]+board_vector[4]+board_vector[8] == 3):
        return 1
    if(board_vector[2]+board_vector[4]+board_vector[6] == 3):
        return 1
    if(board_vector[0]+board_vector[4]+board_vector[8] == -3):
        return -1
    if(board_vector[2]+board_vector[4]+board_vector[6] == -3):
        return -1   

    return 0
    

def runRandomMatch():
    players_sequence = [1, -1, 1, -1, 1, -1, 1, -1, 1]
    available_positions = list(range(0,9))
    board = [0] * 9

    for i in range(9):
        board_pos = random.choice(available_positions)
        board[board_pos] = players_sequence[i]
        #printBoard(board)
        available_positions.remove(board_pos)
        if(checkWinner(board)): 
            winner = checkWinner(board)
            if winner == 1:
                if board not in winner_positions: winner_positions.append(board)
            elif winner == -1:
                if board not in losers_positions: losers_positions.append(board)
            break
    
    #print(board)
    #print(f"{checkWinner(board)} wins")
    #print("end of match")


def trainBot(nb_of_matches):
    print("starting training ... please wait")
    for i in range(nb_of_matches):
        runRandomMatch()
    print("sucessful trained")
    print(f"final positions: {len(winner_positions) + len(losers_positions)}")
    #print(winner_positions)
    print(f"-- number of winners positions = {len(winner_positions)}")
    print(f"-- number of losers positions = {len(losers_positions)}")


def filterMatches(actual_board, future_board):
    count = 0
    for game in future_board:
        point = 1
        for i in range(len(actual_board)):
            if actual_board[i] != game[i] and actual_board[i] != 0:
                point = 0
                break
        count += point

    return count


def bestPosition(board, winner_positions):
    max_score = -1000000
    idx = 0

    for position in range(len(board)):
        if board[position] != 0:
            continue

        future_board = list.copy(board)
        future_board[position] = 1
        #print(future_board)
        nb_of_win_posi = filterMatches(future_board, winner_positions)
        nb_of_los_posi = filterMatches(future_board, losers_positions)
        score = np.dot(weight,[nb_of_win_posi, nb_of_los_posi])
        #print(f'score = {nb_of_win_posi}*{weight[0]} + {nb_of_los_posi}*{weight[1]} ')
        #print(f'position {position} has score of {score}')
        print()
        if score > max_score:
            max_score = score
            idx = position

    return idx


def playGame(mode):
    if mode == "player_vs_bot":
        print()
        print("you are starting a new game")
        print("to be fair, we will let the bot starts ;)")

        turn = 0
        board = [0,0,0,0,0,0,0,0,0]
        printBoard(board)
        
        while not (checkWinner(board) or turn==9):
            if turn % 2 == 0: 
                print(f"Bot turn")
                position = bestPosition(board, winner_positions)
                board[position] = 1

            else:
                print(f"Your turn")
                print(f"Where do you choose?")
                position = input()
                board[int(position)] = -1
            
            printBoard(board)
            turn += 1

        if checkWinner(board) == 1:
            print("BOT won")
        elif checkWinner(board) == -1:
            print("YOU won")
        else:
            print("tie :(")

        return checkWinner(board)

    if mode == "bot_vs_bot":
        players_sequence = [1, -1, 1, -1, 1, -1, 1, -1, 1]
        available_positions = list(range(0,9))
        board = [0] * 9

        for i in range(9):
            if i % 2 == 0:
                board_pos = bestPosition(board, winner_positions)
            else:
                board_pos = random.choice(available_positions)
            
            board[board_pos] = players_sequence[i]
            printBoard(board)
            available_positions.remove(board_pos)
            if(checkWinner(board)): 
                winner = checkWinner(board)
                if winner == 1:
                    if board not in winner_positions: winner_positions.append(board)
                elif winner == -1:
                    if board not in losers_positions: losers_positions.append(board)
                break
            print('press any key to continue')
            input()
        return checkWinner(board)


def findBestWeight():
    max_result = -100000
    max_idx = 0
    for i in range(20):
        weight = [1 - i*0.05, i*0.05]
        # weight (0.95, 0.05) has score of 150
        # weight (0.75, 0.25) has score of 132
        # weight (0.45, 0.55) has score of 134
        final_result = 0
        for j in range(200):
            final_result += playGame(mode = "bot_vs_bot")
        
        if final_result > max_result:
            max_result = final_result
            max_idx = i

        print(f"weight {round(weight[0],2), round(weight[1],2)} has score of {final_result}")

    return ([1 - max_idx*0.05, max_idx*0.05])



winner_positions = []
losers_positions = []
weight = [0.5, -0.5]
trainBot(100000)

while True:
    print('What do you want?')
    print('1 - Start game player vs bot')
    print('2 - Start game bot vs bot')
    print('3 - Exit program')
    choice = input()

    if choice == '1':
        playGame(mode = "player_vs_bot")
    elif choice == '2':
        playGame(mode = "bot_vs_bot")
    elif choice == '3':
        break
    else:
        print('couldnt find you command, please try again')
    
    #findBestWeight()
    #playGame(mode = "player_vs_bot")
    #input()
