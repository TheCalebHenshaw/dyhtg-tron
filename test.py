import pygame
import sys
import subprocess
import os

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
HOVER_COLOR = (135, 206, 235)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Help Page")

# Font settings
title_font = pygame.font.Font(None, 74)
info_font = pygame.font.Font(None, 28)
button_font = pygame.font.Font(None, 36)

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

def help_page():
    clock = pygame.time.Clock()
    current_frame = 0
    last_update_time = pygame.time.get_ticks()

    help_text_lines = [
        "Welcome to the Help Page!",
        "Here are some tips on how to use the game:",
        "1. Press 'Play' to start the game.",
        "2. Player 1 uses the keys WASD and Player 2 uses the keypad to navigate.",
        "3. Avoid obstacles.",
        "4. Press 'Quit' to exit the game.",
        "",
    ]

    button_width = 150
    button_height = 50
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT - 150, button_width, button_height)

    while True:
        # Handle frame timing to update the current frame
        now = pygame.time.get_ticks()
        if now - last_update_time > frame_delay:
            current_frame = (current_frame + 1) % sprite_frame_count
            last_update_time = now

        # Draw the current frame of the sprite sheet as the background
        screen.blit(sprite_frames[current_frame], (0, 0))

        # Render the help text
        title_text = title_font.render("Help", True, RED)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        for i, line in enumerate(help_text_lines):
            info_text = info_font.render(line, True, WHITE)
            screen.blit(info_text, (SCREEN_WIDTH // 2 - info_text.get_width() // 2, 150 + i * 30))

        # Back button
        mouse_pos = pygame.mouse.get_pos()
        button_color = HOVER_COLOR if button_rect.collidepoint(mouse_pos) else LIGHT_BLUE

        pygame.draw.rect(screen, button_color, button_rect)
        back_text = button_font.render("Back", True, BLACK)
        screen.blit(back_text, (button_rect.x + (button_width - back_text.get_width()) // 2,
                                button_rect.y + (button_height - back_text.get_height()) // 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(mouse_pos):
                    pygame.quit()  # Close the current window before going back
                    subprocess.run(["python3", "home_screen.py"])  # Run home_screen.py as a new process

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    help_page()
