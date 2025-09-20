import pygame, sys

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shadow Swap - Extreme Hard Mode")
clock = pygame.time.Clock()

# Colors
LIGHT_BG = (180, 220, 255)
SHADOW_BG = (50, 50, 80)
GREEN = (0, 200, 0)
PURPLE = (150, 0, 200)
RED = (200, 50, 50)
GOLD = (255, 215, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        self.vel_y += 0.8
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.y += self.vel_y

        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect) and self.vel_y >= 0:
                self.rect.bottom = p.rect.top
                self.vel_y = 0
                self.on_ground = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -22  # Higher jump for hard levels

# Platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color, moving=False, move_range=0, speed=2, vertical=False, visible_world="both", fading=False):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.moving = moving
        self.move_range = move_range
        self.speed = speed
        self.vertical = vertical
        self.start_pos = self.rect.topleft
        self.visible_world = visible_world
        self.fading = fading
        self.alpha = 255

    def update(self, current_world):
        # Moving platforms
        if self.moving:
            if self.vertical:
                self.rect.y += self.speed
                if abs(self.rect.y - self.start_pos[1]) > self.move_range:
                    self.speed *= -1
            else:
                self.rect.x += self.speed
                if abs(self.rect.x - self.start_pos[0]) > self.move_range:
                    self.speed *= -1
        # Fading platforms
        if self.fading:
            if current_world == self.visible_world:
                self.alpha = min(255, self.alpha + 5)
            else:
                self.alpha = max(50, self.alpha - 5)
            self.image.set_alpha(self.alpha)

# Key
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, visible_world="both"):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.visible_world = visible_world

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_range=0, speed=2):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.patrol_range = patrol_range
        self.start_x = x
        self.speed = speed

    def update(self):
        if self.patrol_range > 0:
            self.rect.x += self.speed
            if abs(self.rect.x - self.start_x) > self.patrol_range:
                self.speed *= -1

# Door
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect(topleft=(x, y))

# -------------------
# Level Data: platforms, keys, enemies
LEVELS = [
    # Level 1
    {
        "light": [(0,560,800,40,GREEN),(200,450,200,20,GREEN,True,150,3)],
        "shadow": [(0,560,800,40,PURPLE),(400,350,200,20,PURPLE,True,150,3,False,"shadow",False)],
        "keys": [(250,400,"light"),(500,300,"shadow")],
        "enemies": [(500,520,120),(600,320,100)],
        "door": (700,500)
    },
    # Level 2
    {
        "light": [(0,560,800,40,GREEN),(150,450,200,20,GREEN,True,200,3)],
        "shadow": [(0,560,800,40,PURPLE),(350,400,200,20,PURPLE,True,150,2,False,"shadow",True)],
        "keys": [(200,420,"light"),(450,300,"shadow"),(600,200,"shadow")],
        "enemies": [(500,520,120),(600,300,100),(300,350,150)],
        "door": (700,500)
    },
    # Level 3
    {
        "light": [(0,560,800,40,GREEN),(150,450,200,20,GREEN,True,200,3)],
        "shadow": [(0,560,800,40,PURPLE),(350,400,200,20,PURPLE,True,150,2,False,"shadow",True),(500,300,150,20,PURPLE,True,150,2,True,"shadow",True)],
        "keys": [(200,420,"light"),(500,300,"shadow"),(600,200,"shadow")],
        "enemies": [(500,520,120),(600,300,100),(300,350,150),(400,250,80)],
        "door": (700,500)
    },
    # Level 4
    {
        "light": [(0,560,800,40,GREEN),(100,450,150,20,GREEN,True,150,2)],
        "shadow": [(0,560,800,40,PURPLE),(200,400,200,20,PURPLE,True,100,3,True,"shadow",True),(450,300,150,20,PURPLE,True,150,2,True,"shadow",False)],
        "keys": [(150,420,"light"),(400,350,"shadow"),(500,250,"shadow"),(600,200,"light")],
        "enemies": [(400,520,100),(500,300,80),(600,250,120)],
        "door": (700,500)
    },
    # Level 5
    {
        "light": [(0,560,800,40,GREEN),(150,450,150,20,GREEN,True,200,3)],
        "shadow": [(0,560,800,40,PURPLE),(300,400,150,20,PURPLE,True,150,3,True,"shadow",True),(500,300,150,20,PURPLE,True,150,2,True,"shadow",True)],
        "keys": [(200,420,"light"),(350,350,"shadow"),(500,250,"shadow"),(650,200,"shadow")],
        "enemies": [(400,520,100),(500,300,120),(600,250,150)],
        "door": (700,500)
    },
    # Level 6
    {
        "light": [(0,560,800,40,GREEN),(100,450,150,20,GREEN,True,150,3),(400,400,200,20,GREEN,True,100,2)],
        "shadow": [(0,560,800,40,PURPLE),(200,400,150,20,PURPLE,True,150,3,True,"shadow",True),(450,300,150,20,PURPLE,True,150,2,True,"shadow",True),(600,250,100,20,PURPLE,True,100,2,True,"shadow",True)],
        "keys": [(150,420,"light"),(300,350,"shadow"),(450,300,"shadow"),(600,250,"shadow"),(650,200,"light")],
        "enemies": [(400,520,100),(500,300,120),(600,250,150),(550,200,80)],
        "door": (700,500)
    }
]

