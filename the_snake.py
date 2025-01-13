from random import randrange, choice
import pygame as pg

# Константы:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Позиция начальной змейки:
INITIAL_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (0, 0, 0)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 7

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Игра-Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Инициализация шрифта для вывода длины
pg.font.init()
FONT = pg.font.Font(None, 30)


class GameObject:
    """Класс отвечающий за отрисовку игрового поля."""

    def __init__(self, body_color=SNAKE_COLOR, position=INITIAL_POSITION):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод, отвечающий за отрисовку на экране."""
        pass

    def draw_cell(self, position, body_color):
        """Отрисовывает ячейки на игровом поле."""
        rect_x, rect_y = position
        rect = pg.Rect(rect_x, rect_y, GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс отвечающий за поведение змейки и ее отрисовку"""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует змейку на игровом поле."""
        super().__init__(body_color)
        self.reset()

    def draw(self):
        """Рисуем змейку на поле."""
        for position in self.positions:
            self.draw_cell(position, self.body_color)

    def move(self):
        """Передвижение змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_head_x, new_head_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        """Метод для возвращения позиции головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Метод обновляющий направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self) -> None:
        """Метод, возвращающий змейку в начальное состояние."""
        self.direction = choice([UP, RIGHT, DOWN, LEFT])
        self.length = 1
        self.next_direction = None
        self.positions = [self.position]


def handle_keys(game_object):
    """Регулировка направления и обработка нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            key = event.key
            if key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


class Apple(GameObject):
    """Класс, описывающий яблоко и манипуляции с ним."""

    def __init__(self, body_color=APPLE_COLOR, positions=INITIAL_POSITION):
        """Инициализирует яблоко на игровом поле."""
        super().__init__(body_color)
        self.randomize_position(positions)

    def randomize_position(self, positions=INITIAL_POSITION):
        """Генерируем новое яблоко."""
        new_x = randrange(0, SCREEN_WIDTH, GRID_SIZE)
        new_y = randrange(0, SCREEN_HEIGHT, GRID_SIZE)
        new_apple = (new_x, new_y)
        while new_apple in positions:
            new_x = randrange(0, SCREEN_WIDTH, GRID_SIZE)
            new_y = randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            new_apple = (new_x, new_y)

        self.position = new_apple

    def draw(self):
        """Рисуем яблоко на поле."""
        self.draw_cell(self.position, self.body_color)


def display_length(snake_length):
    """Отображение длины змейки на экране."""
    text = f"Length: {snake_length}"
    text_surface = FONT.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))


def main():
    """Главный цикл игры."""
    pg.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.positions)
            snake.length += 1

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        display_length(snake.length)
        pg.display.flip()


if __name__ == '__main__':
    main()
