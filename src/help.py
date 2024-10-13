import pygame
import sys
import os

pygame.init()

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
    """ Draw a single key in a box at (x, y). Special case for arrow keys, drawing them graphically. """
    key_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, KEY_COLOR, key_rect)  # Draw the key box
    pygame.draw.rect(screen, KEY_BORDER_COLOR, key_rect, 2)  # Draw the border

    if text == "up":
        # Draw an upward triangle (up arrow)
        pygame.draw.polygon(screen, WHITE, [(x + width // 2, y + 10), (x + 10, y + height - 10), (x + width - 10, y + height - 10)])
    elif text == "left":
        # Draw a leftward triangle (left arrow)
        pygame.draw.polygon(screen, WHITE, [(x + 10, y + height // 2), (x + width - 10, y + 10), (x + width - 10, y + height - 10)])
    elif text == "down":
        # Draw a downward triangle (down arrow)
        pygame.draw.polygon(screen, WHITE, [(x + width // 2, y + height - 10), (x + 10, y + 10), (x + width - 10, y + 10)])
    elif text == "right":
        # Draw a rightward triangle (right arrow)
        pygame.draw.polygon(screen, WHITE, [(x + width - 10, y + height // 2), (x + 10, y + 10), (x + 10, y + height - 10)])
    else:
        # Render text for non-arrow keys
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

    # Split Player 1 text into two lines
    player1_text_line1 = "Player 1 uses the W A S D"
    player1_text_line2 = "keys to navigate."
    
    # Render and display both lines of text for Player 1
    player1_text_surface_line1 = text_box_font.render(player1_text_line1, True, WHITE)
    player1_text_surface_line2 = text_box_font.render(player1_text_line2, True, WHITE)

    screen.blit(player1_text_surface_line1, (50, 350))
    screen.blit(player1_text_surface_line2, (50, 380))  # Adjust Y-position for the second line

    # Player 2 (right side)
    player2_title = title_font.render("Player 2", True, RED)
    screen.blit(player2_title, (SCREEN_WIDTH - 250, 100))

    # Draw the arrow keys using the graphical arrows
    draw_boxed_key(screen, "up", SCREEN_WIDTH - 175, 200)    # Up arrow
    draw_boxed_key(screen, "left", SCREEN_WIDTH - 225, 260)  # Left arrow
    draw_boxed_key(screen, "down", SCREEN_WIDTH - 175, 260)  # Down arrow
    draw_boxed_key(screen, "right", SCREEN_WIDTH - 125, 260) # Right arrow

    # Split Player 2 text into two lines
    player2_text_line1 = "Player 2 uses the keypad"
    player2_text_line2 = "arrows to navigate."

    # Render and display both lines of text for Player 2
    player2_text_surface_line1 = text_box_font.render(player2_text_line1, True, WHITE)
    player2_text_surface_line2 = text_box_font.render(player2_text_line2, True, WHITE)

    # Calculate the right-aligned x position
    right_align_x1 = SCREEN_WIDTH - 50 - player2_text_surface_line1.get_width()
    right_align_x2 = SCREEN_WIDTH - 96 - player2_text_surface_line2.get_width()

     # Display the Player 2 text lines right-aligned
    screen.blit(player2_text_surface_line1, (right_align_x1, 350))
    screen.blit(player2_text_surface_line2, (right_align_x2, 380))  # Adjust Y-position for the second line


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

        # Create the "How to Play" text
        title_text = title_font.render("How to Play", True, WHITE)
        text_width, text_height = title_text.get_size()
        text_position = (SCREEN_WIDTH // 2 - text_width // 2, 10)

        # Underglow effect: Draw slightly larger blurred text under the main text
        glow_color = (100, 150, 255)  # Soft blue color for the glow
        glow_text = title_font.render("How to Play", True, glow_color)

        # Position the glow text slightly lower and larger
        for offset in range(1, 5):  # Creates multiple layers of the glow for a blur effect
            screen.blit(glow_text, (text_position[0], text_position[1] + offset))

        # Draw the actual "How to Play" text on top
        screen.blit(title_text, text_position)

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
