import pygame
import random
import math
import time

# Ustawienia okna
screen_width = 800
screen_height = 600

# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Kolory
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Funkcja rysująca sześcian (gracz)
def draw_cube(x, y):
    size = 50  # Rozmiar sześcianu
    pygame.draw.rect(screen, WHITE, (x, y, size, size))

# Funkcja rysująca obiekty do zebrania
def draw_sphere(x, y, color):
    radius = 20  # Promień obiektu
    pygame.draw.circle(screen, color, (x, y), radius)

# Funkcja poruszania graczem
def move_player(x, y, keys):
    speed = 5
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed
    return x, y

# Funkcja sprawdzająca kolizję z obiektami
def check_collision(player_x, player_y, object_x, object_y):
    distance = math.sqrt((player_x - object_x) ** 2 + (player_y - object_y) ** 2)
    if distance < 50:  # Kolizja, jeśli obiekt w zasięgu 50 jednostek
        return True
    return False

# Funkcja główna gry
def game():
    player_x = 400
    player_y = 300
    score = 0
    welcome_message_time = 3  # Powitanie będzie widoczne przez 3 sekundy
    start_time = time.time()

    # Lista obiektów do zebrania (losowo generowane zielone i czerwone)
    objects = []
    last_update_time = time.time()  # Czas ostatniej aktualizacji obiektów

    running = True
    while running:
        screen.fill((0, 0, 0))  # Wypełnienie ekranu na czarno

        # Sprawdzanie zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Poruszanie graczem
        keys = pygame.key.get_pressed()
        player_x, player_y = move_player(player_x, player_y, keys)

        # Dodawanie nowych obiektów co sekundę
        current_time = time.time()
        if current_time - last_update_time >= 1:  # Co 1 sekundę
            # Losowo wybieramy kolor obiektu
            color = GREEN if random.choice([True, False]) else RED
            # Dodajemy nowy obiekt w losowym miejscu
            objects.append((random.randint(100, 700), random.randint(100, 500), color))
            last_update_time = current_time  # Zaktualizuj czas

        # Rysowanie gracza
        draw_cube(player_x, player_y)

        # Rysowanie obiektów do zebrania
        for obj in objects[:]:
            draw_sphere(obj[0], obj[1], obj[2])
            if check_collision(player_x, player_y, obj[0], obj[1]):
                if obj[2] == GREEN:
                    score += 1  # Dodaj punkty za zielony obiekt
                else:
                    score -= 1  # Odejmij punkty za czerwony obiekt
                objects.remove(obj)  # Usuwamy obiekt po zebraniu

        # Wyświetlanie powitania
        if current_time - start_time <= welcome_message_time:
            font = pygame.font.SysFont("Arial", 30)
            welcome_text = font.render("Witaj w grze!", True, (255, 255, 0))
            screen.blit(welcome_text, (screen_width // 2 - welcome_text.get_width() // 2, 10))

        # Wyświetlanie wyniku
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(f"Wynik: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 50))

        # Aktualizacja okna
        pygame.display.flip()

        # Opóźnienie dla 60 FPS
        clock.tick(60)

    pygame.quit()

# Uruchomienie gry
game()
