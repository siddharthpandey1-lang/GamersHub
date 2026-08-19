import pygame
import sys
import math

pygame.init()

# =========================================================
# SETTINGS
# =========================================================

WIDTH = 1200
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎮 Gamers Hub")

clock = pygame.time.Clock()

# =========================================================
# COLORS
# =========================================================

BG = (5, 5, 15)
CARD = (15, 15, 30)
WHITE = (255, 255, 255)
GRAY = (160, 160, 180)

CYAN = (0, 230, 255)
PURPLE = (140, 50, 255)
PINK = (255, 0, 170)
GREEN = (0, 255, 130)

# =========================================================
# FONTS
# =========================================================

title_font = pygame.font.SysFont("arial", 52, bold=True)
subtitle_font = pygame.font.SysFont("arial", 18, bold=True)
card_title_font = pygame.font.SysFont("arial", 28, bold=True)
price_font = pygame.font.SysFont("arial", 42, bold=True)
normal_font = pygame.font.SysFont("arial", 16)
button_font = pygame.font.SysFont("arial", 17, bold=True)
small_font = pygame.font.SysFont("arial", 13)

# =========================================================
# PLAN DATA
# =========================================================

plans = [
    {
        "name": "BASIC",
        "icon": "🎮",
        "price": "$5",
        "color": CYAN,
        "features": [
            "Gaming Community",
            "Gaming Guides",
            "Weekly Updates",
            "Community Support"
        ]
    },

    {
        "name": "PREMIUM",
        "icon": "⚡",
        "price": "$10",
        "color": PURPLE,
        "features": [
            "Everything in Basic",
            "Premium Guides",
            "Exclusive Content",
            "Priority Support",
            "Early Access"
        ]
    },

    {
        "name": "ELITE",
        "icon": "👑",
        "price": "$15",
        "color": PINK,
        "features": [
            "Everything in Premium",
            "Elite Content",
            "Exclusive Events",
            "VIP Community",
            "Personalized Support"
        ]
    }
]

# =========================================================
# STATES
# =========================================================

page = "home"
selected_plan = None
name_text = ""
payment_text = ""

# =========================================================
# BACKGROUND PARTICLES
# =========================================================

particles = []

for i in range(80):
    particles.append([
        pygame.rand if False else __import__("random").randint(0, WIDTH),
        __import__("random").randint(0, HEIGHT),
        __import__("random").randint(1, 3),
        __import__("random").randint(1, 3)
    ])


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def draw_text(text, font, color, x, y, center=False):

    surface = font.render(text, True, color)

    if center:
        rect = surface.get_rect(center=(x, y))
    else:
        rect = surface.get_rect(topleft=(x, y))

    screen.blit(surface, rect)


def draw_glow_circle(x, y, radius, color):

    for i in range(8, 0, -1):

        alpha_radius = radius + i * 8

        glow = pygame.Surface(
            (alpha_radius * 2, alpha_radius * 2),
            pygame.SRCALPHA
        )

        alpha = int(10 / i)

        pygame.draw.circle(
            glow,
            (*color, alpha),
            (alpha_radius, alpha_radius),
            alpha_radius
        )

        screen.blit(
            glow,
            (x - alpha_radius, y - alpha_radius)
        )


def draw_background():

    screen.fill(BG)

    # Large glowing circles
    draw_glow_circle(
        150,
        150,
        100,
        PURPLE
    )

    draw_glow_circle(
        1050,
        600,
        120,
        CYAN
    )

    # Moving particles
    for particle in particles:

        particle[1] -= particle[3] * 0.3

        if particle[1] < 0:
            particle[1] = HEIGHT

        pygame.draw.circle(
            screen,
            (40, 40, 70),
            (int(particle[0]), int(particle[1])),
            particle[2]
        )


# =========================================================
# BUTTON
# =========================================================

def draw_button(rect, text, color, mouse_pos):

    hover = rect.collidepoint(mouse_pos)

    current_color = color

    if hover:
        current_color = tuple(
            min(255, c + 35) for c in color
        )

    pygame.draw.rect(
        screen,
        current_color,
        rect,
        border_radius=12
    )

    draw_text(
        text,
        button_font,
        BG,
        rect.centerx,
        rect.centery,
        True
    )

    return hover


