import tkinter as tk
import random
import time
from PIL import ImageTk,Image
import pygame
import archivos



balas=[]
balasaliens=[]
lastshottime = 0.0
lastenemyshottime= 0.0
enemigoslista=[]
contador_enemigos=0

puntos=0

vidas = 3
enemigosmuertos = 0

tiempo=60
 
def reiniciar():
        global balas, balasaliens, enemigoslista, enemigosmuertos, contador_enemigos,tiempo,puntos,vidas
        balas=[]
        balasaliens=[]
        enemigoslista=[]
        enemigosmuertos = 0
        contador_enemigos = 0
        tiempo = 60
        puntos=0
        vidas = 3

        
def destruye_ventana(vD,vG):     #entrar y salir               
        """  
        Funcionalidad: Destruye la ventana actual
        Entradas:N/A
        Salidas:N/A
        """
        vD.destroy()
        vG.deiconify()
        reiniciar()
        
        
def ventana():
    ventanamain = tk.Tk()
    ventanamain.title("Space Shooters")
    ventanamain.minsize(800, 600)
    ventanamain.maxsize(800, 600)

    ventanamain.configure(background="light blue")
    ancho = 800
    largo = 400

    pygame.mixer.init()
    pygame.mixer.music.load("main menu.wav")
    pygame.mixer.music.play(-1)

    canvasmain= tk.Canvas(ventanamain, width= 800, height= 600,bg="#1C1A59")
    canvasmain.place(relx=0.5, rely=0.5, anchor=tk.CENTER)



    def about():
        aboutgame= tk.Toplevel() #se genera la pantalla que se muestra para el about
        aboutgame.title("About Game")
        aboutgame.minsize(800, 600)
        aboutgame.maxsize(800,600)
        aboutgame.configure(background="#1C1A59")


    
        ventanamain.withdraw()
        
        aboutgame.protocol('WM_DELETE_WINDOW', lambda:destruye_ventana(aboutgame,ventanamain))
        
        volver = tk.Button(aboutgame, text="Volver", width=10, command=lambda:destruye_ventana(aboutgame,ventanamain))
        volver.place(x=350, y=70)

        
                

    def gamestart():
        game= tk.Toplevel() #se genera la pantalla que se muestra para el about
        game.title("Space Shooters")
        game.minsize(1000, 600)
        game.maxsize(1000,600)
        game.configure(background="#1C1A59")

        #Marcadores del juego

        canvas= tk.Canvas(game, width= 900, height= 500,bg="black")
        canvas.pack()

        score=tk.Label(game, text='Puntuacion:'+ str(puntos), font=('Fixedsys', 16), bg='powder blue', fg='black')
        score.place(x=100, y =550)
 
        lives=tk.Label(game, text='Vidas:'+ str(vidas), font=('Fixedsys', 16), bg='powder blue', fg='black')
        lives.place (x=400, y=550)

        timeout=tk.Label(game, text='Tiempo:'+ str(tiempo), font=('Fixedsys', 16), bg='powder blue', fg='black')
        timeout.place (x=600, y=550)

        
        #Imagen de fondo
        bgspace=(Image.open('space background.gif'))
        resizedbgspace= bgspace.resize((920,518), Image.LANCZOS)
        newspace= ImageTk.PhotoImage(resizedbgspace)

        bgspace=canvas.create_image(450,250,anchor=tk.CENTER, image=newspace)
        
        #Imagen de la nave
        ship= (Image.open("spaceship.gif"))

        resizedship= ship.resize((82,75), Image.LANCZOS)
        newship= ImageTk.PhotoImage(resizedship)

        ship=canvas.create_image(10,10, anchor=tk.NW, image=newship)

        #Imagen de la bala 
        bullet= (Image.open("bullet.gif"))

        resizedbullet= bullet.resize((100,52), Image.LANCZOS)
        newbullet= ImageTk.PhotoImage(resizedbullet)

        #Imagen de alien
        alien= (Image.open("alien.gif"))

        resizedalien= alien.resize((85,57), Image.LANCZOS)
        newalien= ImageTk.PhotoImage(resizedalien)

        #Funcion de disparo de la bala de la nave


        
        def end():  #termina el juego
                if vidas<=0:
                        gameover= tk.Toplevel()
                        gameover.title("Game Over")
                        gameover.minsize(1000, 600)
                        gameover.maxsize(1000,600)
                        gameover.configure(background="#1C1A59")

                        canvasGO= tk.Canvas(gameover, width= 1000, height= 600,bg="black")
                        canvasGO.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

                        gameoverpic= (Image.open("game over.gif"))
                        resizedGO= gameoverpic.resize((500,247), Image.LANCZOS)
                        newGO= ImageTk.PhotoImage(resizedGO)
                        gameoverpic=canvasGO.create_image(450,250, anchor=tk.CENTER, image=newGO)


                        game.destroy()
        
                        gameover.protocol('WM_DELETE_WINDOW', lambda:destruye_ventana(gameover,ventanamain))

                        gameoverscore=tk.Label(canvasGO, text='Tu puntuacion fue:'+str(puntos),font=('Fixedsys', 32), bg='#3A4BA1', fg='#B7B1F3')
                        gameoverscore.place (x=300, y=450)
                        
                        volver = tk.Button(canvasGO, text="Volver",font=   'Fixedsys', width=10, command=lambda:destruye_ventana(gameover,ventanamain))
                        volver.place(x=800, y=550)

                        gameover.mainloop()
                        

        def levelpassed():   #el nivel se completo
                if tiempo==0:
                        gamepassed= tk.Toplevel() 
                        gamepassed.title("Level Passed")
                        gamepassed.minsize(1000, 600)
                        gamepassed.maxsize(1000,600)
                        gamepassed.configure(background="black")

                        canvasGG= tk.Canvas(gamepassed, width= 1000, height= 600,bg="#1C1A59")
                        canvasGG.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

                        gamepasspic= (Image.open("level passed.gif"))
                        resizedGG= gamepasspic.resize((550,161), Image.LANCZOS)
                        newGG= ImageTk.PhotoImage(resizedGG)
                        gamepasspic=canvasGG.create_image(450,250, anchor=tk.CENTER, image=newGG)

                        game.destroy()
        
                        gamepassed.protocol('WM_DELETE_WINDOW', lambda:destruye_ventana(gameover,ventanamain))

                        gamepassedscore=tk.Label(canvasGG, text='Tu puntuacion fue:'+str(puntos),font=('Fixedsys', 32), bg='#3A4BA1', fg='#B7B1F3')
                        gamepassedscore.place (x=300, y=450)
        
                        volver = tk.Button(canvasGG, text="Volver", width=10, command=lambda:destruye_ventana(gamepassed,ventanamain))
                        volver.place(x=900, y=550)

                        gamepassed.mainloop()
                


           
        def tiempojuego():
                global tiempo,puntos
                tiempo -=1
                puntos +=10
                game.after(1000,tiempojuego)
                score.config(text="Puntuacion:" + str(puntos))
                timeout.config(text="Tiempo:" +str(tiempo))
                if tiempo == 0:
                        levelpassed()
                  

        def movelaser(id, laser, laserloop):  #mueve el laser/bala
                global balas, enemigoslista
                try:
                        bordelaser = canvas.bbox(laser)
                        x1, y1, x2, y2 = bordelaser
                        if x1 > 905:
                                canvas.delete(laser)
                                if laserloop:
                                        game.after_cancel(laserloop)
                                remove_bala(id)      
                        else:
                                canvas.move(laser, 10, 0)
                                laserloop = game.after(10, movelaser, id, laser, laserloop)
                                if len(enemigoslista)>0:
                                        colisionbala(laser,0)
                                        colosionbalabala(laser,laseralien)
                                        colisionenemigo(laser,0)
                except:
                        return

        def colisionbala(laser,i):   #elimina enemigos y las balas al colisionar
                global enemigoslista, puntos
                bordelaser = canvas.bbox(laser)
                x1, y1, x2, y2 = bordelaser
                bordealien = canvas.bbox(enemigoslista[i])
                xa1,ya1,xa2,ya2= bordealien
                if x2 > xa1 and y2 > ya1 and x1 < xa2 and y1 < ya2:
                        canvas.delete(laser)
                        canvas.delete(enemigoslista[i])
                        remove_bala(id)
                        enemigoslista.pop(i)
                        puntos+=100
                        score.config(text="Puntuacion:" + str(puntos))

                        
                        pygame.mixer.init()
                        explosionsound=pygame.mixer.Sound('explosion.wav')
                        explosionsound.play()
                        explosionsound.set_volume(0.1)
                                                
                elif xa2<-100:
                        canvas.delete(enemigoslista[i])   #elimina el alien al salir de la pantalla
                        enemigoslista.pop(i)
                        puntos-=50
                        score.config(text="Puntuacion:" + str(puntos))
                else:
                        colisionbala(laser,i+1)

        def colisionbalabala(laser,laseralien): #elimina balas cuando chocan
                bordelaser = canvas.bbox(laser)
                x1, y1, x2, y2 = bordelaser
                bordelaseralien = canvas.bbox(laseralien)
                xa1, ya1, xa2, ya2 = bordelaseralien
                if x1 < xa2 and x2 > xa1 and y1 < ya2 and y2 > ya1:
                        canvas.delete(laser)
                        remove_bala(id)
                        canvas.delete(laseralien)
                        remove_bala_alien(id)

        def colisionenemigo(laser,i):  #colision de nave y enemigo
                global enemigoslista, vidas
                bordenave = canvas.bbox(ship)
                x1, y1, x2, y2 = bordenave
                bordealien = canvas.bbox(enemigoslista[i])
                xa1,ya1,xa2,ya2= bordealien
                if x2 > xa1:
                        canvas.delete(enemigoslista[i])
                        enemigoslista.pop(i)
                        vidas-=1
                        lives.config(text="Vidas:" + str(vidas))
                        end()
                else:
                        colisionenemigo(laser,i+1)
                

        def puntaje():
                global puntos
                colisionbala(laser,0)
                print(puntos)
        
        def remove_bala(id):  #quita la bala de la lista de balas
                global balas
                if balas[0]['id'] == id:
                        canvas.delete(balas[0]['laser'])
                        game.after_cancel(balas[0]['laserloop'])
                        balas.pop(0)
                elif len(balas) > 1:
                        balas = balas[1:]
                        remove_bala(id)

        def shoot(event): #crea bala
                global balas, lastshottime

                current_time= time.monotonic()
                if current_time - lastshottime>=0.5:  #cooldown
                        lastshottime = current_time
                        try:
                                game.after_cancel(balas[0]['laserloop'])
                                bordenave = canvas.bbox(ship)
                                x1, y1, x2, y2 = bordenave
                                #posicion de bala
                                xbala = x2 + 15
                                ybala = (y1 + y2) / 2
                                laser = canvas.create_image(xbala, ybala, image=newbullet)
                                id = canvas.create_text(xbala, ybala, text='', fill='white', font=('arial', 1))
                                laserloop = game.after(10, movelaser, id, laser, None)
                                balas.append({'id': id, 'laser': laser, 'laserloop': laserloop})

                               

                                movelaser(id, laser, laserloop)
                                pygame.mixer.init()
                                blastsound=pygame.mixer.Sound('blast shot.wav')
                                blastsound.play()
                                blastsound.set_volume(0.3)
                        
                        except IndexError:
                                bordenave = canvas.bbox(ship)
                                x1, y1, x2, y2 = bordenave
                                xbala = x2 + 20
                                ybala = (y1 + y2) / 2
                                laser = canvas.create_image(xbala, ybala, image=newbullet)
                                id = canvas.create_text(xbala, ybala, text='', fill='white', font=('arial', 1))
                                laserloop = game.after(10, movelaser, id, laser, None)
                                balas.append({'id': id, 'laser': laser, 'laserloop': laserloop})

                                movelaser(id, laser, laserloop)
                                pygame.mixer.init()
                                blastsound=pygame.mixer.Sound('blast shot.wav')
                                blastsound.play()
                                blastsound.set_volume(0.3)
                                

        #Creacion del alien

        def movelaseralien(id, laseralien, laseralienloop):  #mueve la bala del alien
                global balasaliens, enemigoslista
                try:
                        bordelaseralien = canvas.bbox(laseralien)
                        x1, y1, x2, y2 = bordelaseralien
                        if x2 < -10:
                                canvas.delete(laseralien)
                                if laseralienloop:
                                        game.after_cancel(laseralienloop)
                                remove_bala_alien(id)      
                        else:
                                canvas.move(laseralien, -10, 0)
                                laserloopalien = game.after(10, movelaseralien, id, laseralien, laseralienloop)
                                if len(enemigoslista)>0:
                                        colisionbalanave(laseralien)
                except:
                        return
        
        def colisionbalanave(laseralien):  #colision de la bala del alien con el jugador
                global vidas
                bordelaseralien = canvas.bbox(laseralien)
                x1, y1, x2, y2 = bordelaseralien
                bordenave=canvas.bbox(ship)
                xb1,yb1,xb2,yb2=bordenave
                if x2 > xb1 and y2 > yb1 and x1 < xb2 and y1 < yb2:
                        canvas.delete(laseralien)
                        remove_bala_alien(id)
                        vidas-=1
                        lives.config(text="Vidas:" + str(vidas))
                        end()

                        
                
        def remove_bala_alien(id):  #elimina la bala de la lista de balas de enemigos
                global balasaliens
                if balasaliens[0]['id'] == id:
                        canvas.delete(balasaliens[0]['laseralien'])
                        game.after_cancel(balasaliens[0]['laseralienloop'])
                        balasaliens.pop(0)
                elif len(balasaliens) > 1:
                        balasaliens = balasaliens[1:]
                        remove_bala_alien(id)

        
        

        def alienshoot(canvas,alien): #balas de los aliens
                global balasaliens, lastenemyshottime,enemigoslista

                current_time= time.monotonic()
                if current_time - lastenemyshottime>=0.5:  #cooldown
                        lastenemyshottime = current_time
                        try:
                                game.after_cancel(balasaliens[0]['laseralienloop'])
                                bordealien = canvas.bbox(alien)
                                if bordealien is not None:
                                        xa1, ya1, xa2, ya2 = bordealien
                                #posicion de bala
                                        xabala = xa1 - 20
                                        yabala = (ya1 + ya2) / 2
                                        laseralien = canvas.create_image(xabala, yabala, image=newbullet)
                                        id = canvas.create_text(xabala, yabala, text='', fill='white', font=('arial', 1))
                                        laseralienloop = game.after(10, movelaseralien, id, laseralien, None)
                                        balasaliens.append({'id': id, 'laseralien': laseralien, 'laseralienloop': laseralienloop})
                                
                                        pygame.mixer.init()
                                        blastsound=pygame.mixer.Sound('blast shot.wav')
                                        blastsound.play()
                                        blastsound.set_volume(0.1)
                        
                        except IndexError:
                                bordealien = canvas.bbox(alien)
                                if bordealien is not None:
                                        xa1, ya1, xa2, ya2 = bordealien
                                        xabala = xa1 - 20
                                        yabala = (ya1 + ya2) / 2
                                        laseralien = canvas.create_image(xabala, yabala, image=newbullet)
                                        id = canvas.create_text(xabala, yabala, text='', fill='white', font=('arial', 1))
                                        laseralienloop = game.after(10, movelaseralien, id, laseralien, None)
                                        balasaliens.append({'id': id, 'laseralien': laseralien, 'laseralienloop': laseralienloop})
                                
                                        pygame.mixer.init()
                                        blastsound=pygame.mixer.Sound('blast shot.wav')
                                        blastsound.play()
                                        blastsound.set_volume(0.1)


        def movealiens(canvas,alien):  #mueve el alien
                canvas.move(alien, -1, 0)
                game.after(10,movealiens,canvas,alien)
                alienshoot(canvas,alien)

        
        def aliens(canvas,newalien):
                global enemigoslista,contador_enemigos
                if contador_enemigos<9:
                        x=random.randint(700,750)
                        y=random.randint(50,450)
                        alien=canvas.create_image(x,y, image=newalien)
                        movealiens(canvas,alien)
                        
                        enemigoslista.append(alien)
                        contador_enemigos+=1
                        game.after(1000,aliens,canvas,newalien)
                        
                else:
                        if not enemigoslista: # si no hay enemigos, reiniciar contador
                                contador_enemigos = 0
                        game.after(1000,aliens,canvas,newalien)
        aliens(canvas,newalien)
        tiempojuego()
        
        
       
        #Funciones de movimiento 

        #Limite de movimiento de la nave
        def bordepantalla():
                borde=canvas.bbox(ship)
                x1,y1,x2,y2=borde
                if y1<10 and y2<115:
                        canvas.move(ship,0,10)  #borde arriba
                elif y1>420:
                        canvas.move(ship,0,-10) #borde abajo
                elif x1<10:
                        canvas.move(ship,10,0)  #borde izquierda
                elif x2>905:
                        canvas.move(ship,-10,0) #borde derecha
        

        #Movimiento de la nave
        def up(event):  #arriba
                global uploop, downloop
                try:
                        game.after_cancel(uploop)
                        canvas.move(ship,0,-10)
                        uploop=game.after(10,lambda: up(event))
                        bordepantalla()
                except NameError:
                        canvas.move(ship,0,-10)
                        uploop=game.after(10,lambda: up(event))
                        bordepantalla()

        def stopup(event):
                global uploop
                game.after_cancel(uploop)
         
        def down(event):        #abajo
                global uploop, downloop
                try:
                        game.after_cancel(downloop)
                        canvas.move(ship,0,10)
                        downloop=game.after(10,lambda: down(event))
                        bordepantalla()
                except NameError:
                        canvas.move(ship,0,10)
                        downloop=game.after(10,lambda: down(event))
                        bordepantalla()

        def stopdown(event):
                global downloop
                game.after_cancel(downloop)
                
        def left(event):        #izquierda
                global rightloop, leftloop
                try:
                        game.after_cancel(leftloop)
                        canvas.move(ship,-10,0)
                        leftloop=game.after(10,lambda: left(event))
                        bordepantalla()
                except NameError:
                        canvas.move(ship,-10,0)
                        leftloop=game.after(10,lambda: left(event))
                        bordepantalla()

        def stopleft(event):
                global leftloop
                game.after_cancel(leftloop)
                        
        def right(event):       #derecha
                global rightloop, leftloop
                try:
                        game.after_cancel(rightloop)
                        canvas.move(ship,10,0)
                        rightloop=game.after(10,lambda: right(event))
                        bordepantalla()
                except NameError:
                        canvas.move(ship,10,0)
                        rightloop=game.after(10,lambda: right(event))
                        bordepantalla()

        def stopright(event):
                global rightloop
                game.after_cancel(rightloop)
                
        
        
        
      
        #Funciones de Tecla
                
        game.bind("<Up>",up)
        game.bind("<Down>",down)
        game.bind_all("<Left>",left)
        game.bind_all("<Right>",right)
        game.bind_all("<space>",shoot)

        game.bind_all("<KeyRelease - Left>",stopleft)
        game.bind_all("<KeyRelease - Right>",stopright)
        game.bind_all("<KeyRelease - Up>",stopup)
        game.bind_all("<KeyRelease - Down>",stopdown)

   
        ventanamain.withdraw()
        
        game.protocol('WM_DELETE_WINDOW', lambda:destruye_ventana(game,ventanamain))

        #Boton de Regreso
        volver = tk.Button(game, text="Volver",font="Fixedsys", width=10, command=lambda:(destruye_ventana(game,ventanamain)))
        volver.place(x=900, y=570)

       

        game.mainloop()
        

    def highscore():
        hiscore= tk.Toplevel() #se genera la pantalla que se muestra para el about
        hiscore.title("High Scores")
        hiscore.minsize(800, 400)
        hiscore.maxsize(800,400)
        hiscore.configure(background="#1C1A59")

        ventanamain.withdraw()
        
        hiscore.protocol('WM_DELETE_WINDOW', lambda:destruye_ventana(hiscore,ventanamain))

        
        placeLabels(hiscore,archivos.leer_archivo('archivo.txt').split("\n"),70)
        volver = tk.Button(hiscore, text="Volver", width=10, command=lambda:destruye_ventana(hiscore,ventanamain))
        volver.place(x=700, y=350)
            

    def reEscribirArchivo(archivo,nuevoValor):
            with open(archivo, 'r+') as f:
                    reEscribirArchivoRecursivamente(f,nuevoValor,"")

    def reEscribirArchivoRecursivamente(archivo, nuevoValor, texto):
            lineaActual = archivo.readline().strip()
            if lineaActual == '':
                    archivo.truncate()
                    archivo.seek(0)
                    archivo.write(texto+"\n"+nuevoValor)
                    return 
            elif int(lineaActual.split(" ")[1]) < int(nuevoValor.split(" ")[1]):
                    pos_actual = archivo.tell()
                    archivo.seek(pos_actual)
                    if(texto==""):
                            reEscribirArchivoRecursivamente(archivo, lineaActual, nuevoValor)
                    else:
                            reEscribirArchivoRecursivamente(archivo, lineaActual, texto+"\n"+nuevoValor)
            else:
                    pos_actual = archivo.tell()
                    archivo.seek(pos_actual)
                    if texto !='':
                            reEscribirArchivoRecursivamente(archivo,nuevoValor,texto+"\n"+lineaActual)
                    else:
                            reEscribirArchivoRecursivamente(archivo,nuevoValor,lineaActual)
    def placeLabels(hiscore,texto,y_Value):
        if texto!="":
            tk.Label(hiscore, text=texto[0], font=('Arial', 18), bg='white', fg='black').place(x=200, y = y_Value)
            if len(texto)>1:
                placeLabels(hiscore,texto[1:],y_Value+50)
            else:
                placeLabels(hiscore,"",y_Value+50)

