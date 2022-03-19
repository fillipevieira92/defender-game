import pygame
from time import sleep
from pygame import font
from pygame.locals import *
from random import randint
from datetime import datetime
import databaser as db
from sys import exit



pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_TEXT = pygame.Surface((1200,150))
SCREEN_TEXT.fill((30,30,30))


FONT = pygame.font.Font('freesansbold.ttf', 20)


class Player:

    PLAYER_X = 0
    PLAYER_Y = 400

    def __init__(self):

        self.rect = pygame.Rect(self.PLAYER_X, self.PLAYER_Y, 50, 50)
        self.player_surface = pygame.Surface((50,50))
        self.player_surface.fill((255,255,255))
        self.player_life = 3
                 
    def draw(self, SCREEN):
        SCREEN.blit(self.player_surface, (self.rect.x, self.rect.y))     


class Enemy:

    ENEMY_X = 1200    

    def __init__(self):

        self.rect = pygame.Rect(self.ENEMY_X, randint(160,550), 50, 50)
        self.enemy_surface = pygame.Surface((50,50))
        self.enemy_surface.fill((255,0,0))
                 
    def draw(self, SCREEN):
        SCREEN.blit(self.enemy_surface, (self.rect.x, self.rect.y))


class Bullet:

    def __init__(self, shooter_x, shooter_y):

        self.rect = pygame.Rect(shooter_x, shooter_y+20, 10, 10)
        self.bullet_surface = pygame.Surface((10,10))
        self.bullet_surface.fill((255,255,0))
    
    def draw(self, SCREEN):
        SCREEN.blit(self.bullet_surface, (self.rect.x, self.rect.y))


class Text:
    
    def __init__(self, text):
        self.text = text
        
    
    def input_name(self):
        
        self.font = pygame.font.Font(None, 32)
        self.alert = pygame.font.Font(None, 22)

        self.input_box = pygame.Rect(480,350, 150, 32)
        self.input_color = ((200,200,20))
        alert_txt = self.alert.render('* Five digits', True, self.input_color)
        
        if self.text == '':
            txt_surface = self.font.render('Enter player name...', True, self.input_color)
        else:
            txt_surface = self.font.render(self.text, True, self.input_color)

        if len(self.text ) < 5:
            SCREEN.blit(alert_txt, (480,390))

        width = max(200, txt_surface.get_width()+10)
        self.input_box.w = width
        SCREEN.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        pygame.draw.rect(SCREEN, self.input_color, self.input_box, 2)
        
    def stage_text(self):

        stage_txt_font = pygame.font.Font(None, 55)
        stage_num_font = pygame.font.Font('freesansbold.ttf', 70)

        text_w = stage_txt_font.render('STAGE', True, (255,255,255))
        stage_n = stage_num_font.render(f'{self.text}', True, (255,0,0))
        SCREEN.blit(text_w, (540, 30))
        SCREEN.blit(stage_n, (590, 70))

    def score(self):
        text_w = FONT.render(f'SCORE:  {self.text}', True, (255, 255, 255))
        SCREEN.blit(text_w, (25,35))

    def game_speed(self):
        text_w = FONT.render(f'GAME SPEED:  {self.text}', True, (255, 255, 255))
        SCREEN.blit(text_w, (25,110))
    
    def player_name(self):
        text_w = FONT.render(f'PLAYER:  {self.text}', True, (255, 255, 255))
        SCREEN.blit(text_w, (25,10))
    
    def home_screen(self):

        defender_font = pygame.font.Font('freesansbold.ttf', 100)

        text_defender = defender_font.render('DEFENDER', True, (255, 0, 0))
        text_press = FONT.render('Press SPACE', True, (255, 255, 255))
        SCREEN.blit(text_defender, (330,200))
        SCREEN.blit(text_press, (530,500))
    
    def game_over(self):

        gameOver_font = pygame.font.Font('freesansbold.ttf', 100)

        text_gameOver = gameOver_font.render('GAME-OVER', True, (255, 0, 0))
        text_score = FONT.render(f'SCORE: {self.text}', True, (255, 255, 255))
        text_return = FONT.render(f'Press SPACE to try again', True, (255, 255, 255))
        SCREEN.blit(text_gameOver, (275,200))
        SCREEN.blit(text_score, (550,330))
        SCREEN.blit(text_return, (470,500))
    
    def records(self, top_five):

        records_font = pygame.font.Font('freesansbold.ttf', 15)
        top_x = 1000
        top_y = 5
        
        for i, row in enumerate(top_five):
            top_y += 20
            player_name = row['player_name']
            player_score = row['player_score']
            left = records_font.render(f'{i+1}º -', True, (255, 255, 255))
            SCREEN.blit(left, (top_x, top_y))
            center = records_font.render(player_name, True, (255, 255, 255))
            SCREEN.blit(center, (top_x + 30, top_y))
            right = records_font.render(f'{player_score} PTS', True, (255, 255, 255))
            SCREEN.blit(right, (top_x + 125, top_y))        


