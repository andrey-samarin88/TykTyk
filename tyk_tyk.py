import pgzrun
from random import randrange as rr, uniform as ru
from math import pi, cos, sin


# ------------------------------------------------------------
# Константы (настройки игры)
# ------------------------------------------------------------
TITLE = "Тык-тык"
WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOR = (20, 30, 40)
TEXT_COLOR = (220, 220, 220)
SECONDARY_TEXT_COLOR = (200, 200, 200)
HINT_TEXT_COLOR = (180, 180, 200)
HELP_TEXT_COLOR = (160, 160, 180)
MIN_SPEED = 1.0
MAX_SPEED = 3.0
MIN_CIRCLES = 3
MAX_CIRCLES = 7


class Circle:
    def __init__(self):
        self.radius = rr(15, 35)
        self.color = (rr(100, 256), rr(100, 256), rr(100, 256))
        self.x = rr(self.radius, WIDTH)
        self.y = rr(self.radius, HEIGHT)
        speed = ru(MIN_SPEED, MAX_SPEED)
        angle = ru(0, 2 * pi)
        self.dx = cos(angle) * speed
        self.dy = sin(angle) * speed
        self.is_popping = False
        self.pop_speed = 0.7

    def move(self, multiplier):
        self.x += self.dx * multiplier
        self.y += self.dy * multiplier

        if self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
            self.dx = -self.dx
        elif self.x < self.radius:
            self.x = self.radius
            self.dx = -self.dx

        if self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.dy = -self.dy
        elif self.y < self.radius:
            self.y = self.radius
            self.dy = -self.dy

    def is_clicked(self, pos):
        mouse_x, mouse_y = pos
        d = ((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2) ** 0.5
        return d <= self.radius

    def draw(self):
        if not self.is_popping:
            screen.draw.filled_circle((self.x, self.y), self.radius, self.color)
            screen.draw.circle((self.x, self.y), self.radius, (255, 255, 255))
            return

        self.radius -= self.pop_speed
        if self.radius < 1:
            game.popping_circles.remove(self)
            return

        screen.draw.filled_circle((self.x, self.y), self.radius, self.color)


class Game:
    def __init__(self):
        self.circles = [Circle() for _ in range(rr(MIN_CIRCLES, MAX_CIRCLES))]
        self.popping_circles = []  # Список лопающихся кружков
        self.score = 0
        self.speed_multiplier = 0.5

    def setup_game(self):
        self.__init__()

    def handle_click(self, pos):
        for circle in self.circles:
            if circle.is_clicked(pos):
                circle.is_popping = True
                self.score += 1
                self.speed_multiplier += 0.025
                break

    def update(self):
        for circle in self.circles[:]:
            if circle.is_popping:
                self.circles.remove(circle)  # Удаляем кружок из списка целых
                self.popping_circles.append(circle)  # Добавляем его в список лопающихся
                self.circles.append(Circle())  # Добавляем в список целых новый кружок
            circle.move(self.speed_multiplier) # Двигаем целые круги

        for circle in self.popping_circles:
            circle.move(self.speed_multiplier)  # Двигаем все лопающиеся круги

    def draw(self):
        screen.fill(BACKGROUND_COLOR)

        for circle in (self.circles + self.popping_circles)[:]:
            circle.draw()

        screen.draw.text(
            f"Счет: {self.score}",
            topleft=(20, 20),
            fontsize=30,
            color=TEXT_COLOR,
        )

        screen.draw.text(
            f"Скорость: x{self.speed_multiplier:.1f}",
            topright=(WIDTH - 20, 20),
            fontsize=30,
            color=SECONDARY_TEXT_COLOR,
        )

        screen.draw.text(
            "Нажимай левой кнопкой мыши на шарики, чтобы лопать их",
            center=(WIDTH // 2, HEIGHT - 40),
            fontsize=24,
            color=HINT_TEXT_COLOR,
        )

        screen.draw.text(
            "R - новая игра | ESC - выход",
            center=(WIDTH // 2, HEIGHT - 15),
            fontsize=20,
            color=HELP_TEXT_COLOR,
        )


# ------------------------------------------------------------
# Pygame Zero hooks (функции, которые вызывает движок)
# ------------------------------------------------------------
game = Game()


def update():
    game.update()


def draw():
    game.draw()


def on_mouse_down(pos, button):
    if button == mouse.LEFT:
        game.handle_click(pos)


def on_key_down(key):
    if key == keys.R:
        game.setup_game()
    elif key == keys.ESCAPE:
        exit()


pgzrun.go()
