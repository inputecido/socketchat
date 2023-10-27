import socket
import threading
import curses
from curses import wrapper
from curses.textpad import Textbox , rectangle
from sys import getsizeof , argv
from time import sleep

def mssrecebida(janelamss,stdscr,x,y):
    global s
    mss = []

    while True:

            tamanho_resposta = s.recv(1024).strip()
            
            if tamanho_resposta.decode('utf-8').strip() == 'FIM' or tamanho_resposta.decode('utf-8').strip() == '52':

                break

            else:
                
                resposta = s.recv(int(tamanho_resposta)).decode('utf-8').strip()

                mss.append(resposta)
                janelamss.clear()
                try:
                    if len(mss) >= y-11:mss.pop(0)

                    for linha in mss:janelamss.addstr(f'{linha}\n')
                except:pass

                janelamss.refresh(0,0,2,2,y-11,x-2) 



    s.close() 


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


def main(stdscr):
    try:nick = f'[{argv[1]}] '
    except:nick = ' '
    stdscr.clear()
    stdscr.refresh()
    global s
    s.connect(('localhost',5000))

    y , x = stdscr.getmaxyx()
    
    bordamss = curses.newwin(y-10,x-3,1,1)
    bordamss.border()
    bordamss.refresh()
    janelamss = curses.newpad(y-12,x-5)
    janelamss.refresh(0,0,2,2,y-11,x-2)
    bordamss = rectangle(stdscr,y-7,5,y-5,x-25)
    winmss = curses.newwin(1,x-35,y-6,10)
    boxmss = Textbox(winmss)
    stdscr.refresh()
        
    receber = threading.Thread(target=mssrecebida,args=(janelamss,stdscr,x,y))
    receber.start()



    while True: 
        stdscr.addstr(y-6,6,'[l]>')
        stdscr.refresh()
        boxmss.edit()

        if (mss:= boxmss.gather().strip()) == '/listar':

            s.send(f'!M-listar_usuarios'.encode('utf-8'))
            receber.join(0.1)

        elif mss == '/global':
        
            stdscr.addstr(y-6,6,'[g]>')
            stdscr.refresh()
            boxmss.edit()

            s.send('!M-mssglobal'.encode('utf-8'))
            while True:
                boxmss.edit()
                if (mss:=boxmss.gather().strip()) == '/leave':break
                if len(mss.strip()) > 0:s.send((nick+mss).encode('utf-8'))
                sleep(0.1)
            s.send(mss.encode('utf-8'))
 




        elif mss == '/sair':
            s.send((f'!M-SAIR'+(' '*(1024-len(str(getsizeof('!M-SAIR')))))).encode('utf-8'))
            exit('programa finalizado')
            



wrapper(main)
