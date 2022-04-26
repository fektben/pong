from turtle import up
import pygame
pygame.init()

#Display Setup

WIDTH, HEIGHT = 800, 600
flags = pygame.RESIZABLE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), flags)
pygame.display.set_caption("Pong")
FPS = 60

WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

class Paddle:
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

class Ball:
    MAX_VELOCITY = 5
    COLOR = (102, 204, 255)

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (self.x,self.y), self.radius)
    
    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        

def draw(surface, paddles, ball):
    surface.fill(BLACK)

    for paddle in paddles:
        paddle.draw(surface)
    
    pygame.draw.line(surface, RED, (WIDTH//2,0), (WIDTH//2,HEIGHT))

    ball.draw(surface)

    pygame.display.update()

def paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)
    
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)
    
def collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_velocity *= -1
    if ball.y - ball.radius <= 0:
        ball.y_velocity *= -1

    if ball.x_velocity < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_velocity *= -1


def main():
    running = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    while running:
        clock.tick(FPS)
        draw(SCREEN, [left_paddle, right_paddle], ball)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        keys = pygame.key.get_pressed()
        paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        collision(ball, left_paddle, right_paddle)

    pygame.quit()

if __name__ == '__main__':
    main()
