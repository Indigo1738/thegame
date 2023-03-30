import pygame

pygame.init()
pygame.font.init()

WIDTH,HEIGHT=500,900
WIN=pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("WARIOR ANGEL")
FPS=60
BACKGROUND = pygame.transform.scale(pygame.image.load('spacework2.jpg'),(HEIGHT,WIDTH))

BLACK=(0,0,0)
yellow = (255,255,0)
red1 = (255,0,0)

velocity=5
BULLET_VELOCITY=7
MAX_BUll= 3

red_hit = pygame.USEREVENT + 1
black_hit = pygame.USEREVENT + 2

BORDER=pygame.Rect(HEIGHT//2-5 , 0,10,HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 80)
spaceship_height,spaceship_width=120,100

BLACK_SPACE=pygame.image.load('myspace18.png')
BLACK_SPACE=pygame.transform.rotate(pygame.transform.scale(BLACK_SPACE,(spaceship_height,spaceship_width)),90)

RED_SPACE=pygame.image.load('redspace5.png')
RED_SPACE=pygame.transform.rotate(pygame.transform.scale(RED_SPACE,(spaceship_height,spaceship_width)),-90)

def handle_bullet(red_bullets,black_bullets,black,red):
    for bullet in red_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(black_hit))
            red_bullets.remove(bullet)
        elif bullet.x > WIN.get_width():
            red_bullets.remove(bullet)

    for bullet in black_bullets:
        bullet.x -= BULLET_VELOCITY
        if black.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            black_bullets.remove(bullet)
        elif bullet.x < 0:
            black_bullets.remove(bullet)

def black_handle_movement(keys_pressed,black):
    if keys_pressed[pygame.K_RIGHT] and black.x + velocity + black.width < WIN.get_width():  # right
        black.x += velocity
    if keys_pressed[pygame.K_LEFT] and black.x - velocity > BORDER.x + BORDER.width:  # left
        black.x -= velocity
    if keys_pressed[pygame.K_UP] and black.y - velocity >0:  # UP
        black.y -= velocity
    if keys_pressed[pygame.K_DOWN] and black.y + velocity + black.height<WIDTH - 20:  # down
        black.y += velocity

def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_a] and red.x-velocity>0:  # right
        red.x -= velocity
    if keys_pressed[pygame.K_d] and red.x + velocity + red.width < BORDER.x:  # left
        red.x += velocity
    if keys_pressed[pygame.K_w] and red.y + velocity > 0:  # UP
        red.y -= velocity
    if keys_pressed[pygame.K_s] and red.y + velocity + red.height < BORDER.x + 35:  # down
        red.y += velocity

def draw_window(red,black,red_bullets,black_bullets,red_health,black_health):
    #wind_color=(238,130,238)
    #WIN.fill(wind_color)
    WIN.blit(BACKGROUND,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)

    red_health_text = HEALTH_FONT.render("LIFE::"+str(red_health), 1, (255,255,255))
    black_health_text = HEALTH_FONT.render("LIFE::"+str(black_health), 1, (255,255,255))
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-300,10))
    WIN.blit(black_health_text,(700,10))

    WIN.blit(BLACK_SPACE,(black.x,black.y))
    WIN.blit(RED_SPACE,(red.x,red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN,red1,bullet)

    for bullet in black_bullets:
        pygame.draw.rect(WIN,yellow,bullet)

    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,(255,255,255))
    WIN.blit(draw_text,(WIDTH//2-draw_text.get_width()//2+200,HEIGHT//2-draw_text.get_height()//2))

    pygame.display.update()
    pygame.time.delay(8000)

def main():
    red=pygame.Rect(100,300,spaceship_height,spaceship_width)
    black=pygame.Rect(700,300,spaceship_height,spaceship_width)
    red_bullets= []
    black_bullets= []

    black_health = 10
    red_health = 10

    clock=pygame.time.Clock()

    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()

            if event.type== pygame.KEYDOWN:
                if event.key== pygame.K_LCTRL and len(red_bullets) < MAX_BUll:
                    bullet=pygame.Rect(red.x + red.width, red.y + red.height//2-2, 10, 5)
                    red_bullets.append(bullet)

                if event.key== pygame.K_RCTRL and len(black_bullets) < MAX_BUll:
                    bullet2=pygame.Rect(black.x, black.y + black.height//2-2, 10, 5)
                    black_bullets.append(bullet2)

            if event.type == black_hit:
                black_health -= 1
            if event.type == red_hit:
                red_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Black player wins"

        if black_health <= 0:
            winner_text = "Red player wins"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed=pygame.key.get_pressed()
        black_handle_movement(keys_pressed,black)
        handle_bullet(red_bullets,black_bullets,red,black)
        red_handle_movement(keys_pressed,red)
        draw_window(red,black,red_bullets,black_bullets,red_health,black_health)

    main()

if __name__=='__main__':
    main()

