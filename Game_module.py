import pygame
import random
import pickle

# Инициализация Pygame
pygame.init()

# Создание окна
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Змейка")

# Цвета
black = pygame.Color(0, 0, 0)
green = pygame.Color(0, 255, 0)
red = pygame.Color(255, 0, 0)
white = pygame.Color(255, 255, 255)

# Параметры змейки
snake_x = 100
snake_y = 50
snake_size = 10
snake_body = [[snake_x, snake_y]]

# Параметры еды
food_x = random.randrange(1, width // snake_size) * snake_size
food_y = random.randrange(1, height // snake_size) * snake_size

# Направление движения
direction = "RIGHT"
change_to = direction

# Уровень скорости игры
game_speed = 10

# Счетчик очков
score = 0

# Таблица рекордов
high_scores = []

# Загрузка рекордов из файла (если существует)
try:
    with open("high_scores.dat", "rb") as file:
        high_scores = pickle.load(file)
except FileNotFoundError:
    pass

# Флаги для состояний игры
game_over = False
show_help = True
show_scores = False
restart_game = False
exit_game = False

# Основной игровой цикл
clock = pygame.time.Clock()

while not exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = True
        elif event.type == pygame.KEYDOWN:
            if show_help:
                if event.key == pygame.K_RETURN:
                    show_help = False
            elif show_scores:
                if event.key == pygame.K_RETURN:
                    restart_game = True
            else:
                if event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                elif event.key == pygame.K_UP:
                    change_to = "UP"
                elif event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                elif event.key == pygame.K_1:
                    game_speed = 10
                elif event.key == pygame.K_2:
                    game_speed = 20
                elif event.key == pygame.K_3:
                    game_speed = 30
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_scores:
                restart_game = True

    if not show_help and not show_scores:
        # Изменение направления движения
        if change_to == "RIGHT" and direction != "LEFT":
            direction = "RIGHT"
        elif change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        elif change_to == "UP" and direction != "DOWN":
            direction = "UP"
        elif change_to == "DOWN" and direction != "UP":
            direction = "DOWN"

        # Обновление позиции змейки
        if direction == "RIGHT":
            snake_x += snake_size
        elif direction == "LEFT":
            snake_x -= snake_size
        elif direction == "UP":
            snake_y -= snake_size
        elif direction == "DOWN":
            snake_y += snake_size

        # Проверка столкновения со стенками
        if snake_x >= width or snake_x < 0 or snake_y >= height or snake_y < 0:
            game_over = True

        # Проверка на самопересечение змеи
        for segment in snake_body[1:]:
            if segment[0] == snake_x and segment[1] == snake_y:
                game_over = True

        # Генерация новой еды и увеличение длины змейки
        if snake_x == food_x and snake_y == food_y:
            food_x = random.randrange(1, width // snake_size) * snake_size
            food_y = random.randrange(1, height // snake_size) * snake_size
            snake_body.append([snake_x, snake_y])
            score += 1
        else:
            # Обновление позиции тела змейки
            snake_body.insert(0, [snake_x, snake_y])
            snake_body.pop()

    # Заполнение фона
    window.fill(black)

    # Отрисовка змейки
    for segment in snake_body:
        pygame.draw.rect(window, green, (segment[0], segment[1], snake_size, snake_size))

    # Отрисовка еды
    pygame.draw.rect(window, red, (food_x, food_y, snake_size, snake_size))

    # Отображение счетчика очков
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, white)
    window.blit(score_text, (10, 10))

    # Отображение справки
    if show_help:
        text1 = font.render("Управление:", True, white)
        text2 = font.render("Стрелки - движение", True, white)
        text3 = font.render("1 - низкая скорость", True, white)
        text4 = font.render("2 - средняя скорость", True, white)
        text5 = font.render("3 - высокая скорость", True, white)
        text6 = font.render("Enter - начать игру", True, white)
        window.blit(text1, (width // 2 - text1.get_width() // 2, height // 2 - 100))
        window.blit(text2, (width // 2 - text2.get_width() // 2, height // 2 - 50))
        window.blit(text3, (width // 2 - text3.get_width() // 2, height // 2))
        window.blit(text4, (width // 2 - text4.get_width() // 2, height // 2 + 50))
        window.blit(text5, (width // 2 - text5.get_width() // 2, height // 2 + 100))
        window.blit(text6, (width // 2 - text6.get_width() // 2, height // 2 + 150))

    # Проверка окончания игры
    if game_over:
        # Добавление текущего счета в таблицу рекордов
        high_scores.append(score)
        show_scores = True
        # Сортировка таблицы рекордов в порядке убывания
        high_scores.sort(reverse=True)

        # Ограничение таблицы рекордов до 5 записей
        high_scores = high_scores[:5]

        # Сохранение таблицы рекордов в файл
        with open("high_scores.dat", "wb") as file:
            pickle.dump(high_scores, file)

        # Отображение таблицы рекордов
        text1 = font.render("Игра окончена!", True, white)
        text2 = font.render("Ваш счет: " + str(score), True, white)
        text3 = font.render("Таблица рекордов:", True, white)
        window.blit(text1, (width // 2 - text1.get_width() // 2, height // 2 - 100))
        window.blit(text2, (width // 2 - text2.get_width() // 2, height // 2 - 50))
        window.blit(text3, (width // 2 - text3.get_width() // 2, height // 2))
        y = height // 2 + 50
        for i, high_score in enumerate(high_scores):
            text = font.render(str(i + 1) + ". " + str(high_score), True, white)
            window.blit(text, (width // 2 - text.get_width() // 2, y))
            y += 30

        # Отображение инструкции о рестарте игры
        text4 = font.render("Нажмите Enter, чтобы перезапустить игру", True, white)
        window.blit(text4, (width // 2 - text4.get_width() // 2, height - 50))

        # Ожидание нажатия кнопки для рестарта игры
        if restart_game:
            # Сброс всех параметров
            snake_x = 100
            snake_y = 50
            snake_body = [[snake_x, snake_y]]
            food_x = random.randrange(1, width // snake_size) * snake_size
            food_y = random.randrange(1, height // snake_size) * snake_size
            direction = "RIGHT"
            change_to = direction
            game_speed = 10
            score = 0
            game_over = False
            show_help = True
            show_scores = False
            restart_game = False

    # Обновление экрана
    pygame.display.flip()

    # Ограничение частоты кадров
    clock.tick(game_speed)

# Завершение игры
pygame.quit()
