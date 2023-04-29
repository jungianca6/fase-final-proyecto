import tkinter as tk
import random
import time
from PIL import ImageTk,Image
import pygame


balas=[]
balasaliens=[]
lastshottime = 0.0
lastenemyshottime= 0.0
enemigoslista=[]

hitbox=0

puntos=0

tiempo=0

enemigosmuertos = 0

contador_enemigos = 0



def destruye_ventana(vD,vG):     #entrar y salir               
        """  
        Funcionalidad: Destruye la ventana actual
        Entradas:N/A
        Salidas:N/A
        """
        vG.deiconify()
        vD.destroy()
        
def ventana():
    ventanamain = tk.Tk()
    ventanamain.title("Space Shooters")
    ventanamain.minsize(600, 300)
    ventanamain.maxsize(600, 300)

    ventanamain.configure(background="light blue")
    ancho = 600
    largo = 400

    def about():
        aboutgame= tk.Toplevel() #se genera la pantalla que se muestra para el about
        aboutgame.title("About Game")
        aboutgame.minsize(600, 150)
        aboutgame.maxsize(600,150)
        aboutgame.configure(background="light blue")
        
    
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

        canvas= tk.Canvas(game, width= 900, height= 500,bg="black")
        canvas.pack()

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

        def end():
                global enemigosmuertos
                if enemigosmuertos>=10:
                        gameover= tk.Toplevel() #se genera la pantalla que se muestra para el about
                        gameover.title("Space Shooters")
                        gameover.minsize(1000, 600)
                        gameover.maxsize(1000,600)
                        gameover.configure(background="#1C1A59")

                        game.withdraw()
        
                        gameover.protocol('WM_DELETE_WINDOW', lambda:destruye_ventana(gameover,ventanamain))
        
                        volver = tk.Button(gameover, text="Volver", width=10, command=lambda:destruye_ventana(gameover,ventanamain))
                        volver.place(x=350, y=70)
        def restart():
                game.destroy()
                game = tk()
                game.mainloop()              

        def movelaser(id, laser, laserloop):
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
                except:
                        return

        def colisionbala(laser,i):
                global enemigoslista, puntos, enemigosmuertos
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
                        enemigosmuertos+=1
                        print(enemigosmuertos)
                        end()

                        pygame.mixer.init()
                        explosionsound=pygame.mixer.Sound('explosion.wav')
                        explosionsound.play()
                        explosionsound.set_volume(0.1)
                                                
                elif xa2<-100:
                      canvas.delete(enemigoslista[i])   #elimina el alien al salir de la pantalla
                      enemigoslista.pop(i)
                else:
                        colisionbala(laser,i+1)
        
        def remove_bala(id):
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

        def movelaseralien(id, laseralien, laseralienloop):
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
        
        def colisionbalanave(laseralien):
                global hitbox, enemigosmuertos
                bordelaseralien = canvas.bbox(laseralien)
                x1, y1, x2, y2 = bordelaseralien
                bordenave=canvas.bbox(ship)
                xb1,yb1,xb2,yb2=bordenave
                if x2 > xb1 and y2 > yb1 and x1 < xb2 and y1 < yb2:
                        canvas.delete(laseralien)
                        remove_bala_alien(id)
                        hitbox+=1
                        enemigosmuertos+=1
                        print(enemigosmuertos)
                        
                
        def remove_bala_alien(id):
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

        def movealiens(canvas,alien):
                canvas.move(alien, -1, 0)
                game.after(10,movealiens,canvas,alien)
                alienshoot(canvas,alien)
       
                
        def aliens(canvas,newalien):
                global enemigoslista,contador_enemigos
                if contador_enemigos<9:
                        x=random.randint(700,750)
                        y=random.randint(100,400)
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
        volver = tk.Button(game, text="Volver", width=10, command=lambda:destruye_ventana(game,ventanamain))
        volver.place(x=900, y=570)

        
        ventanamain.mainloop()
        

    def highscore():
        hiscore= tk.Toplevel() #se genera la pantalla que se muestra para el about
        hiscore.title("High Scores")
        hiscore.minsize(600, 150)
        hiscore.maxsize(600,150)
        hiscore.configure(background="light blue")

        ventanamain.withdraw()
        
        hiscore.protocol('WM_DELETE_WINDOW', lambda:destruye_ventana(hiscore,ventanamain))
        
        volver = tk.Button(hiscore, text="Volver", width=10, command=lambda:destruye_ventana(hiscore,ventanamain))
        volver.place(x=350, y=70)



    aboutthegame = tk.Button(ventanamain,text= "About the game" ,padx=10,pady=10,command=about)
    aboutthegame.place(x=210,y=20)
#---------------------------------------------------------------------------------------------------------------------
    gamebegin = tk.Button(ventanamain,text= "Start game",padx=10,pady=10,command=gamestart)
    gamebegin.place(x=210,y=80)
#---------------------------------------------------------------------------------------------------------------------
    HIscore = tk.Button(ventanamain,text= "High Score" ,padx=10,pady=10,command=highscore)
    HIscore.place(x=210,y=140)
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
