#!/usr/lib/python3
import pygame as py

clock = py.time.Clock()

py.init()
screen = py.display.set_mode((640, 480))
py.display.set_caption('First_game')
icon = py.image.load('images/logo.png').convert_alpha()
py.display.set_icon(icon)

bg = py.image.load('images/bg.png').convert_alpha()
zombie = py.image.load('images/zombie.png').convert_alpha()
zombie = py.transform.scale(zombie, (65,65))
zombie_x = 645  
zombie_y = 380
zombie_list_in_game = [] 

walk_left = [
    py.image.load('images/player_left/pygame_left_1.png').convert_alpha(),
    py.image.load('images/player_left/pygame_left_2.png').convert_alpha(),
    py.image.load('images/player_left/pygame_left_3.png').convert_alpha(),
    py.image.load('images/player_left/pygame_left_4.png').convert_alpha(),
    py.image.load('images/player_left/pygame_left_5.png').convert_alpha(),
    py.image.load('images/player_left/pygame_left_6.png').convert_alpha(),
]
walk_right = [
    py.image.load('images/player_right/pygame_right_1.png').convert_alpha(),
    py.image.load('images/player_right/pygame_right_2.png').convert_alpha(),
    py.image.load('images/player_right/pygame_right_3.png').convert_alpha(),
    py.image.load('images/player_right/pygame_right_4.png').convert_alpha(),
    py.image.load('images/player_right/pygame_right_5.png').convert_alpha(),
    py.image.load('images/player_right/pygame_right_6.png').convert_alpha(),
]

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 150
player_y = 370
is_jump = False
jump_count = 8

bg_sound = py.mixer.Sound('sounds/bg_s2.mp3')
bg_sound.play()

gameplay = True
label = py.font.Font('fonts/Sono-ExtraLight.ttf', 100)
label_mini_text = py.font.Font('fonts/Sono-ExtraLight.ttf', 20)
lose_label = label.render('You lose!', False, (193,196,199))
restart_label = label.render('Play again', False, (115,132,148))
restart_label_rect = restart_label.get_rect(topleft=(50,200))

bullets_left = 5
bullet = py.image.load('images/bullet.png').convert_alpha()
bullet = py.transform.scale(bullet, (15,15))
bullets = []

magazine = py.transform.scale(bullet, (45,45))
magazines = []

heart = py.image.load('images/heart.png').convert_alpha()
heart = py.transform.scale(heart, (45,45))
hearts = []

zombie_time = py.USEREVENT + 1
py.time.set_timer(zombie_time, 2500)

bullet_time = py.USEREVENT + 2
py.time.set_timer(bullet_time, 10000)

heart_time = py.USEREVENT + 3
py.time.set_timer(heart_time, 15000)

score = 0
health = 3
running = True
screen.fill((30, 199, 35))
while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 640, 0))
    if gameplay:
        health_label =  label_mini_text.render(f'health: {health}', False, (193,196,199))
        score_label =  label_mini_text.render(f'score: {score}', False, (193,196,199))
        bullets_label =  label_mini_text.render(f'bullets left: {bullets_left}', False, (193,196,199))
        screen.blit(health_label, (15, 15))
        screen.blit(score_label, (15, 40))
        screen.blit(bullets_label, (15, 65))
        score +=1
        player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))
        
        if zombie_list_in_game:
            for (i, el) in enumerate(zombie_list_in_game):
                screen.blit(zombie, el)
                el.x -=10
                
                if el.x < -10:
                    zombie_list_in_game.pop(i)
                if player_rect.colliderect(el):
                    if health == 1:
                        gameplay = False
                    else:
                        zombie_list_in_game.pop(i)
                        health -=1
                    
        
        keys = py.key.get_pressed()
        # ! Анимация передвижения
        if keys[py.K_a]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
        # ! Логика передвижения
        if keys[py.K_a] and player_x > 50:
            player_x -= player_speed
        elif keys[py.K_d] and player_x < 400:
            player_x += player_speed
        # ! Логика прыжка
        if not is_jump:
            if keys[py.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count >0:
                    player_y -= (jump_count **2) /2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -=1
            else:
                is_jump = False
                jump_count = 8
        if player_anim_count == 5:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 20
        if bg_x == -640:
            bg_x = 0
        
        if bullets:
            for (i,el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 4
                if el.x > 640:
                    bullets.pop(i)
                
                if zombie_list_in_game:
                    for (index, zombie_el) in enumerate(zombie_list_in_game):
                        if el.colliderect(zombie_el):
                            zombie_list_in_game.pop(index)
                            bullets.pop(i)
        if magazines:
            for (i, el) in enumerate(magazines):
                screen.blit(magazine, (el.x, el.y))
                el.x -=12
                if player_rect.colliderect(el):
                    bullets_left += 3
                    magazines.pop(i)
                if el.x < 0:
                    magazines.pop(i)
        if hearts:
            for (i,el) in enumerate(hearts):
                # for (i2, el2) in enumerate(magazines):
                #     if el.colliderect(el2):
                #         screen.blit(heart, (el.x+el2.x, el.y))
                #     else:
                screen.blit(heart, (el.x, el.y))
                el.x -=20
                if el.colliderect(player_rect):
                    health +=1
                    hearts.pop(i)
                if el.x <0:
                    hearts.pop(i)
                    
    else:
        screen.fill((87,88,89))
        screen.blit(lose_label, (100,100))
        screen.blit(restart_label, restart_label_rect)
        score_label =  label.render(f'score: {score}', False, (193,196,199))
        screen.blit(score_label,(100,300))
        mouse = py.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and py.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            zombie_list_in_game.clear()
            bullets.clear()
            bullets_left = 5
            health = 3
            score = 0
            print(hearts)
    py.display.update()

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == zombie_time:
            zombie_list_in_game.append(zombie.get_rect(topleft=(zombie_x, zombie_y)))
        if event.type == bullet_time:
            magazines.append(magazine.get_rect(topleft=(zombie_x, zombie_y-55)))
        if event.type == heart_time:
            hearts.append(heart.get_rect(topleft=(zombie_x, zombie_y-55)))
        if gameplay and event.type == py.KEYUP and event.key == py.K_e and bullets_left >0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y+10)))
            bullets_left -=1
        
    clock.tick(25)
