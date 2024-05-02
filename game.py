import pygame
import sys
import asyncio
from nillion_game_client import determine_game_result

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Rock Paper Scissors Game')

# Load and resize images
def load_and_resize(image_path, new_width, new_height):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (new_width, new_height))

rock_img = load_and_resize('rock.png', 200, 200)
paper_img = load_and_resize('paper.png', 200, 200)
scissors_img = load_and_resize('scissors.png', 200, 200)

# Define colors and font
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)

# Choices dictionary
choices = {
    'rock': rock_img,
    'paper': paper_img,
    'scissors': scissors_img
}

# Game state variables
player_choice = None
computer_choice = None
result = ''
show_play_again = False
loading = False

# Function to reset game
def reset_game():
    global player_choice, computer_choice, result, show_play_again, loading
    player_choice = None
    computer_choice = None
    result = ''
    show_play_again = False
    loading = False

# Callback function to handle results
def handle_result(com_choice, res):
    global computer_choice, result, show_play_again, loading
    computer_choice = com_choice
    loading = False
    result = res
    show_play_again = True
    print('showing play again')

# Function to handle completion of loading
def loading_complete():
    global loading
    loading = False

reset_game()
# Main game loop
async def main_game_loop(handle_result):
    global player_choice, computer_choice, result, show_play_again, loading

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if not player_choice and not show_play_again:
                    if event.key == pygame.K_r:
                        player_choice = 'rock'
                    elif event.key == pygame.K_p:
                        player_choice = 'paper'
                    elif event.key == pygame.K_s:
                        player_choice = 'scissors'

                    # Call game logic with callback
                    loading = True
                    asyncio.create_task(determine_game_result(player_choice, handle_result))
                    
                elif show_play_again:
                    if event.key == pygame.K_y:
                        reset_game()
                    elif event.key == pygame.K_n:
                        pygame.quit()
                        sys.exit()

        screen.fill(WHITE)

        if loading:
            loading_text = font.render(f"You picked {player_choice}! Nillion is computing the result...", True, BLACK)
            screen.blit(loading_text, (width // 2 - 300, height // 2))

        elif player_choice and computer_choice:
            screen.blit(choices[computer_choice], (width // 4 - 50, height // 2 - 100))
            screen.blit(choices[player_choice], (3 * width // 4 - 50, height // 2 - 100))
            text_result = font.render(result, True, BLACK)
            screen.blit(text_result, (width // 2 - 50, 50))

        instructions = "Press R for Rock, P for Paper, S for Scissors"
        screen.blit(font.render(instructions, True, BLACK), (50, 10))

        if show_play_again:
            play_again_text = "Play again? Press Y to continue or N to quit."
            screen.blit(font.render(play_again_text, True, BLACK), (50, 420))

        pygame.display.flip()
        await asyncio.sleep(0.02)  # Control the frame rate

# Run the main game loop
asyncio.run(main_game_loop(handle_result))