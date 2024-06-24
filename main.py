import pygame
import random

pygame.init()

# Ustawienia ekranu
screen_w = 1280
screen_h = 720
main_block_h = 100
main_block_w = 400

current_score = 0
num_blocks = 1
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption('Build a Wall!')

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(f'Current high score: {current_score}', True, "black", "blue")
textRect = text.get_rect()
textRect.center = (190, 30)
clock = pygame.time.Clock()
running = True

background_color = (153, 217, 243)

def generate_random():
    return random.randint(0, 1000000)

class BuildingBlock:
    def __init__(self, x, y, velocity_x, velocity_y, highest_y=None, leftest_x=None) -> None:
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, main_block_w, main_block_h)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.highest_y = highest_y
        self.leftest_x = leftest_x
        self.stopped = False

    def drawRect(self, screen):
        pygame.draw.rect(screen, "brown", self.rect)

    def set_velocity(self, vel_x, vel_y):
        self.velocity_x = vel_x
        self.velocity_y = vel_y

    def change_y(self, Y):
        #self.y += Y
        #self.rect.y += Y
        pass

    def moveRect(self):
        global current_score, running
        self.x += self.velocity_x
        self.rect.x = self.x

        self.y += self.velocity_y
        self.rect.y = self.y

        if self.x < 0 or self.x + main_block_w > screen_w:
            self.velocity_x = -self.velocity_x

    def check_collision(self):
        global running, current_score
        if self.velocity_y != 0:
            if self.y == self.highest_y and self.x + main_block_w - self.leftest_x > 0:
                self.velocity_y = 0
                self.stopped = True
                current_score += 1
            elif self.y > self.highest_y + main_block_h:
                running = False

main_block = BuildingBlock(x=screen_w // 2 - main_block_w // 2, y=screen_h - main_block_h, velocity_x=0, velocity_y=0, highest_y=screen_h - main_block_h, leftest_x=screen_w // 2 - main_block_w // 2)
block1 = BuildingBlock(x=main_block_w, y=screen_h // 6, velocity_x=5, velocity_y=0, highest_y=screen_h - main_block_h - main_block_h, leftest_x=screen_w // 2 - main_block_w // 2)
curr_y = screen_h - main_block_h
curr_x = screen_w // 2 - main_block_w // 2
blocks_to_draw = [main_block]
current_block = block1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_color)
    text = font.render(f'Current high score: {current_score}', True, "black", "blue")
    screen.blit(text, textRect)

    for i in blocks_to_draw:
        i.drawRect(screen)

    current_block.moveRect()
    current_block.drawRect(screen)

    if pygame.mouse.get_pressed(3)[0]:
        current_block.set_velocity(0, 20)
        current_block.stopped = False
    current_block.check_collision()
    
    if current_block.stopped and current_block.velocity_y == 0:
        current_block.highest_y -= main_block_h
        curr_y = current_block.highest_y
        curr_x = current_block.x
        blocks_to_draw.append(current_block)

        new_block = BuildingBlock(x=main_block_w, y=screen_h // 6, velocity_x=5, velocity_y=0, highest_y=curr_y, leftest_x=curr_x)
        current_block = new_block
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
