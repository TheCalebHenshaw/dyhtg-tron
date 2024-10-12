import pygame
from player import Player  # Assuming player.py is the file where your Player class is
import os
import home_screen  # Import home_screen to go back to it

def display_end_screen(screen, winner_name):
    screen.fill((0, 0, 0))  # Black background
    font = pygame.font.Font(None, 74)
    text = font.render(f"Game Over! {winner_name} Wins", True, (255, 255, 255))
    screen.blit(text, (100, 200))

    # "Quit Game" button settings
    button_font = pygame.font.Font(None, 50)
    quit_text = button_font.render("Quit Game", True, (255, 255, 255))
    quit_button_rect = pygame.Rect(100, 400, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), quit_button_rect)
    screen.blit(quit_text, (quit_button_rect.x + 25, quit_button_rect.y + 10))

    # "Play Again" button settings
    play_again_text = button_font.render("Play Again", True, (255, 255, 255))
    play_again_button_rect = pygame.Rect(350, 400, 200, 50)
    pygame.draw.rect(screen, (0, 255, 0), play_again_button_rect)
    screen.blit(play_again_text, (play_again_button_rect.x + 25, play_again_button_rect.y + 10))

    # "Go Back to Home" button settings
    home_text = button_font.render("Go Back to Home", True, (255, 255, 255))
    home_button_rect = pygame.Rect(600, 400, 250, 50)
    pygame.draw.rect(screen, (0, 0, 255), home_button_rect)
    screen.blit(home_text, (home_button_rect.x + 15, home_button_rect.y + 10))

    pygame.display.flip()

    waiting = True
    while waiting:
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

def main(player_data):
    # Game loop that allows replay
    while True:
        # Initialize Pygame
        pygame.init()

        # Initialize sound system
        pygame.mixer.init()

        audio_file = os.path.join("media", "Audio", "DaftPunkEndOfLine.mp3")

        # Load the background music 
        backgroundMusic = pygame.mixer.Sound(audio_file)
        backgroundMusic.play(-1)
        backgroundMusic.set_volume(0.5)

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
        
        bikeAudio = os.path.join("media", "Audio", "TronCycleNoise.wav")
        bikeSound = pygame.mixer.Sound(bikeAudio)
        bikeSound.play()
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
            explosionAudio = os.path.join("media", "Audio", "Explosion.wav")
            explosionSound = pygame.mixer.Sound(explosionAudio)

            # If the player dies (collision), display end screen
            if not player1.alive:
                backgroundMusic.stop()
                bikeSound.stop()
                explosionSound.play()
                display_end_screen(screen, player2.name)
                running = False
            if not player2.alive:
                backgroundMusic.stop()
                bikeSound.stop()
                explosionSound.play()
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
