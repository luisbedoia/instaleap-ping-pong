import time
import os

# Configuración de los archivos de entrada y salida
path = 'app/player_2/'
input_file = path + "data.txt"
output_file = path + "direction.txt"

# Constantes del juego
PLAYER_HEIGHT = 50
PLAYER_WIDTH = 10
BOARD_HEIGHT = 600
BALL_DIAMETER = 14
PLAYER_OFFSET = 50

# Modo de apertura de archivos
READ_FLAGS = os.O_RDONLY
WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC

# Variables de predicción
last_bx = None
last_by = None
ball_velocity = 0  # Velocidad aproximada de la pelota (en píxeles/ms)
ball_direction_y = 0  # Dirección en el eje Y de la pelota
ball_direction_x = ''
player_side = ''

# Delay en milisegundos
def delay(ms):
    time.sleep(ms / 1000.0)

def move_center(py):
    if py > 300:
        return -1
    elif py < 300:
        return 1
    else:
        return 0

def how_move_player(py, by, ball_direction_y, ball_direction_x, player_side, direction):
    # Predicción de la posición futura de la pelota
    predicted_by = by + ball_direction_y * 0.05  # Predice posición en los próximos 50 ms

    # Lógica para mover el jugador
    if ball_direction_y > 0 and predicted_by > py + 10:  # La pelota viene hacia abajo
        direction = 1   # Mover hacia abajo
    elif ball_direction_y < 0 and predicted_by < py - 10:  # La pelota viene hacia arriba
        direction = -1  # Mover hacia arriba

    # Evitar moverse más allá del tablero
    if py <= 50 and direction == -1:
        direction = 0
    elif py + PLAYER_HEIGHT >= BOARD_HEIGHT and direction == 1:
        direction = 0

    if player_side == 'left' and ball_direction_x != 'left':
        direction = move_center(py)
    elif player_side == 'right' and ball_direction_x != 'right':
        direction = move_center(py)
    
    return direction

try:
    while True:
        print('PLAYER 2')        # Leer contenido del archivo de entrada
        try:
            fd_input = os.open(input_file, READ_FLAGS)
            input_data = os.read(fd_input, 1024).decode("utf-8")
            os.close(fd_input)
        except FileNotFoundError:
            print(f"Error: {input_file} no encontrado.")
            break

        # Procesar los datos
        if input_data:
            px, py, e, bx, by = map(float, input_data.split(","))
            direction = 0

            # Calcular la velocidad de la pelota y su dirección en Y
            if last_bx is not None and last_by is not None:
                ball_velocity = ((bx - last_bx)**2 + (by - last_by)**2)**0.5
                ball_direction_y = by - last_by  # Dirección en el eje Y

            if px <= 50:
                player_side = 'left'
            elif px >= 840:
                player_side = 'right'

            if last_bx is not None:
                if bx > last_bx:
                    ball_direction_x = 'right'
                elif bx < last_bx:
                    ball_direction_x = 'left'

            last_bx, last_by = bx, by

            # Logica para mover el jugador
            direction = how_move_player(py, by, ball_direction_y, ball_direction_x, player_side, direction)

            # Escribir la dirección en el archivo de salida
            try:
                fd_output = os.open(output_file, WRITE_FLAGS)
                os.write(fd_output, str(direction).encode("utf-8"))
                os.close(fd_output)
            except Exception as err:
                print(f"Error al escribir dirección: {err}")

        delay(30)

except KeyboardInterrupt:
    print("Proceso interrumpido.")
except Exception as e:
    print(f"Error inesperado: {e}")
