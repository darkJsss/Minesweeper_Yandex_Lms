import pygame
from datetime import timedelta

# Инициализация Pygame
pygame.init()

# Размеры окна
screen_width = 600
screen_height = 400
# игровое поле
mine_field = None

# Создание экрана
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Saper")

# Загрузка изображений
play_img = pygame.image.load('images/play.png')
story_img = pygame.image.load('images/story.png')
options_img = pygame.image.load('images/options.png')
leaderboard_img = pygame.image.load('images/leaderboard.png')

# Изображения для режимов игры
gameMode_imgs = [
    pygame.image.load(f'images/gameMode{i}.png') for i in range(1, 6)
]

# Изображение для storyS
storyS_img = pygame.image.load('images/storyS.png')

# Изображения для опций
options_imgs = [
    pygame.image.load(f'images/options{i}.png') for i in range(1, 4)
]
current_option_index = 0
leaderboard_imgs = [
    pygame.image.load(f'images/gameMode{i}.png') for i in range(1, 6)
]
current_leaderboard_index = 0
# Список всех меню изображений
menu_images = [play_img, story_img, options_img, leaderboard_img]
current_menu_index = 0

# Переменные для отслеживания состояний
in_record_mode_screen = False
time_to_records = False
in_game_mode_selection = False
in_game_play = False
current_game_mode_index = 0
in_story_screen = False
in_options_screen = False

# Изображения для игрового поля
QUE_tile = pygame.image.load('images/QUEtile.png')
UNC_tile = pygame.image.load('images/UNCtile.png')
FLA_tile = pygame.image.load('images/FLAtile.png')
lost_img = pygame.image.load('images/lost.png')
won_img = pygame.image.load('images/won.png')
numbers = {i: pygame.image.load(f'images/{i}.png') for i in range(1, 9)}
font = pygame.font.Font(None, 32)
# музыка на фон
pygame.mixer.music.load("music/menu.mp3")
# Начало воспроизведения музыки
pygame.mixer.music.play(-1)


# Класс для управления игровым полем
class MineField:
    def __init__(self, rows, cols, mines, mode):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.mode = mode
        pygame.display.set_mode((cols * 20, rows * 20))
        self.field = generate_minefield(rows, cols, mines)
        self.revealed = [[False for _ in range(cols)] for _ in range(rows)]
        self.flags = [[False for _ in range(cols)] for _ in range(rows)]
        self.game_over = False
        self.won = False
        self.start_time = None
        self.end_time = None

    def reveal(self, row, col):
        if self.revealed[row][col]:
            return
        if self.flags[row][col]:
            return

        self.revealed[row][col] = True
        if self.field[row][col] == -1:
            self.game_over = True
        elif self.field[row][col] > 0:
            pass
        else:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r = row + dr
                    c = col + dc
                    if 0 <= r < self.rows and 0 <= c < self.cols:
                        self.reveal(r, c)

    def toggle_flag(self, row, col):
        if self.revealed[row][col]:
            return
        self.flags[row][col] = not self.flags[row][col]

    def check_win(self):
        for flag, reveal in zip(self.flags, self.revealed):
            for i, j in zip(flag, reveal):
                if i is False and j is False:
                    return False
        return True


# Функция для генерации игрового поля
def generate_minefield(rows, cols, mines):
    import random
    field = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set(random.sample(range(rows * cols), mines))
    for pos in mine_positions:
        row = pos // cols
        col = pos % cols
        field[row][col] = -1
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r = row + dr
                c = col + dc
                if 0 <= r < rows and 0 <= c < cols and field[r][c] != -1:
                    field[r][c] += 1
    return field


# Функция для запуска игры
def start_game(mode):
    global mine_field
    rows, cols, mines = 10, 10, 10
    if mode == 0:
        rows, cols, mines = 10, 10, 10
    elif mode == 1:
        rows, cols, mines = 16, 16, 40
    elif mode == 2:
        rows, cols, mines = 30, 16, 99
    elif mode == 3:
        rows, cols, mines = map(int, input().split())
    elif mode == 4:
        rows, cols, mines = 24, 30, 120
    mine_field = MineField(rows, cols, mines, mode)
    mine_field.start_time = int(pygame.time.get_ticks())

