import pygame
from player import Player  # Assuming player.py is the file where your Player class is
import os

def main(player_data):
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
    # Create a Player instance
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

        # If the player dies (collision), print a message
        if not player1.alive:
            print(f"{player1.name} collided!")
            pygame.init()
            running = False
        if not player2.alive:
            print(f"{player2.name} collided!")
            pygame.init()
            running = False

        # Update the screen
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)  # Adjust frame rate as needed


if __name__ == "__main__":
    main()


