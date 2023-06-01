import pygame
import sys
import random
 
def game_floor():
    screen.blit(floor_base, (floor_x_pos, 900))
    screen.blit(floor_base, (floor_x_pos + 576, 900))


def check_collision(pipes):
    #collision with pipe
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            die_sound.play()
            can_score = True
            return False
    #check if floor is hit
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        can_score = True
        die_sound.play()
        return False
    return True


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos-300))
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)


def rotate_bird(bird_surface):
    new_bird = pygame.transform.rotozoom(bird_surface, -bird_movement * 4, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), False, (255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', False, (255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', False, (255,255,255))
        high_score_rect = score_surface.get_rect(center = (220,850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def pipe_score_check():
    global score, can_score
    if pipe_list:
        for pipe in pipe_list:
            if 99 < pipe.centerx < 101 and can_score:
                score += 1
                point_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True

pygame.init()   
clock = pygame.time.Clock()
#variables
gravity = 0.20
bird_movement = 0
screen = pygame.display.set_mode((576, 1024))
score = 0
high_score = 0
game_font = pygame.font.Font("Flappy/ABC.ttf",55)
can_score = True

background = pygame.image.load("Flappy/assets/backgroundday.png").convert()
background = pygame.transform.scale2x(background)

bird_downflap = pygame.transform.scale2x(pygame.image.load("Flappy/assets/bluebird-downflap.png")).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load("Flappy/assets/bluebird-midflap.png")).convert_alpha()
bird_upflap = pygame.transform.scale2x(pygame.image.load("Flappy/assets/bluebird-upflap.png")).convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird = bird_frames[bird_index]
bird_rect = bird.get_rect(center=(100,400))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

bird = pygame.image.load("Flappy/assets/bluebird-midflap.png").convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100,512))

floor_base = pygame.image.load("Flappy/assets/base.png").convert()
floor_base = pygame.transform.scale2x(floor_base)
floor_x_pos = 0

message = pygame.image.load("Flappy/assets/message.png").convert_alpha()
message = pygame.transform.scale2x(message)
game_over_rect = message.get_rect(center = (288, 512))

#building pipes
pipe_surface = pygame.image.load("Flappy/assets/pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400,450,500,550,600,650,700,750,800]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

flap_sound = pygame.mixer.Sound("Flappy/audio/wing.wav")
die_sound = pygame.mixer.Sound("Flappy/audio/die.wav")
hit_sound = pygame.mixer.Sound("Flappy/audio/hit.wav")
point_sound = pygame.mixer.Sound("Flappy/audio/point.wav")

game_active = True
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6.7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center = (100,512)
                bird_movement = 0
                pipe_list.clear()
                game_active = True
                score = 0
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index +=1
            else:
                bird_index = 0
            
            bird, bird_rect = bird_animation()

    screen.blit(background,(0, 0))
    if game_active:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        #Draw pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        pipe_score_check()
        score_display('main_game')

        #Check for Collision
        game_active = check_collision(pipe_list)
    else:
        high_score = update_score(score, high_score)
        score_display('game_over')
        screen.blit(message, game_over_rect)

    #Create Floor
    floor_x_pos -= 1
    game_floor()

    if floor_x_pos <= -576:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)
