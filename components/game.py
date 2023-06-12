from random import *
from tkinter import *
import sqlite3
from PIL import ImageTk, Image
import time
import _thread
import pygame
from sys import exit


class gifplay:
    def __init__(self,label,giffile,delay):
        self.frame=[]
        i=0
        while 1:
            try:
                image=PhotoImage(file = giffile, format="gif -index "+str(i))
                self.frame.append(image)
                i=i+1
            except:
                break
        self.totalFrames=i-1
        self.delay=delay
        self.labelspace=label
        self.labelspace.image=self.frame[0]

    def play(self):
        _thread.start_new_thread(self.infinite,())

    def infinite(self):
        i=0
        while 1:
            try:
                self.labelspace.configure(image=self.frame[i])
                i=(i+1)%self.totalFrames
                time.sleep(self.delay)
            except:
                break
        

class DeathRoll(Frame):
    def __init__(self, window):
        Frame.__init__(self, window)
        container = window
        container.resizable(width=FALSE, height=FALSE)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1) 
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        pygame.mixer.init()
        self.tankmusic = pygame.mixer.Sound('C:/deathroll/music/tank.wav')
        self.roguemusic = pygame.mixer.Sound('C:/deathroll/music/rogue.wav')
        self.archermusic = pygame.mixer.Sound('C:/deathroll/music/archer.wav')
        self.healermusic = pygame.mixer.Sound('C:/deathroll/music/healer.wav')
        self.readymusic = pygame.mixer.Sound('C:/deathroll/music/readyus.wav')
        self.lang = 0


        pygame.mixer.music.load('C:/deathroll/music/bg.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.tank = StringVar()
        self.rogue = StringVar()
        self.archer = StringVar()
        self.healer = StringVar()

        self.players = []

        self.frames = {}

        frame = StartPage(container, self)
        self.frames[StartPage] = frame
        frame.grid(row = 0, column = 0, sticky = 'nsew')

        self.show_frame(StartPage)

    def player_screen(self, container):
        frame = PlayerCreation(container, self)
        self.frames[PlayerCreation] = frame
        frame.grid(row = 0, column = 0, sticky = 'nsew')
        self.show_frame(PlayerCreation)

    def game_screen(self, container):
        frame = MainGame(container, self)
        self.frames[MainGame] = frame
        frame.grid(row = 0, column = 0, sticky = 'nsew')
        self.show_frame(MainGame)

    def last_will_screen(self, container, player):
        frame = PostGame(container, self, player)
        self.frames[PostGame] = frame
        frame.grid(row = 0, column = 0, sticky = 'nsew')
        self.show_frame(PostGame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(Frame):
    def __init__(self, parent, controller):
        def changeLanguage(number):
            if number == 0:
                language.configure(image = phimg)
                language.image = phimg
                controller.tankmusic = pygame.mixer.Sound('C:/deathroll/music/tankph.wav')
                controller.roguemusic = pygame.mixer.Sound('C:/deathroll/music/rogueph.wav')
                controller.archermusic = pygame.mixer.Sound('C:/deathroll/music/archerph.wav')
                controller.healermusic = pygame.mixer.Sound('C:/deathroll/music/healerph.wav')
                controller.readymusic = pygame.mixer.Sound('C:/deathroll/music/readyph.wav')
                phlang = pygame.mixer.Sound('C:/deathroll/music/langph.wav')
                phlang.play()
                controller.lang = 1
            elif number == 1:
                language.configure(image = usimg)
                language.image = usimg
                controller.tankmusic = pygame.mixer.Sound('C:/deathroll/music/tank.wav')
                controller.roguemusic = pygame.mixer.Sound('C:/deathroll/music/rogue.wav')
                controller.archermusic = pygame.mixer.Sound('C:/deathroll/music/archer.wav')
                controller.healermusic = pygame.mixer.Sound('C:/deathroll/music/healer.wav')
                controller.readymusic = pygame.mixer.Sound('C:/deathroll/music/readyus.wav')
                uslang = pygame.mixer.Sound('C:/deathroll/music/langus.wav')
                uslang.play()
                controller.lang = 0

        Frame.__init__(self, parent)
        
        mainlbl = Label(self)
        mainlbl.place(x = 0, y = 0)
        gif = gifplay(mainlbl, 'C:/deathroll/pictures/main.gif', 0.005)
        gif.play()

        try:
            pygame.init()
        except:
            pass

        playimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/play.png")
        play = Button(self, bg = 'brown', image = playimg, command = lambda: controller.player_screen(parent))
        play.image = playimg
        play.place(x = 380, y = 400)
        regimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/register.png")
        register = Button(self, bg = 'brown', image = regimg, command = lambda: Bank())
        register.image = regimg
        register.place(x = 380, y = 530)
        mquitimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/mquit.png")
        mquit = Button(self, bg = 'brown', image = mquitimg, command = lambda: exit())
        mquit.image = mquitimg
        mquit.place(x = 505, y = 530)

        usimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/us.png")
        phimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/ph.png")
        language = Button(self, bg = 'brown', image = usimg, command = lambda: changeLanguage(controller.lang))
        language.image = usimg
        language.place(x = 630, y = 548)


class PlayerCreation(Frame):
    def __init__(self, parent, controller):
        def reset(words, window):
            del words
            window.destroy()
        def infoSet():
            ineligible = ''
            controller.players.clear()
            controller.players.append(str(controller.tank.get()))
            controller.players.append(str(controller.rogue.get()))
            controller.players.append(str(controller.archer.get()))
            controller.players.append(str(controller.healer.get()))

            conn = sqlite3.connect("C:/deathroll/components/players.db")
            c = conn.cursor()

            sql = "SELECT * FROM players"
            for check in controller.players:
                gate = False
                for row in c.execute(sql):
                    if check.upper() == row[0]:
                        gate = True
                if not gate:
                    ineligible = ineligible + check + '; '

            conn.close()

            if ineligible == '':
                shuffle(controller.players)
                controller.readymusic.play()
                controller.game_screen(parent)
            else:
                notif = Toplevel()
                notif.title("Error")
                notif.geometry("500x200")
                errorCode = Label(notif, text = 'One or more players do not have accounts:\n' + ineligible, pady =10, font = ("Helvetica", 13, 'bold', 'underline'), wraplength = 400)
                errorCode.pack()
                quitB = Button(notif, text = 'OK', width = 12, bg = 'brown', fg = 'white', command = lambda: reset(ineligible, notif))
                quitB.pack()
            
        Frame.__init__(self, parent)

        backimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/back.png")
        back = Button(self, image = backimg, command = lambda: controller.show_frame(StartPage))
        back.image = backimg
        back.place(x = 0, y = 0)

        logoimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/logo.png") 
        logo = Label(self, image = logoimg)
        logo.image = logoimg
        logo.pack()

        tankimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/tank.png")
        rogueimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/rogue.png")
        archerimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/archer.png")
        healerimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/healer.png")


        tanklbl = Label(self, image = tankimg)
        tanklbl.image = tankimg
        tanklbl.place(x = 50, y = 150)

        roguelbl = Label(self, image = rogueimg)
        roguelbl.image = rogueimg
        roguelbl.place(x = 50, y = 400)

        archerlbl = Label(self, image = archerimg)
        archerlbl.image = archerimg
        archerlbl.place(x = 800, y = 150)

        healerlbl = Label(self, image = healerimg)
        healerlbl.image = healerimg
        healerlbl.place(x = 800, y = 400)


        self._tankname = Label(self, text = 'The Tank', width = 20, font = ("Helvetica", 11, 'bold'))
        self._tankname.place(x = 35, y = 300)

        self._roguename = Label(self, text = 'The Rogue', width = 20, font = ("Helvetica", 11, 'bold'))
        self._roguename.place(x = 35, y = 550)

        self._archername = Label(self, text = 'The Archer', width = 20, font = ("Helvetica", 11, 'bold'))
        self._archername.place(x = 781, y = 300)

        self._healername = Label(self, text = 'The Healer', width = 20, font = ("Helvetica", 11, 'bold'))
        self._healername.place(x = 781, y = 550)

        self._p1Name = Label(self, text = 'Player 1:', width = 10, font = ("Helvetica", 11, 'bold'))
        self._p1Name.place(x = 365, y = 200)
        
        self._p2Name = Label(self, text = 'Player 2:', width = 10, font = ("Helvetica", 11, 'bold'))
        self._p2Name.place(x = 365, y = 250)

        self._p3Name = Label(self, text = 'Player 3:', width = 10, font = ("Helvetica", 11, 'bold'))
        self._p3Name.place(x = 365, y = 300)

        self._p4Name = Label(self, text = 'Player 4:', width = 10, font = ("Helvetica", 11, 'bold'))
        self._p4Name.place(x = 365, y = 350)

        self._entryTank = Entry(self, width = 25, textvar = controller.tank)
        self._entryTank.place(x = 470, y = 200)

        self._entryRogue = Entry(self, width = 25, textvar = controller.rogue)
        self._entryRogue.place(x = 470, y = 250)
        
        self._entryArcher = Entry(self, width = 25, textvar = controller.archer)
        self._entryArcher.place(x = 470, y = 300)
        
        self._entryHealer = Entry(self, width = 25, textvar = controller.healer)
        self._entryHealer.place(x = 470, y = 350)


        rockimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/letsrock.png")
        rock = Button(self, image = rockimg, command = lambda: infoSet())
        rock.image = rockimg
        rock.place(x = 380, y = 400)

class MainGame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self._mana = [1, 1, 1, 1]

        tankimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/tank.png")
        rogueimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/rogue.png")
        archerimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/archer.png")
        healerimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/healer.png")

        tanklbl = Label(self, image = tankimg)
        tanklbl.image = tankimg
        tanklbl.place(x = 100, y = 170)

        roguelbl = Label(self, image = rogueimg)
        roguelbl.image = rogueimg
        roguelbl.place(x = 100, y = 400)

        archerlbl = Label(self, image = archerimg)
        archerlbl.image = archerimg
        archerlbl.place(x = 750, y = 170)

        healerlbl = Label(self, image = healerimg)
        healerlbl.image = healerimg
        healerlbl.place(x = 750, y = 400)

        
        self._tankname = Label(self, text = 'Tank : ' + controller.players[0], width = 20, font = ("Helvetica", 11, 'bold'))
        self._tankname.place(x = 85, y = 320)

        self._roguename = Label(self, text = 'Rogue : ' + controller.players[1], width = 20, font = ("Helvetica", 11, 'bold'))
        self._roguename.place(x = 85, y = 545)

        self._archername = Label(self, text = 'Archer : ' + controller.players[2], width = 20, font = ("Helvetica", 11, 'bold'))
        self._archername.place(x = 735, y = 320)

        self._healername = Label(self, text = 'Healer : ' + controller.players[3], width = 20, font = ("Helvetica", 11, 'bold'))
        self._healername.place(x = 735, y = 545)
        
        self._turn = 0
        self._max_roll = 10000
        logoimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/logo.png") 
        logo = Label(self, image = logoimg)
        logo.image = logoimg
        logo.pack()

        self._lblTurn = Label(self, fg = 'red', font = ("Helvetica, 16"))
        self._lblTurn.pack()

        self._dice_thrown = Label(self, text = "Health: " + str(self._max_roll), font = ("Helvetica, 16"))
        self._dice_thrown.pack(anchor = CENTER)

        self.rng = Label(self, text = str(self._max_roll), font = ("Helvetica, 42"), anchor = CENTER, justify = CENTER)
        self.rng.pack(anchor = CENTER)


        self.startimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/charge.png")
        self.start = Button(self, image = self.startimg, command = lambda: self.playerTurn(parent, controller))
        self.start.image = self.startimg
        self.start.place(x = 392, y = 400)


    def playerTurn(self, parent, controller):
        def process(parent,controller):
            self.gif = ''
            del self.gif
            parent.after(1000, self.deathRoll(parent, controller))

        def skillSound(number):
            if number == 0:
                controller.tankmusic.play()
            elif number == 1:
                controller.roguemusic.play()
            elif number == 2:
                controller.archermusic.play()
            elif number == 3:
                controller.healermusic.play()
            parent.after(1000, skill(number))

        def skill(number):
            if number == 0: #tank
                self.nSkillimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/block.png") #skill frame
                self.nSkill = Label(self, image = self.nSkillimg)
                self.nSkill.image = self.nSkillimg
                self.nSkill.place(x = 392, y = 275)
                self._mana[number] = self._mana[number] - 1
                if self._turn < 3:
                    self._turn = self._turn + 1
                    self.startimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/endturn.png")
                    self.start.image = self.startimg
                    self.start.configure(image = self.startimg, command = lambda: self.playerTurn(parent, controller))
                else:
                    self._turn = 0
                    self.startimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/endturn.png")
                    self.start.image = self.startimg
                    self.start.configure(image = self.startimg, command = lambda: self.playerTurn(parent, controller))

            elif number == 1: #rogue
                self._mana[number] = self._mana[number] - 1
                number = choice([i for i in range(0,3) if i != 1])
                self._mana[number] = self._mana[number] + 1
                skill(number)

            elif number == 2: #archer
                self.nSkillimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/misdirect.png") #skill frame
                self.nSkill = Label(self, image = self.nSkillimg)
                self.nSkill.image = self.nSkillimg
                self.nSkill.place(x = 392, y = 275)
                self._mana[number] = self._mana[number] - 1

                self._turn = choice([i for i in range(0,3) if i != 2])
                self.startimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/endturn.png")
                self.start.image = self.startimg
                self.start.configure(image = self.startimg, command = lambda: self.playerTurn(parent, controller))

            elif number == 3: #healer
                self.nSkillimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/heal.png") #skill frame
                self.nSkill = Label(self, image = self.nSkillimg)
                self.nSkill.image = self.nSkillimg
                self.nSkill.place(x = 392, y = 275)
                self._max_roll = self._max_roll + 2000
                self._dice = randint(1, self._max_roll)
                self._max_roll = self._dice
                self._mana[number] = self._mana[number] - 1

                if self._turn < 3:
                    self._turn = self._turn + 1
                    self.startimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/endturn.png")
                    self.start.image = self.startimg
                    self.start.configure(image = self.startimg, command = lambda: self.playerTurn(parent, controller))
                else:
                    self._turn = 0
                    self.startimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/endturn.png")
                    self.start.image = self.startimg
                    self.start.configure(image = self.startimg, command = lambda: self.playerTurn(parent, controller))


        self._dice_thrown.configure(text = "Health: " + str(self._max_roll))
        
        self._lblTurn.configure(text = controller.players[self._turn] + "'s Turn")
        self.start.image = self.startimg

        if self._mana[self._turn] == 0:
            self.skillimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/used.png")
            self.skill = Label(self, image = self.skillimg)
            self.skill.image = self.skillimg
            self.skill.place(x = 392, y = 275)
        else:
            self.skillimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/skill.png")
            self.skill = Button(self, image = self.skillimg, command = lambda: skillSound(self._turn))
            self.skill.image = self.skillimg
            self.skill.place(x = 392, y = 275)

        self.gif = gifplay(self.rng,'C:/deathroll/pictures/rng.gif', 0.05)
        self.gif.play()

        self.startimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/roll.png")
        self.start.image = self.startimg
        self.start.configure(image = self.startimg, command = lambda: process(parent, controller))
    
    def deathRoll(self, parent, controller):
        
        self._dice = randint(1, self._max_roll)
        self.rng.destroy()
        self.rng = Label(self, text = str(self._dice), font = ("Helvetica, 42"), anchor = CENTER, justify = CENTER)
        self.rng.pack(anchor = CENTER)
        self._max_roll = self._dice

        self.skillimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/used.png")
        self.skill = Label(self, image = self.skillimg)
        self.skill.image = self.skillimg
        self.skill.place(x = 392, y = 275)

        if self._max_roll == 1:
            self._lblTurn.configure(text = controller.players[self._turn] + " is Dead!")
            self.startimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/endgame.png")
            self.start.image = self.startimg
            self.start.configure(image = self.startimg, command = lambda: controller.last_will_screen(parent, self._turn))
        else:
            if self._turn < 3:
                self._turn = self._turn + 1
                self.startimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/endturn.png")
                self.start.image = self.startimg
                self.start.configure(image = self.startimg, command = lambda: self.playerTurn(parent, controller))
            else:
                self._turn = 0
                self.startimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/endturn.png")
                self.start.image = self.startimg
                self.start.configure(image = self.startimg, command = lambda: self.playerTurn(parent, controller))

class PostGame(Frame):
    def __init__(self, parent, controller, player):
        Frame.__init__(self, parent)

        mainimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/end.png") 
        mainlbl = Label(self, image = mainimg)
        mainlbl.image = mainimg
        mainlbl.place(x = 0, y = 0)

        dielbl = Label(self, bg = 'black')
        dielbl.place(x = 425, y = 250)

        if player == 0:
            dieimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/tank.png")
            dielbl.image = dieimg
            dielbl.configure(image = dieimg)
        elif player == 1:
            dieimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/rogue.png")
            dielbl.image = dieimg
            dielbl.configure(image = dieimg)
        elif player == 2:
            dieimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/archer.png")
            dielbl.image = dieimg
            dielbl.configure(image = dieimg)
        elif player == 3:
            dieimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/healer.png")
            dielbl.image = dieimg
            dielbl.configure(image = dieimg)

        conn = sqlite3.connect("C:/deathroll/components/players.db")
        c = conn.cursor()

        money = 0
        sql = "SELECT MONEY FROM players where NAME = ?"
        for row in c.execute(sql, [controller.players[player].upper()]):
            money = row[0]

        c.execute("DELETE FROM players where NAME = ?", [controller.players[player].upper()])
        conn.commit()

        money = int(money/3)

        controller.players.remove(controller.players[player])

        sql = "UPDATE players SET MONEY = MONEY + " + str(money) + " where NAME = ?"
        for names in controller.players:
            c.execute(sql, [names.upper()])
            conn.commit()

        conn.close()

        award = Label(self, text = 'Surviving players are awarded ' + str(money) + ' points.', width = 80, font = ("Helvetica", 16, 'bold'), fg = 'red', bg = 'black')
        award.place(x = 0, y = 450)

        quitimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/quit.png")
        quitButton = Button(self, image = quitimg, bg = 'black', command = lambda: exit())
        quitButton.image = quitimg
        quitButton.place(x = 385, y = 550)

class Bank(Tk):
    def __init__(self):
        
        def infoSet():
            self.pName = self.name.get()
            self.pMoney = self.money.get()
            conn = sqlite3.connect("C:/deathroll/components/players.db")
            c = conn.cursor()
            gate = False

            sql = "SELECT * FROM players"
            for row in c.execute(sql):
                if row[0] == str(self.pName).upper():
                    gate = True
            if gate:
                notif = Toplevel()
                notif.title("Error")
                notif.geometry("500x200")
                errorCode = Label(notif, text = 'User already exists.', pady =10, font = ("Helvetica", 13, 'bold', 'underline'), wraplength = 400)
                errorCode.pack()
                quitB = Button(notif, text = 'OK', width = 12, bg = 'brown', fg = 'white', command = lambda: notif.destroy())
                quitB.pack()
            else:
                c.execute("INSERT INTO players (NAME, MONEY) VALUES (?, ?)", (str(self.pName).upper(), self.pMoney))
                conn.commit()
                conn.close()
                notif = Toplevel()
                notif.title("Success")
                notif.geometry("500x200")
                errorCode = Label(notif, text = 'Registration Successful.', pady =10, font = ("Helvetica", 13, 'bold', 'underline'), wraplength = 400)
                errorCode.pack()
                quitB = Button(notif, text = 'OK', width = 12, bg = 'brown', fg = 'white', command = lambda: [notif.destroy(), reg.destroy()])
                quitB.pack()

                
        self.name = StringVar()
        self.money = StringVar()

        reg = Toplevel()
        reg.title("Deathbank")
        reg.geometry("500x600")
        reg.resizable(width=FALSE, height=FALSE)
        reg.columnconfigure(0, weight=1)
        reg.rowconfigure(0, weight=1) 
        reg.grid_rowconfigure(0, weight = 1)
        reg.grid_columnconfigure(0, weight = 1)


        logoimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/logo.png") 
        logo = Label(reg, image = logoimg)
        logo.image = logoimg
        logo.pack()

        formName = Label(reg, text = 'Name : ', width = 20, font = ("Helvetica", 11, 'bold'))
        formName.place(x = 50, y = 150)

        formMoney = Label(reg, text = 'Money : ', width = 20, font = ("Helvetica", 11, 'bold'))
        formMoney.place(x = 50, y = 190)

        entryName = Entry(reg, width = 30, textvar = self.name)
        entryName.place(x = 200, y = 150)

        entryMoney = Entry(reg, width = 30, textvar = self.money)
        entryMoney.place(x = 200, y = 190)

        loginimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/bet.png")
        login = Button(reg, image = loginimg, command = lambda: infoSet())
        login.image = loginimg
        login.place(x = 130, y = 250)

        bquitimg = ImageTk.PhotoImage(file = "C:/deathroll/pictures/bquit.png")
        rquit = Button(reg, image = bquitimg, command = lambda: reg.destroy())
        rquit.image = bquitimg
        rquit.place(x = 130, y = 400)
