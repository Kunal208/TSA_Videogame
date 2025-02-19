import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Level setup
level = 1
currlevel = 1
collideend = False

# Constants
WIDTH, HEIGHT = 1920, 1020
PLAYER_SIZE = 40
PLAYER_SPEED = 5
JUMP_FORCE = 10
GRAVITY = 0.5
CHAIN_LENGTH = 100  # Max distance between players

# Colors
WHITE = (26, 31, 46)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (20, 70, 74)
ORANGE = (199, 114, 40)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bound Together")

METEOR_RADIUS = 20
METEOR_SPEED = 5

design_RADIUS = 20
design_SPEED = 5

# Floor setup
floor = pygame.Rect(0, HEIGHT - 50, 500, 50)  # Base floor at the bottom

platformRect1Rand=random.randint(100,150)
platformRect2Rand=random.randint(100,platformRect1Rand+150)
platformRect3Rand=random.randint(100,platformRect2Rand+150)
platformRect4Rand=random.randint(100,platformRect3Rand+150)

platforms4 = [
    pygame.Rect(600, HEIGHT-platformRect1Rand, 100, 50),
    pygame.Rect(900, HEIGHT-platformRect2Rand, 150, 50),
    pygame.Rect(1300, HEIGHT-platformRect3Rand, 100, 50),
    pygame.Rect(1650, HEIGHT-platformRect4Rand, 150, 50),
]

# Font
font = pygame.font.Font(None, 50)