#--------------------------------------------------------------------------------------------------------------------
    titlename=tk.Label(ventanamain, text="SPACE SHOOTERS",font=('Fixedsys', 32),bg="#b7b1f3")
    titlename.place (x=210, y=50)
#--------------------------------------------------------------------------------------------------------------------    
    aboutthegame = tk.Button(ventanamain,text= "About the game",font=('Fixedsys', 28),bg="#b7b1f3",padx=10,pady=10,command=about)
    aboutthegame.place(x=210,y=150)
#---------------------------------------------------------------------------------------------------------------------
    gamebegin = tk.Button(ventanamain,text= "Start game",font=('Fixedsys', 28),bg="#b7b1f3",padx=10,pady=10,command=gamestart)
    gamebegin.place(x=210,y=300)
#---------------------------------------------------------------------------------------------------------------------
    HIscore = tk.Button(ventanamain,text= "High Score",font=('Fixedsys', 28),bg="#b7b1f3",padx=10,pady=10,command=highscore)
    HIscore.place(x=210,y=450)
    ventanamain.mainloop()
ventana()


#Cosas fuera del juego que tal vez vaya a usar
"""def game_loop():
    # Actualizar estado del juego
    update_game_state()

    # Redibujar pantalla
    redraw_screen()

    # Verificar si el juego ha terminado
    if not game_over():
        # Esperar un tiempo antes de llamar a la función de nuevo
        root.after(10, game_loop)"""
