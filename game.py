# -*- coding: utf-8 -*-

# imports 
from words import words
import pygame, sys, os
import random
from random import shuffle
from tkinter import *
from tkinter import filedialog, messagebox

# gs - grid size -> (3,3)
# ts - tile size -> 200
# ms - margin size -> 5 
# mainwindo -> lamding window
# root -> child windows

############ Main Window ##################
global mainwindow
mainwindow = Tk()
mainwindow.title("Python Games")
mainwindow.configure(bg='black')
mainwindow.geometry("600x400+400+100") 

############ Main Window ##################

class SlidePuzzle:
    def __init__(self, gs, ts, ms):
        self.gs, self.ts, self.ms = gs, ts, ms
        self.tiles_len = (gs[0]*gs[1]) - 1      # 3 * 3 - 1  = 8
        self.tiles = [(x,y) for x in range(gs[0]) for y in range(gs[1])]
        self.tilesOG = [(x,y) for x in range(gs[0]) for y in range(gs[1])]    
        self.tilespos = {(x,y):(x*(ts+ms)+ms,y*(ts+ms)+ms) for y in range(gs[1]) for x in range(gs[0])}    
        self.font = pygame.font.Font(None, 120)    
        w,h = gs[0]*(ts+ms)+ms, gs[1]*(ts+ms)+ms
        
        mainwindow.withdraw()
        root = Toplevel()
        root.attributes('-alpha', 0)   #to make this window invisible
        root.filename =  filedialog.askopenfilename(title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        pic = pygame.image.load(root.filename)
        pic = pygame.transform.scale(pic, (w,h))
        root.destroy()
        
        self.images = []
        for i in range(self.tiles_len):
            x,y = self.tilespos[self.tiles[i]]
            image = pic.subsurface(x,y,ts,ts)
            self.images += [image]
            
        self.temp = self.tiles[:-1]
        shuffle(self.temp)
        self.temp.insert(len(self.temp), self.tiles[-1])
        self.tiles = self.temp

    def getBlank(self): return self.tiles[-1]
    def setBlank(self, pos): self.tiles[-1] = pos
    
    opentile = property(getBlank, setBlank)
    
    def switch(self, tile):
        n = self.tiles.index(tile)
        self.tiles[n], self.opentile = self.opentile, self.tiles[n]
        if self.tiles == self.tilesOG:
            print("COMPLETE")
    
    def is_grid(self, tile): 
        return tile[0] >= 0 and tile[0] < self.gs[0] and tile[1] >= 0 and tile[1] < self.gs[1]
    
    def adjacent(self):
        x,y = self.opentile;
        return (x-1, y), (x+1,y), (x,y-1), (x,y+1)
    
    def update(self, dt):
        """
        # Find the tile mouse is on
        # Switch as long as open tile is adjacent
        """
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()
        
        # Convert mouse position relative to tile position and check in grid
        if mouse[0]:
            tile = mpos[0]//self.ts, mpos[1]//self.ts
            
            if self.is_grid(tile): 
                if tile in self.adjacent():
                    self.switch(tile)
    
    def draw(self, screen):
        for i in range(self.tiles_len):
            x,y = self.tilespos[self.tiles[i]]
            screen.blit(self.images[i], (x,y)) 

           
def imageSliderGame():
    mainwindow.withdraw()
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("Slide Puzzle")
    screen = pygame.display.set_mode((600,600))
    fpsclock = pygame.time.Clock()
    
    program = SlidePuzzle((3,3), 200, 5)

    while True:
        dt = fpsclock.tick()/1000
        screen.fill((1,1,1))
        
        program.draw(screen)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                mainwindow.deiconify()
                
        program.update(dt)


def typingSpeedGame():
    mainwindow.withdraw()
    global score, miss, count, timer, sliderwords
    score = miss = count = 0
    timer=60
    sliderwords =''

    root = Toplevel()
    root.geometry('800x600+300+100')
    root.configure(bg='black')
    root.title('Typing Speed Increaser')
    root.iconbitmap('logo.ico')

    ############################################################
    def slider():
        global count,sliderwords
        text='Test Your Typing Speed with us'
        if count>= len(text):
            count = 0
            sliderwords =""
        sliderwords += text[count]
        count +=1
        fontlabel.configure(text=sliderwords)
        fontlabel.after(150,slider)


    def time():
        global timer, score, miss
        if timer>11:
            pass
        else:
            timerlabelcount.configure(fg='red')
        if timer>0:
            timer -=1
            timerlabelcount.configure(text=timer)
            timerlabelcount.after(1000,time)
        else:
            instruction.configure(text='Hit = {} | Miss = {} | Total Score = {}'
                                    .format(score,miss,score-miss))
            rr= messagebox.askretrycancel('Notification','Wanna Play Again!!!!')
            if rr==True:
                score=0
                miss=0
                timer=60
                timerlabelcount.configure(text=timer)
                wordlabel.configure(text=words[0])
                scorelabelcount.configure(text=score)
                wordentry.delete(0, END)

    def startgame(event):
        global score, miss
        if timer==60:
            time()
        instruction.configure(text='')
        startlabel.configure(text='')
        if wordentry.get()== wordlabel['text']:
            score +=1
            scorelabelcount.configure(text=score)
        else:
            miss +=1
        random.shuffle(words)
        wordlabel.configure(text=words[0])
        wordentry.delete(0,END)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit the game?"):
            root.destroy()
            mainwindow.deiconify()

    ##################################################

    # define labels 
    fontlabel=Label(root,text='',font=('airal',25,'italic bold'),bg='black',fg='purple',width=40)
    fontlabel.place(x=10,y=20)
    slider()

    startlabel=Label(root,text='Lets begin!!!',font=('airal',30,'italic bold'),bg='black',fg='white')
    startlabel.place(x=275,y=60)

    random.shuffle(words)
    wordlabel=Label(root,text=words[0],font=('airal',45,'italic bold'),bg='black',fg='green')
    wordlabel.place(x=320,y=240)

    scorelabel=Label(root,text='Your Score:',font=('arial',25,'italic bold'),bg='black',fg='red')
    scorelabel.place(x=10,y=140)

    scorelabelcount=Label(root,text=score,font=('arial',25,'italic bold'),bg='black',fg='blue')
    scorelabelcount.place(x=150,y=180)

    timerlabel=Label(root,text='Time Left:',font=('arial',25,'italic bold'),bg='black',fg='red')
    timerlabel.place(x=600,y=140)

    timerlabelcount=Label(root,text=timer,font=('arial',25,'italic bold'),bg='black',fg='blue')
    timerlabelcount.place(x=600,y=180)

    instruction= Label(root,
        text='Type the Word and hit enter button',
        font=('arial',25,'italic bold'),bg='black',fg='grey'
    )
    instruction.place(x=120,y=500)

    wordentry= Entry(root,font=('airal',25,'italic bold'), bd=10, justify='center')
    wordentry.place(x=220,y=330)
    wordentry.focus_set()

    root.protocol("WM_DELETE_WINDOW", on_closing)   
    root.bind('<Return>', startgame)
    root.resizable(width=False, height=False)
    root.mainloop()


def main():
    ########## landing page mainwindow ##########
    label=Label(mainwindow,text='Lets Play Some Games !!!',font=('airal',20,'italic bold'),bg='black',fg='green')
    label.place(x=150,y=50)

    topframe = Frame(mainwindow)
    topframe.pack()
    redbutton = Button(mainwindow, text="Image Slider Game", fg="red", height = 5, width = 20, command = imageSliderGame)
    redbutton.place(x=120,y=150)

    blackbutton = Button(mainwindow, text="Typing Speed Test", fg="black", height = 5, width = 20, command = typingSpeedGame)
    blackbutton.place(x=360,y=150)

    mainwindow.resizable(width=False, height=False)
    mainwindow.mainloop()

    #############################################


if __name__ == '__main__':
    main()
