#!/usr/bin/env python

import pygame

KeyConfig = open("KeyConfig.kc", 'w')

pygame.init()
screen = pygame.display.set_mode((200, 200))
print("Press the keys in the right order. Press Escape to finish.")
while True:
    event = pygame.event.wait()
    if event.type is pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            break
        else:
            name = pygame.key.name(event.key)
            print("Last key pressed:", name)
            KeyConfig.write(name + '\n')

KeyConfig.close()
print("Done. you have a new keyboard configuration file:", KeyConfig.name)
pygame.quit()
