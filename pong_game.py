import pygame

pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font('vaca.ttf', 20)

# RGB values of standard colors
LIGHT_ORANGE = (221, 190, 169)
LIGHT_YELLOW = (235, 225, 205)
BROWN = (88, 64, 52)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

clock = pygame.time.Clock()
FPS = 30


# Striker class


class Striker:
    # Take the initial position, dimensions, speed and color of the object
    def __init__(self, pos_x, pos_y, width, height, speed, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        # Rect that is used to control the position and collision of the object
        self.geekRect = pygame.Rect(pos_x, pos_y, width, height)
        # Object that is blit on the screen
        self.player = pygame.draw.rect(screen, self.color, self.geekRect)

    # Used to display the object on the screen
    def display(self):
        self.player = pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, y_fac):
        self.pos_y = self.pos_y + self.speed * y_fac

        # Restricting the striker to be below the top surface of the screen
        if self.pos_y <= 0:
            self.pos_y = 0
        # Restricting the striker to be above the bottom surface of the screen
        elif self.pos_y + self.height >= HEIGHT:
            self.pos_y = HEIGHT - self.height

        # Updating the rect with the new values
        self.geekRect = (self.pos_x, self.pos_y, self.width, self.height)

    def display_score(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        text_rect = text.get_rect()
        text_rect.center = (x, y)

        screen.blit(text, text_rect)

    def get_rect(self):
        return self.geekRect


# Ball class


class Ball:
    def __init__(self, pos_x, pos_y, radius, speed, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.radius = radius
        self.speed = speed
        self.color = color
        self.x_fac = 1
        self.y_fac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.pos_x, self.pos_y), self.radius)
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.pos_x, self.pos_y), self.radius)

    def update(self):
        self.pos_x += self.speed * self.x_fac
        self.pos_y += self.speed * self.y_fac

        # If the ball hits the top or bottom surfaces,
        # then the sign of y_fac is changed and
        # it results in a reflection
        if self.pos_y <= 0 or self.pos_y >= HEIGHT:
            self.y_fac *= -1

        if self.pos_x <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.pos_x >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.pos_x = WIDTH // 2
        self.pos_y = HEIGHT // 2
        self.x_fac *= -1
        self.firstTime = 1

    # Used to reflect the ball along the X-axis
    def hit(self):
        self.x_fac *= -1

    def get_rect(self):
        return self.ball


# Game Manager

def main():
    running = True

    # Defining the objects
    first_player = Striker(20, 0, 10, 100, 10, BROWN)
    second_player = Striker(WIDTH - 30, 0, 10, 100, 10, BROWN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, LIGHT_YELLOW)

    players_list = [first_player, second_player]

    # Initial parameters of the players
    first_player_score, second_player_score = 0, 0
    first_player_y_fac, second_player_y_fac = 0, 0

    while running:
        screen.fill(LIGHT_ORANGE)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    second_player_y_fac = -1
                if event.key == pygame.K_DOWN:
                    second_player_y_fac = 1
                if event.key == pygame.K_w:
                    first_player_y_fac = -1
                if event.key == pygame.K_s:
                    first_player_y_fac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    second_player_y_fac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    first_player_y_fac = 0

        # Collision detection
        for player in players_list:
            if pygame.Rect.colliderect(ball.get_rect(), player.get_rect()):
                ball.hit()

        # Updating the objects
        first_player.update(first_player_y_fac)
        second_player.update(second_player_y_fac)
        point = ball.update()

        # -1 -> Geek_1 has scored
        # +1 -> Geek_2 has scored
        # 0 -> None of them scored
        if point == -1:
            first_player_score += 1
        elif point == 1:
            second_player_score += 1

        # Someone has scored
        # a point and the ball is out of bounds.
        # So, we reset it's position
        if point:
            ball.reset()

        # Displaying the objects on the screen
        first_player.display()
        second_player.display()
        ball.display()

        # Displaying the scores of the players
        first_player.display_score("Geek_1 : ", first_player_score, 100, 20, LIGHT_YELLOW)
        second_player.display_score("Geek_2 : ", second_player_score, WIDTH - 100, 20, LIGHT_YELLOW)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
