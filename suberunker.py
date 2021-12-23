import pygame
import random
import os

####################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width,screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("똥피하기")

# FPS
clock = pygame.time.Clock()
####################################################################################

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 폰트 등)

# 현재 파일 위치 
current_path = os.path.dirname(__file__)

# 캐릭터
character = pygame.image.load(os.path.join(current_path, "character_R.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height
character_speed = 0.6
to_x = 0


# 똥
enemy = pygame.image.load(os.path.join(current_path, "enemy.png"))
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0,screen_width - enemy_width)
enemy_y_pos = 0 
enemy_speed = 0.4

# 폰트 정의
game_font = pygame.font.Font(None, 40) # (폰트, 크기)

# 총 시간
total_time = 60

# 시작 시간 정보
start_ticks = pygame.time.get_ticks()

running = True
while running:
    dt = clock.tick(30)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 3. 캐릭터 위치 조작

        # 캐릭터 좌우 조작
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
                character = pygame.image.load(os.path.join(current_path, "character_L.png"))
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed
                character = pygame.image.load(os.path.join(current_path, "character_R.png"))


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0

    # 똥 재생
    if enemy_y_pos >= screen_height - enemy_height:
        enemy_x_pos = random.randint(0,481 - enemy_width)
        enemy_y_pos = 0 

    # 캐릭터 위치 조정
    character_x_pos += to_x * dt
    enemy_y_pos  += enemy_speed * dt

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width  - character_width :
        character_x_pos = screen_width  - character_width

    # 4. 충돌 처리

    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    if character_rect.colliderect(enemy_rect):
        print("충돌했어요")
        running = False

    # 5. 화면에 그리기
    screen.fill((255,255,255))
    screen.blit(character,(character_x_pos, character_y_pos))
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))

    # 타이머
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

    timer = game_font.render(str(int(total_time - elapsed_time)), True, (0,0,0))

    # 출력할 내용, True, 글자 색상
    screen.blit(timer, (10,10))

    if total_time - elapsed_time <= 0:
        print("타임아웃")
        running = False
    
    # 게임 화면 다시 그리기
    pygame.display.update()

pygame.quit()
