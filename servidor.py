import socket
import threading
from sys import getsizeof

usuarios = []
lista_addr = []


def cliente(conn,addr):
    global usuarios , lista_addr

    print('novo cliente conectado')
    while True:

        mss = conn.recv(1024)


        if mss.decode('utf-8').strip() == '!M-listar_usuarios':
            lista_usuarios = str(lista_addr)
            lista_usuarios = ('conexões: '+lista_usuarios+(' '*(1014-len(lista_usuarios)))).encode('utf-8')
            tamanho = (str(getsizeof(lista_usuarios)).encode('utf-8'))
            
            conn.send((tamanho+(' '*(1024-len(tamanho))).encode('utf-8')))

            conn.send(lista_usuarios)

            
            
        elif mss.decode('utf-8').strip() == '!M-mssglobal':
            print('mais um falando no global')
            while (mss := conn.recv(1024)).decode('utf-8').strip() != 'leave':                    
                for i in usuarios:
                    try:
                        i[1].send((str(getsizeof(f'\n[{addr}]'.encode('utf-8')+mss))+(' '*(1024-len(str(getsizeof(f'\n[{i[0]}] '.encode('utf-8')+mss)))))).encode('utf-8'))
                        i[1].send(f'\n[{addr}]'.encode('utf-8')+mss)
                    except:   
                        usuarios.remove(i)
                        lista_addr.remove(i[0])


            print('menos um falando no global')
            


        elif mss.decode('utf-8').strip() == '!M-SAIR':
            conn.send('FIM'.encode('utf-8'))

            usuarios.remove((addr,conn))
            lista_addr.remove(addr)

        #conn.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('localhost',5000))

    while True:

        s.listen()

        conn , addr = s.accept()
        usuarios.append((addr,conn))
        lista_addr.append(addr)
        threading.Thread(target=cliente,args=(conn,addr)).start()


main()
