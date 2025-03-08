#hi
import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dos figuras rebotando")

# Definir algunos colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Propiedades de las figuras (posición, velocidad, radio)
circle1 = {"pos": [100, 100], "vel": [3, 2], "radius": 30, "color": RED}
circle2 = {"pos": [200, 200], "vel": [2, 3], "radius": 40, "color": BLUE}

clock = pygame.time.Clock()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Actualizar la posición de cada círculo
    for circle in [circle1, circle2]:
        circle["pos"][0] += circle["vel"][0]
        circle["pos"][1] += circle["vel"][1]
        
        # Comprobar colisiones con los bordes horizontales
        if circle["pos"][0] - circle["radius"] < 0 or circle["pos"][0] + circle["radius"] > width:
            circle["vel"][0] = -circle["vel"][0]
        
        # Comprobar colisiones con los bordes verticales
        if circle["pos"][1] - circle["radius"] < 0 or circle["pos"][1] + circle["radius"] > height:
            circle["vel"][1] = -circle["vel"][1]
    
    # Rellenar la pantalla con negro
    screen.fill(BLACK)
    
    # Dibujar los círculos
    pygame.draw.circle(screen, circle1["color"], (int(circle1["pos"][0]), int(circle1["pos"][1])), circle1["radius"])
    pygame.draw.circle(screen, circle2["color"], (int(circle2["pos"][0]), int(circle2["pos"][1])), circle2["radius"])
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Controlar los FPS
    clock.tick(60)