# =========================================================
# HOME PAGE
# =========================================================

def draw_home(mouse_pos):

    draw_background()

    # Title
    draw_text(
        "🎮 GAMERS HUB",
        title_font,
        CYAN,
        WIDTH // 2,
        65,
        True
    )

    draw_text(
        "LEVEL UP YOUR GAMING EXPERIENCE",
        subtitle_font,
        GRAY,
        WIDTH // 2,
        110,
        True
    )

    draw_text(
        "Choose your gaming plan",
        card_title_font,
        WHITE,
        WIDTH // 2,
        160,
        True
    )

    # Cards
    card_width = 330
    card_height = 475
    gap = 25

    start_x = (
        WIDTH -
        (card_width * 3 + gap * 2)
    ) // 2

    buttons = []

    for i, plan in enumerate(plans):

        x = start_x + i * (card_width + gap)
        y = 210

        card_rect = pygame.Rect(
            x,
            y,
            card_width,
            card_height
        )

        # Card
        pygame.draw.rect(
            screen,
            CARD,
            card_rect,
            border_radius=25
        )

        pygame.draw.rect(
            screen,
            plan["color"],
            card_rect,
            width=2,
            border_radius=25
        )

        # Premium badge
        if i == 1:

            badge = pygame.Rect(
                x + 75,
                y + 12,
                180,
                30
            )

            pygame.draw.rect(
                screen,
                PURPLE,
                badge,
                border_radius=15
            )

            draw_text(
                "⭐ MOST POPULAR",
                small_font,
                WHITE,
                badge.centerx,
                badge.centery,
                True
            )

        # Icon
        draw_text(
            plan["icon"],
            card_title_font,
            WHITE,
            x + card_width // 2,
            y + 80,
            True
        )

        # Name
        draw_text(
            plan["name"],
            card_title_font,
            WHITE,
            x + card_width // 2,
            y + 125,
            True
        )

        # Price
        draw_text(
            plan["price"],
            price_font,
            plan["color"],
            x + card_width // 2,
            y + 175,
            True
        )

        draw_text(
            "/ month",
            small_font,
            GRAY,
            x + card_width // 2,
            y + 215,
            True
        )

        # Features
        feature_y = y + 250

        for feature in plan["features"]:

            draw_text(
                "✓",
                normal_font,
                plan["color"],
                x + 30,
                feature_y
            )

            draw_text(
                feature,
                normal_font,
                GRAY,
                x + 55,
                feature_y
            )

            feature_y += 32

        # Button
        button_rect = pygame.Rect(
            x + 50,
            y + card_height - 60,
            card_width - 100,
            42
        )

        draw_button(
            button_rect,
            f"CHOOSE {plan['name']}",
            plan["color"],
            mouse_pos
        )

        buttons.append((button_rect, plan))

    return buttons


# =========================================================
# PAYMENT PAGE
# =========================================================

def draw_payment(mouse_pos):

    draw_background()

    # Window
    box = pygame.Rect(
        350,
        100,
        500,
        550
    )

    pygame.draw.rect(
        screen,
        CARD,
        box,
        border_radius=25
    )

    pygame.draw.rect(
        screen,
        CYAN,
        box,
        width=2,
        border_radius=25
    )

    draw_text(
        "💳 COMPLETE SUBSCRIPTION",
        card_title_font,
        CYAN,
        WIDTH // 2,
        150,
        True
    )

    draw_text(
        f"{selected_plan['name']} PLAN",
        card_title_font,
        WHITE,
        WIDTH // 2,
        200,
        True
    )

    draw_text(
        f"{selected_plan['price']} / MONTH",
        price_font,
        selected_plan["color"],
        WIDTH // 2,
        245,
        True
    )

    # Name box
    draw_text(
        "CARDHOLDER NAME",
        small_font,
        GRAY,
        420,
        300
    )

    name_box = pygame.Rect(
        420,
        325,
        360,
        45
    )

    pygame.draw.rect(
        screen,
        (8, 8, 18),
        name_box,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        CYAN,
        name_box,
        width=1,
        border_radius=10
    )

    draw_text(
        name_text if name_text else "Enter your name...",
        normal_font,
        WHITE if name_text else GRAY,
        435,
        340
    )

    # Payment box
    draw_text(
        "PAYMENT DETAILS",
        small_font,
        GRAY,
        420,
        395
    )

    payment_box = pygame.Rect(
        420,
        420,
        360,
        45
    )

    pygame.draw.rect(
        screen,
        (8, 8, 18),
        payment_box,
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        CYAN,
        payment_box,
        width=1,
        border_radius=10
    )

    display_payment = "*" * len(payment_text)

    draw_text(
        display_payment if payment_text else "Enter demo payment...",
        normal_font,
        WHITE if payment_text else GRAY,
        435,
        435
    )

    # Pay button
    pay_button = pygame.Rect(
        420,
        500,
        360,
        50
    )

    draw_button(
        pay_button,
        "🔒 COMPLETE PAYMENT",
        PURPLE,
        mouse_pos
    )

    # Back button
    back_button = pygame.Rect(
        420,
        570,
        150,
        40
    )

    draw_button(
        back_button,
        "← BACK",
        (80, 80, 100),
        mouse_pos
    )

    return name_box, payment_box, pay_button, back_button


