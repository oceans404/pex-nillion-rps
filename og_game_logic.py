import random
import threading
import time

def determine_game_result(player_choice, callback):
    def game_logic():
        # Simulate network delay or heavy computation
        time.sleep(5)  # Delay for 2 seconds
        computer_choice = random.choice(['rock', 'paper', 'scissors'])

        # Determine result
        if player_choice == computer_choice:
            result = 'Tie'
        elif (player_choice == 'rock' and computer_choice == 'scissors') \
            or (player_choice == 'paper' and computer_choice == 'rock') \
            or (player_choice == 'scissors' and computer_choice == 'paper'):
            result = 'Player Wins!'
        else:
            result = 'Computer Wins!'

        # Callback with results
        callback(computer_choice, result)

    # Start the thread
    thread = threading.Thread(target=game_logic)
    thread.start()
