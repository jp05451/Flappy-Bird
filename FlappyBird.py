import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -5
SPEED_INCREMENT = 0.5
ORIGIN_SPEED = 3
PIPE_SPEED = ORIGIN_SPEED
PIPE_SPAWN_TIME = 1500  # milliseconds
PIPE_GAP = 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Bird:
    def __init__(self):
        self.x = WINDOW_WIDTH // 3
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, 30, 30)

        # bird sticker
        bird_image = pygame.image.load("flappybird.png").convert_alpha()
        self.bird_image = pygame.transform.scale(bird_image, (40, 30))

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

    def draw(self, screen):
        # pygame.draw.rect(screen, BLACK, (self.x, self.y, 30, 30))

        screen.blit(self.bird_image, (self.x, self.y))


class Pipe:
    def __init__(self):
        self.gap_y = random.randint(150, WINDOW_HEIGHT - 150)
        self.x = WINDOW_WIDTH
        self.width = 50
        self.scored = False
        self.pipeSpeed = PIPE_SPEED

        # Create rectangles for top and bottom pipes
        self.top_pipe = pygame.Rect(self.x, 0, self.width, self.gap_y - PIPE_GAP // 2)
        self.bottom_pipe = pygame.Rect(
            self.x,
            self.gap_y + PIPE_GAP // 2,
            self.width,
            WINDOW_HEIGHT - (self.gap_y + PIPE_GAP // 2),
        )

        # create pipe sticker
        pipe_image = pygame.image.load("pipe.png").convert_alpha()
        self.topPipe_image = pygame.transform.scale(
            pipe_image, (self.width, self.top_pipe.height)
        )
        self.bottonPipe_image = pygame.transform.scale(
            pipe_image, (self.width, self.bottom_pipe.height)
        )
        self.topPipe_image = pygame.transform.flip(self.topPipe_image, 0, 1)

    def update(self):
        self.x -= self.pipeSpeed
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x

    def draw(self, screen):
        screen.blit(self.bottonPipe_image, (self.bottom_pipe.x, self.bottom_pipe.y))
        screen.blit(self.topPipe_image, (self.top_pipe.x, self.top_pipe.y))
        # pygame.draw.rect(screen, GREEN, self.top_pipe)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background = pygame.image.load("flappybird_background.jpg").convert()
        self.background = pygame.transform.scale(
            self.background, (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.screen.blit(self.background, (0, 0))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.reset()
        self.bestScore = self.loadBestScore()

    def loadBestScore(self):
        try:
            with open("best.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.last_pipe = pygame.time.get_ticks()
        self.game_over = False
        global PIPE_SPEED
        PIPE_SPEED = ORIGIN_SPEED

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    else:
                        self.bird.flap()

    def update(self):
        current_time = pygame.time.get_ticks()
        if not self.game_over:
            self.bird.update()

            if self.score > self.bestScore:
                self.bestScore = self.score

            if current_time - self.last_pipe > PIPE_SPAWN_TIME:
                self.pipes.append(Pipe())
                self.last_pipe = current_time

            if self.score % 10 == 0 and self.score != 0:
                global PIPE_SPEED
                PIPE_SPEED = SPEED_INCREMENT * int(self.score / 10) + ORIGIN_SPEED

            for pipe in self.pipes[:]:
                pipe.update()
                if (
                    self.bird.rect.colliderect(pipe.top_pipe)
                    or self.bird.rect.colliderect(pipe.bottom_pipe)
                    or self.bird.y < 0
                    or self.bird.y > WINDOW_HEIGHT
                ):
                    self.game_over = True

                if not pipe.scored and pipe.x < self.bird.x:
                    self.score += 1
                    pipe.scored = True

                if pipe.x < -pipe.width:
                    self.pipes.remove(pipe)

    def draw(self):
        self.screen.fill(WHITE)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.bird.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        bestScore = self.font.render(f"Best Score: {self.bestScore}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(bestScore, (10, 30))

        if self.game_over:
            game_over_text = self.font.render(
                "Game Over! Press SPACE to restart", True, BLACK
            )
            text_rect = game_over_text.get_rect(
                center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            )
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
