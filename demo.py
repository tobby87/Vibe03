import tkinter as tk
import random

WIDTH = 600
HEIGHT = 500
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_SIZE = 14
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = 54
BRICK_HEIGHT = 20
BRICK_PADDING = 6
TOP_OFFSET = 50

class BlockBreaker:
    def __init__(self, root):
        self.root = root
        self.root.title("블럭깨기 게임")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.score = 0
        self.lives = 3
        self.running = True

        self.paddle = self.canvas.create_rectangle(
            (WIDTH - PADDLE_WIDTH) / 2,
            HEIGHT - 40,
            (WIDTH + PADDLE_WIDTH) / 2,
            HEIGHT - 40 + PADDLE_HEIGHT,
            fill="skyblue"
        )

        self.ball = self.canvas.create_oval(
            WIDTH / 2 - BALL_SIZE / 2,
            HEIGHT / 2 - BALL_SIZE / 2,
            WIDTH / 2 + BALL_SIZE / 2,
            HEIGHT / 2 + BALL_SIZE / 2,
            fill="white"
        )

        self.ball_dx = 4
        self.ball_dy = -4

        self.bricks = []
        self.create_bricks()

        self.score_text = self.canvas.create_text(80, 20, fill="white", font=("Helvetica", 14), text=f"점수: {self.score}")
        self.lives_text = self.canvas.create_text(520, 20, fill="white", font=("Helvetica", 14), text=f"목숨: {self.lives}")
        self.message_text = self.canvas.create_text(WIDTH / 2, HEIGHT / 2, fill="yellow", font=("Helvetica", 24), text="")

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.start_game)
        self.root.bind("<Escape>", self.exit_game)

        self.update()

    def create_bricks(self):
        colors = ["red", "orange", "yellow", "green", "blue"]
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x1 = BRICK_PADDING + col * (BRICK_WIDTH + BRICK_PADDING)
                y1 = TOP_OFFSET + row * (BRICK_HEIGHT + BRICK_PADDING)
                x2 = x1 + BRICK_WIDTH
                y2 = y1 + BRICK_HEIGHT
                brick = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[row % len(colors)], width=0)
                self.bricks.append(brick)

    def move_left(self, event=None):
        if not self.running:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        if x1 > 0:
            self.canvas.move(self.paddle, -30, 0)

    def move_right(self, event=None):
        if not self.running:
            return
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        if x2 < WIDTH:
            self.canvas.move(self.paddle, 30, 0)

    def start_game(self, event=None):
        if not self.running:
            self.running = True
            self.ball_dx = random.choice([-4, 4])
            self.ball_dy = -4
            self.canvas.itemconfig(self.message_text, text="")
            self.update()

    def exit_game(self, event=None):
        self.root.destroy()

    def update(self):
        if self.running:
            self.move_ball()
            self.check_collisions()
            self.check_game_over()
        self.root.after(16, self.update)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        x1, y1, x2, y2 = self.canvas.coords(self.ball)

        if x1 <= 0 or x2 >= WIDTH:
            self.ball_dx *= -1
        if y1 <= 0:
            self.ball_dy *= -1

        if y2 >= HEIGHT:
            self.lose_life()

    def check_collisions(self):
        ball_coords = self.canvas.coords(self.ball)
        overlapping = self.canvas.find_overlapping(*ball_coords)

        for item in overlapping:
            if item == self.paddle and self.ball_dy > 0:
                self.ball_dy *= -1
                paddle_coords = self.canvas.coords(self.paddle)
                paddle_center = (paddle_coords[0] + paddle_coords[2]) / 2
                ball_center = (ball_coords[0] + ball_coords[2]) / 2
                diff = ball_center - paddle_center
                self.ball_dx = diff / (PADDLE_WIDTH / 2) * 6
                return

            if item in self.bricks:
                self.bricks.remove(item)
                self.canvas.delete(item)
                self.ball_dy *= -1
                self.score += 10
                self.canvas.itemconfig(self.score_text, text=f"점수: {self.score}")
                return

    def lose_life(self):
        self.lives -= 1
        self.canvas.itemconfig(self.lives_text, text=f"목숨: {self.lives}")
        if self.lives > 0:
            self.reset_ball()
        else:
            self.running = False
            self.canvas.itemconfig(self.message_text, text="게임 오버! 스페이스로 재시작")

    def reset_ball(self):
        self.canvas.coords(
            self.ball,
            WIDTH / 2 - BALL_SIZE / 2,
            HEIGHT / 2 - BALL_SIZE / 2,
            WIDTH / 2 + BALL_SIZE / 2,
            HEIGHT / 2 + BALL_SIZE / 2,
        )
        self.ball_dx = random.choice([-4, 4])
        self.ball_dy = -4
        self.running = False
        self.canvas.itemconfig(self.message_text, text="스페이스를 눌러 시작")

    def check_game_over(self):
        if not self.bricks:
            self.running = False
            self.canvas.itemconfig(self.message_text, text="클리어! 축하합니다!")

if __name__ == "__main__":
    root = tk.Tk()
    game = BlockBreaker(root)
    root.mainloop()

    