# -------------------
# Build level
def build_level(index):
    level = LEVELS[index]
    light = pygame.sprite.Group()
    for p in level["light"]:
        light.add(Platform(*p))
    shadow = pygame.sprite.Group()
    for p in level["shadow"]:
        shadow.add(Platform(*p))
    keys = pygame.sprite.Group()
    for k in level["keys"]:
        keys.add(Key(*k))
    enemies = pygame.sprite.Group()
    for e in level["enemies"]:
        enemies.add(Enemy(*e))
    door = Door(*level["door"])
    return light, shadow, keys, enemies, door

# -------------------
# Game state
current_level = 0
player = Player(50,500)
current_world = "light"
light_platforms, shadow_platforms, keys, enemies, door = build_level(current_level)
font = pygame.font.SysFont(None,40)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                current_world = "shadow" if current_world=="light" else "light"

    # Update
    platforms = light_platforms if current_world=="light" else shadow_platforms
    for p in platforms:
        p.update(current_world)
    player.update(platforms)
    enemies.update()

    # Lose: fall
    if player.rect.top>HEIGHT:
        player = Player(50,500)
        light_platforms, shadow_platforms, keys, enemies, door = build_level(current_level)

    # Lose: touch enemy in Shadow
    if current_world=="shadow":
        for e in enemies:
            if player.rect.colliderect(e.rect):
                player = Player(50,500)
                light_platforms, shadow_platforms, keys, enemies, door = build_level(current_level)

    # Collect keys
    for k in keys:
        if player.rect.colliderect(k.rect) and (k.visible_world=="both" or k.visible_world==current_world):
            k.kill()

    # Check door
    if len(keys)==0 and player.rect.colliderect(door.rect):
        current_level+=1
        if current_level>=len(LEVELS):
            print("🎉 You finished all levels!")
            running=False
        else:
            player = Player(50,500)
            light_platforms, shadow_platforms, keys, enemies, door = build_level(current_level)

    # Draw
    screen.fill(LIGHT_BG if current_world=="light" else SHADOW_BG)
    for p in platforms:
        if p.visible_world=="both" or p.visible_world==current_world:
            screen.blit(p.image,p.rect)
    for k in keys:
        if k.visible_world=="both" or k.visible_world==current_world:
            screen.blit(k.image,k.rect)
    if current_world=="shadow":
        enemies.draw(screen)
    screen.blit(door.image,door.rect)
    screen.blit(player.image,player.rect)
    key_text = font.render(f"Keys remaining: {len(keys)}",True,WHITE)
    screen.blit(key_text,(10,10))

    pygame.display.flip()
