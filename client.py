import pygame
from sys import exit
from grid import Grid


win = pygame.display.set_mode((600,600))
pygame.display.set_caption("Tic Tac Toe")

import threading


def create_thread(target):
    thread = threading.Thread(target = target)
    thread.daemon = True
    thread.start()




import socket

HOST = "127.0.0.1"
PORT = 65432

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect((HOST,PORT))

def recieve_data():
    global turn
    while True: # infinite loop
        data = sock.recv(1024).decode() # not responsive
        data = data.split('-')
        x,y = int(data[0]), int(data[1])
        if data[2]=="yourturn":
            turn = True
        if data[3]=="False":
            grid.game_over = True
        if grid.get_block_value(x,y) ==0:
            grid.set_block_value(x,y,"X")
        print(data)

create_thread(recieve_data)




grid= Grid()

player = "O"


turn = False
playing = "True"


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed()[0]:
                if turn and not grid.game_over:
                    
                    pos = pygame.mouse.get_pos()
                    cellX,cellY = pos[0]//200,pos[1]//200
                    print(pos[0]//200,pos[1]//200) # amazing trick
                    grid.get_mouse(cellX,cellY,player)
                    if grid.game_over:
                        playing = "False"
                    send_data = "{}-{}-{}-{}".format(cellX,cellY,"yourturn",playing).encode()
                    sock.send(send_data)
                    turn = False
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over = False
                playing = "True"

    win.fill((0,0,0))

    grid.draw(win)
    
    
    pygame.display.flip()

