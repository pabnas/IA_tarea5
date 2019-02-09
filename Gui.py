import pygame
import sys
from pygame.locals import *
import numpy as np

escala = 5
CLICK_LEFT = 1
CLICK_RIGHT = 3

color = np.zeros((20,3))
color[0]  = (255,255,255)	#blanco
color[1]  = (255,255,0)		#amarillo
color[2]  = (34,113,179)	#azul
color[3]  = (87,166,57)		#verde
color[4]  = (213,48,50)		#rojo
color[5]  = (99,58,52)		#cafe
color[6]  = (215,45,109)	#magenta
color[7]  = (255,117,20)	#naranja
color[8]  = (127,181,181)	#turquesa
color[9]  = (234,137,154)	#rosa
color[10] = (40,114,51)		#esmeralda
color[11] = (1,93,82)		#opalo
color[12] = (0,247,0)		#verde brillante
color[13] = (244,169,0)		#melon
color[14] = (71,64,46)		#oliva
color[15] = (37,109,123)	#agua
color[16] = (194,176,120)	#beige
color[17] = (110,28,52)		#brudeos
color[18] = (125,132,113)	#gris cemento
color[19] = (10,10,10)		#negro
cuadro_size = 70
ventana = pygame.display.set_mode((cuadro_size*10,cuadro_size*7))

class GUI:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Q-Learning")
        ventana.fill(color[0])
        self.pintar_cuadro(0,3,3)
        self.pintar_cuadro(7,3,4)

    def pintar_cuadro(self,x,y,num):
        pygame.draw.rect(ventana, color[num], (cuadro_size * x, cuadro_size * y, cuadro_size, cuadro_size))
        self.pintar_grilla()

    def pintar_grilla(self):
        grosor = 1
        for x in range(9):
            pygame.draw.line(ventana, color[19],(cuadro_size*(x+1),0),(cuadro_size*(x+1),cuadro_size*10),grosor)
        for x in range(6):
            pygame.draw.line(ventana, color[19],(0,cuadro_size*(x+1)),(cuadro_size*10,cuadro_size*(x+1)),grosor)
        pygame.display.update()

    def wait(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #if event.type == MOUSEBUTTONDOWN and event.button == CLICK_LEFT:
            pygame.display.update()

    def show_policy(self,q_table):
        pygame.font.init()
        myfont = pygame.font.SysFont('arial', int(0.2*cuadro_size))
        myfont2 = pygame.font.SysFont('arial', int(0.2*cuadro_size))

        for x in range(7):
            for y in range(10):
                accion = np.argmax(q_table[(x, y)])
                texto = q_table[x][y][accion]
                textsurface = myfont.render('%.3f' % texto, False, color[19])
                ventana.blit(textsurface, (cuadro_size*y,cuadro_size*x))

                if accion == 0:
                    texto = "W"
                elif accion == 1:
                    texto = "D"
                elif accion == 2:
                    texto = "S"
                elif accion == 3:
                    texto = "A"
                textsurface = myfont2.render(texto, False, color[19])
                ventana.blit(textsurface, ((cuadro_size * y)+30,(cuadro_size * x)+30))
                pygame.display.update()

    def show_state(self,state,q_table,rastro):
        if rastro==False:
            ventana.fill(color[0])
            self.pintar_cuadro(0, 3, 3)
            self.pintar_cuadro(7, 3, 4)

        self.pintar_cuadro(state[1],state[0],7)
        self.show_policy(q_table)
