import pygame
import math

BLACK = (0, 0, 0) #define colors
WHITE = (255, 255, 255)
GREY = (150, 150, 150)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DARK_GREEN = (0, 150, 0)
DARK_BLUE = (0, 0, 100)

YELLOW = (255,255,0)
PURPLE = (255,0,255)
HOT_PINK = (255,105,180)

BLOCK_SIZE = 45 
MARGIN = 5
UNIT = MARGIN + BLOCK_SIZE
BLOCK_VAL = 0

LEFT = 1
RIGHT = 3

ship_len = [5, 4, 3, 3, 2]
 
Letter = ['A','B','C','D','E','F','G','H','I','J']
Number = ['1','2','3','4','5','6','7','8','9','10']

ocean_grid = []
screen_grid = []

ship_info = []

for row in range(10): #insert 0 in every position of the 3D array ocean_grid[row][column][val]
    ocean_grid.append([])
    for column in range(10):
        ocean_grid[row].append([])
        for val in range(3):
            ocean_grid[row][column].append(0)

for row in range(10): #insert 0 in every position of the 2D array ocean_grid[row][column]
    screen_grid.append([])
    for column in range(10):
        screen_grid[row].append([])
        for values in range(2):
            screen_grid[row][column].append(0)

for order in range(5): #insert 0 in every position of the 2D array ocean_grid[row][column]
    ship_info.append([])
    for details in range(5):
        ship_info[order].append(0)

pygame.init()

WINDOW_SIZE = [26*UNIT, 15*UNIT] # set up window
screen = pygame.display.set_mode(WINDOW_SIZE) 
font = pygame.font.SysFont('arial', BLOCK_SIZE)
pygame.display.set_caption("BATTLESHIP : The Classic Naval Combat Game")

done = False
placed = 0
orientation = 1
across = 1
down = 0
order = 0
index = 0
turns = 0
#max_row = 100
 
clock = pygame.time.Clock()

#Place Ships (First Battleship)
while placed != 5: 
    for event in pygame.event.get(): 
        pos = pygame.mouse.get_pos()

        for row in range(0,10):
            for column in range(0,10):
                for val in range(0,3):
                    ocean_grid[row][column][2] = 0 #reset temperary color value of all squares to 0

        if event.type == pygame.QUIT: #quit program condition
            placed = 5
            done = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            orientation = 0

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            orientation = 1

        
        elif event.type == pygame.MOUSEMOTION and pos[0] > 15*UNIT and pos[0] < 25*UNIT and pos[1] > 2*UNIT and pos[1] < 12*UNIT:
            column = (pos[0] - 15*UNIT)// UNIT 
            row = (pos[1] - 2*UNIT)// UNIT
            
            overlap = 0
            out_of_bounds = 0

            if orientation == 1:
                if column >= 11 - ship_len[placed]:
                    for i in range (column,10):
                        ocean_grid[row][i][2] = 2
                        out_of_bounds = 1

                elif column < 11 - ship_len[placed]:
                    for i in range (0,ship_len[placed]):
                        if ocean_grid[row][column+i][0] == 1:
                            overlap = 1
            
                    if overlap == 0:
                        for i in range (0,ship_len[placed]):
                            ocean_grid[row][column+i][2] = 1

                    elif overlap == 1:
                        for i in range (0,ship_len[placed]):
                            ocean_grid[row][column+i][2] = 2

            elif orientation == 0:
                if row >= 11 - ship_len[placed]:
                    for i in range (row,10):
                        ocean_grid[i][column][2] = 2
                        out_of_bounds = 1

                elif row < 11 - ship_len[placed]:
                    for i in range (0,ship_len[placed]):
                        if ocean_grid[row+i][column][0] == 1:
                            overlap = 1
            
                    if overlap == 0:
                        for i in range (0,ship_len[placed]):
                            ocean_grid[row+i][column][2] = 1

                    elif overlap == 1:
                        for i in range (0,ship_len[placed]):
                            ocean_grid[row+i][column][2] = 2

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and pos[0] > 15*UNIT and pos[0] < 25*UNIT and pos[1] > 2*UNIT and pos[1] < 12*UNIT and out_of_bounds == 0 and overlap == 0:
            column = (pos[0] - 15*UNIT)// UNIT
            row = (pos[1] - 2*UNIT)// UNIT

            ship_info[index][0] = row
            ship_info[index][1] = column
            ship_info[index][2] = orientation
            ship_info[index][3] = ship_len[placed]
            ship_info[index][4] = 0
            
            index += 1

            if orientation == 1:
                for i in range (0,ship_len[placed]):
                    ocean_grid[row][column+i][0] = 1
                    #ship_info[0]
            
            elif orientation == 0:
                for i in range (0,ship_len[placed]):
                    ocean_grid[row+i][column][0] = 1

            placed += 1

        screen.fill(BLACK)

        

        for row in range(0,10):
            for column in range(0,10):
                color = DARK_GREEN
                if screen_grid[row][column] == 1:
                    color = WHITE
                elif screen_grid[row][column] == 3:
                    color = RED
                pygame.draw.rect(screen, color, [2*UNIT+(UNIT * column) , (2*UNIT)+UNIT * row, BLOCK_SIZE, BLOCK_SIZE])

        for row in range(0,10):
            for column in range(0,10):
                color = DARK_BLUE
            
                if ocean_grid[row][column][2] == 2:
                    color = RED
                elif  ocean_grid[row][column][2] == 1 or ocean_grid[row][column][0] == 1:
                    color = GREY
                pygame.draw.rect(screen, color, [15*UNIT + UNIT * column ,(2*UNIT)+ UNIT * row, BLOCK_SIZE, BLOCK_SIZE])

    for i in range (0,10):
        text = font.render(Letter[i], True, WHITE)
        screen.blit(text, [1*UNIT,(2+i)*UNIT])
        screen.blit(text, [14*UNIT,(2+i)*UNIT])
        text = font.render(Number[i], True, WHITE)
        screen.blit(text, [(2+i)*UNIT,1*UNIT])
        screen.blit(text, [(15+i)*UNIT,1*UNIT])

    text = font.render("SCREEN", True, WHITE)
    screen.blit(text, [5*UNIT,12*UNIT])
    text = font.render("OCEAN", True, WHITE)
    screen.blit(text, [18*UNIT,12*UNIT])

    clock.tick(60)

    pygame.display.flip()

