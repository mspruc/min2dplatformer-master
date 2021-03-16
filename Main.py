import pygame, sys

from pygame.locals import *
from Player import *
from GameMap import *
from HUD import *


def main():
    from Mediator import Mediator
    pygame.init()

    WINDOW_SIZE = (1024,768)
    clock = pygame.time.Clock()


    screen = pygame.display.set_mode(WINDOW_SIZE,0,32)
    display = pygame.Surface((256,192))

    player = Player(display, 'player', Mediator)
    print(Mediator.i)
    Mediator.all_game_entities.append(player)

    gameMap = GameMap(display, 'tiles', Mediator, player)
    hud = HUD(display,player)


    while True:
        display.fill((57, 138, 215))
        Mediator.all_game_tiles.clear()
        gameMap.draw_map()
        hud.draw_overlay()

        for object in Mediator.all_game_entities:
            object.loop()
            object.draw()
    

        Mediator.all_game_entities = [object for object in Mediator.all_game_entities if object not in Mediator.to_be_removed]
        Mediator.to_be_removed.clear()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0) #TODO remember to exit with a code so we dont throw an exception i think
    

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        screen.blit(surf, (0,0))
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()