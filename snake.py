import turtle
import time
import random

# 화면 설정
screen = turtle.Screen()
screen.title("뱀 게임")
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.tracer(0)

# 뱀 설정
snake = turtle.Turtle()
snake.shape("square")
snake.color("lime")
snake.speed(0)
snake_segments = [snake]
snake_direction = "right"
next_direction = "right"

# 음식 설정
food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.speed(0)
food.penup()
food.goto(random.randint(-20, 20) * 20, random.randint(-15, 15) * 20)

# 점수 설정
score = 0
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-380, 280)

def update_score():
    score_display.clear()
    score_display.write(f"점수: {score}", align="left", font=("Arial", 16, "normal"))

def move_snake():
    global snake_direction, next_direction
    snake_direction = next_direction
    
    # 현재 머리 위치
    head = snake_segments[-1]
    
    # 방향에 따라 새로운 위치 계산
    if snake_direction == "right":
        new_x = head.xcor() + 20
        new_y = head.ycor()
    elif snake_direction == "left":
        new_x = head.xcor() - 20
        new_y = head.ycor()
    elif snake_direction == "up":
        new_x = head.xcor()
        new_y = head.ycor() + 20
    elif snake_direction == "down":
        new_x = head.xcor()
        new_y = head.ycor() - 20
    
    # 새로운 머리 생성
    new_head = turtle.Turtle()
    new_head.shape("square")
    new_head.color("lime")
    new_head.speed(0)
    new_head.penup()
    new_head.goto(new_x, new_y)
    snake_segments.append(new_head)
    
    # 음식 먹었는지 확인
    if new_head.distance(food) < 15:
        global score
        score += 10
        food.goto(random.randint(-20, 20) * 20, random.randint(-15, 15) * 20)
        update_score()
    else:
        # 꼬리 제거
        tail = snake_segments.pop(0)
        tail.hideturtle()

def check_collision():
    # 벽과 충돌 확인
    head = snake_segments[-1]
    if head.xcor() < -400 or head.xcor() >= 400 or head.ycor() < -300 or head.ycor() >= 300:
        return True
    
    # 자기 몸과 충돌 확인
    for segment in snake_segments[:-1]:
        if head.distance(segment) < 1:
            return True
    
    return False

def game_over():
    game_over_text = turtle.Turtle()
    game_over_text.speed(0)
    game_over_text.color("white")
    game_over_text.penup()
    game_over_text.goto(0, 0)
    game_over_text.write(f"게임 오버!\n최종 점수: {score}", align="center", font=("Arial", 24, "bold"))

def move_right():
    global next_direction
    if snake_direction != "left":
        next_direction = "right"

def move_left():
    global next_direction
    if snake_direction != "right":
        next_direction = "left"

def move_up():
    global next_direction
    if snake_direction != "down":
        next_direction = "up"

def move_down():
    global next_direction
    if snake_direction != "up":
        next_direction = "down"

# 키 바인딩
screen.listen()
screen.onkey(move_right, "Right")
screen.onkey(move_left, "Left")
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")

# 초기 점수 표시
update_score()

# 게임 루프
running = True
while running:
    screen.update()
    time.sleep(0.1)
    
    move_snake()
    
    if check_collision():
        game_over()
        running = False

screen.mainloop()
