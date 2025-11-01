import pygame, sys, random, math

pygame.init()
WIDTH, HEIGHT = 900, 300
GROUND_Y = HEIGHT - 40
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🦖 Dino Runner Pro Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 20)
big_font = pygame.font.SysFont("consolas", 44)

def beep(freq, dur):
    try:
        s = pygame.mixer.Sound(buffer=pygame.sndarray.make_sound(
            pygame.sndarray.array([[int(math.sin(x / (44100 / freq) * math.pi * 2) * 32767)
                                   for x in range(int(44100 * dur / 1000))]] * 2, dtype="int16")))
        s.play()
    except:
        pass

class Dino:
    def __init__(self):
        self.x, self.y = 80, GROUND_Y - 44
        self.vel_y = 0
        self.on_ground = True
        self.frame = 0
        self.color = (60, 60, 60)

    def jump(self):
        if self.on_ground:
            self.vel_y = -14
            self.on_ground = False
            beep(600, 100)

    def update(self):
        self.y += self.vel_y
        self.vel_y += 0.8
        if self.y >= GROUND_Y - 44:
            self.y = GROUND_Y - 44
            self.vel_y = 0
            self.on_ground = True
        self.frame += 0.25

    def draw(self, surf, night=False):
        base = (240, 240, 240) if night else self.color
        pygame.draw.rect(surf, base, (self.x, self.y + 10, 34, 24), border_radius=6)
        pygame.draw.rect(surf, base, (self.x + 24, self.y - 6, 20, 20), border_radius=4)
        tail_angle = math.sin(self.frame) * 4
        pygame.draw.polygon(surf, base, [
            (self.x, self.y + 30),
            (self.x - 10, self.y + 25 + tail_angle),
            (self.x, self.y + 25),
        ])
        leg_phase = int(self.frame * 2) % 2
        if leg_phase == 0:
            pygame.draw.rect(surf, base, (self.x + 6, self.y + 30, 6, 8))
            pygame.draw.rect(surf, base, (self.x + 20, self.y + 30, 6, 8))
        else:
            pygame.draw.rect(surf, base, (self.x + 12, self.y + 30, 6, 8))
            pygame.draw.rect(surf, base, (self.x + 26, self.y + 30, 6, 8))
        pygame.draw.circle(surf, (0, 0, 0), (self.x + 38, self.y), 2)

    def rect(self):
        return pygame.Rect(self.x, self.y, 44, 44)

