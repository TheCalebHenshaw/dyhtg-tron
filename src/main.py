from player import Player
import pygame
import sys
import random
import math
import os

pygame.init()

width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Player Setup')

NEON_COLORS = {
    "Neon Red": (255, 0, 0),          # Bright red
    "Neon Green": (0, 255, 0),        # Bright green
    "Neon Blue": (0, 0, 255),         # Bright blue
    "Neon Yellow": (255, 255, 0),     # Bright yellow
    "Neon Magenta": (255, 0, 255),    # Bright magenta
    "Neon Cyan": (0, 255, 255),       # Bright cyan
    "Neon Orange": (255, 165, 0),     # Bright orange
    "Neon Pink": (255, 20, 147),      # Bright pink
    "Neon Purple": (128, 0, 128),     # Bright purple
    "Neon Lime": (50, 255, 0),        # Bright lime green
    "Neon Turquoise": (0, 200, 255),  # Bright turquoise
    "Neon Gold": (255, 215, 0),       # Bright gold
    "Neon Teal": (0, 128, 128),       # Bright teal
    "Neon Violet": (238, 130, 238),   # Bright violet
    "Neon Peach": (255, 218, 185),    # Bright peach
    "Neon Coral": (255, 127, 80),     # Bright coral
    "Neon Lavender": (230, 230, 250),  # Bright lavender
    "Neon Sea Green": (46, 139, 87),  # Bright sea green
    "Neon Hot Pink": (255, 105, 180),  # Bright hot pink
    "Neon Sky Blue": (135, 206, 235),  # Bright sky blue
    "Neon Chartreuse": (127, 255, 0),  # Bright chartreuse
}

# Convert NEON_COLORS dictionary to a list of color values
colors = list(NEON_COLORS.values())

font_path = os.path.join('Venora-G36PO.otf')
font = pygame.font.Font(font_path, 24)

player1_name = ''
player2_name = ''
player1_colour = None
player2_colour = None

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

player_states = [{'name_input': True, 'color_input': False, 'ready': False},
                 {'name_input': True, 'color_input': False, 'ready': False}]

# TextBox class to handle player name input
class TextBox:
    def __init__(self, x, y, width, height, player_index):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (30, 30, 30)  # Dark background for the text box
        self.border_color = (255, 255, 255)  # White border
        self.text = ''
        self.active = False
        self.font = font
        self.player_index = player_index  # Store player index

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the text box is clicked
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False  # Deactivate the textbox when done
                if self.player_index == 0:
                    global player1_name
                    player1_name = self.text  # Store Player 1 name
                else:
                    global player2_name
                    player2_name = self.text  # Store Player 2 name
                return True  # Indicate to move to the next input
            else:
                self.text += event.unicode

        return False  # Indicate to stay on the current input

    def draw(self, screen):
        # Draw the text box background and border
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)  # Border
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (255, 255, 255)  # White button background
        self.text = text
        self.font = font
        self.active = False

    def draw(self, screen):
        # Draw the button rectangle
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw the button text centered in the button
        text_surface = self.font.render(self.text, True, (0, 0, 0))  # Black text
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True  # Button was clicked
        return False

def draw_text(text, pos, color=(255, 255, 255)):  # White text by default
    """Draw text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def choose_color(x_offset):
    """Display color selection options for players in a 4x4 grid format."""
    square_size = 80  # Size of each color square
    for i, color in enumerate(colors[:16]):  # Show only 16 colors (4x4 grid)
        row = i // 4  # Determine the row (4 colors per row)
        col = i % 4   # Determine the column
        pygame.draw.rect(screen, color, pygame.Rect(x_offset + col * (square_size + 10), 200 + row * (square_size + 10), square_size, square_size))

def handle_color_selection(event, player_index, x_offset):
    """Handle color selection for the current player."""
    global player1_colour, player2_colour
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos = event.pos
        square_size = 80  # Size of each color square
        for i, color in enumerate(colors[:16]):  # Match the reduced grid
            row = i // 4
            col = i % 4
            if pygame.Rect(x_offset + col * (square_size + 10), 200 + row * (square_size + 10), square_size, square_size).collidepoint(mouse_pos):
                if player_index == 0:
                    player1_colour = color
                    player_states[player_index]['color_input'] = False
                    player_states[player_index]['ready'] = True  # Automatically set ready to True
                else:
                    player2_colour = color
                    player_states[player_index]['color_input'] = False
                    player_states[player_index]['ready'] = True  # Automatically set ready to True

def playerStart() -> None:
    """Main setup loop to handle input and ready state."""

    
    running = True

    # Create text boxes for player names
    player1_textbox = TextBox(150, 100, 200, 40, 0)  # Position below the player prompt
    player2_textbox = TextBox(450, 100, 200, 40, 1)  # Position below the player prompt

    # Create start button (will only be shown when both players are ready)
    start_button = Button(350, 500, 120, 50, "Start")


    while running:
        screen.fill((0, 0, 0))  # Black background

        # Draw all UI elements on top
        # Player 1 setup on the left
        draw_text("Player 1 Name: ", (120, 50))
        player1_textbox.draw(screen)  # Draw Player 1 text box

        if player_states[0]['color_input']:
            draw_text("Choose a Color: ", (90, 160))
            choose_color(20)

        if not player_states[0]['color_input'] and player1_colour is not None:
            draw_text("Ready", (240, 250), player1_colour)  # Use player 1 color

        # Player 2 setup on the right
        draw_text("Player 2 Name: ", (420, 50))
        player2_textbox.draw(screen)  # Draw Player 2 text box

        if player_states[1]['color_input']:
            draw_text("Choose a Color: ", (430, 160))
            choose_color(430)

        if not player_states[1]['color_input'] and player2_colour is not None:
            draw_text("Ready", (450, 250), player2_colour)  # Use player 2 color

        # Check if both players are ready to show the start button
        if player_states[0]['ready'] and player_states[1]['ready']:
            start_button.draw(screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle Player 1 Input
            if player_states[0]['name_input']:
                if player1_textbox.handle_event(event):
                    player_states[0]['name_input'] = False
                    player_states[0]['color_input'] = True  # Switch to color selection

            # Handle Player 2 Input
            if player_states[1]['name_input']:
                if player2_textbox.handle_event(event):
                    player_states[1]['name_input'] = False
                    player_states[1]['color_input'] = True  # Switch to color selection

            # Handle color selections
            if player_states[0]['color_input']:
                handle_color_selection(event, 0, 20)
            if player_states[1]['color_input']:
                handle_color_selection(event, 1, 430)

            # Handle the start button click
            if player_states[0]['ready'] and player_states[1]['ready']:
                if start_button.handle_event(event):
                    import player_test
                    player_test.main([(player1_colour,player1_name),(player2_colour,player2_name)])
                    running = False  # Exit the setup and start the game

        pygame.display.flip()

if __name__ == '__main__':
    playerStart()

