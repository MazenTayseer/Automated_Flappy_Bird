import pygame
import neat
import os
import random

pygame.init()
pygame.font.init()

WIDTH = 500
HEIGHT = 800

GEN = 0
GAME_STARTED = False

BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load("Assets/Images/bird1.png")),
               pygame.transform.scale2x(pygame.image.load("Assets/Images/bird2.png")),
               pygame.transform.scale2x(pygame.image.load("Assets/Images/bird3.png"))]

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load("Assets/Images/pipe.png"))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load("Assets/Images/bg.png"))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load("Assets/Images/base.png"))

STAT_FONT = pygame.font.Font("font/Pixeltype.ttf", 50)

pygame.display.set_caption("Flappy bird")
pygame.display.set_icon(BIRD_IMAGES[0])

BG_MUSIC = pygame.mixer.Sound('music/music.wav')
BG_MUSIC.play(loops=-1)


class Bird:
    IMAGES = BIRD_IMAGES
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMAGES[0]

    def jump(self):
        self.velocity = -10
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y += d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMAGES[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMAGES[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMAGES[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMAGES[1]
        elif self.img_count == self.ANIMATION_TIME * 4:
            self.img = self.IMAGES[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMAGES[1]
            self.img_count = self.ANIMATION_TIME * 2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VELOCITY = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    VELOCITY = 5
    WIDTH = BASE_IMAGE.get_width()
    IMAGE = BASE_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMAGE, (self.x1, self.y))
        win.blit(self.IMAGE, (self.x2, self.y))


def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BACKGROUND_IMAGE, (0, 0))
    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), True, (255, 255, 255))
    win.blit(text, (WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Generation: " + str(gen), True, (255, 255, 255))
    win.blit(text, (10, 10))

    text = STAT_FONT.render("Birds: " + str(len(birds)), True, (255, 255, 255))
    win.blit(text, (10, 60))

    base.draw(win)

    for bird in birds:
        bird.draw(win)
    pygame.display.update()


def draw_welcome_screen(win):
    win.blit(BACKGROUND_IMAGE, (0, 0))

    title_font = pygame.font.Font("font/Pixeltype.ttf", 70)
    title_text = title_font.render("Flappy Bird", True, (255, 255, 255))
    title_x = WIDTH / 2 - title_text.get_width() / 2
    title_y = HEIGHT / 2 - title_text.get_height()
    win.blit(title_text, (title_x, title_y))

    bird_index = (pygame.time.get_ticks() // 200) % len(BIRD_IMAGES)
    bird_x = WIDTH / 2 - BIRD_IMAGES[bird_index].get_width() / 2
    bird_y = title_y - BIRD_IMAGES[bird_index].get_height() - 20
    win.blit(BIRD_IMAGES[bird_index], (bird_x, bird_y))

    instructions_font = pygame.font.Font("font/Pixeltype.ttf", 30)
    instructions_text = instructions_font.render("Press Space to Start", True, (255, 255, 255))
    instructions_x = WIDTH / 2 - instructions_text.get_width() / 2
    instructions_y = HEIGHT / 2 + instructions_text.get_height()
    win.blit(instructions_text, (instructions_x, instructions_y))

    pygame.display.update()


def main(genomes, config):
    global GEN
    global GAME_STARTED

    GEN += 1

    nets = []
    ge = []
    birds = []

    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(250, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(700)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    while True:
        if not GAME_STARTED:
            draw_welcome_screen(win)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GAME_STARTED = True

        if GAME_STARTED:
            clock.tick(30)

            pipe_ind = 0
            if len(birds) > 0:
                if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                    pipe_ind = 1
            else:
                break

            for x, bird in enumerate(birds):
                bird.move()
                ge[x].fitness += 0.1

                output = nets[x].activate(
                    (bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
                if output[0] > 0.3:
                    bird.jump()

            add_pipe = False
            rem = []
            for pipe in pipes:
                for x, bird in enumerate(birds):
                    if pipe.collide(bird):
                        birds.pop(x)
                        nets.pop(x)
                        ge.pop(x)

                    if not pipe.passed and pipe.x < bird.x:
                        pipe.passed = True
                        add_pipe = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                pipe.move()

            if add_pipe:
                score += 1
                for g in ge:
                    g.fitness += 5
                pipes.append(Pipe(600))

            for r in rem:
                pipes.remove(r)

            for x, bird in enumerate(birds):
                if bird.y + bird.img.get_height() >= 700 or bird.y < 0:
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            if score > 20:
                if len(birds) > 1:
                    for bird in birds:
                        birds.pop()
                        if len(birds) == 1:
                            break

            base.move()
            draw_window(win, birds, pipes, base, score, GEN)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    try:
        p.run(main, 50)
    except neat.population.CompleteExtinctionException:
        print("EXTINCTION")


if __name__ == "__main__":
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, "config.txt")
    run(config_path)
