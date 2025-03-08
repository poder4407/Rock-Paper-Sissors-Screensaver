import pygame
import sys

pygame.init()

# Configurar pantalla completa
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Piedra, Papel o Tijeras en movimiento")

BLACK = (0, 0, 0)

# Cargar las imágenes desde la carpeta "images"
rock_img = pygame.image.load("images/rock.png")
paper_img = pygame.image.load("images/paper.png")
scissors_img = pygame.image.load("images/sissors.png")  # Nota: el archivo se llama "sissors.png"

# Escalar las imágenes a un tamaño más pequeño (50x50 píxeles)
rock_img = pygame.transform.scale(rock_img, (50, 50))
paper_img = pygame.transform.scale(paper_img, (50, 50))
scissors_img = pygame.transform.scale(scissors_img, (50, 50))

# Configurar cada objeto con su imagen, tipo, posición y velocidad
rock = {"name": "rock", "image": rock_img, "pos": [100, 100], "vel": [3, 2]}
paper = {"name": "paper", "image": paper_img, "pos": [200, 200], "vel": [2, 3]}
scissors = {"name": "scissors", "image": scissors_img, "pos": [300, 300], "vel": [3, 3]}

# Lista de objetos para facilitar iteraciones
objects = [rock, paper, scissors]

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Permitir salir presionando ESC
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

    # Actualizar posición y detectar rebotes en los bordes
    for obj in objects:
        obj["pos"][0] += obj["vel"][0]
        obj["pos"][1] += obj["vel"][1]
        
        img_width = obj["image"].get_width()
        img_height = obj["image"].get_height()

        if obj["pos"][0] < 0 or obj["pos"][0] + img_width > width:
            obj["vel"][0] = -obj["vel"][0]
        if obj["pos"][1] < 0 or obj["pos"][1] + img_height > height:
            obj["vel"][1] = -obj["vel"][1]

    # Detección de colisiones y aplicación de las reglas de piedra, papel o tijeras
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            rect_i = objects[i]["image"].get_rect(topleft=objects[i]["pos"])
            rect_j = objects[j]["image"].get_rect(topleft=objects[j]["pos"])
            if rect_i.colliderect(rect_j):
                # Regla: Piedra aplasta tijera
                if objects[i]["name"] == "rock" and objects[j]["name"] == "scissors":
                    objects[j]["name"] = "rock"
                    objects[j]["image"] = rock_img
                elif objects[i]["name"] == "scissors" and objects[j]["name"] == "rock":
                    objects[i]["name"] = "rock"
                    objects[i]["image"] = rock_img
                # Regla: Tijera corta papel
                elif objects[i]["name"] == "scissors" and objects[j]["name"] == "paper":
                    objects[j]["name"] = "scissors"
                    objects[j]["image"] = scissors_img
                elif objects[i]["name"] == "paper" and objects[j]["name"] == "scissors":
                    objects[i]["name"] = "scissors"
                    objects[i]["image"] = scissors_img
                # Regla: Papel envuelve piedra
                elif objects[i]["name"] == "paper" and objects[j]["name"] == "rock":
                    objects[j]["name"] = "paper"
                    objects[j]["image"] = paper_img
                elif objects[i]["name"] == "rock" and objects[j]["name"] == "paper":
                    objects[i]["name"] = "paper"
                    objects[i]["image"] = paper_img

    # Dibujar todo en pantalla
    screen.fill(BLACK)
    for obj in objects:
        screen.blit(obj["image"], obj["pos"])
    
    pygame.display.flip()
    clock.tick(60)
#comment to make valid the commit