# функция дла записи рекордов
def update_and_sort_records(file_path, new_time):
    # Чтение содержимого файла
    with open(file_path, 'r') as f:
        records = [float(line.strip()) for line in f]
        if len(records) > 0 and new_time < records[-1]:
            records.pop()
        records.append(new_time)
        records.sort()
        # Перезапись данных в файл
        with open(file_path, 'w') as f1:
            for time_record in records:
                f1.write(f"{time_record}\n")

# функция дла сброса рекордов
def reset_records():
    name_records_table = ["record_easy.txt", "record_medium.txt", "record_hard.txt", "record_concentric.txt",
                          "record_custom.txt"]
    for name in name_records_table:
        with open(name, 'w') as f1:
            pass

# функция дла получения списка рекордов
def read_records_from_file(file_path):
    records = []
    with open(file_path, 'r') as f:
        for line in f:
            records.append(float(line.strip()))
    return records


# Основной цикл игры
def main_loop():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("music/start.mp3")
    pygame.mixer.music.play()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row = mouse_pos[1] // 20
                col = mouse_pos[0] // 20
                if event.button == 1:
                    pygame.mixer.music.load("music/click.mp3")
                    pygame.mixer.music.play()
                    mine_field.reveal(row, col)
                elif event.button == 3:
                    pygame.mixer.music.load("music/tick.mp3")
                    pygame.mixer.music.play()
                    mine_field.toggle_flag(row, col)

        # Проверяем окончание игры
        if mine_field.game_over:
            pygame.mixer.music.load("music/lose.mp3")
            pygame.mixer.music.play()
            pygame.display.set_mode((screen_width, screen_height))
            lost_rect = lost_img.get_rect(center=(300, 200))
            screen.blit(lost_img, lost_rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            return

        if mine_field.check_win():
            pygame.mixer.music.load("music/win.mp3")
            pygame.mixer.music.play()
            pygame.display.set_mode((screen_width, screen_height))
            won_rect = won_img.get_rect(center=(300, 200))
            screen.blit(won_img, won_rect)
            pygame.display.flip()
            s = "record"
            if mine_field.mode == 0:
                s += "_easy.txt"
            elif mine_field.mode == 1:
                s += "_medium.txt"
            elif mine_field.mode == 2:
                s += "_hard.txt"
            elif mine_field.mode == 4:
                s += "_concentric.txt"
            elif mine_field.mode == 3:
                s += "_custom.txt"
            update_and_sort_records(s, (pygame.time.get_ticks() - mine_field.start_time) / 1000)
            pygame.time.delay(2000)
            return

        # Рисование игрового поля
        screen.fill((0, 0, 0))
        for row in range(mine_field.rows):
            for col in range(mine_field.cols):
                x = col * 20
                y = row * 20
                tile = QUE_tile
                if mine_field.revealed[row][col]:
                    if mine_field.field[row][col] == -1:
                        tile = numbers[-1]
                    elif mine_field.field[row][col] == 0:
                        tile = UNC_tile
                    else:
                        tile = numbers[mine_field.field[row][col]]
                elif mine_field.flags[row][col]:
                    tile = FLA_tile
                screen.blit(tile, (x, y))

        # Обновление экрана
        pygame.display.flip()


# Основной цикл программы
running = True
while running:
    # Обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not in_game_mode_selection and not in_story_screen and not in_options_screen and not in_record_mode_screen:
                if event.key == pygame.K_UP:
                    current_menu_index -= 1
                    if current_menu_index < 0:
                        current_menu_index = len(menu_images) - 1
                elif event.key == pygame.K_DOWN:
                    current_menu_index += 1
                    if current_menu_index >= len(menu_images):
                        current_menu_index = 0
                elif event.key == pygame.K_RETURN and current_menu_index == 0:
                    in_game_mode_selection = True
                elif event.key == pygame.K_RETURN and current_menu_index == 1:
                    in_story_screen = True
                elif event.key == pygame.K_RETURN and current_menu_index == 2:
                    in_options_screen = True
                elif event.key == pygame.K_RETURN and current_menu_index == 3:
                    in_record_mode_screen = True
            elif in_game_mode_selection:
                if event.key == pygame.K_UP:
                    current_game_mode_index -= 1
                    if current_game_mode_index < 0:
                        current_game_mode_index = len(gameMode_imgs) - 1
                elif event.key == pygame.K_DOWN:
                    current_game_mode_index += 1
                    if current_game_mode_index >= len(gameMode_imgs):
                        current_game_mode_index = 0
                elif event.key == pygame.K_ESCAPE:
                    in_game_mode_selection = False
                elif event.key == pygame.K_RETURN:
                    in_game_play = True
            elif in_story_screen:
                if event.key == pygame.K_ESCAPE:
                    in_story_screen = False
            elif in_record_mode_screen:
                if event.key == pygame.K_UP:
                    current_leaderboard_index -= 1
                    if current_leaderboard_index < 0:
                        current_leaderboard_index = len(leaderboard_imgs) - 1
                elif event.key == pygame.K_DOWN:
                    current_leaderboard_index += 1
                    if current_leaderboard_index >= len(leaderboard_imgs):
                        current_leaderboard_index = 0
                elif event.key == pygame.K_ESCAPE:
                    in_record_mode_screen = False
                    time_to_records = False
                elif event.key == pygame.K_RETURN and current_leaderboard_index == 0:
                    records = read_records_from_file('record_easy.txt')
                    time_to_records = True
                elif event.key == pygame.K_RETURN and current_leaderboard_index == 1:
                    records = read_records_from_file('record_medium.txt')
                    time_to_records = True
                elif event.key == pygame.K_RETURN and current_leaderboard_index == 2:
                    records = read_records_from_file('record_hard.txt')
                    time_to_records = True
                elif event.key == pygame.K_RETURN and current_leaderboard_index == 3:
                    records = read_records_from_file('record_custom.txt')
                    time_to_records = True
                elif event.key == pygame.K_RETURN and current_leaderboard_index == 4:
                    records = read_records_from_file('record_concentric.txt')
                    time_to_records = True
            elif in_options_screen:
                if event.key == pygame.K_UP:
                    current_option_index -= 1
                    if current_option_index < 0:
                        current_option_index = len(options_imgs) - 1
                elif event.key == pygame.K_DOWN:
                    current_option_index += 1
                    if current_option_index >= len(options_imgs):
                        current_option_index = 0
                elif event.key == pygame.K_ESCAPE:
                    in_options_screen = False
                elif event.key == pygame.K_RETURN and current_option_index == 0:
                    reset_records()
                elif event.key == pygame.K_RETURN and current_option_index == 1:
                    pygame.mixer.music.set_volume(0.0)
                elif event.key == pygame.K_RETURN and current_option_index == 2:
                    in_options_screen = False
        # Очистка экрана
    screen.fill((0, 0, 0))
    # Отрисовка текущей картинки
    if not in_game_mode_selection and not in_story_screen and not in_options_screen and not in_game_play and not in_record_mode_screen:
        screen.blit(menu_images[current_menu_index], (0, 0))
    elif in_game_mode_selection and in_game_play is False:
        screen.blit(gameMode_imgs[current_game_mode_index], (0, 0))
    elif in_story_screen:
        screen.blit(storyS_img, (0, 0))
    elif in_record_mode_screen and time_to_records:
        y_pos = 50
        for i, record in enumerate(records):
            text_surface = font.render(f'{i + 1})  {record} секунд', True, (255, 255, 255))
            screen.blit(text_surface, (50, y_pos))
            y_pos += 40
    elif in_record_mode_screen:
        screen.blit(leaderboard_imgs[current_leaderboard_index], (0, 0))
    elif in_options_screen:
        screen.blit(options_imgs[current_option_index], (0, 0))
    elif in_game_play:
        start_game(current_game_mode_index)
        in_game_play = False
        in_game_mode_selection = False
        main_loop()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("music/menu.mp3")
        pygame.mixer.music.play(-1)
        pygame.display.set_mode((screen_width, screen_height))
    # Обновление экрана
    pygame.display.flip()

pygame.quit()
