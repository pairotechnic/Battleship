# Standard Library Imports
import math
from datetime import datetime

# Third-Party Library Imports
import pygame

# Local Application Imports
from core.config import *
from core.board import create_ocean_grid, create_screen_grid, create_ship_info

ocean_grid = create_ocean_grid()
screen_grid = create_screen_grid()
ship_info = create_ship_info()

pygame.init()

WINDOW_SIZE = [26*UNIT, 15*UNIT] # set up window
screen = pygame.display.set_mode(WINDOW_SIZE) 
font = pygame.font.SysFont('arial', BLOCK_SIZE)
pygame.display.set_caption("BATTLESHIP : The Classic Naval Combat Game")

done = False
placed = 0
orientation = "horizontal"
across = 1
down = 0
order = 0
index = 0
turns = 0
#max_row = 100
 
clock = pygame.time.Clock()

overlap = False
out_of_bounds = False

#Place Ships (First Battleship)

# Runs 60 times per second due to clock.tick(60)
while placed != 5: 

    # Consumes all queued events since last frame execution of while loop above
    for event in pygame.event.get(): 
        pos = pygame.mouse.get_pos()

        for row in range(0,10):
            for column in range(0,10):
                ocean_grid[row][column]["preview"] = None #reset temperary color value of all squares to 0

        # quit program condition
        if (
            event.type == pygame.QUIT or
            (
                event.type == pygame.KEYUP and
                event.key == pygame.K_q
            )
        ):
            placed = 5
            done = True

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            orientation = "vertical"

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            orientation = "horizontal"

        elif (
            event.type in (pygame.MOUSEMOTION, pygame.KEYUP, pygame.MOUSEBUTTONUP) and 
            15*UNIT < pos[0] < 25*UNIT and 
            2*UNIT < pos[1] < 12*UNIT
        ):
            column = (pos[0] - 15*UNIT)// UNIT 
            row = (pos[1] - 2*UNIT)// UNIT

            overlap = False
            out_of_bounds = False

            if orientation == "horizontal":
                if column >= 11 - ship_len[placed]:
                    for i in range (column,10):
                        ocean_grid[row][i]["preview"] = "invalid"
                        out_of_bounds = True

                elif column < 11 - ship_len[placed]:
                    for i in range (0,ship_len[placed]):
                        if ocean_grid[row][column+i]["has_ship"]:
                            overlap = True
            
                    if not overlap:
                        for i in range (0,ship_len[placed]):
                            ocean_grid[row][column+i]["preview"] = "valid"

                    elif overlap:
                        for i in range (0,ship_len[placed]):
                            ocean_grid[row][column+i]["preview"] = "invalid"

            elif orientation == "vertical":
                if row >= 11 - ship_len[placed]:
                    for i in range (row,10):
                        ocean_grid[i][column]["preview"] = "invalid"
                        out_of_bounds = True

                elif row < 11 - ship_len[placed]:
                    for i in range (0,ship_len[placed]):
                        if ocean_grid[row+i][column]["has_ship"]:
                            overlap = True
            
                    if not overlap:
                        for i in range (0,ship_len[placed]):
                            ocean_grid[row+i][column]["preview"] = "valid"

                    elif overlap:
                        for i in range (0,ship_len[placed]):
                            ocean_grid[row+i][column]["preview"] = "invalid"

            if event.type == pygame.MOUSEBUTTONUP:
                print(f"out_of_bounds : {out_of_bounds}")
                print(f"overlap : {overlap}")

        elif (
            event.type == pygame.MOUSEBUTTONDOWN and 
            event.button == LEFT and 
            15*UNIT < pos[0] < 25*UNIT and 
            2*UNIT < pos[1] < 12*UNIT and 
            not out_of_bounds and 
            not overlap
        ):
            print(f"button down event triggerred : {datetime.now()}")
            print(f"out_of_bounds : {out_of_bounds}")
            print(f"overlap : {overlap}")
            column = (pos[0] - 15*UNIT)// UNIT
            row = (pos[1] - 2*UNIT)// UNIT

            ship_info[index]["row"] = row
            ship_info[index]["col"] = column
            ship_info[index]["orientation"] = orientation
            ship_info[index]["length"] = ship_len[placed]
            ship_info[index]["hits"] = 0
            
            index += 1

            if orientation == "horizontal":
                for i in range (0,ship_len[placed]):
                    ocean_grid[row][column+i]["has_ship"] = True
            
            elif orientation == "vertical":
                for i in range (0,ship_len[placed]):
                    ocean_grid[row+i][column]["has_ship"] = True
            
            placed += 1

        
        screen.fill(BLACK)

        for row in range(0,10):
            for column in range(0,10):
                color = DARK_GREEN
                if screen_grid[row][column]["shot"] == "miss":
                    color = WHITE
                elif screen_grid[row][column]["shot"] == "hit":
                    color = RED
                pygame.draw.rect(screen, color, [2*UNIT+(UNIT * column) , (2*UNIT)+UNIT * row, BLOCK_SIZE, BLOCK_SIZE])

        for row in range(0,10):
            for column in range(0,10):
                color = DARK_BLUE
            
                if ocean_grid[row][column]["preview"] == "invalid":
                    color = RED
                    
                elif ocean_grid[row][column]["preview"] == "valid" or ocean_grid[row][column]["has_ship"]:
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
        
        elif (
            event.type == pygame.MOUSEBUTTONDOWN and 
            event.button == LEFT and 
            15*UNIT < pos[0] < 25*UNIT and 
            2*UNIT < pos[1] < 12*UNIT
        ):
            column = (pos[0] - 15*UNIT)// UNIT 
            row = (pos[1] - 2*UNIT)// UNIT
            if (ocean_grid[row][column]["shot"] != "miss" and ocean_grid[row][column]["shot"] != "hit" and not ocean_grid[row][column]["has_ship"]):
                ocean_grid[row][column]["shot"] = "miss"
                print("Opponent's Turn : ", Letter[row], Number[column], "MISS")

        elif (
            event.type == pygame.MOUSEBUTTONDOWN and 
            event.button == RIGHT and 
            15*UNIT < pos[0] < 25*UNIT and 
            2*UNIT < pos[1] < 12*UNIT
        ):
            column = (pos[0] - 15*UNIT)// UNIT
            row = (pos[1] - 2*UNIT)// UNIT
            if (ocean_grid[row][column]["shot"] != "miss" and ocean_grid[row][column]["shot"] != "hit" and ocean_grid[row][column]["has_ship"]):
                ocean_grid[row][column]["shot"] = "hit" # hit

                for i in range(5):
                    if ship_info[i]["orientation"] == "horizontal":
                        for j in range (ship_info[i]["length"]):
                            if (row == ship_info[i]["row"] and column == ship_info[i]["col"] + j):
                                check_i = i

                    elif ship_info[i]["orientation"] == "vertical":
                        for j in range (ship_info[i]["length"]):
                            if (row == ship_info[i]["row"] + j and column == ship_info[i]["col"]):
                                check_i = i
                                
                if check_i != 10:
                    if ship_info[check_i]["orientation"] == "horizontal":
                        for j in range (ship_info[check_i]["length"]):
                            if not ocean_grid[ship_info[check_i]["row"]][ship_info[check_i]["col"] + j]["shot"]:
                                sink_status = 0

                    elif ship_info[check_i]["orientation"] == "vertical":
                        for j in range (ship_info[check_i]["length"]):
                            if not ocean_grid[ship_info[check_i]["row"] + j][ship_info[check_i]["col"]]["shot"]:
                                sink_status = 0

                if sink_status == 0:
                    print("Opponent's Turn : ", Letter[row], Number[column], "HIT")
                elif sink_status == 1:
                    print("Opponent's Turn : ", Letter[row], Number[column], "HIT", "SINK")

        elif (
            event.type == pygame.MOUSEBUTTONDOWN and 
            event.button == LEFT and 
            pos[0] > 2*UNIT and pos[0] < 12*UNIT and 
            pos[1] > 2*UNIT and pos[1] < 12*UNIT
        ):
            column = (pos[0] - 2*UNIT)// UNIT
            row = (pos[1] - 2*UNIT)// UNIT
            if (screen_grid[row][column]["shot"] != "miss" and screen_grid[row][column]["shot"] != "hit"):
                screen_grid[row][column]["shot"] = "miss"
                screen_grid[row][column]["score"] = 0
                turns += 1
                print("My turn         : ", Letter[row], Number[column], "MISS")

        elif (
            event.type == pygame.MOUSEBUTTONDOWN and 
            event.button == RIGHT and 
            2*UNIT < pos[0] < 12*UNIT and 
            2*UNIT < pos[1] < 12*UNIT
        ):
            column = (pos[0] - 2*UNIT)// UNIT 
            row = (pos[1] - 2*UNIT)// UNIT
            if (screen_grid[row][column]["shot"] != "miss" and screen_grid[row][column]["shot"] != "hit"):
                screen_grid[row][column]["shot"] = "hit"
                screen_grid[row][column]["score"] = 0
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
                screen_grid[row][column]["score"] = 0

        for i in range(5):
            for j in range(11-ship_len[i]):
                for k in range(10):
                    valid_hor = True
                    valid_vert = True
                    for inc in range (0,ship_len[i]):
                        if screen_grid[k][j+inc]["shot"] == "miss":
                            valid_hor = False
                        if screen_grid[j+inc][k]["shot"] == "miss":
                            valid_vert = False

                    if valid_hor:
                        for inc in range (0,ship_len[i]):
                            if not screen_grid[k][j+inc]["shot"]:
                                screen_grid[k][j+inc]["score"] += 1
                    if valid_vert:
                        for inc in range (0,ship_len[i]):
                            if not screen_grid[j+inc][k]["shot"]:
                                screen_grid[j+inc][k]["score"] += 1

        for row in range(10):
            for column in range(10):
                total_val += screen_grid[row][column]["score"]
                if screen_grid[row][column]["score"] > max_val:
                    max_val = screen_grid[row][column]["score"]

        for row in range(10):
            if loop_break == 1:
                break
            for column in range(10):
                if screen_grid[row][column]["score"] == max_val:
                    max_row = row
                    max_column = column
                    loop_break = 1
                    break

        screen.fill(BLACK)


    

        for row in range(0,10):
            for column in range(0,10):
                if max_val != 0:
                    intensity = (screen_grid[row][column]["score"]*255)/max_val
                elif max_val == 0:
                    intensity = 0
                color = (0,intensity,255-intensity)
                #color = (0,intensity,0)
                if row == max_row and column == max_column:
                    color = HOT_PINK
                if screen_grid[row][column]["shot"] == "miss":
                    color = WHITE
                elif screen_grid[row][column]["shot"] == "hit":
                    color = RED
                pygame.draw.rect(screen, color, [2*UNIT+(UNIT * column) , (2*UNIT)+UNIT * row, BLOCK_SIZE, BLOCK_SIZE])

        for row in range(0,10):
            for column in range(0,10):
                color = DARK_BLUE
            
                if ocean_grid[row][column]["shot"] == "miss":
                    color = WHITE
                elif ocean_grid[row][column]["shot"] == "hit":
                    color = RED
                elif ocean_grid[row][column]["has_ship"]:
                    color = GREY
                pygame.draw.rect(screen, color, [15*UNIT + UNIT * column ,(2*UNIT)+ UNIT * row, BLOCK_SIZE, BLOCK_SIZE])

        font = pygame.font.SysFont('arial', math.floor(BLOCK_SIZE*0.85))
        for row in range (10):
            for column in range(10):
                if not screen_grid[row][column]["shot"]:
                    text = font.render(str(screen_grid[row][column]["score"]), True, WHITE)
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