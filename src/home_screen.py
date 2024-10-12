import pygame
import sys

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HOVER_COLOR = (170, 170, 170)  # A lighter gray for hover effect

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tron - Home Screen")

# Font settings
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

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

        # Button dimensions
        button_width = 200
        button_height = 50
        button_spacing = 20

        # Number of buttons
        N = 3

        # Calculate total height required for buttons and spacing
        total_buttons_height = N * button_height + (N - 1) * button_spacing

        # Compute top margin to center the buttons
        top_margin = (SCREEN_HEIGHT - total_buttons_height) // 2

        # Y positions of buttons
        play_button_y = top_margin
        help_button_y = top_margin + button_height + button_spacing
        quit_button_y = top_margin + 2 * (button_height + button_spacing)

        # Create button rectangles
        play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                                       play_button_y,
                                       button_width, button_height)
        help_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                                       help_button_y,
                                       button_width, button_height)
        quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2,
                                       quit_button_y,
                                       button_width, button_height)

        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Determine button colors based on hover
        if play_button_rect.collidepoint(mouse_pos):
            play_button_color = HOVER_COLOR
        else:
            play_button_color = GRAY

        if help_button_rect.collidepoint(mouse_pos):
            help_button_color = HOVER_COLOR
        else:
            help_button_color = GRAY

        if quit_button_rect.collidepoint(mouse_pos):
            quit_button_color = HOVER_COLOR
        else:
            quit_button_color = GRAY

        # Draw buttons with the appropriate color
        pygame.draw.rect(screen, play_button_color, play_button_rect)
        pygame.draw.rect(screen, help_button_color, help_button_rect)
        pygame.draw.rect(screen, quit_button_color, quit_button_rect)

        # Button text (centered within the buttons)
        play_text = small_font.render("Play", True, BLACK)
        help_text = small_font.render("Help", True, BLACK)
        quit_text = small_font.render("Quit", True, BLACK)

        screen.blit(play_text, (play_button_rect.x + (button_width - play_text.get_width()) // 2,
                                play_button_rect.y + (button_height - play_text.get_height()) // 2))
        screen.blit(help_text, (help_button_rect.x + (button_width - help_text.get_width()) // 2,
                                help_button_rect.y + (button_height - help_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button_rect.x + (button_width - quit_text.get_width()) // 2,
                                quit_button_rect.y + (button_height - quit_text.get_height()) // 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(mouse_pos):
                    print("Start Game!")
                    game_loop()
                if help_button_rect.collidepoint(mouse_pos):
                    print("Show Help!")
                if quit_button_rect.collidepoint(mouse_pos):
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
