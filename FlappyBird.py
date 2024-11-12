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
PIPE_SPEED = 3
PIPE_SPAWN_TIME = 1500  # milliseconds
PIPE_GAP = 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()


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
        self.x -= PIPE_SPEED
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_pipe)
        pygame.draw.rect(screen, GREEN, self.bottom_pipe)


def main():
    bird = Bird()
    pipes = []
    score = 0
    font = pygame.font.Font(None, 36)
    last_pipe = pygame.time.get_ticks()
    game_over = False

    while True:
        current_time = pygame.time.get_ticks()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        # Reset game
                        bird = Bird()
                        pipes = []
                        score = 0
                        game_over = False
                    else:
                        bird.flap()

        if not game_over:
            # Update bird
            bird.update()

            # Spawn new pipes
            if current_time - last_pipe > PIPE_SPAWN_TIME:
                pipes.append(Pipe())
                last_pipe = current_time

            # Update and check pipes
            for pipe in pipes[:]:
                pipe.update()

                # Check collision
                if (
                    bird.rect.colliderect(pipe.top_pipe)
                    or bird.rect.colliderect(pipe.bottom_pipe)
                    or bird.y < 0
                    or bird.y > WINDOW_HEIGHT
                ):
                    game_over = True

                # Score points
                if not pipe.scored and pipe.x < bird.x:
                    score += 1
                    pipe.scored = True

                # Remove pipes that are off screen
                if pipe.x < -pipe.width:
                    pipes.remove(pipe)

        # Draw everything
        screen.fill(WHITE)

        for pipe in pipes:
            pipe.draw()

        bird.draw()

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render(
                "Game Over! Press SPACE to restart", True, BLACK
            )
            text_rect = game_over_text.get_rect(
                center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
            )
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
