''' Traccia 2 - Corso di Programmazione di Reti - UniversitÃ  di Bologna - di Parrinello Angelo'''

#!/bin/env python
from time import *
import sys, signal
import http.server
import socketserver



def accedi():
    #variabili per la funzione
    found_id = 0
    found_psw = 0
    counter = 0
    max_error = 3
    u="a"
    p="b"
    
    while True:
        #prende in inpu id e psw
        u = input('UserID:')+"\n"
        p = input('Password:')+"\n"
        #apre i file .txt
        file_id = open("userID.txt", "r")
        file_psw = open("password.txt", "r")
        #controlla che ci sia l'id
        for line in file_id :
            if u == line :
                found_id = 1
                
         #controlla che ci sia la psw       
        for line2 in file_psw :
            if p == line2:
                found_psw = 1
        #chiude i file    
        file_psw.close()     
        file_id.close()
        if found_id == 1 and found_psw == 1 :
            print("Hi:",u)
            print("Welcome to the Angelo's Web Server")
            break
        else :
            found_id = 0
            found_psw = 0
            counter = counter + 1
            print("Your userID or password were wrong")
            print ("Error number:", counter)
            #interrompe l'esecuzione se sbaglio password o Id o entrambi un numero pari a max_error di volte
            if counter == max_error :
              print( 'Exiting http server (max Attempts made)')
              sleep(3)
              sys.exit(0) 

def registrati():
    id_used = 0
    
    while True:
        id_used = 0
        u = input('UserID: ')+"\n"
        p = input('Password:')+"\n"
        #apre prima il file in modalità lettura per vedere se l'id già esiste
        file_id_1 = open("userID.txt", "r")
        for line in file_id_1 :
                if u == line :
                    print("UserID already used\n Please change it\n")
                    id_used=1
                    break
        if id_used == 0:
            print("Ok the information are valide\n")
            break
                    
    file_id_1.close()
    #apre i file per scrivere i nuovi dati
    file_id = open("userID.txt", "a")
    file_id.write(u+"\n")
    file_id.close()
    file_psw = open("password.txt", "a")
    file_psw.write(p+"\n")
    file_psw.close()
    print("Hi:",u)
    print("Welcome to the Angelo's Web Server")
    
while True:
    intro = input("\n What do you want to do? Access or Sign in? (access/signin)>")
    if intro.lower().startswith('a'):
        accedi()
        break
    elif intro.lower().startswith('s'):
        registrati()
        break
    else:
        print(intro + " is not a valid value\n")
        print("Please choose between access (a) or sign in (s)\n")
    


# Legge il numero della porta dalla riga di comando
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8080
  
# classe che mantiene le funzioni di SimpleHTTPRequestHandler e implementa
# il metodo get nel caso in cui si vogliano aggiungere funzioni
class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    # def do_POST(self):
    #     content_length = int(self.headers['Content-Length'])
    #     body = self.rfile.read(content_length)
    #     self.send_response(200)
    #     self.end_headers()
    #     response = BytesIO()
    #     response.write(b'This is POST request. ')
    #     response.write(b'Received: ')
    #     response.write(body)
    #     self.wfile.write(response.getvalue())

# Nota ForkingTCPServer non funziona su Windows come os.fork ()
# La funzione non Ã¨ disponibile su quel sistema operativo. Invece dobbiamo usare il      
# ThreadingTCPServer per gestire più richieste
server = socketserver.ThreadingTCPServer(('',port), ServerHandler)


#Assicura che da tastiera usando la combinazione
#di tasti Ctrl-C termini in modo pulito tutti i thread generati
server.daemon_threads = True
#il Server acconsente al riutilizzo del socket anche se ancora non Ã¨ stato
#rilasciato quello precedente, andandolo a sovrascrivere
server.allow_reuse_address = True

#definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
  if input("\nReally quit? (y/n)>").lower().startswith('y'):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
        if( server ):
          server.server_close()
    finally:
          sys.exit(0)
  else:
    print("Ok, let's go")
    
      

#interrompe lâ€™esecuzione se da tastiera arriva la sequenza (CTRL + C)
signal.signal(signal.SIGINT, signal_handler)

# entra nel loop infinito
try:
  while True:
        server.serve_forever()
except KeyboardInterrupt:
  pass

server.server_close()
