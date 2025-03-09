import pygame
import sys
import random
import math

pygame.init()

# Ocultar el cursor (comportamiento típico de un protector de pantalla)
pygame.mouse.set_visible(False)

# Configurar pantalla completa y obtener su resolución actual
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Protector de Pantalla: Piedra, Papel o Tijeras")

BLACK = (0, 0, 0)

# Cargar las imágenes desde la carpeta "images"
rock_img = pygame.image.load("images/rock.png")
paper_img = pygame.image.load("images/paper.png")
scissors_img = pygame.image.load("images/sissors.png")  # Verifica el nombre del archivo

# Escalar las imágenes a 50x50 píxeles
rock_img = pygame.transform.scale(rock_img, (50, 50))
paper_img = pygame.transform.scale(paper_img, (50, 50))
scissors_img = pygame.transform.scale(scissors_img, (50, 50))

def random_velocity_constant(speed=3):
    """Devuelve una velocidad aleatoria con magnitud 'speed' y dirección aleatoria."""
    angle = random.uniform(0, 2 * math.pi)
    vx = speed * math.cos(angle)
    vy = speed * math.sin(angle)
    return [vx, vy]

def random_position(image):
    """Devuelve una posición aleatoria [x, y] para la imagen, dentro de la pantalla."""
    img_width = image.get_width()
    img_height = image.get_height()
    x = random.randint(0, width - img_width)
    y = random.randint(0, height - img_height)
    return [x, y]

def reset_game():
    """Reinicia los objetos con su tipo e imagen original, pero con posición y velocidad aleatoria."""
    rock_obj = {
        "name": "rock",
        "image": rock_img,
        "pos": random_position(rock_img),
        "vel": random_velocity_constant(3)
    }
    paper_obj = {
        "name": "paper",
        "image": paper_img,
        "pos": random_position(paper_img),
        "vel": random_velocity_constant(3)
    }
    scissors_obj = {
        "name": "scissors",
        "image": scissors_img,
        "pos": random_position(scissors_img),
        "vel": random_velocity_constant(3)
    }
    return [rock_obj, paper_obj, scissors_obj]

# Inicializar los objetos
objects = reset_game()

clock = pygame.time.Clock()

# Configurar fuente y contadores para los textos
font = pygame.font.SysFont(None, 48)
margin = 20
counter_piedra = 0
counter_papel = 0
counter_tijera = 0

# Variable para registrar el estado ganador actual
winner_state = None

# Evento para evaluar el estado cada 1000 ms
update_event = pygame.USEREVENT + 1
pygame.time.set_timer(update_event, 1000)

# Tiempo inicial para ignorar eventos de entrada durante 1 segundo
start_time = pygame.time.get_ticks()
ignore_input_duration = 1000  # milisegundos

while True:
    for event in pygame.event.get():
        # Solo consideramos eventos de salida si ya pasó el tiempo de ignorar
        if pygame.time.get_ticks() - start_time > ignore_input_duration:
            if event.type in (pygame.KEYDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                pygame.quit()
                sys.exit()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == update_event:
            # Verificar si todas las imágenes tienen el mismo tipo
            winning_type = None
            if all(obj["name"] == "rock" for obj in objects):
                winning_type = "rock"
            elif all(obj["name"] == "paper" for obj in objects):
                winning_type = "paper"
            elif all(obj["name"] == "scissors" for obj in objects):
                winning_type = "scissors"
            else:
                winning_type = None

            # Sumar 1 al contador solo si se detecta un nuevo estado ganador y reiniciar el juego
            if winning_type is not None and winning_type != winner_state:
                if winning_type == "rock":
                    counter_piedra += 1
                elif winning_type == "paper":
                    counter_papel += 1
                elif winning_type == "scissors":
                    counter_tijera += 1
                objects = reset_game()  # Reiniciar la posición y velocidad de los objetos
                winner_state = winning_type
            if winning_type is None:
                winner_state = None

    screen_rect = screen.get_rect()
    
    # Actualizar posiciones y rebotar en los bordes
    for obj in objects:
        obj["pos"][0] += obj["vel"][0]
        obj["pos"][1] += obj["vel"][1]
        
        img_width = obj["image"].get_width()
        img_height = obj["image"].get_height()
        
        if obj["pos"][0] < screen_rect.left or obj["pos"][0] + img_width > screen_rect.right:
            obj["vel"][0] = -obj["vel"][0]
        if obj["pos"][1] < screen_rect.top or obj["pos"][1] + img_height > screen_rect.bottom:
            obj["vel"][1] = -obj["vel"][1]
    
    # Detección de colisiones y reglas de Piedra, Papel o Tijeras
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            rect_i = objects[i]["image"].get_rect(topleft=objects[i]["pos"])
            rect_j = objects[j]["image"].get_rect(topleft=objects[j]["pos"])
            if rect_i.colliderect(rect_j):
                if objects[i]["name"] == "rock" and objects[j]["name"] == "scissors":
                    objects[j]["name"] = "rock"
                    objects[j]["image"] = rock_img
                elif objects[i]["name"] == "scissors" and objects[j]["name"] == "rock":
                    objects[i]["name"] = "rock"
                    objects[i]["image"] = rock_img
                elif objects[i]["name"] == "scissors" and objects[j]["name"] == "paper":
                    objects[j]["name"] = "scissors"
                    objects[j]["image"] = scissors_img
                elif objects[i]["name"] == "paper" and objects[j]["name"] == "scissors":
                    objects[i]["name"] = "scissors"
                    objects[i]["image"] = scissors_img
                elif objects[i]["name"] == "paper" and objects[j]["name"] == "rock":
                    objects[j]["name"] = "paper"
                    objects[j]["image"] = paper_img
                elif objects[i]["name"] == "rock" and objects[j]["name"] == "paper":
                    objects[i]["name"] = "paper"
                    objects[i]["image"] = paper_img

    screen.fill(BLACK)
    for obj in objects:
        screen.blit(obj["image"], obj["pos"])
    
    # Renderizar y posicionar los textos con los contadores
    text_piedra = font.render("PIEDRA " + str(counter_piedra), True, (255, 255, 255))
    text_papel = font.render("PAPEL " + str(counter_papel), True, (255, 255, 255))
    text_tijera = font.render("TIJERA " + str(counter_tijera), True, (255, 255, 255))
    
    pos_text_piedra = (margin, margin)
    pos_text_papel = (width - text_papel.get_width() - margin, margin)
    pos_text_tijera = (margin, height - text_tijera.get_height() - margin)
    
    screen.blit(text_piedra, pos_text_piedra)
    screen.blit(text_papel, pos_text_papel)
    screen.blit(text_tijera, pos_text_tijera)
    
    pygame.display.flip()
    clock.tick(30)
