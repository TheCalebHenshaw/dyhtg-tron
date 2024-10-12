import pygame
from player import Player  # Assuming player.py is the file where your Player class is

# Initialize Pygame
pygame.init()
#Initialize sound system
pygame.mixer.init()

#Load the background music 
pygame.mixer.music.load("media\Audio\DaftPunkEndOfLine.mp3")
pygame.mixer.music.play(-1)

# Set up the screen
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Player Test")

# Define controls for the playerd
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
RED = (255, 0, 0)
GRAY = (200, 200, 200)
HIGHLIGHT_COLOR = (255, 255, 0)

# Set up the game clock
clock = pygame.time.Clock()

def display_game_over(winner):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 50)
    game_over_text = font.render(f"Game Over! {winner} Wins!", True, RED)
    play_again_text = small_font.render("Play Again", True, WHITE)
    quit_text = small_font.render("Quit", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    quit_rect = quit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 200))
    running = True
    while running:
        screen.fill(BLACK)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 100))
        mouse_pos = pygame.mouse.get_pos()
        if play_again_rect.collidepoint(mouse_pos):
            play_again_text = small_font.render("Play Again", True, HIGHLIGHT_COLOR)  # Highlight
        else:
            play_again_text = small_font.render("Play Again", True, WHITE)

        if quit_rect.collidepoint(mouse_pos):
            quit_text = small_font.render("Quit", True, HIGHLIGHT_COLOR)  # Highlight
        else:
            quit_text = small_font.render("Quit", True, WHITE)

        screen.blit(play_again_text, play_again_rect)
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()



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
        display_game_over(player1.name)
        running = False
    if not player2.alive:
        print(f"{player2.name} collided")
        display_game_over(player2.name)
        running = False
    # Update the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)  # Adjust frame rate as needed

# Quit Pygame
pygame.quit()
