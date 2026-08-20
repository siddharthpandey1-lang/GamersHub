import pygame
import sqlite3
import hashlib
import sys

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 60)
clock = pygame.time.Clock()

# ---------------- DATABASE ----------------

db = sqlite3.connect("users.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

db.commit()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_account(username, password):
    try:
        cursor.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            (username, hash_password(password))
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def login(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    return cursor.fetchone() is not None


# ---------------- INPUT BOX ----------------

class InputBox:

    def __init__(self, x, y, w, h, password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.active = False
        self.password = password

    def draw(self):
        pygame.draw.rect(screen, (45, 45, 45), self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)

        text = self.text

        if self.password:
            text = "*" * len(self.text)

        surface = font.render(text, True, "white")
        screen.blit(surface, (self.rect.x + 10, self.rect.y + 10))

    def handle(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:

            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif event.key == pygame.K_RETURN:
                return True

            else:
                if len(self.text) < 30:
                    self.text += event.unicode

        return False


# ---------------- LOGIN SCREEN ----------------

def login_screen():

    username = InputBox(300, 220, 300, 50)
    password = InputBox(300, 290, 300, 50, True)

    message = ""

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            username.handle(event)
            password.handle(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if login(username.text, password.text):
                        return username.text

                    message = "Invalid username or password!"

                if event.key == pygame.K_TAB:
                    return signup_screen()

        # background
        screen.fill((15, 15, 15))

        title = big_font.render("LOGIN", True, "white")
        screen.blit(title, (350, 100))

        username.draw()
        password.draw()

        pygame.draw.rect(
            screen,
            (80, 100, 220),
            (300, 370, 300, 55)
        )

        button = font.render("LOGIN", True, "white")
        screen.blit(button, (410, 380))

        info = font.render(
            "Press TAB for Sign Up",
            True,
            (160, 160, 160)
        )

        screen.blit(info, (300, 450))

        if message:
            error = font.render(message, True, (255, 80, 80))
            screen.blit(error, (250, 520))

        pygame.display.flip()
        clock.tick(60)


# ---------------- SIGN UP SCREEN ----------------

def signup_screen():

    username = InputBox(300, 190, 300, 50)
    password = InputBox(300, 260, 300, 50, True)
    confirm = InputBox(300, 330, 300, 50, True)

    message = ""

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            username.handle(event)
            password.handle(event)
            confirm.handle(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    if len(username.text) < 3:
                        message = "Username must be 3+ characters."

                    elif len(password.text) < 6:
                        message = "Password must be 6+ characters."

                    elif password.text != confirm.text:
                        message = "Passwords don't match."

                    elif create_account(
                        username.text,
                        password.text
                    ):
                        return username.text

                    else:
                        message = "Username already exists."

                if event.key == pygame.K_ESCAPE:
                    return login_screen()

        screen.fill((15, 15, 15))

        title = big_font.render("CREATE ACCOUNT", True, "white")
        screen.blit(title, (270, 90))

        username.draw()
        password.draw()
        confirm.draw()

        info1 = font.render("Username", True, (170, 170, 170))
        info2 = font.render("Password", True, (170, 170, 170))
        info3 = font.render("Confirm", True, (170, 170, 170))

        screen.blit(info1, (300, 165))
        screen.blit(info2, (300, 235))
        screen.blit(info3, (300, 305))

        pygame.draw.rect(
            screen,
            (80, 100, 220),
            (300, 410, 300, 55)
        )

        button = font.render("CREATE ACCOUNT", True, "white")
        screen.blit(button, (330, 420))

        if message:
            error = font.render(message, True, (255, 80, 80))
            screen.blit(error, (250, 500))

        pygame.display.flip()
        clock.tick(60)


# ---------------- MAIN GAME ----------------

def game(username):

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        screen.fill((20, 20, 30))

        title = big_font.render(
            f"Welcome, {username}!",
            True,
            "white"
        )

        screen.blit(title, (250, 200))

        text = font.render(
            "Your actual game starts here.",
            True,
            (180, 180, 180)
        )

        screen.blit(text, (280, 280))

        pygame.display.flip()
        clock.tick(60)


# ---------------- START ----------------

username = login_screen()

game(username)

pygame.quit()
db.close()