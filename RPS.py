import pygame
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tres imágenes rebotando")

# Color de fondo
BLACK = (0, 0, 0)

# Cargar las imágenes desde la carpeta "images"
rock_img = pygame.image.load("images/rock.png")
paper_img = pygame.image.load("images/paper.png")
sissors_img = pygame.image.load("images/sissors.png")

# Escalar las imágenes para que sean más pequeñas (50x50 píxeles)
rock_img = pygame.transform.scale(rock_img, (50, 50))
paper_img = pygame.transform.scale(paper_img, (50, 50))
sissors_img = pygame.transform.scale(sissors_img, (50, 50))

# Configurar cada imagen con su posición inicial y velocidad
rock = {"image": rock_img, "pos": [100, 100], "vel": [3, 2]}
paper = {"image": paper_img, "pos": [200, 200], "vel": [2, 3]}
sissors = {"image": sissors_img, "pos": [300, 300], "vel": [3, 3]}

clock = pygame.time.Clock()

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Actualizar la posición de cada imagen y comprobar colisiones con los bordes
    for obj in (rock, paper, sissors):
        obj["pos"][0] += obj["vel"][0]
        obj["pos"][1] += obj["vel"][1]
        
        # Obtener dimensiones de la imagen
        img_width = obj["image"].get_width()
        img_height = obj["image"].get_height()
        
        # Rebotar en los bordes horizontales
        if obj["pos"][0] < 0 or obj["pos"][0] + img_width > width:
            obj["vel"][0] = -obj["vel"][0]
        
        # Rebotar en los bordes verticales
        if obj["pos"][1] < 0 or obj["pos"][1] + img_height > height:
            obj["vel"][1] = -obj["vel"][1]
    
    # Rellenar la pantalla de negro
    screen.fill(BLACK)
    
    # Dibujar cada imagen en su posición actual
    screen.blit(rock["image"], rock["pos"])
    screen.blit(paper["image"], paper["pos"])
    screen.blit(sissors["image"], sissors["pos"])
    
    pygame.display.flip()
    clock.tick(60)