# Play Game
while not done:
    sink_status = 1
    index = 0
    for event in pygame.event.get(): 
        pos = pygame.mouse.get_pos()

        sink_status = 1
        check_i = 10
        if event.type == pygame.QUIT:  
            done = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and pos[0] > 15*UNIT and pos[0] < 25*UNIT and pos[1] > 2*UNIT and pos[1] < 12*UNIT:
            column = (pos[0] - 15*UNIT)// UNIT 
            row = (pos[1] - 2*UNIT)// UNIT
            if (ocean_grid[row][column][1] != 1 and ocean_grid[row][column][1] != 3 and ocean_grid[row][column][0] == 0):
                ocean_grid[row][column][1] = 1
                print("Opponent's Turn : ", Letter[row], Number[column], "MISS")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT and pos[0] > 15*UNIT and pos[0] < 25*UNIT and pos[1] > 2*UNIT and pos[1] < 12*UNIT:
            column = (pos[0] - 15*UNIT)// UNIT
            row = (pos[1] - 2*UNIT)// UNIT
            if (ocean_grid[row][column][1] != 1 and ocean_grid[row][column][1] != 3 and ocean_grid[row][column][0] == 1):
                ocean_grid[row][column][1] = 3 # hit
                #if ship_info[index]
                for i in range(5):
                    if ship_info[i][2] == 1:
                        for j in range (ship_info[i][3]):
                            if (row == ship_info[i][0] and column == ship_info[i][1] + j):
                                check_i = i

                    elif ship_info[i][2] == 0:
                        for j in range (ship_info[i][3]):
                            if (row == ship_info[i][0] + j and column == ship_info[i][1]):
                                check_i = i
                                
                if check_i != 10:
                    if ship_info[check_i][2] == 1:
                        for j in range (ship_info[check_i][3]):
                            if ocean_grid[ship_info[check_i][0]][ship_info[check_i][1] + j][1] == 0:
                                sink_status = 0

                    elif ship_info[check_i][2] == 0:
                        for j in range (ship_info[check_i][3]):
                            if ocean_grid[ship_info[check_i][0] + j][ship_info[check_i][1]][1] == 0:
                                sink_status = 0

                if sink_status == 0:
                    print("Opponent's Turn : ", Letter[row], Number[column], "HIT")
                elif sink_status == 1:
                    print("Opponent's Turn : ", Letter[row], Number[column], "HIT", "SINK")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and pos[0] > 2*UNIT and pos[0] < 12*UNIT and pos[1] > 2*UNIT and pos[1] < 12*UNIT:
            column = (pos[0] - 2*UNIT)// UNIT
            row = (pos[1] - 2*UNIT)// UNIT
            if (screen_grid[row][column][0] != 1 and screen_grid[row][column][0] != 3):
                screen_grid[row][column][0] = 1
                screen_grid[row][column][1] = 0
                turns += 1
                print("My turn         : ", Letter[row], Number[column], "MISS")

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT and pos[0] > 2*UNIT and pos[0] < 12*UNIT and pos[1] > 2*UNIT and pos[1] < 12*UNIT:
            column = (pos[0] - 2*UNIT)// UNIT 
            row = (pos[1] - 2*UNIT)// UNIT
            if (screen_grid[row][column][0] != 1 and screen_grid[row][column][0] != 3):
                screen_grid[row][column][0] = 3
                screen_grid[row][column][1] = 0
                turns += 1
                print("My turn         : ", Letter[row], Number[column], "HIT")
        
        max_val = 0
        intensity = 0
        total_val = 0
        max_row = 99
        max_column = 99
        loop_break = 0

        for row in range(10):
            for column in range(10):
                screen_grid[row][column][1] = 0

        for i in range(5):
            for j in range(11-ship_len[i]):
                for k in range(10):
                    #for orientation == 1 and 0 positions:
                    valid_hor = 1
                    valid_vert = 1
                    for inc in range (0,ship_len[i]):
                        if screen_grid[k][j+inc][0] == 1 or screen_grid[k][j+inc][0] == 3:
                            valid_hor = 0
                        if screen_grid[j+inc][k][0] == 1 or screen_grid[k][j+inc][0] == 3:
                            valid_vert = 0

                    if valid_hor == 1:
                        for inc in range (0,ship_len[i]):
                            if screen_grid[k][j+inc][0] == 0:
                                screen_grid[k][j+inc][1] += 1
                    if valid_vert == 1:
                        for inc in range (0,ship_len[i]):
                            if screen_grid[j+inc][k][0] == 0:
                                screen_grid[j+inc][k][1] += 1

        for row in range(10):
            for column in range(10):
                total_val += screen_grid[row][column][1]
                if screen_grid[row][column][1] > max_val:
                    max_val = screen_grid[row][column][1]

        for row in range(10):
            if loop_break == 1:
                break
            for column in range(10):
                if screen_grid[row][column][1] == max_val:
                    max_row = row
                    max_column = column
                    loop_break = 1
                    break

        screen.fill(BLACK)


    

        for row in range(0,10):
            for column in range(0,10):
                if max_val != 0:
                    intensity = (screen_grid[row][column][1]*255)/max_val
                elif max_val == 0:
                    intensity = 0
                color = (0,intensity,255-intensity)
                #color = (0,intensity,0)
                if row == max_row and column == max_column:
                    color = HOT_PINK
                if screen_grid[row][column][0] == 1:
                    color = WHITE
                elif screen_grid[row][column][0] == 3:
                    color = RED
                pygame.draw.rect(screen, color, [2*UNIT+(UNIT * column) , (2*UNIT)+UNIT * row, BLOCK_SIZE, BLOCK_SIZE])

        for row in range(0,10):
            for column in range(0,10):
                color = DARK_BLUE
            
                if ocean_grid[row][column][1] == 1:
                    color = WHITE
                elif ocean_grid[row][column][1] == 3:
                    color = RED
                elif ocean_grid[row][column][0] == 1:
                    color = GREY
                pygame.draw.rect(screen, color, [15*UNIT + UNIT * column ,(2*UNIT)+ UNIT * row, BLOCK_SIZE, BLOCK_SIZE])

        font = pygame.font.SysFont('arial', math.floor(BLOCK_SIZE*0.85))
        for row in range (10):
            for column in range(10):
                if screen_grid[row][column][0] == 0:
                    text = font.render(str(screen_grid[row][column][1]), True, WHITE)
                    screen.blit(text, [(column+2)*UNIT,(row+2)*UNIT])

        font = pygame.font.SysFont('arial', BLOCK_SIZE)
        for i in range (0,10):
            text = font.render(Letter[i], True, WHITE)
            screen.blit(text, [1*UNIT,(2+i)*UNIT])
            screen.blit(text, [14*UNIT,(2+i)*UNIT])
            text = font.render(Number[i], True, WHITE)
            screen.blit(text, [(2+i)*UNIT,1*UNIT])
            screen.blit(text, [(15+i)*UNIT,1*UNIT])

        text = font.render("SCREEN", True, WHITE)
        screen.blit(text, [5*UNIT,12*UNIT])
        
        text = font.render("OCEAN", True, WHITE)
        screen.blit(text, [18*UNIT,12*UNIT])

        font = pygame.font.SysFont('arial', math.floor(BLOCK_SIZE*0.85))

        text = font.render("Total Value : " + str(total_val), True, WHITE)
        screen.blit(text, [10*UNIT,12*UNIT])

        text = font.render("Turns : " + str(turns), True, WHITE)
        screen.blit(text, [10*UNIT,13*UNIT])

        text = font.render("Suggestion :",True, WHITE)
        screen.blit(text, [10*UNIT,14*UNIT])

        text = font.render(Letter[max_row], True, WHITE)
        screen.blit(text, [15*UNIT,14*UNIT])

        text = font.render(Number[max_column], True, WHITE)
        screen.blit(text, [16*UNIT,14*UNIT])

    clock.tick(60)

    pygame.display.flip()

pygame.quit()