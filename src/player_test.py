import pygame
from player import Player  # Assuming player.py is the file where your Player class is

# Initialize Pygame
pygame.init()

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
    'up' : pygame.K_UP,
    'down' : pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT

}

# Create a Player instance
player1 = Player(250, 50, (0, 255, 0), player1_controls, 'Player1', None)
player2 = Player(650,50,(255,127,80),player2_controls, 'Player2', None)

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
