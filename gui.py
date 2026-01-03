import pygame
from hypertle import Hypertle
import threading


class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = (200, 200, 200)
        self.hover_color = (150, 150, 150)
        self.text_color = (0, 0, 0)
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()
                return True
        return False


def background(turtle, exit_flag_ref):
    """Background thread for command-line input"""
    from hypertle import parse
    while not exit_flag_ref[0]:
        try:
            cmd_queue = input('> ').strip('\n').split(' ')
            parse(cmd_queue, turtle, exit_flag_ref)
        except EOFError:
            break


def run_gui():
    """Main GUI application"""
    exit_flag = [False]  # Use list to allow modification in nested scope
    R = 400
    TURTLE_SCALE = 20
    turtle = Hypertle(R, TURTLE_SCALE)

    # Create GUI buttons
    buttons = [
        Button(820, 50, 120, 40, "Forward 1", lambda: turtle.fd(1)),
        Button(820, 100, 120, 40, "Forward 10", lambda: turtle.fd(10)),
        Button(820, 180, 120, 40, "Left 15°", lambda: turtle.lt(15)),
        Button(820, 230, 120, 40, "Right 15°", lambda: turtle.rt(15)),
        Button(820, 310, 120, 40, "Pen Up", lambda: turtle.pu()),
        Button(820, 360, 120, 40, "Pen Down", lambda: turtle.pd()),
        Button(820, 440, 120, 40, "Clear", lambda: turtle.clear()),
    ]

    pygame.init()

    # Adjust window size to accommodate buttons
    screen = pygame.display.set_mode((960, 800))
    pygame.display.set_caption("Hyperbolic Turtle")

    cmd_thread = threading.Thread(target=background, args=(turtle, exit_flag))
    cmd_thread.daemon = True
    cmd_thread.start()

    while not exit_flag[0]:
        screen.fill((240, 240, 240))
        
        # Draw turtle canvas
        turtle.draw()
        screen.blit(turtle.surface, (0, 0))
        
        # Draw buttons
        for button in buttons:
            button.draw(screen)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_flag[0] = True
            
            # Handle button events
            for button in buttons:
                button.handle_event(event)

    pygame.display.quit()
    cmd_thread.join()


if __name__ == '__main__':
    run_gui()
