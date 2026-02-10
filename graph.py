import pygame, sys, math

class lines(pygame.sprite.Sprite):
    def __init__(self, screen, spos, epos, color):
        super().__init__()
        self.screen = screen
        self.color = color
        self.spos= spos
        self.epos = epos
    
    def draw(self):
        pygame.draw.line(self.screen, self.color, self.spos, self.epos)




pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((800,800))
screen_width = screen.get_width()
screen_height = screen.get_height()





while True:
    
    screen.fill("silver")
    for x in range(60, screen_width, 20):
        pygame.draw.line(screen, (169,169,169), (x, 0),(x, screen_height-40), 2)
    for y in range(20, screen_height-40, 20):
        pygame.draw.line(screen, (100,100,100), (40, y),(screen_width, y), 2)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.draw.line(screen, "black", (40, 0),(40, screen_height), 2)
    pygame.draw.line(screen, "black", (0, screen_height-40),(screen_width, screen_height-40), 2)
    pygame.display.flip()
    clock.tick(60)