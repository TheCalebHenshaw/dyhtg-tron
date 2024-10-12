import pygame
import sys

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tron - Home Screen")

# Font settings
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Create buttons for the menu
def create_button(text, font, color, rect):
    button_text = font.render(text, True, color)
    screen.blit(button_text, rect)

# Check if a point is within a rectangle (for button clicks)
def is_mouse_over(rect):
    mouse_pos = pygame.mouse.get_pos()
    return rect.collidepoint(mouse_pos)

# Main menu function
def main_menu():
    while True:
        screen.fill(WHITE)

        # Title Text
        title_text = font.render("Tron", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Button Rectangles (centered horizontally and stacked vertically)
        button_width = 200
        button_height = 50
        button_spacing = 20
        
        # Button positions
        play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - 1.5 * button_height - button_spacing, button_width, button_height)
        help_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - 0.5 * button_height, button_width, button_height)
        quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 1.5 * button_height + button_spacing, button_width, button_height)

        # Draw buttons
        pygame.draw.rect(screen, GRAY, play_button_rect)
        pygame.draw.rect(screen, GRAY, help_button_rect)
        pygame.draw.rect(screen, GRAY, quit_button_rect)

        # Button text
        create_button("Play", small_font, BLACK, play_button_rect.move(50, 10))
        create_button("Help", small_font, BLACK, help_button_rect.move(50, 10))
        create_button("Quit", small_font, BLACK, quit_button_rect.move(50, 10))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_mouse_over(play_button_rect):
                    # Transition to the game
                    print("Start Game!")
                    game_loop()
                if is_mouse_over(help_button_rect):
                    # Show help screen (placeholder)
                    print("Show Help!")
                if is_mouse_over(quit_button_rect):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Example of a simple game loop (just for demonstration purposes)
def game_loop():
    running = True
    while running:
        screen.fill((0, 100, 255))  # Game background color

        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()
    sys.exit()

# Start the home screen
if __name__ == "__main__":
    main_menu()
