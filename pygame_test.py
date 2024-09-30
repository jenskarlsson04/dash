import pygame
import sys

# Initialize Pygame
pygame.init()

# Define colors
BLUE = (0, 102, 255)
DARK_BLUE = (0, 76, 204)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define user and design resolutions (for scaling)
user_x, user_y = 1920, 1080  # User's window size (High DPI)
design_x, design_y = 1024, 600   # Design resolution (Low DPI)
window = pygame.display.set_mode([user_x, user_y])  # Window with high resolution
w = pygame.Surface([design_x, design_y])  # Surface with lower design resolution

# Set up the font for the button text
FONT = pygame.font.SysFont("Arial", 20)

class Button:
    def __init__(self, x, y, width, height, text, font, color_normal=BLUE, color_hover=DARK_BLUE, text_color=BLACK):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.text_color = text_color
        self.current_color = self.color_normal

    def draw(self, screen):
        # Draw button rectangle with current color
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)

        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Blit the text onto the button
        screen.blit(text_surface, text_rect)

    def check_hover(self):
        # Change color on hover
        mouse_pos = pygame.mouse.get_pos()
        # Adjust mouse position for the design resolution
        scaled_mouse_pos = (mouse_pos[0] * design_x // user_x, mouse_pos[1] * design_y // user_y)
        if self.rect.collidepoint(scaled_mouse_pos):
            self.current_color = self.color_hover
        else:
            self.current_color = self.color_normal

    def is_clicked(self, event):
        # Check for click event on the button
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            # Adjust mouse position for the design resolution
            scaled_mouse_pos = (mouse_pos[0] * design_x // user_x, mouse_pos[1] * design_y // user_y)
            if self.rect.collidepoint(scaled_mouse_pos):
                return True
        return False

def draw():
    # Scale the design surface to the user window size and blit to the window
    frame = pygame.transform.scale(w, (user_x, user_y))
    window.blit(frame, frame.get_rect())
    pygame.display.flip()

def main():
    # Setup clock for managing frame rate
    clock = pygame.time.Clock()

    # Button instance with a smaller design resolution
    button = Button(220, 150, 200, 60, "Click Me", FONT)

    while True:
        w.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if button.is_clicked(event):
                print("Button Clicked!")

        # Check hover and draw button on the design surface
        button.check_hover()
        button.draw(w)

        # Scale and display the frame
        draw()

        clock.tick(60)


if __name__ == "__main__":
    main()
