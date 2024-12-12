import time
import os
# Configuration
path = ‘app/player_2/’
input_file = path + “data.txt”
output_file = path + “direction.txt”
# Constans
PLAYER_HEIGHT = 50
PLAYER_WIDTH = 10
BOARD_HEIGHT = 600
BALL_DIAMETER = 14
PLAYER_OFFSET = 50
# Flags
READ_FLAGS = os.O_RDONLY
WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
# Variables
last_ball_x = None
last_ball_y = None
ball_velocity = 0
ball_direction_y = 0
ball_direction_x = ‘’
player_side = ‘’
# Delay en milisegundos
def delay(ms):
    time.sleep(ms / 1000.0)
def move_center(player_y, limit=300):
    if player_y > limit:
        return -1
    elif player_y < limit:
        return 1
    else:
        return 0
def how_move_player(player_y, ball_y, ball_direction_y, ball_direction_x, player_side, direction):
    predicted_by = ball_y + ball_direction_y * 0.05
    if ball_direction_y > 0 and predicted_by > player_y + 10:
        direction = 1
    elif ball_direction_y < 0 and predicted_by < player_y - 10:
        direction = -1
    if player_y <= 50 and direction == -1:
        direction = 0
    elif player_y + PLAYER_HEIGHT >= BOARD_HEIGHT and direction == 1:
        direction = 0
    if player_side == ‘left’ and ball_direction_x != ‘left’:
        direction = move_center(player_y)
    elif player_side == ‘right’ and ball_direction_x != ‘right’:
        direction = move_center(player_y)
    return direction
try:
    while True:
        print(‘PLAYER 2’)
        try:
            fd_input = os.open(input_file, READ_FLAGS)
            input_data = os.read(fd_input, 1024).decode(“utf-8")
            os.close(fd_input)
        except FileNotFoundError:
            print(f”Error: {input_file} no encontrado.“)
            break
        if input_data:
            player_x, player_y, energy, ball_x, ball_y = map(float, input_data.split(“,”))
            direction = 0
            if last_ball_x is not None and last_ball_y is not None:
                ball_velocity = ((ball_x - last_ball_x)**2 + (ball_y - last_ball_y)**2)**0.5
                ball_direction_y = ball_y - last_ball_y
            if player_x <= 55:
                player_side = ‘left’
            elif player_x >= 845:
                player_side = ‘right’
            if last_ball_x is not None:
                if ball_x > last_ball_x:
                    ball_direction_x = ‘right’
                elif ball_x < last_ball_x:
                    ball_direction_x = ‘left’
            last_ball_x, last_ball_y = ball_x, ball_y
            direction = how_move_player(player_y, ball_y, ball_direction_y, ball_direction_x, player_side, direction)
            try:
                fd_output = os.open(output_file, WRITE_FLAGS)
                os.write(fd_output, str(direction).encode(“utf-8"))
                os.close(fd_output)
            except Exception as err:
                print(f”Error al escribir dirección: {err}“)
        delay(30)
except KeyboardInterrupt:
    print(“Proceso interrumpido.“)
except Exception as e:
    print(f”Error inesperado: {e}“)