import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def create_chess_board():
    """
    This function creates a chess board with alternating black and white squares.
    """
    size = 8  # size of the board
    board = []

    for row in range(size):
        board.append([])
        for col in range(size):
            if (row + col) % 2 == 0:
                board[row].append((1.0, 1.0, 1.0))  # white square
            else:
                board[row].append((0.2, 0.2, 0.2))  # black square

    return board

def draw_chess_board(board, width):
    """
    This function draws the chess board on the screen using OpenGL.
    """
    glBegin(GL_QUADS)
    for row in range(len(board)):
        for col in range(len(board[row])):
            glColor3fv(board[row][col])
            glVertex3f(row - (width/2) + 0.5, col - (width/2) + 0.5, 0)
            glVertex3f(row - (width/2) + 1.5, col - (width/2) + 0.5, 0)
            glVertex3f(row - (width/2) + 1.5, col - (width/2) + 1.5, 0)
            glVertex3f(row - (width/2) + 0.5, col - (width/2) + 1.5, 0)
    glEnd()

def main():
    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    width = 8.0
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -10.0)
    glTranslatef(-(width - 1) / 2, -(width - 1) / 2, 0.0)  # center the board on the screen
    glEnable(GL_DEPTH_TEST)

    # initialize mouse movement variables
    mouse_down = False
    last_pos = None
    spin_speed = 0.1

    # create the chess board
    board = create_chess_board()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    last_pos = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False

        # handle mouse movement
        if mouse_down:
            curr_pos = pygame.mouse.get_pos()
            if last_pos:
                dx, dy = curr_pos[0] - last_pos[0], curr_pos[1] - last_pos[1]
                glRotatef(dx * spin_speed, 0, 1, 0)
                glRotatef(dy * spin_speed, 1, 0, 0)
            last_pos = curr_pos

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glClearColor(0.5, 0.5, 0.5, 0.5)  # set background color to gray
        draw_chess_board(board, width) 
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == '__main__':
    main()
