import pygame, sys, math

pygame.init()
clock = pygame.time.Clock()

screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Projectile Motion")

base_font = pygame.font.SysFont("Arial", 20)
velocity_label = "Velocity (m/s): "
angle_label = "Angle : "

velocity_value = ""
angle_value = ""

inputV_rect = pygame.Rect(screen_width - 120, 5, 100, 30)
inputA_rect = pygame.Rect(screen_width - 120, 42, 100, 30)
color_active = pygame.Color((88, 196, 221))
color_passive = pygame.Color((40, 80, 95))
color = color_passive

active_v = False
active_a = False


#POSITION  [ 1 px = 100 Metre ]
pos_x = 20
pos_y = screen_height - 20

#THETA
angle = 70
angle_rad = math.radians(angle)

#VELOCITY
v = 25
v_x = 0
v_y = 0



#GRAVITY
g=9.8

#RANGE
range_m = (v*v * math.sin(2 * angle_rad)) / g

#MAX_HEIGHT
h = (v**2 * math.sin(angle_rad)**2) / (2 * g)

#MARGIN
LEFT_MARGIN = 40
BOTTOM_MARGIN = 40

#SCALE
GRID = 20    #pixels
METERS_PER_GRID = 5 #20px = 5 m 
"""visible_grids = (screen_width - 40) // GRID
METERS_PER_GRID = max(1, int(range_m / visible_grids))"""


font = pygame.font.SysFont("Segoe UI", 14)

origin_x = 40
origin_y = screen_height - 40

path = []                
p = False
landed = False
t=0
launched = False 
screen_x = origin_x
screen_y = origin_y
radius = 20
   

while True:
    dt = clock.tick(60)/1000
    screen.fill((12, 12, 15))
    
    #EVENT LOOP
#----------------------------------------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if inputV_rect.collidepoint(event.pos):
                active_v = True
            else:
                active_v = False    
                
            if inputA_rect.collidepoint(event.pos):
                active_a = True
            else:
                active_a = False
        
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE and not launched:
                if velocity_value == "":
                    velocity_value = "30"
                if angle_value == "":
                    angle_value = "45"
                v = int(velocity_value)
                angle = int(angle_value)
                angle_rad = math.radians(angle)
                h = (v**2 * math.sin(angle_rad)**2) / (2 * g) 
                range_m = (v**2 * math.sin(2 * angle_rad)) / g
                h_x = v_x * (v_y / g)
                v_x = v * math.cos(angle_rad)
                v_y = v * math.sin(angle_rad)
                h_x = (v * math.cos(angle_rad)) * (v * math.sin(angle_rad) / g)
                h_x = v_x * (v_y/g)
                screen_x = origin_x
                screen_y = origin_y
                launched = True
                
            if event.key == pygame.K_r:
                launched = False
                landed = False
                t = 0
                path = []
                screen_x = origin_x
                screen_y = origin_y
                p = False
                
            if active_v == True:
                if event.key == pygame.K_BACKSPACE:
                    velocity_value = velocity_value[:-1]
                else:
                    velocity_value += event.unicode
                    
            if active_a == True:
                if event.key == pygame.K_BACKSPACE:
                    angle_value = angle_value[:-1]
                else:
                    angle_value += event.unicode
                
            
        """if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                METERS_PER_GRID = max(1, METERS_PER_GRID-1)
            
            if event.y < 0:
                METERS_PER_GRID += 1"""
 #-----------------------------------------------------------------------------------------------------------
                
    if launched and landed == False:
        t += dt
        x_m = v_x * t
        y_m = v_y * t - 0.5 * g * t * t
        if y_m <= 0:
            y_m = 0
            landed = True
        
        pixel_per_meter = GRID / METERS_PER_GRID
        screen_x = origin_x + x_m * pixel_per_meter
        screen_y = origin_y - y_m * pixel_per_meter

        path.append((int(screen_x), int(screen_y)))
        
    x_count = 0
    for x in range(origin_x, screen_width, GRID):
        value = x_count * METERS_PER_GRID
        text = font.render(str(value), True, (200, 200, 200))#NUMBERINGS
        if value % 20 == 0:
            screen.blit(text, (x-5, origin_y + 5))
        x_count += 1
        
    y_count = 0
    for y in range(origin_y, 0, -GRID):
        value = y_count * METERS_PER_GRID
        text = font.render(str(value), True, (200, 200, 200))#NUMBERINGS
        if value % 20 == 0:
            screen.blit(text, (origin_x - 30, y - 5))
        y_count += 1

    
    for x in range(60, screen_width, 20):
        pygame.draw.line(screen, (68, 68, 68), (x, 0),(x, screen_height-40), 2)#GRIDS
    for y in range(20, screen_height-40, 20):
        pygame.draw.line(screen, (68, 68, 68), (40, y),(screen_width, y), 2)    #GRIDS
    
     
    if len(path) > 1:
        pygame.draw.lines(screen, (88, 196, 221), False, path, 2)
    
    if landed and p == False:
        print("*" * 80)    
        print("Range (theory):", range_m)
        print("Range (sim):", x_m)
        print("MAXIMUM Height:", h)
        print("*" * 80)  
        screen_h_x = origin_x + h_x * pixel_per_meter
        screen_h_y = origin_y - h * pixel_per_meter 
        
        p = True

    if landed:
        pygame.draw.line(screen,(255, 200, 80),(screen_h_x, screen_h_y),(screen_h_x, origin_y),2)
        screen_y = origin_y - radius
        range_text = base_font.render(f"Range : {round(range_m, 2)} m", True, (255, 200, 80))
        MAX_h_text = base_font.render(f"MAX Height : {round(h, 2)} m", True, (255, 200, 80))
        screen.blit(range_text, (screen_width - 190, 82))
        screen.blit(MAX_h_text, (screen_width - 235, 122))
        T = (2 * v * math.sin(angle_rad))/g
        TF_text = base_font.render(f"Time Of Flight : {round(T, 2)} sec", True, (255, 200, 80))
        screen.blit(TF_text, (screen_width - 255, 162))
        
    if active_v:
        colorV = color_active
    else:
        colorV = color_passive
        
    if active_a:
        colorA = color_active
    else:
        colorA = color_passive
    
    
    circle = pygame.draw.circle(screen, (255, 214, 70), (int(screen_x), int(screen_y)), radius, 0 )
    pygame.draw.line(screen, (136, 136, 136), (40, 0),(40, screen_height ), 2)                          #Y AXIS
    pygame.draw.line(screen, (136, 136, 136), (0, screen_height-40),(screen_width, screen_height-40), 2)#X AXIS
    
    text_v = base_font.render(velocity_label, True, (200, 220, 210))
    text_a = base_font.render(angle_label, True, (200, 220, 210))
    screen.blit(text_v, (screen_width-250, 10))
    screen.blit(text_a, (screen_width-185, 42))
    
    text_v_value = base_font.render(velocity_value, True, (88, 196, 221))
    text_a_value = base_font.render(angle_value, True, (88, 196, 221))
    
    screen.blit(text_v_value, (inputV_rect.x + 5, inputV_rect.y + 5))
    screen.blit(text_a_value, (inputA_rect.x + 5, inputA_rect.y + 5))

    pygame.draw.rect(screen, colorV, inputV_rect, 2)
    pygame.draw.rect(screen, colorA, inputA_rect, 2)
    
    pygame.display.flip()

