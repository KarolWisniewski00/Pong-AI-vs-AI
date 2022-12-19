import pygame
from sklearn.neural_network import MLPRegressor

# Inicjalizuj pygame
pygame.init()

# Ustaw szerokość i wysokość okna gry
window_width = 700
window_height = 500

# Utwórz okno gry
screen = pygame.display.set_mode((window_width, window_height))

# Ustaw tytuł okna
pygame.display.set_caption("Pong")

# Ustaw parametry piłki
ball_radius = 20
ball_x = window_width // 2
ball_y = window_height // 2
ball_dx = 6
ball_dy = 6

# Ustaw parametry paletki gracza
player_width = 15
player_height = 100
player_x = 20
player_y = window_height // 2 - player_height // 2

# Ustaw parametry paletki komputera
computer_width = 15
computer_height = 100
computer_x = window_width - 20 - computer_width
computer_y = window_height // 2 - computer_height // 2

# Ustaw parametry punktacji
player_score = 0
computer_score = 0
font = pygame.font.Font(None, 36)

# Ustaw warunki zakończenia gry
game_over = False
winner = None

# Ustaw zegar
clock = pygame.time.Clock()

# Utwórz dane treningowe
X= []
y = []
X_1= []
y_1 = []

# Utwórz model sieci neuronowej
model = MLPRegressor(hidden_layer_sizes=(10,), activation='relu', solver='adam', max_iter=1000)
model_1 = MLPRegressor(hidden_layer_sizes=(10,), activation='relu', solver='adam', max_iter=1000)


# Pętla główna gry
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Przewiduj pozycję paletki komputera na podstawie pozycji piłki, paletki gracza i paletki komputera
    try:
        prediction = model.predict([[ball_x, ball_y, computer_y]])
        computer_y = prediction[0]
    except:
        pass
    try:
        prediction_1 = model_1.predict([[ball_x, ball_y, player_y]])
        player_y = prediction_1[0]
    except:
        pass

    # Uaktualnij pozycję piłki
    ball_x += ball_dx
    ball_y += ball_dy

    # Sprawdź, czy piłka dotknęła górnej lub dolnej krawędzi okna
    if ball_y - ball_radius < 0 or ball_y + ball_radius > window_height:
        ball_dy *= -1

    # Sprawdź, czy piłka dotknęła paletki gracza
    if ball_x - ball_radius < player_x + player_width and player_y < ball_y < player_y + player_height:
        # Dodaj dane treningowe
        X_1.append([ball_x, ball_y, player_y])
        y_1.append(player_y)
        ball_dx *= -1
    # Sprawdź, czy piłka dotknęła paletki komputera
    elif ball_x + ball_radius > computer_x and computer_y < ball_y < computer_y + computer_height:
        # Dodaj dane treningowe
        X.append([ball_x, ball_y, computer_y])
        y.append(computer_y)
        ball_dx *= -1
    # Sprawdź, czy piłka wyszła poza pole gry po stronie gracza
    elif ball_x + ball_radius < 0:
        # Dodaj dane treningowe
        X_1.append([ball_x, ball_y, player_y])
        y_1.append(ball_y)

        computer_score += 1
        ball_x = window_width // 2
        ball_y = window_height // 2

        #spróbuj nauczuć
        try:
            model_1.fit(X_1,y_1)
        except:
            pass
    # Sprawdź, czy piłka wyszła poza pole gry po stronie komputera
    elif ball_x - ball_radius > window_width:
        # Dodaj dane treningowe
        X.append([ball_x, ball_y, computer_y])
        y.append(ball_y)

        player_score += 1
        ball_x = window_width // 2
        ball_y = window_height // 2

        # Spróbuj nauczuć
        try:
            model.fit(X,y)
        except:
            pass

    # Wyczyść ekran
    screen.fill((0, 0, 0))

    # Narysuj piłkę
    pygame.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), ball_radius)

    # Narysuj paletki gracza i komputera
    pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, player_width, player_height))
    pygame.draw.rect(screen, (255, 255, 255), (computer_x, computer_y, computer_width, computer_height))

    # Wyświetl punktację
    player_text = font.render(f"AI: {player_score}", True, (255, 255, 255))
    computer_text = font.render(f"AI: {computer_score}", True, (255, 255, 255))
    screen.blit(player_text, (window_width // 2 - 150, 50))
    screen.blit(computer_text, (window_width // 2 + 50, 50))

    # Odśwież ekran
    pygame.display.flip()

    # Zmień ilość klatek na sekundę
    clock.tick(60)
