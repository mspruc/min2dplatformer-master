from GameObject import *
from Player import *
import pygame
from Mediator import Mediator

class Enemy(GameObject):

    def __init__(self, screen, x_pos, y_pos, objectID, player):
        super().__init__(objectID ,pygame.math.Vector2(x_pos,y_pos))
        self.screen = screen
        self.objectID = objectID
        self.player = player

        self.enemy_img = pygame.image.load('sprites/enemy/enemy_mock.png')
        self.enemy_img.set_colorkey((253,77,211))


        self.x_pos = x_pos
        self.y_pos = y_pos
        self.enemy_speed = [1,0]
        self.enemy_rect = pygame.Rect(self.x_pos,self.y_pos,self.enemy_img.get_width(),self.enemy_img.get_height())
        
        ## Health Bar
        self.enemy_health = 100
        self.enemy_health_rect = pygame.Rect(0,0,16,6)
        self.enemy_health_rect_red = pygame.Rect(self.enemy_rect.x - self.player.get_player_scroll() + 1, self.enemy_rect.y - 11, 14, 2)
        self.enemy_health_rect_green = pygame.Rect(self.enemy_rect.x -self.player.get_player_scroll() + 1, self.enemy_rect.y - 11, (self.enemy_health/100)*14, 2)

    
    def get_rect(self):
        return self.enemy_rect
    
    def loop(self):

        if self.on_screen(self.enemy_rect, self.player):
            self.enemy_speed[1] += 0.2

            self.enemy_rect, collisions = self.object_check_collision_tiles(self.enemy_rect,self.enemy_speed)

            if collisions['bottom']:
                self.enemy_speed[1] = 0

            if collisions['left'] or collisions['right']:
                self.enemy_speed[0] *= -1

            if self.check_boundary(self.enemy_rect):
                self.enemy_speed[0] *= -1

            self.enemy_health_rect_red = pygame.Rect(self.enemy_rect.x - self.player.get_player_scroll() + 1, self.enemy_rect.y - 11, 14, 2)
            self.enemy_health_rect_green = pygame.Rect(self.enemy_rect.x -self.player.get_player_scroll() + 1, self.enemy_rect.y - 11, (self.enemy_health/100)*14, 2)



            if self.get_collision_bullet(self.enemy_rect):
                self.enemy_health -= 10
            
            if self.enemy_health <= 0:
                Mediator.to_be_removed.append(self)


            if self.enemy_rect.y > 200:
                Mediator.to_be_removed.append(self)

    def draw(self):
        if self.on_screen(self.enemy_rect, self.player):
            pygame.draw.rect(self.screen,(186,6,0),self.enemy_health_rect_red)
            pygame.draw.rect(self.screen,(5,143,0),self.enemy_health_rect_green)
            self.screen.blit(self.enemy_img,(self.enemy_rect.x - self.player.get_player_scroll(),self.enemy_rect.y))