class Cactus:
    def __init__(self, speed):
        self.x = WIDTH + random.randint(0, 150)
        self.y = GROUND_Y - 40
        self.speed = speed
        self.h = random.choice([30, 40, 50])

    def update(self): self.x -= self.speed
    def off_screen(self): return self.x < -20
    def draw(self, surf, night=False):
        c = (200, 255, 200) if night else (0, 160, 0)
        pygame.draw.rect(surf, c, (self.x, self.y - self.h, 14, self.h))
        pygame.draw.rect(surf, c, (self.x - 6, self.y - self.h // 2, 6, 12))
        pygame.draw.rect(surf, c, (self.x + 14, self.y - self.h // 3, 6, 12))
    def rect(self): return pygame.Rect(self.x, self.y - self.h, 14, self.h)

class Bird:
    def __init__(self, speed):
        self.x = WIDTH + random.randint(0, 200)
        self.y = random.choice([GROUND_Y - 60, GROUND_Y - 90])
        self.speed = speed
        self.frame = 0
    def update(self):
        self.x -= self.speed
        self.frame += 0.2
    def off_screen(self): return self.x < -40
    def draw(self, surf, night=False):
        c = (230, 230, 230) if night else (80, 80, 80)
        phase = int(self.frame) % 2
        pygame.draw.circle(surf, c, (int(self.x), int(self.y)), 10)
        wing_offset = 8 if phase else -8
        pygame.draw.line(surf, c, (self.x - 8, self.y), (self.x - 20, self.y + wing_offset), 3)
        pygame.draw.line(surf, c, (self.x + 8, self.y), (self.x + 20, self.y + wing_offset), 3)
    def rect(self): return pygame.Rect(self.x - 10, self.y - 10, 20, 20)

class Coin:
    def __init__(self, speed):
        self.x = WIDTH + random.randint(100, 250)
        self.y = random.randint(GROUND_Y - 120, GROUND_Y - 50)
        self.speed = speed
        self.frame = 0
    def update(self):
        self.x -= self.speed
        self.frame += 0.3
    def off_screen(self): return self.x < -20
    def draw(self, surf, night=False):
        c = (255, 220, 0) if not night else (255, 250, 140)
        pygame.draw.circle(surf, c, (int(self.x), int(self.y)), 10)
        pygame.draw.circle(surf, (255, 255, 255), (int(self.x - 3), int(self.y - 3)), 2)
    def rect(self): return pygame.Rect(self.x - 10, self.y - 10, 20, 20)

class Cloud:
    def __init__(self):
        self.x = WIDTH + random.randint(0, 200)
        self.y = random.randint(40, 120)
        self.speed = random.uniform(1, 2)
    def update(self): self.x -= self.speed
    def draw(self, surf, night=False):
        c = (180, 180, 180) if night else (255, 255, 255)
        pygame.draw.circle(surf, c, (int(self.x), self.y), 15)
        pygame.draw.circle(surf, c, (int(self.x) + 15, self.y + 5), 12)
        pygame.draw.circle(surf, c, (int(self.x) - 15, self.y + 5), 12)
    def off_screen(self): return self.x < -30

def load_highscore():
    try: return int(open("highscore.txt").read())
    except: return 0

def save_highscore(s): open("highscore.txt", "w").write(str(s))

def game_loop():
    dino = Dino()
    obstacles, birds, coins, clouds = [], [], [], [Cloud() for _ in range(3)]
    score, highscore, speed, game_over = 0, load_highscore(), 6, False
    spawn_timer = coin_timer = bird_timer = 0

    while True:
        dt = clock.tick(FPS)
        is_night = (pygame.time.get_ticks() // 15000) % 2 == 1

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                save_highscore(max(score, highscore))
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if not game_over and e.key in [pygame.K_SPACE, pygame.K_UP]:
                    dino.jump()
                if game_over and e.key == pygame.K_r:
                    return True
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        if not game_over:
            dino.update()
            spawn_timer += dt; coin_timer += dt; bird_timer += dt

            if spawn_timer > 1300:
                obstacles.append(Cactus(speed)); spawn_timer = 0
            if coin_timer > 1800:
                coins.append(Coin(speed)); coin_timer = 0
            if bird_timer > 4500 and random.random() < 0.5:
                birds.append(Bird(speed)); bird_timer = 0
            if random.random() < 0.005:
                clouds.append(Cloud())

            for lst in [obstacles, birds, coins, clouds]:
                for o in lst: o.update()
                lst[:] = [o for o in lst if not o.off_screen()]

            for o in obstacles + birds:
                if dino.rect().colliderect(o.rect()):
                    game_over = True
                    beep(200, 200)
                    if score > highscore: save_highscore(score); highscore = score

            for c in coins[:]:
                if dino.rect().colliderect(c.rect()):
                    score += 10
                    coins.remove(c)
                    beep(800, 50)

            score += 0.1
            speed = 6 + int(score // 100)

        screen.fill((30, 30, 60) if is_night else (240, 240, 240))
        for cl in clouds: cl.draw(screen, is_night)
        pygame.draw.line(screen, (100, 100, 100), (0, GROUND_Y), (WIDTH, GROUND_Y), 3)
        for o in obstacles: o.draw(screen, is_night)
        for b in birds: b.draw(screen, is_night)
        for c in coins: c.draw(screen, is_night)
        dino.draw(screen, is_night)

        txt = font.render(f"SCORE: {int(score)}", True, (255,255,255) if is_night else (0,0,0))
        htxt = font.render(f"HIGH: {highscore}", True, (255,255,255) if is_night else (0,0,0))
        screen.blit(txt, (WIDTH - 160, 10))
        screen.blit(htxt, (WIDTH - 260, 10))

        if game_over:
            over = big_font.render("GAME OVER", True, (255, 80, 80))
            restart = font.render("Press R to Restart", True, (200, 200, 200))
            screen.blit(over, ((WIDTH - over.get_width()) // 2, HEIGHT // 2 - 40))
            screen.blit(restart, ((WIDTH - restart.get_width()) // 2, HEIGHT // 2 + 10))

        pygame.display.flip()

def main_menu():
    while True:
        screen.fill((240, 240, 240))
        title = big_font.render("🦖 DINO RUNNER PRO EDITION", True, (40, 40, 40))
        sub = font.render("Press SPACE to Start | Jump: SPACE/UP | Quit: ESC", True, (60, 60, 60))
        screen.blit(title, ((WIDTH - title.get_width()) // 2, HEIGHT // 2 - 60))
        screen.blit(sub, ((WIDTH - sub.get_width()) // 2, HEIGHT // 2 + 10))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                game_loop()

if __name__ == "__main__":
    main_menu()