"""def play():
        pygame.mixer.init()
        pygame.mixer.music.load("On Melancholy Hill.wav")
        pygame.mixer.music.play(0)

    canvasC1 = tk.Canvas(ventanamain, width=300, height=200, borderwidth=0, highlightthickness=0, bg="black")
    canvasC1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    img=ImageTk.PhotoImage(Image.open("gorillaz.gif"))
    canvasC1.pack()

    canvasC1.create_image(100, 50, image=img)

    play=tk.Button(ventanamain, text="Play song", width=10,command=play)
    play.place(x=350, y=250)
"""
"""def move(img, dx, dy):
                canvas.move(img, dx, dy)
                x, y, w, h = canvas.coords(img)
                if x < 0:
                        move(img, -x, 0)
                elif x + w > canvas.winfo_width():
                        move(img, canvas.winfo_width() - (x + w), 0)
                if y < 0:
                        move(img, 0, -y)
                elif y + h > canvas.winfo_height():
                        move(img, 0, canvas.winfo_height() - (y + h))"""

"""borde4=canvas.bbox(ship)
                x1,y1,x2,y2=borde4
                print(borde4)"""

"""#.after
#eventos teclas tkinter
#moveq
#focus para detectar el teclado


def todo()
        movimiento
        ventanauqeesta.after(10,todo)

todo()"""
