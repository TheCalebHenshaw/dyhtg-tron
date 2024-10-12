import pygame
import sys
import os

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
HOVER_COLOR = (135, 206, 235)
RED = (255, 0, 0)
KEY_COLOR = (50, 50, 50)  # Key box color
KEY_BORDER_COLOR = WHITE  # Key border color

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Font settings
title_font = pygame.font.Font(None, 74)
info_font = pygame.font.Font(None, 28)
control_font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 36)
text_box_font = pygame.font.Font(None, 24)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the new sprite sheet image
sprite_sheet_path = os.path.join(script_dir, 'ezgif.com-gif-to-sprite-converter.png')

# Frame size in the sprite sheet (5 columns, 10 rows)
frame_width = 500  # (2500px width / 5 columns)
frame_height = 500  # (5000px height / 10 rows)

# Load the sprite sheet
def load_sprite_sheet(filename, frame_width, frame_height):
    sprite_sheet = pygame.image.load(filename).convert_alpha()
    sheet_width, sheet_height = sprite_sheet.get_size()

    frames = []

    # Assuming 5 columns and 10 rows of frames
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

# Load the frames from the new sprite sheet
sprite_frames = load_sprite_sheet(sprite_sheet_path, frame_width, frame_height)
sprite_frame_count = len(sprite_frames)

# Set the frame delay (in milliseconds)
frame_delay = 100  # You can adjust this value to control the speed of the animation

def draw_boxed_key(screen, text, x, y, width=50, height=50):
    """ Draw a single key in a box at (x, y) """
    key_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, KEY_COLOR, key_rect)  # Draw the key box
    pygame.draw.rect(screen, KEY_BORDER_COLOR, key_rect, 2)  # Draw the border
    key_text = control_font.render(text, True, WHITE)
    screen.blit(key_text, (x + (width - key_text.get_width()) // 2, y + (height - key_text.get_height()) // 2))

def draw_controls(screen):
    # Player 1 (left side)
    player1_title = title_font.render("Player 1", True, RED)
    screen.blit(player1_title, (50, 100))

    # Draw the WASD controls in individual boxes
    draw_boxed_key(screen, "W", 100, 200)
    draw_boxed_key(screen, "A", 50, 260)
    draw_boxed_key(screen, "S", 100, 260)
    draw_boxed_key(screen, "D", 150, 260)

    # Add text box below Player 1
    player1_text = "Player 1 uses the W A S D keys to navigate."
    player1_text_surface = text_box_font.render(player1_text, True, WHITE)
    screen.blit(player1_text_surface, (50, 350))

    # Player 2 (right side)
    player2_title = title_font.render("Player 2", True, RED)
    screen.blit(player2_title, (SCREEN_WIDTH - 250, 100))

    # Draw the arrow keys in individual boxes
    draw_boxed_key(screen, "↑", SCREEN_WIDTH - 175, 200)
    draw_boxed_key(screen, "←", SCREEN_WIDTH - 225, 260)
    draw_boxed_key(screen, "↓", SCREEN_WIDTH - 175, 260)
    draw_boxed_key(screen, "→", SCREEN_WIDTH - 125, 260)

    # Add text box below Player 2
    player2_text = "Player 2 uses the keypad arrows to navigate."
    player2_text_surface = text_box_font.render(player2_text, True, WHITE)
    screen.blit(player2_text_surface, (SCREEN_WIDTH - 350, 350))

def help_page(screen):
    clock = pygame.time.Clock()
    current_frame = 0
    last_update_time = pygame.time.get_ticks()

    button_width = 150
    button_height = 50
    button_rect = pygame.Rect(
        SCREEN_WIDTH // 2 - button_width // 2,
        SCREEN_HEIGHT - 150,
        button_width,
        button_height
    )

    while True:
        # Handle frame timing to update the current frame
        now = pygame.time.get_ticks()
        if now - last_update_time > frame_delay:
            current_frame = (current_frame + 1) % sprite_frame_count
            last_update_time = now

        # Draw the current frame of the sprite sheet as the background
        screen.blit(sprite_frames[current_frame], (0, 0))

        # Draw the "How to Play" heading
        title_text = title_font.render("How to Play", True, WHITE)
        screen.blit(
            title_text,
            (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10)
        )

        # Draw the player controls and text boxes
        draw_controls(screen)

        # Back button
        mouse_pos = pygame.mouse.get_pos()
        button_color = HOVER_COLOR if button_rect.collidepoint(mouse_pos) else LIGHT_BLUE

        pygame.draw.rect(screen, button_color, button_rect)
        back_text = button_font.render("Back", True, BLACK)
        screen.blit(
            back_text,
            (
                button_rect.x + (button_width - back_text.get_width()) // 2,
                button_rect.y + (button_height - back_text.get_height()) // 2
            )
        )

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(mouse_pos):
                    return  # Simply exit the help_page function to return control to home_screen.py

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    # If help.py is run directly, initialize Pygame and create the screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("How to Play Page")
    help_page(screen)