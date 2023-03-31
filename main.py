import pygame
from random import randint

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Flappy Bird game')
pygame.display.set_icon(pygame.image.load('картинки/иконки/icon.png'))

font1 = pygame.font.Font('шрифты/technofosiano.ttf', 35)
game_over = pygame.image.load('картинки/спрайты/gameover.png')

imgInstruc = pygame.image.load('картинки/инструкция/инструкция.png')
imgBG = pygame.image.load('картинки/спрайты/background-day.png')
imgBirdMidl = pygame.image.load('картинки/спрайты/midl.png')
imgBirdUp = pygame.image.load('картинки/спрайты/up.png')
imgBirdDown = pygame.image.load('картинки/спрайты/down.png')
imgPT = pygame.image.load('картинки/спрайты/верхняя.png')
imgPB = pygame.image.load('картинки/спрайты/нижняя.png')

sndPoint = pygame.mixer.Sound('звуки/каждые_100_очков.wav')
sndFall = pygame.mixer.Sound('звуки/столкновение.ogg')
sndMusic = pygame.mixer.music.load('звуки/music.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)


py, sy, ay = HEIGHT // 2, 0, 0
player = pygame.Rect(WIDTH // 3, py, 34, 24)
frame = 0

state = 'start'
timer = 10000
pliv = 1

pipes = []
bgs = []
pipesScores = []
pipeSpeed = 3
pipeGateSize = 200
pipeGatePos = HEIGHT //2

bgs.append(pygame.Rect(0, 0, 288, 600))

lives = 3
scores = 0

GAMEOVER = False
instruc = False

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False

    press = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    if timer > 0:
        timer -= 1

    frame = (frame + 0.2) % 4
    pipeSpeed = 3 + scores // 100

    for i in range(len(bgs) - 1, -1, -1):
        bg = bgs[i]
        bg.x -= pipeSpeed // 2

        if bg.right < 0:
            bgs.remove(bg)

        if bgs[len(bgs) - 1].right <= WIDTH:
            bgs.append(pygame.Rect(bgs[len(bgs) - 1].right, 0, 288, 600))

    for i in range(len(pipes) - 1, -1, -1):
        pipe = pipes[i]
        pipe.x -= pipeSpeed

        if pipe.right < 0:
            pipes.remove(pipe)
            if pipe in pipesScores:
                pipesScores.remove(pipe)

    if state == 'start':
        if pliv == 1:
            imgInstrucRect = imgInstruc.get_rect(center=(WIDTH//2, HEIGHT//2))
            instruc = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if imgInstrucRect.collidepoint(pygame.mouse.get_pos()):
                    timer = 0
            if timer == 0:
                instruc = False
        if click and timer == 0 and len(pipes) == 0:
            state = 'play'

        py += (HEIGHT // 2 - py) * 0.1
        player.y = py

    elif state == 'play':
        pliv = 2
        if click:
            ay = -2
        else:
            ay = 0
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if len(pipes) == 0 or pipes[len(pipes)-1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 52, pipeGatePos - pipeGateSize // 2))
            pipes.append(pygame.Rect(WIDTH, pipeGatePos + pipeGateSize // 2, 52, HEIGHT - pipeGatePos + pipeGateSize // 2))

            pipeGatePos += randint(-100, 100)
            if pipeGatePos < pipeGateSize:
                pipeGatePos = pipeGateSize
            elif pipeGatePos > HEIGHT - pipeGateSize:
                pipeGatePos = HEIGHT - pipeGateSize

        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'

        for pipe in pipes:
            if player.colliderect(pipe):
                state = 'fall'

            if pipe.right < player.right and pipe not in pipesScores:
                pipesScores.append(pipe)
                scores += 5
                if scores % 10:
                    sndPoint.play()

    elif state == 'fall':
        sndFall.play()
        sy, ay = 0, 0
        pipeGatePos = HEIGHT // 2

        lives -= 1
        if lives > 0:
            state = 'start'
            timer = 60
        else:
            state = 'game over'
            timer = 60

    else:
        py += sy
        sy = (sy + ay + 1) * 0.98
        player.y = py

        if timer == 0:
            game_over_rect = game_over.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            GAMEOVER = True
            if keys[pygame.K_SPACE] or keys[pygame.K_RETURN]:
                py, sy, ay = HEIGHT // 2, 0, 0
                player = pygame.Rect(WIDTH // 3, py, 34, 24)
                frame = 0
                state = 'start'
                timer = 10
                pipes = []
                lives = 3
                scores = 0
                GAMEOVER = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_over_rect.collidepoint(pygame.mouse.get_pos()):
                    py, sy, ay = HEIGHT // 2, 0, 0
                    player = pygame.Rect(WIDTH // 3, py, 34, 24)
                    frame = 0
                    state = 'start'
                    timer = 10
                    pipes = []
                    lives = 3
                    scores = 0
                    GAMEOVER = False

    window.fill(pygame.Color('black'))

    for bg in bgs:
        window.blit(imgBG, bg)

    for pipe in pipes:
        if pipe.y == 0:
            rect = imgPT.get_rect(bottomleft=pipe.bottomleft)
            window.blit(imgPT, rect)
        else:
            rect = imgPB.get_rect(topleft=pipe.topleft)
            window.blit(imgPB, rect)


    if int(frame) == 1:
        image = imgBirdDown
    elif int(frame) == 2 :
        image = imgBirdMidl
    elif int(frame) == 3:
        image = imgBirdUp
    else:
        image = imgBirdMidl

    image = pygame.transform.rotate(image, -sy * 2)
    window.blit(image, player)

    text = font1.render('scores: ' + str(scores), 0, pygame.Color('black'))
    window.blit(text, (10, 10))

    text1 = font1.render('lives: ' + str(lives), 0, pygame.Color('black'))
    window.blit(text1, (WIDTH - 180, 10))

    if instruc:
        window.blit(imgInstruc, imgInstrucRect)

    if GAMEOVER:
        window.blit(game_over, game_over_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.QUIT