import pygame
import sys
import random
import math

pygame.init()

# Configurar pantalla completa y obtener su resolución actual
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Piedra, Papel o Tijeras (Reinicio al ganar)")

BLACK = (0, 0, 0)

# Cargar las imágenes desde la carpeta "images"
rock_img = pygame.image.load("images/rock.png")
paper_img = pygame.image.load("images/paper.png")
scissors_img = pygame.image.load("images/sissors.png")  # Asegúrate de que el nombre del archivo sea correcto

# Escalar las imágenes a 50x50 píxeles
rock_img = pygame.transform.scale(rock_img, (50, 50))
paper_img = pygame.transform.scale(paper_img, (50, 50))
scissors_img = pygame.transform.scale(scissors_img, (50, 50))

def random_velocity_constant(speed=3):
    """
    Devuelve una velocidad aleatoria con la misma magnitud 'speed' y dirección aleatoria.
    """
    angle = random.uniform(0, 2 * math.pi)
    vx = speed * math.cos(angle)
    vy = speed * math.sin(angle)
    return [vx, vy]

def random_position(image):
    """
    Devuelve una posición aleatoria [x, y] para la imagen, asegurando que esté completamente dentro de la pantalla.
    """
    img_width = image.get_width()
    img_height = image.get_height()
    x = random.randint(0, width - img_width)
    y = random.randint(0, height - img_height)
    return [x, y]

def reset_game():
    """
    Reinicia los objetos a su estado original (tipo, imagen) pero con posición y velocidad aleatoria.
    """
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

# Variable para registrar el estado ganador actual (para evitar sumar repetidamente)
winner_state = None

# Evento para evaluar el estado cada 1000 ms
update_event = pygame.USEREVENT + 1
pygame.time.set_timer(update_event, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Ahora, cualquier tecla presionada cierra el programa
        if event.type == pygame.KEYDOWN:
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

            # Solo se suma 1 si se detecta un ganador nuevo y, a continuación, se reinicia el juego
            if winning_type is not None and winning_type != winner_state:
                if winning_type == "rock":
                    counter_piedra += 1
                elif winning_type == "paper":
                    counter_papel += 1
                elif winning_type == "scissors":
                    counter_tijera += 1
                # Reiniciar el juego manteniendo la puntuación
                objects = reset_game()
                winner_state = winning_type
            # Si no hay ganador, se reinicia el estado para permitir futuros incrementos
            if winning_type is None:
                winner_state = None

    # Obtener el rectángulo de la pantalla (área de colisión)
    screen_rect = screen.get_rect()
    
    # Actualizar la posición de cada objeto y comprobar rebotes en los bordes
    for obj in objects:
        obj["pos"][0] += obj["vel"][0]
        obj["pos"][1] += obj["vel"][1]
        
        img_width = obj["image"].get_width()
        img_height = obj["image"].get_height()
        
        if obj["pos"][0] < screen_rect.left or obj["pos"][0] + img_width > screen_rect.right:
            obj["vel"][0] = -obj["vel"][0]
        if obj["pos"][1] < screen_rect.top or obj["pos"][1] + img_height > screen_rect.bottom:
            obj["vel"][1] = -obj["vel"][1]
    
    # Detección de colisiones y aplicación de reglas de piedra, papel o tijeras
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

    # Dibujar fondo y objetos en movimiento
    screen.fill(BLACK)
    for obj in objects:
        screen.blit(obj["image"], obj["pos"])
    
    # Renderizar textos con palabra y contador
    text_piedra = font.render("PIEDRA " + str(counter_piedra), True, (255, 255, 255))
    text_papel = font.render("PAPEL " + str(counter_papel), True, (255, 255, 255))
    text_tijera = font.render("TIJERA " + str(counter_tijera), True, (255, 255, 255))
    
    # Posicionar los textos en esquinas diferentes:
    # "PIEDRA" en la esquina superior izquierda
    pos_text_piedra = (margin, margin)
    # "PAPEL" en la esquina superior derecha, se calcula la posición en función del ancho del texto
    pos_text_papel = (width - text_papel.get_width() - margin, margin)
    # "TIJERA" en la esquina inferior izquierda
    pos_text_tijera = (margin, height - text_tijera.get_height() - margin)
    
    # Dibujar los textos en pantalla
    screen.blit(text_piedra, pos_text_piedra)
    screen.blit(text_papel, pos_text_papel)
    screen.blit(text_tijera, pos_text_tijera)
    
    pygame.display.flip()
    clock.tick(30) #optimized