class Game:

    def __init__(self):
        self.players = [Player()]
        self.enemys = []
        self.players_bullets = []
        self.enemys_bullets = []

        self.R = 20
        self.G = 20
        self.B = 20
        
        self.night = True
        self.danger = False

        self.score = 0
        self.aux_enemy = 0
        self.aux_bullet = 0
        self.speed = 20
        self.frames = 0
        self.stage = 1

        self.clock = pygame.time.Clock()


    def home_screen(self):
        
        self.record()
        homeScreen = True
        self.user_name = ''
        while homeScreen:
            
            self.clock.tick(20)
            SCREEN.fill((20,20,80))
            welcome_text = Text('welcome')
            welcome_text.home_screen()
            self.user_name = self.user_name.upper()
            input_txt = Text(self.user_name)
            input_txt.input_name()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                elif event.type == KEYDOWN:
                    
                    if event.key == K_BACKSPACE and len(self.user_name) >= 0:
                        self.user_name = self.user_name[:-1]
                    else:
                        if event.key != K_SPACE and len(self.user_name) < 5:
                            self.user_name += event.unicode
                    if len(self.user_name) == 5:
                        if event.key == K_SPACE:
                            homeScreen = False
                            self.main_loop() 
            
            pygame.display.flip()
    

    def game_over(self):
        
        gameOverScreen = True
        
        while gameOverScreen:
            
            self.clock.tick(20)
            SCREEN.fill((20,20,80))
            gameOver_text = Text(self.score)
            gameOver_text.game_over()            
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        gameOverScreen = False                    
        
            pygame.display.flip()
        
        db.cursor.execute('INSERT INTO records(name, score) VALUES(?,?);', (self.user_name, str(self.score).zfill(3)))
        db.conn.commit()
        
        self.record()
        self.__init__()
        self.main_loop()


    def main_loop(self):
        
        while True:
            
            self.clock.tick(self.speed)
            self.screen_color()
            self.colissions()
            self.stages()
            
            SCREEN.blit(SCREEN_TEXT, (0,0))

            self.frames += 1
            
            name = Text(self.user_name) # Exemple
            name.player_name()

            top_records = Text('')
            top_records.records(self.top_five)
            score_print = Text(str(self.score).zfill(3))
            score_print.score()
            game_speed_print = Text(str(self.speed).zfill(3))
            game_speed_print.game_speed()
            stage_txt = Text(self.stage)
            stage_txt.stage_text()

            self.get_event()

            microsecond = str(datetime.now().microsecond)[0]
            player = self.players[0]
            
            if self.frames % 100 == 0:
                self.speed+=1
                
            
            if microsecond == '9':
                self.aux_enemy += 1
                self.aux_bullet += 1
            
            if self.aux_bullet == 3:
                if len(self.enemys) != 0:
                    for enemy in self.enemys:
                        bullet_x = enemy.rect.x
                        bullet_y = enemy.rect.y
                        self.enemys_bullets.append(Bullet(bullet_x, bullet_y))
                self.aux_bullet = 0
            
            if self.aux_enemy == 10:
                self.enemys.append(Enemy())
                self.aux_enemy = 0

            

            player.draw(SCREEN)
            pygame.display.flip()


    def stages(self):
        
        if self.speed == 45:
            self.stage = 2
        
        elif self.speed == 70:
            self.stage = 3
        


    def screen_color(self):

        if self.B >= 80:
            self.night = False

        if self.B <= 20:
            self.night = True
        
        if not self.danger:
            self.R = 20
            if self.night:
                self.B += 0.1
            else:
                self.B -= 0.1

        if self.danger:
            if self.R < 70:
                self.R += 0.2
        
        SCREEN.fill((self.R,self.G, self.B))


    def get_event(self):

        player = self.players[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.stage == 1:
                        self.players_bullets.append(Bullet(player.rect.x+20, player.rect.y))
                    
                    elif self.stage == 2:
                        self.players_bullets.append(Bullet(player.rect.x+20, player.rect.y-20))
                        self.players_bullets.append(Bullet(player.rect.x+20, player.rect.y+20))

                    elif self.stage == 3:
                        self.players_bullets.append(Bullet(player.rect.x+20, player.rect.y))
                        self.players_bullets.append(Bullet(player.rect.x+20, player.rect.y-20))
                        self.players_bullets.append(Bullet(player.rect.x+20, player.rect.y+20))
                    
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if player.rect.y >= 160:
                player.rect.y -= 10
            
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if player.rect.y <= SCREEN_HEIGHT - player.rect.width - 10:
                player.rect.y += 10
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if player.rect.x >= 10:
                player.rect.x -= 10

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if player.rect.x <= 300:
                player.rect.x += 10

    def record(self):
        
        data = db.cursor.execute('SELECT * FROM records;')
        records = []
        for row in data:
            records.append({'player_id':row[0], 'player_name':row[1], 'player_score':row[2]})
        
        self.top_five = sorted(records, key=lambda d: d['player_score'], reverse=True)[:5]

    
    def colissions(self):
        
        if self.enemys:
            if self.enemys[0].rect.x < 600:
                self.danger = True
            if self.enemys[0].rect.x > 600:
                self.danger = False

        for enemy in self.enemys:
            if enemy.rect.x > 0:
                enemy.rect.x -= 2
            else:
                self.game_over()
            enemy.draw(SCREEN)            
        
        for bullet in self.players_bullets:
            if bullet.rect.x < SCREEN_WIDTH:
                bullet.rect.x += 15
            else:
                try:
                    self.players_bullets.remove(bullet)
                except:
                    continue
            
            bullet.draw(SCREEN)
            for enemy in self.enemys:
                if bullet.rect.colliderect(enemy.rect):
                    try:
                        self.enemys.remove(enemy)
                    except:
                        continue
                    self.score+=1            
                    try:
                        self.players_bullets.remove(bullet)
                    except:
                        continue

            for enemy_bullet in self.enemys_bullets:
                if bullet.rect.colliderect(enemy_bullet.rect):
                    try:
                        self.enemys_bullets.remove(enemy_bullet)
                    except:
                        continue
                    try:
                        self.players_bullets.remove(bullet)
                    except:
                        continue


        for bullet in self.enemys_bullets:
            if bullet.rect.x > 0:
                bullet.rect.x -= 15
            else:
                try:
                    self.enemys_bullets.remove(bullet)
                except:
                    continue

            bullet.draw(SCREEN)
            for player in self.players:
                if bullet.rect.colliderect(player.rect):
                    sleep(1)
                    self.game_over()


if __name__ == '__main__':
    game = Game()
    game.home_screen()
