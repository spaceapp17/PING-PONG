import pygame
pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Ping-Pong")
clock = pygame.time.Clock()
WHITE_BLUE = (67, 245, 244)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
speed_x = 3
speed_y = 3
platform_speed = 5

class Area:
    def __init__(self, x=0, y=0, width=10, height=10, color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color
    def colliderect(self, rect):
        return self.rect.colliderect(rect)
    def set_color(self, new_color):
        self.fill_color = new_color
    def fill(self):
        pygame.draw.rect(screen, self.fill_color, self.rect)

class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=50, height=50):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=WHITE)
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (width, height))
    def drawing(self, shift_x=0, shift_y=0):
        screen.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

class Label(Area):
    def set_text(self, text, fsize=12, text_color=BLACK):
        self.image = pygame.font.SysFont("verdana", fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        screen.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

try:
    ball = Picture("ball.png", 225, 250, 40, 40)
except:
    ball = Area(270, 250, 40, 40, WHITE)

try:
    left_platform = Picture("probnick.png", 20, 200, 20, 100)
except:
    left_platform = Area(20, 200, 20, 100, WHITE)

try:
    right_platform = Picture("probnick.png", WIDTH - 40, 200, 20, 100)
except:
    right_platform = Area(WIDTH - 40, 200, 20, 100, WHITE)

move_left_up = False
move_left_down = False
move_right_up = False
move_right_down = False
game_over = False

while not game_over:
    screen.fill(WHITE_BLUE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                move_left_up = True
            if event.key == pygame.K_s:
                move_left_down = True
            if event.key == pygame.K_UP:
                move_right_up = True
            if event.key == pygame.K_DOWN:
                move_right_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                move_left_up = False
            if event.key == pygame.K_s:
                move_left_down = False
            if event.key == pygame.K_UP:
                move_right_up = False
            if event.key == pygame.K_DOWN:
                move_right_down = False

    if move_left_up and left_platform.rect.y > 0:
        left_platform.rect.y -= platform_speed
    if move_left_down and left_platform.rect.y < HEIGHT - left_platform.rect.height:
        left_platform.rect.y += platform_speed

    if move_right_up and right_platform.rect.y > 0:
        right_platform.rect.y -= platform_speed
    if move_right_down and right_platform.rect.y < HEIGHT - right_platform.rect.height:
        right_platform.rect.y += platform_speed

    ball.rect.x += speed_x
    ball.rect.y += speed_y

    if ball.rect.y <= 0 or ball.rect.y >= HEIGHT - ball.rect.height:
        speed_y *= -1

    if ball.colliderect(left_platform.rect):
        speed_x = abs(speed_x)

    if ball.colliderect(right_platform.rect):
        speed_x = -abs(speed_x)

    if ball.rect.x < 0 or ball.rect.x > WIDTH:
        text = Label(100, 200, 300, 80, BLACK)
        text.set_text("YOU LOSE", 50, RED)
        text.draw()
        pygame.display.update()
        pygame.time.wait(2000)
        game_over = True

    if hasattr(ball, 'drawing'):
        ball.drawing()
    else:
        ball.fill()

    if hasattr(left_platform, 'drawing'):
        left_platform.drawing()
    else:
        left_platform.fill()

    if hasattr(right_platform, 'drawing'):
        right_platform.drawing()
    else:
        right_platform.fill()

    pygame.display.update()
    clock.tick(60)

pygame.quit()