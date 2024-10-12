import pygame
from player import Player  # Assuming player.py is the file where your Player class is
import os
import home_screen  # Import home_screen to go back to it

import pygame
import os

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FRAME_WIDTH = 500  # Frame width in the sprite sheet
FRAME_HEIGHT = 500  # Frame height in the sprite sheet
FRAME_DELAY = 100  # Delay between sprite frames in milliseconds

# Load the sprite sheet image
script_dir = os.path.dirname(os.path.abspath(__file__))
sprite_sheet_path = os.path.join(script_dir, 'endgamebackground.png')

# Function to load sprite sheet and extract frames
def load_sprite_sheet(filename, frame_width, frame_height):
    sprite_sheet = pygame.image.load(filename).convert_alpha()
    sheet_width, sheet_height = sprite_sheet.get_size()

    frames = []
    columns = sheet_width // frame_width
    rows = sheet_height // frame_height

    for row in range(rows):
        for col in range(columns):
            x = col * frame_width
            y = row * frame_height
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit the screen
            frames.append(frame)

    return frames

# Load the frames from the sprite sheet
sprite_frames = load_sprite_sheet(sprite_sheet_path, FRAME_WIDTH, FRAME_HEIGHT)
sprite_frame_count = len(sprite_frames)

def display_end_screen(screen, winner_name):
    screen_width, screen_height = screen.get_size()

    # Game Over! heading settings
    font = pygame.font.Font(None, 100)
    game_over_text = font.render("Game Over!", True, (255, 0, 0))  # Red color for the heading
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, 150))

    # Winner's name settings
    winner_font = pygame.font.Font(None, 74)
    winner_text = winner_font.render(f"{winner_name} Wins", True, (255, 255, 255))
    winner_rect = winner_text.get_rect(center=(screen_width // 2, 250))

    # Button settings
    button_font = pygame.font.Font(None, 50)

    quit_text = button_font.render(" Quit Game", True, (255, 255, 255))
    play_again_text = button_font.render(" Play Again", True, (255, 255, 255))
    home_text = button_font.render("       Home", True, (255, 255, 255))

    # Centering buttons and spacing them equally
    button_width, button_height = 250, 50
    spacing = 80  # Vertical spacing between buttons

    quit_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, 400), (button_width, button_height))
    play_again_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, 400 + spacing), (button_width, button_height))
    home_button_rect = pygame.Rect((screen_width // 2 - button_width // 2, 400 + 2 * spacing), (button_width, button_height))

    # Fading effect variables
    alpha = 255
    fading_out = True  # Start with fading out

    # Sprite animation variables
    current_frame = 0
    last_update_time = pygame.time.get_ticks()

    pygame.display.flip()

    waiting = True
    clock = pygame.time.Clock()

    while waiting:
        screen.fill((0, 0, 0))  # Black background

        # Handle frame timing to update the current frame
        now = pygame.time.get_ticks()
        if now - last_update_time > FRAME_DELAY:
            current_frame = (current_frame + 1) % sprite_frame_count
            last_update_time = now

        # Draw the current frame of the sprite sheet as the background
        screen.blit(sprite_frames[current_frame], (0, 0))

        # Handle fading effect for Game Over text
        game_over_text.set_alpha(alpha)
        screen.blit(game_over_text, game_over_rect)

        # Fade in/out logic
        if fading_out:
            alpha -= 5
            if alpha <= 50:
                fading_out = False
        else:
            alpha += 5
            if alpha >= 255:
                fading_out = True

        # Draw winner name
        screen.blit(winner_text, winner_rect)

        # Draw buttons
        pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)
        screen.blit(quit_text, (quit_button_rect.x + 25, quit_button_rect.y + 10))

        pygame.draw.rect(screen, (0, 255, 0), play_again_button_rect)
        screen.blit(play_again_text, (play_again_button_rect.x + 25, play_again_button_rect.y + 10))

        pygame.draw.rect(screen, (0, 0, 255), home_button_rect)
        screen.blit(home_text, (home_button_rect.x + 15, home_button_rect.y + 10))

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()
                elif play_again_button_rect.collidepoint(event.pos):
                    waiting = False  # Exit the waiting loop to restart the game
                elif home_button_rect.collidepoint(event.pos):
                    waiting = False
                    home_screen.main_menu()  # Call home_screen.py to return to the home screen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to play again
                    waiting = False

        clock.tick(30)  # Control the frame rate


def main(player_data):
    # Game loop that allows replay
    while True:
        # Initialize Pygame
        pygame.init()

        # Initialize sound system
        pygame.mixer.init()

        audio_file = os.path.join("media", "Audio", "DaftPunkEndOfLine.mp3")

        # Load the background music 
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play(-1)

        # Set up the screen
        screen_width = 1200
        screen_height = 900
        x_border = 150
        y_border = 0
        close_in = 1
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Player Test")

        # Define controls for the player
        player1_controls = {
            'up': pygame.K_w,
            'down': pygame.K_s,
            'left': pygame.K_a,
            'right': pygame.K_d
        }
        player2_controls = {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT
        }
        [(player1_color, player1_name), (player2_color, player2_name)] = player_data
        
        # Create Player instances
        player1 = Player(250, 50, player1_color, player1_controls, player1_name, 'media/Sprites/spaceships/PNG/Spaceships/ship/')
        player2 = Player(650, 50, player2_color, player2_controls, player2_name, 'media/Sprites/spaceships/PNG/Spaceships/ship/')

        # Define some colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        NAVY = (0, 0, 96)

        # Set up the game clock
        clock = pygame.time.Clock()
        TIMER_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMER_EVENT, (3000 // 30))

        # Main game loop for testing
        running = True
        while running:
            screen.fill(BLACK)  # Clear screen with black
            blockSize = 30  # Set the size of the grid block
            for x in range(x_border, screen_width-x_border, blockSize):
                for y in range(y_border, screen_height-y_border, blockSize):
                    rect = pygame.Rect(x, y, blockSize, blockSize)
                    pygame.draw.rect(screen, NAVY, rect, 2)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == TIMER_EVENT:
                    x_border += close_in
                    y_border += close_in
                    player1.x_collision += close_in
                    player1.y_collision += close_in
                    player2.x_collision += close_in
                    player2.y_collision += close_in

            # Get pressed keys
            keys = pygame.key.get_pressed()

            # Handle controls and movement
            player1.handle_controls(keys)
            player1.move()
            player2.handle_controls(keys)
            player2.move()

            # Check for collisions with the screen edges
            player1.checkForCollision(screen_width, screen_height, player2.trail)
            player2.checkForCollision(screen_width, screen_height, player1.trail)

            # Draw the player and its trail
            player1.draw(screen)
            player2.draw(screen)

            # If the player dies (collision), display end screen
            if not player1.alive:
                display_end_screen(screen, player2.name)
                running = False
            if not player2.alive:
                display_end_screen(screen, player1.name)
                running = False

            # Update the screen
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(60)  # Adjust frame rate as needed

if __name__ == "__main__":
    # Example player data passed to main
    player_data = [(pygame.Color('red'), 'Player 1'), (pygame.Color('blue'), 'Player 2')]
    main(player_data)
