import pygame
from player import Player  # Assuming player.py is the file where your Player class is

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1200
screen_height = 900
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
    'up' : pygame.K_UP,
    'down' : pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT

}

# Create a Player instance
player1 = Player(100, 50, (0, 255, 0), player1_controls, 'Player1', None)
player2 = Player(500,50,(255,127,80),player2_controls, 'Player2', None)

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the game clock
clock = pygame.time.Clock()

# Main game loop for testing
running = True
while running:
    screen.fill(BLACK)  # Clear screen with black

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Handle controls and movement
    player1.handle_controls(keys)
    player1.move()


    player2.handle_controls(keys)
    player2.move()

    # Check for collisions with the screen edges
    player1.checkForCollision(screen_width, screen_height,player2.trail)
    player2.checkForCollision(screen_width,screen_height,player1.trail)

    # Draw the player and its trail
    player1.draw(screen)
    player2.draw(screen)

    # If the player dies (collision), print a message
    if not player1.alive:
        print(f"{player1.name} collided!")
        running = False
    if not player2.alive:
        print(f"{player2.name} collided")
        running = False
    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)  # Adjust frame rate as needed

# Quit Pygame
pygame.quit()
