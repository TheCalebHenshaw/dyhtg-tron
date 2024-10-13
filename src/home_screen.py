import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)    # Button color
HOVER_COLOR = (135, 206, 235)   # Hover color for buttons
WHITE = (255, 255, 255)         # For text
NEON_CYAN = (0, 255, 255)       # Luminous color for glow

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600 

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tron - Home Screen")

# Font settings
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 28)

# Load the sprite sheet
def load_sprite_sheet(filename, frame_width, frame_height, columns, rows):
    sprite_sheet = pygame.image.load(filename).convert_alpha()
    sheet_width, sheet_height = sprite_sheet.get_size()
    
    frames = []
    for row in range(rows):
        for col in range(columns):
            x = col * frame_width
            y = row * frame_height
            frame = sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
            frames.append(frame)
    return frames

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
sprite_sheet_path = os.path.join(script_dir, 'background-ezgif.com-gif-to-sprite-converter.png')

# Frame size in the sprite sheet
frame_width = 480
frame_height = 480
columns = 5
rows = 3

# Load the frames from the sprite sheet
sprite_frames = load_sprite_sheet(sprite_sheet_path, frame_width, frame_height, columns, rows)
sprite_frame_count = len(sprite_frames)

# Set the frame delay
frame_delay = 50

# Scrolling text settings
scrolling_text = "Caleb Henshaw | Tom Blunt | Abhishek Shadakshari | Nathan Rooney | Neelan Patel"
scroll_speed = 2
text_x = -300

# Glow text rendering function
def render_glow_text_with_fade(text, font, base_color, glow_color, max_glow_size, fade_steps):
    base_text = font.render(text, True, base_color)

    glow_surface = pygame.Surface(
        (base_text.get_width() + max_glow_size * 2, base_text.get_height() + max_glow_size * 2),
        pygame.SRCALPHA
    )
    
    for step in range(fade_steps):
        glow_size = max_glow_size * (step + 1) / fade_steps
        opacity = 255 * (fade_steps - step) / fade_steps
        glow_text = font.render(text, True, glow_color)
        glow_text.set_alpha(opacity)
        glow_surface.blit(
            glow_text,
            (max_glow_size - glow_size, max_glow_size - glow_size)
        )

    glow_surface.blit(base_text, (max_glow_size, max_glow_size))
    
    return glow_surface

# Main menu function
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tron - Home Screen")
    global text_x
    clock = pygame.time.Clock()
    current_frame = 0
    last_update_time = pygame.time.get_ticks()

    while True:
        now = pygame.time.get_ticks()
        if now - last_update_time > frame_delay:
            current_frame = (current_frame + 1) % sprite_frame_count
            last_update_time = now

        screen.fill(BLACK)
        screen.blit(sprite_frames[current_frame], (0, 0))

        # Create and render the glow text
        glow_text_surface = render_glow_text_with_fade(
            "Tron",
            font,
            WHITE,
            NEON_CYAN,
            max_glow_size=10,
            fade_steps=5
        )
        screen.blit(
            glow_text_surface,
            (SCREEN_WIDTH // 2 - glow_text_surface.get_width() // 2, 100)
        )

        # Button settings
        button_width = 200
        button_height = 50
        play_button_y = 250
        help_button_y = play_button_y + button_height + 20
        quit_button_y = help_button_y + button_height + 20

        play_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2,
            play_button_y,
            button_width,
            button_height
        )
        help_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2,
            help_button_y,
            button_width,
            button_height
        )
        quit_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - button_width // 2,
            quit_button_y,
            button_width,
            button_height
        )

        mouse_pos = pygame.mouse.get_pos()
        play_button_color = HOVER_COLOR if play_button_rect.collidepoint(mouse_pos) else LIGHT_BLUE
        help_button_color = HOVER_COLOR if help_button_rect.collidepoint(mouse_pos) else LIGHT_BLUE
        quit_button_color = HOVER_COLOR if quit_button_rect.collidepoint(mouse_pos) else LIGHT_BLUE

        pygame.draw.rect(screen, play_button_color, play_button_rect)
        pygame.draw.rect(screen, help_button_color, help_button_rect)
        pygame.draw.rect(screen, quit_button_color, quit_button_rect)

        play_text = small_font.render("Play", True, BLACK)
        help_text = small_font.render("How to Play", True, BLACK)
        quit_text = small_font.render("Quit", True, BLACK)

        screen.blit(
            play_text,
            (
                play_button_rect.x + (button_width - play_text.get_width()) // 2,
                play_button_rect.y + (button_height - play_text.get_height()) // 2
            )
        )
        screen.blit(
            help_text,
            (
                help_button_rect.x + (button_width - help_text.get_width()) // 2,
                help_button_rect.y + (button_height - help_text.get_height()) // 2
            )
        )
        screen.blit(
            quit_text,
            (
                quit_button_rect.x + (button_width - quit_text.get_width()) // 2,
                quit_button_rect.y + (button_height - quit_text.get_height()) // 2
            )
        )

        # Add scrolling text at the top
        scrolling_text_surface = small_font.render(scrolling_text, True, WHITE)
        text_x += scroll_speed
        if text_x > SCREEN_WIDTH:
            text_x = -scrolling_text_surface.get_width()
        screen.blit(scrolling_text_surface, (text_x, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(mouse_pos):
                    import main
                    main.playerStart()
                elif help_button_rect.collidepoint(mouse_pos):
                    import help  # Import the help module
                    help.help_page(screen)  # Call the help_page function and pass the screen
                elif quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