# =========================================================
# SUCCESS PAGE
# =========================================================

def draw_success():

    draw_background()

    draw_text(
        "✅",
        title_font,
        GREEN,
        WIDTH // 2,
        220,
        True
    )

    draw_text(
        "PAYMENT SUCCESSFUL!",
        title_font,
        GREEN,
        WIDTH // 2,
        300,
        True
    )

    draw_text(
        f"Welcome to Gamers Hub!",
        card_title_font,
        WHITE,
        WIDTH // 2,
        365,
        True
    )

    draw_text(
        f"You are now subscribed to the",
        normal_font,
        GRAY,
        WIDTH // 2,
        410,
        True
    )

    draw_text(
        f"{selected_plan['name']} PLAN",
        card_title_font,
        selected_plan["color"],
        WIDTH // 2,
        450,
        True
    )

    draw_text(
        "🎮 GAME ON! 🚀",
        card_title_font,
        CYAN,
        WIDTH // 2,
        530,
        True
    )


# =========================================================
# MAIN LOOP
# =========================================================

running = True

while running:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # -----------------------------------------
        # HOME
        # -----------------------------------------

        if page == "home":

            if event.type == pygame.MOUSEBUTTONDOWN:

                buttons = draw_home(mouse_pos)

                for button, plan in buttons:

                    if button.collidepoint(mouse_pos):

                        selected_plan = plan

                        name_text = ""
                        payment_text = ""

                        page = "payment"

        # -----------------------------------------
        # PAYMENT
        # -----------------------------------------

        elif page == "payment":

            if event.type == pygame.KEYDOWN:

                # Backspace
                if event.key == pygame.K_BACKSPACE:

                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        payment_text = payment_text[:-1]

                    else:
                        name_text = name_text[:-1]

                # TAB switches fields
                elif event.key == pygame.K_TAB:
                    pass

                # Enter
                elif event.key == pygame.K_RETURN:

                    if name_text and payment_text:
                        page = "success"

                else:

                    char = event.unicode

                    if char.isprintable():

                        if len(name_text) < 25:
                            name_text += char

            if event.type == pygame.MOUSEBUTTONDOWN:

                name_box, payment_box, pay_button, back_button = draw_payment(
                    mouse_pos
                )

                if name_box.collidepoint(mouse_pos):
                    pass

                elif payment_box.collidepoint(mouse_pos):
                    pass

                elif pay_button.collidepoint(mouse_pos):

                    if not name_text or not payment_text:

                        print("Please enter all details!")

                    else:

                        page = "success"

                elif back_button.collidepoint(mouse_pos):

                    page = "home"

        # -----------------------------------------
        # SUCCESS
        # -----------------------------------------

        elif page == "success":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    page = "home"

    # =====================================================
    # DRAW CURRENT PAGE
    # =====================================================

    if page == "home":

        draw_home(mouse_pos)

    elif page == "payment":

        draw_payment(mouse_pos)

    elif page == "success":

        draw_success()

    pygame.display.flip()

    clock.tick(60)


pygame.quit()
sys.exit()