# Borders
leftBorder = pygame.Surface((20, HEIGHT))
rightBorder = pygame.Surface((20, HEIGHT))
leftRect = leftBorder.get_rect(center=(0, HEIGHT // 2))
rightRect = rightBorder.get_rect(center=(WIDTH - 10, HEIGHT // 2))

def spawn_meteor():
    """Spawns meteors at random x positions from the top."""
    x = random.randint(500, WIDTH - METEOR_RADIUS * 2)
    meteor_list.append(pygame.Rect(x, 0, METEOR_RADIUS * 2, METEOR_RADIUS * 2))

def spawn_design():
    """Spawns design elements (sideways meteors) with random colors."""
    y = random.randint(0, 500)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    design_list.append({
        'rect': pygame.Rect(0, y, 60, 60),
        'color': color,
        'speed': random.choice([design_SPEED])  # Random direction
    })

class Player:
    def __init__(self, x, y, color, controls):
        self.ogx = x
        self.ogy = y
        self.x = x
        self.y = y
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.color = color
        self.speed = PLAYER_SPEED
        self.velocity_y = 0  # For jumping and gravity
        self.on_ground = False
        self.controls = controls
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Rectangle for collision
        self.jumplength=0

    def move(self):
        keys = pygame.key.get_pressed()

        # Left/Right movement
        if keys[self.controls["left"]] and not self.rect.colliderect(leftRect):
            self.rect.x -= self.speed
        if keys[self.controls["right"]]:
            self.rect.x += self.speed

        # Jumping
        if keys[self.controls["up"]] and self.jumplength<4:
            self.velocity_y = -JUMP_FORCE  # Jump
            self.jumplength +=1

        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Platform collision
        self.on_ground = False  # Reset before checking for platform collision
        for platform in platforms4:
            if self.rect.colliderect(platform):
                self.rect.y = platform.top - self.height
                self.velocity_y = 0
                self.jumplength=0
                

        # Floor collision
        if self.rect.colliderect(floor):
            self.rect.y = floor.top - self.height
            self.velocity_y = 0
            self.jumplength=0

    def meteor_collisions(self):
        for meteors in meteor_list:
            if self.rect.colliderect(meteors):
                return True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)  # Draw player

    def reset(self):
        self.rect.x = self.ogx
        self.rect.y = self.ogy


def draw_text(text, x, y, color=ORANGE):
    """Draw text on the screen."""
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def selection_screen():
    """Selection screen to choose between 2 to 4 players."""
    selected_players = 2  # Default to 2 players
    running = True

    while running:
        screen.fill(BLACK)

        draw_text("Select number of players:", WIDTH // 4, HEIGHT // 4)
        draw_text(f"{selected_players}", WIDTH // 2, HEIGHT // 2, RED)

        draw_text("Press LEFT/RIGHT to change", WIDTH // 4, HEIGHT // 2 + 50, ORANGE)
        draw_text("Press ENTER to start", WIDTH // 4, HEIGHT // 2 + 100, ORANGE)
        draw_text("Player 1 controls: A W D  Player 2 controls: Arrow Keys", WIDTH // 4, 50, ORANGE)
        draw_text("Player 3 controls: J I L  Player 4 controls: F T H", WIDTH // 4, 150, ORANGE)
        draw_text("Objective: Get to the other side of the room", WIDTH // 4, 225, ORANGE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and selected_players > 2:
                    selected_players -= 1
                if event.key == pygame.K_RIGHT and selected_players < 4:
                    selected_players += 1
                if event.key == pygame.K_RETURN:
                    return selected_players  # Start game with chosen number of players


# Get selected number of players
num_players = selection_screen()

# Create players based on selection
all_players = [
    Player(30, HEIGHT - 100, RED, {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w}),
    Player(230, HEIGHT - 100, BLUE, {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP}),
    Player(430, HEIGHT - 100, GREEN, {"left": pygame.K_j, "right": pygame.K_l, "up": pygame.K_i}),
    Player(530, HEIGHT - 100, YELLOW, {"left": pygame.K_f, "right": pygame.K_h, "up": pygame.K_t}),
]

meteor_list = [
    pygame.Rect(random.randint(0,WIDTH),HEIGHT, 50, 50)
]

design_list = []

# Only keep the selected number of players
players = all_players[:num_players]


def enforce_chain():
    """Keep players within CHAIN_LENGTH of each other."""
    for i in range(len(players) - 1):
        p1, p2 = players[i], players[i + 1]

        dx = p2.rect.centerx - p1.rect.centerx
        dy = p2.rect.centery - p1.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > CHAIN_LENGTH:
            ratio = CHAIN_LENGTH / distance
            mid_x = (p1.rect.centerx + p2.rect.centerx) / 2
            mid_y = (p1.rect.centery + p2.rect.centery) / 2

            # Move players closer together
            p1.rect.centerx = int(mid_x - (dx * ratio / 2))
            p1.rect.centery = int(mid_y - (dy * ratio / 2))
            p2.rect.centerx = int(mid_x + (dx * ratio / 2))
            p2.rect.centery = int(mid_y + (dy * ratio / 2))


# Game loop
meteor_timer=0
design_timer=0

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)  # Clear screen
    pygame.draw.rect(screen, BLACK, floor)  # Draw floor

    for platform in platforms4:
        pygame.draw.rect(screen, GRAY, platform)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move players and enforce chain physics
    for player in players:
        player.move()

    enforce_chain()

    # Draw players
    for player in players:
        player.draw(screen)

    # Draw chains
    for i in range(len(players) - 1):
        pygame.draw.line(screen, BLACK, players[i].rect.center, players[i + 1].rect.center, 5)

    # Spawn meteors every 60 frames (~1 second at 60 FPS)
    meteor_timer += 1
    if meteor_timer >= 100:
        
        
        spawn_meteor()
        meteor_timer = 0

    design_timer += 1
    if design_timer >= 50:
        spawn_design()
        
        design_timer = 0

    # Move and draw design elements (sideways meteors)
    for design in design_list[:]:
        design['rect'].x += design['speed']
        pygame.draw.rect(screen, design['color'], design['rect'])

        # Remove design elements that go off the screen
        if design['rect'].x > WIDTH or design['rect'].x < -design['rect'].width:
            design_list.remove(design)

    # Move and draw meteors
    for meteor in meteor_list[:]:  # Iterate over a copy to avoid modification issues
        meteor.y += METEOR_SPEED
        pygame.draw.circle(screen, ORANGE, (meteor.x + METEOR_RADIUS, meteor.y + METEOR_RADIUS), METEOR_RADIUS)

        # Remove meteors that fall off the screen
        if meteor.y > HEIGHT:
            meteor_list.remove(meteor)
    
    
    

    for player in players:
        if player.rect.colliderect(rightRect):
            collideend=True

    if collideend:
        for player in players:
            player.reset()
        collideend = False
        level += 1

    # Death/game over check
    alive = True
    for player in players:
        if player.rect.y > HEIGHT:
            alive = False
        if player.meteor_collisions():
            alive= False

    if not alive:
        for player in players:
            player.reset()
        level = 1
        currlevel = 1

    draw_text("Level: " + str(level), WIDTH - 150, 20)

    if level > currlevel:
        platformRect1Rand=random.randint(100,150)
        platformRect2Rand=random.randint(100,platformRect1Rand+150)
        platformRect3Rand=random.randint(100,platformRect2Rand+150)
        platformRect4Rand=random.randint(100,platformRect3Rand+150)
        platforms4[0].y=HEIGHT-platformRect1Rand
        platforms4[1].y=HEIGHT-platformRect2Rand
        platforms4[2].y=HEIGHT-platformRect3Rand
        platforms4[3].y=HEIGHT-platformRect4Rand

        currlevel=level
    meteor_timer+=1
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()