#gui module
#from tkinter import *
from os import replace
from tkinter import  Menu, ttk, Frame,Tk, StringVar, N,E,S,W, PhotoImage
from tkinter import messagebox
from tkinter import filedialog
from typing import Sequence 
import tkinter.simpledialog as simpledialog
import tkinter

import sys
import random
import copy
import time
#crypto
#
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except:
    print("Crypography Package required. To install, use ' pip install cryptography '")
import base64



#file saving
#pickle can save objects as str and turn them back into objects
import pickle
#
try:
    from PIL import Image
except:
    print("Pillow Package required. To install, use ' pip install pillow '")

#alphabet module
import string 

class Grid():
    def __init__(self):
        Grid.computerCoordinates = []
    def make_grid(self,size): #makes 2D list for the size given by the user when the game is started
        self.newGrid = [['0' for i in range(size)]for j in range(size)]
        Grid.playerGrid = self.newGrid
        self.oNewGrid= [['0' for i in range(size)]for j in range(size)]
        Grid.oponentGrid = self.oNewGrid
        #return (self.newGrid)
        print("New grid")              
                
    def get_letters(self,a):
        self.letters = string.ascii_uppercase #stores the letters of the alphabet in uppercase 
        return self.letters[a]
    def get_count_boat_player_Grid(self,length):
        return sum(row.count(length) for row in Grid.playerGrid)

    def get_count_boat_oponent_Grid(self,length):
        return sum(row.count(length) for row in Grid.oponentGrid)
        
    #tidy up by making fire inherit its variables from a player object

    def playerFire(self,i,j):
        print("You have fired at ", i , j )
        if 'B' in Grid.oponentGrid[i][j]:
            MenuGUI.hintText2.set(f"You hit a {Grid.oponentGrid[i][j]}")
            Grid.oponentGrid[i][j] ='H' + Grid.oponentGrid[i][j][1]
            print("it's a hit")
            MenuGUI.playerHit += 1
            MenuGUI.playerSunkList =[]
            for n in range(1,6):
                square = 'H' + str(n)
                if self.get_count_boat_oponent_Grid(square)==n:
                    print(f"Sunk length {n}")
                    MenuGUI.playerSunkList.append(n)
                    MenuGUI.hintText2.set(f"You hit a boat {Grid.oponentGrid[i][j]} and sunk ship lengths {MenuGUI.playerSunkList}")
                    MenuGUI.playerSunk = len(MenuGUI.playerSunkList)

            MenuGUI.changeOponentSquareIcon(self)
            MenuGUI.disableAllPlayerButtons(self)
            
        elif Grid.oponentGrid[i][j]== '0':
            print("It's a miss")
            MenuGUI.hintText2.set(f"You missed")
            Grid.oponentGrid[i][j] = 'M'
            MenuGUI.playerMiss += 1
            MenuGUI.changeOponentSquareIcon(self)
            MenuGUI.disableAllOponentButtons(self)
            MenuGUI.changePlayerSquareIcon(self)
            if MenuGUI.mode == 2:
                pass
            elif MenuGUI.mode == 1:
                MenuGUI.disableAllPlayerButtons(self)
                #second = random.randint(1,2)
                #time.sleep(second)
                self.computer_fire()
            
        MenuGUI.hintText3.set(f"{MenuGUI.playerHit} Hits {MenuGUI.playerSunk} Sinks {MenuGUI.playerMiss} Misses")
        if MenuGUI.playerSunk == 5:
            MenuGUI.disableAllOponentButtons(self)
            MenuGUI.disableAllPlayerButtons(self)
            messagebox.showinfo('You WON',"Congratualations you won!")
        

    def computer_fire(self):
        repeat = True
        while repeat == True:
            ir = random.randint(0,MenuGUI.getSize(self)-1)
            jr = random.randint(0,MenuGUI.getSize(self)-1)
            
    
            if ([ir,jr]in Grid.computerCoordinates):
                print(f"Duplicate {ir},{jr}")
                    
            else: 
                print(f"Non duplicate {ir},{jr}")
                Grid.computerCoordinates.append([ir,jr])
                
                print(Grid.computerCoordinates)
                print(f"Computer fired at {ir},{jr}")
                self.oponentFire(ir,jr)
                repeat = False
                break
                
                
                
        
        
        

        return    

    def oponentFire(self,i,j):
        print("Oponent fired at ", i , j )
        if 'B' in Grid.playerGrid[i][j]:

            MenuGUI.hintText5.set(f"Oponent hit a {Grid.playerGrid[i][j]}")
            Grid.playerGrid[i][j] ='H' + Grid.playerGrid[i][j][1]
            print("You've hit boat")
            MenuGUI.oponentSunkList = []
            MenuGUI.oponentHit += 1
            #checks how many ships have sunk
            for n in range(1,6):
                square = 'H' + str(n)
                if self.get_count_boat_player_Grid(square)==n:
                    print(f"Sunk length {n}")
                    MenuGUI.oponentSunkList.append(n)
                    MenuGUI.oponentSunk =len(MenuGUI.oponentSunkList)
                    MenuGUI.hintText5.set(f"Oponent hit a boat {Grid.playerGrid[i][j]} and sunk ship length {MenuGUI.oponentSunkList}")
                    


            MenuGUI.changePlayerSquareIcon(self)
            MenuGUI.disableAllOponentButtons(self)
            if MenuGUI.mode == 1:
                MenuGUI.disableAllPlayerButtons(self)
                self.computer_fire()

            
        elif Grid.playerGrid[i][j]== '0':
            print("It's a miss")
            MenuGUI.hintText5.set(f"Opponent missed")
            Grid.playerGrid[i][j] = 'M'
            MenuGUI.changeOponentSquareIcon(self)
            MenuGUI.changePlayerSquareIcon(self)
            MenuGUI.disableAllPlayerButtons(self)
            
            MenuGUI.oponentMiss +=1
        MenuGUI.hintText6.set(f"{MenuGUI.oponentHit} Hits {MenuGUI.oponentSunk} Sinks {MenuGUI.oponentMiss} Misses")
        if MenuGUI.oponentSunk == 5:
            MenuGUI.disableAllOponentButtons(self)
            MenuGUI.disableAllPlayerButtons(self)
            messagebox.showinfo('You LOST',"Oh dear! Your Oponent beat you!")
              

class Ships(Grid):
    
    #function when a square is clicked and boat is placed

    
        
    def place_ship(self,i,j):
        
        print()
        
        try:
    

            self.tempPlayerGrid = copy.deepcopy(Grid.playerGrid)
            
            self.tempShip=[]
            self.tempList = []
            self.selectedI = i
            self.selectedJ = j
            for n in range(MenuGUI.shipSize):
                if Grid.playerGrid[i+n][j] == '0': 
                    Grid.playerGrid[i+n][j] = 'B'+ str(MenuGUI.shipSize)
                    self.tempList = []
                    self.tempList.append(i+n)
                    self.tempList.append(j)
                    self.tempShip.append(self.tempList)
                    
                else:
                    messagebox.showerror("Overlap","You have entered a square that will result in a ship overlap. Please enter again")
                    Grid.playerGrid = copy.deepcopy(self.tempPlayerGrid)
                    MenuGUI.shipSize = MenuGUI.shipSize+1
                    break
                    
            MenuGUI.shipSize = MenuGUI.shipSize-1      
            MenuGUI.changePlayerSquareIcon(self)
            MenuGUI.disableBoatSquares(self)
            self.shipCount =(MenuGUI.getSize(self)*MenuGUI.getSize(self))-sum(row.count('0') for row in Grid.playerGrid)
            print("Square ( %i,%i ) = "%(i,j)   , Grid.playerGrid[i][j] , ". Ship count: " , self.shipCount)
            print(self.tempShip)
            if self.shipCount >=15:
                MenuGUI.firing = 1
                MenuGUI.disableAllPlayerButtons(self)
                if MenuGUI.mode == 2:
                    MenuGUI.fileSaveButton.configure(state='enable')            
                    MenuGUI.hintText1.set("Thank You. Please now select save game config")
                    MenuGUI.hintText2.set("Swap files with your oponent by sending the config file produced.")
                    MenuGUI.hintText3.set("Then open your oponent's file")
                elif MenuGUI.mode == 1:
                    
                    MenuGUI.enableAllOponentButtons(self)
            else:
                MenuGUI.hintText1.set("Now select where your battleship of length %i is placed" % MenuGUI.shipSize)
            print(Grid.playerGrid)

            
    
        except:
                messagebox.showerror("Outside of Range","You have entered a square outside the grid, please enter again")
                Grid.playerGrid = copy.deepcopy(self.tempPlayerGrid)
                

    def randomStartingPoints(self):
        #starting places
        i = []
        j = []
        
        n = 0
        while n < 5:
            MenuGUI.shipSize = n+1
            ia = random.randint(0,MenuGUI.getSize(self)-1)
            ja = random.randint(0,MenuGUI.getSize(self)-1)
            if (ia in i) and (ja in j):
                print("Duplicate")
                
            else:
                
                i.append(ia)
                j.append(ja)

                #Grid.oponentGrid[i[n]][j[n]] = 'B'+ str(MenuGUI.shipSize)
                n +=1
        return [i,j]
    
    def is_ship_length_n_possible(self,i,j,length):
        x = []
        y = []
        for q in range (length):
            x.append(i + q)
            y.append(j)
            if x[q] > MenuGUI.getSize(self)-1:
                return False
            else:
                continue
    def do_ships_overlap(self,i,j,length):
        x = []
        y = []
        for q in range(length):
            x.append(i+q)
            y.append(j)
            if x[q] in self.boardShipsj and y[q] in self.boardShipsj:
                print("Extended boats overlap")
                return False
            else:
                continue



    def ship_lengths(self,i,j,length):
        x = []
        y = []
        for q in range (length):
            x.append(i + q)
            y.append(j)
            
        return [x,y]
            

        


    def computer_place_ships(self):
        self.boardShipsi = []
        self.boardShipsj = []
        point = self.randomStartingPoints()
        #returns list with coordinates of boat starting places


        #one iteration for each boat
        for n in range (5):
            a = n + 1
            i = point[0][n]
            j = point[1][n]
            if self.is_ship_length_n_possible(i,j,a) == False or self.do_ships_overlap(i,j,a) == False:
                print("Not Possible")
                print()
                Grid.make_grid(self,(MenuGUI.getSize(self)))
                
                self.computer_place_ships()
                break

            else:

                shipBodies = self.ship_lengths(i,j,a)
                for m in range(a):
                    x = shipBodies[0][m]
                    y = shipBodies[1][m]
                    Grid.oponentGrid[x][y] = 'B'+ str(a)
                    self.boardShipsi.append(x)
                    self.boardShipsj.append(y)

                
            
        if sum(row.count('0') for row in Grid.oponentGrid) > ((MenuGUI.getSize(self)*MenuGUI.getSize(self))-15) :
            print("Not Possible due to not 15 elements")
            count =(MenuGUI.getSize(self)*MenuGUI.getSize(self)-sum(row.count('0') for row in Grid.oponentGrid))
            print(f"There are {count} boat squares so not possible")
            print()
            Grid.make_grid(self,(MenuGUI.getSize(self))) 
            self.computer_place_ships()
        else:
            pass
            
            

                
    def rotate90(self):
        #this will attempt to rotate the boat 90 degrees anticlockwise. If that's not possible, it will attempt to
        #rotate 90 degrees clockwise. If that's not possible ,it will prompt the user to select again
        
            try:
                self.tempPlayerGrid = copy.deepcopy(Grid.playerGrid)
                i = self.selectedI
                j = self.selectedJ
                self.tempShipBefore = self.tempShip
                for n in range (1,MenuGUI.shipSize+1):
                    Grid.playerGrid[(self.tempShip[n][0])][(self.tempShip[n][1])] = '0'
                    
                    
                    
                    x = self.tempShip[n][0]
                    y = self.tempShip[n][1]
                    xB = i+j-y
                    yB = -i+j+x
                    x=xB
                    y=yB
                    if Grid.playerGrid[x][y] == '0':
                        Grid.playerGrid[x][y]='B'+str(MenuGUI.shipSize+1)
                    else:
                        messagebox.showerror("Overlap","You have entered a square that will result in a ship overlap. Please enter again")
                        Grid.playerGrid = copy.deepcopy(self.tempPlayerGrid)
                        

                    
                MenuGUI.changePlayerSquareIcon(self)
                MenuGUI.disableBoatSquares(self)
                print(self.tempShip)
                
            except:
                try:
                    self.tempPlayerGrid = copy.deepcopy(Grid.playerGrid)
                    i = self.selectedI
                    j = self.selectedJ
                    self.tempShipBefore = self.tempShip
                    for n in range (1,MenuGUI.shipSize+1):
                        Grid.playerGrid[(self.tempShip[n][0])][(self.tempShip[n][1])] = '0'
                        
                        
                        
                        x = self.tempShip[n][0]
                        y = self.tempShip[n][1]
                        xB = y-j+i
                        yB = -x+i+j
                        x=xB
                        y=yB
                        if Grid.playerGrid[x][y] == '0':
                            Grid.playerGrid[x][y]='B'+str(MenuGUI.shipSize+1)
                        else:
                            messagebox.showerror("Overlap","You have entered a square that will result in a ship overlap. Please enter again")
                            Grid.playerGrid = copy.deepcopy(self.tempPlayerGrid)
                            

                        
                    MenuGUI.changePlayerSquareIcon(self)
                    MenuGUI.disableBoatSquares(self)
                    print(self.tempShip)
                except:
                    messagebox.showerror("Outside of Range","You have entered a square outside the grid, Please enter again")
                    Grid.playerGrid = copy.deepcopy(self.tempPlayerGrid)
                
                


        #tempButton = MenuGUI.playerGridButtons[i][j]
        #tempButton.config(bg='red')



class MenuGUI(Frame,Ships,Grid):
    def __init__(self,root): 
        
        MenuGUI.mode = 0
        MenuGUI.firing = 0

        root.title("Battleships")#sets the title of the window
        


        #setup file save encryption

        #self.key = Fernet.generate_key()
        #self.keyFile = open('key.key','wb')
        #self.keyFile.write(self.key)
        #self.keyFile.close()

        #sets the icon for the UI
        #Replace this path with where you've stored the Icons folder.
        # Python requires forward slashes(/), not backslashes(\)
        #Ensure there is a forward slash at the end of path(/)
        path = "D:/BBC Apprenticeship/University/Semester 3/Programming/COURSEWORK/Icons/"

        self.icon = PhotoImage(file= path + "ship.png")
        root.iconphoto(False,self.icon)

        self.battleshipImage = PhotoImage(file=path + "logo.png")
        
        

        #imports photo icons
        self.hitImg = PhotoImage(file= path + "ship_body_sunk.png" )
        self.emptyImg = PhotoImage(file= path + "empty.png")
        self.boatImg = PhotoImage(file= path + "ship_body.png")
        self.missImg = PhotoImage(file=path + "miss.png")

        self.smallEmptyImg = PhotoImage(file = path + "/oponent_icons/empty.png")
        self.smallHitImg = PhotoImage(file = path + "/oponent_icons/hit.png")
        self.smallMissImg = PhotoImage(file = path + "/oponent_icons/miss.png")
    

        #make the frames for the GUI
        self.mainMenuFrame = ttk.Frame(root, padding="3 3 12 12")
        self.mainMenuFrame.grid(column=0, row=0, sticky=(N, W, E, S))
        self.middleFrame = ttk.Frame(root,padding="3 3 12 12")
        self.middleFrame.grid(column=1,row=0,sticky=(N, W, E, S))
        self.rightFrame = ttk.Frame(root,padding="3 3 12 12")
        self.rightFrame.grid(column=2,row=0,sticky=(N, W, E, S))
        self.playerBoardFrame = ttk.Frame(self.middleFrame,padding="3 3 12 12")
        self.playerBoardFrame.grid(column=0,row=0,sticky=(N, W, E, S))
        self.oponentBoardFrame = ttk.Frame(self.rightFrame, padding="3 3 12 12")
        self.oponentBoardFrame.grid(column=0,row=0,sticky=(N, W, E, S))
        self.placeshipsFrame = ttk.Frame(self.middleFrame,padding="3 3 12 12")
        self.placeshipsFrame.grid(column=0,row=1)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)	



        #setup for dropdown list
        self.gridList = ['','6x6','8x8','10x10','12x12','14x14','16x16']
        self.defListItem = StringVar(root)
        self.defListItem.set(self.gridList[3]) #default value


    
        #gui elements

        #main menu frame Gui (left)

        
        #image
        ##insert image code here##

        #name label
        ttk.Label(self.mainMenuFrame, text= "Battleships!").grid(row=2,column=2,sticky=(W,E))        

        #dropdown description label
        ttk.Label(self.mainMenuFrame, text= "Grid Size:").grid(row=3,column=1,sticky=(W,E))

        #dropdown grid size selection
        ttk.OptionMenu(self.mainMenuFrame,self.defListItem,*self.gridList).grid(row=3,column=2,sticky=(W,E))

        #load game button ##add command##
        MenuGUI.fileSaveButton = ttk.Button(self.mainMenuFrame,text="Save game config",command = lambda: SaveState.saveGame(self),state='disabled')
        MenuGUI.fileSaveButton.grid(row=4,column=2,sticky=(W,E)) 

        MenuGUI.fileOpenButton = ttk.Button(self.mainMenuFrame,text="Open Oponent config",command = lambda: SaveState.openOponentState(self),state='disabled')
        MenuGUI.fileOpenButton.grid(row=4,column=3,sticky=(W,E)) 

        self.fileGameStateButton = ttk.Button(self.mainMenuFrame,text="Open Previous Game Config",command = lambda: SaveState.openGameState(self),state='disabled')
        self.fileGameStateButton.grid(row=5,column=2,columnspan=2,sticky=(W,E)) 

        #player number label new game
        ttk.Label(self.mainMenuFrame, text= "New Game:").grid(row=6,column=1,sticky=(W,E))

        #1 player  button ##add command##
        ttk.Button(self.mainMenuFrame,text="1 Player",command=self.onePlayerBtn).grid(row=6,column=2,sticky=(W,E))        

        #2player  button 
        ttk.Button(self.mainMenuFrame,text="2 Player",command=self.twoPlayerBtn).grid(row=6,column=3,sticky=(W,E))

        #instruction text label
        MenuGUI.hintText1=tkinter.StringVar()
        MenuGUI.hintText1.set("Select Grid size then select 1 or 2 players")
        MenuGUI.hintLbl1 = ttk.Label(self.mainMenuFrame,textvariable=self.hintText1).grid(row=7,column=1,columnspan=3)
        
        MenuGUI.playerSunkList = []
        MenuGUI.oponentSunkList = []

        MenuGUI.playerMiss = 0
        MenuGUI.playerHit = 0
        MenuGUI.playerSunk = 0

        MenuGUI.oponentMiss = 0
        MenuGUI.oponentHit = 0
        MenuGUI.oponentSunk = 0 


        MenuGUI.hintText2=tkinter.StringVar()
        MenuGUI.hintText2.set("To load a file, create a game with the correct grid size")
        MenuGUI.hintLbl2 = ttk.Label(self.mainMenuFrame,textvariable=self.hintText2).grid(row=8,column=1,columnspan=3) 

        MenuGUI.hintText3 = tkinter.StringVar()
        MenuGUI.hintText3.set("")
        MenuGUI.hintLbl3 = ttk.Label(self.mainMenuFrame,textvariable=self.hintText3).grid(row=9,column=1,columnspan=3) 

        MenuGUI.hintText4 = tkinter.StringVar()
        MenuGUI.hintText4.set("")
        MenuGUI.hintLbl4 = ttk.Label(self.mainMenuFrame,textvariable=self.hintText4).grid(row=10,column=1,columnspan=3)

        MenuGUI.hintText5 = tkinter.StringVar()
        MenuGUI.hintText5.set("")
        MenuGUI.hintLbl5 = ttk.Label(self.mainMenuFrame,textvariable=self.hintText5).grid(row=11,column=1,columnspan=3)

        MenuGUI.hintText6 = tkinter.StringVar()
        MenuGUI.hintText6.set("")
        MenuGUI.hintLbl6 = ttk.Label(self.mainMenuFrame,textvariable=self.hintText6).grid(row=12,column=1,columnspan=3)
       
        for child in self.mainMenuFrame.winfo_children():#adds padding
            child.grid_configure(padx=2, pady=5)

        #tempory player and oponent board frame GUI elements (both)
        for i in range (2*(self.gridList.index(self.defListItem.get()))+4):
            for j in range (2*(self.gridList.index(self.defListItem.get()))+4):
                ttk.Button(self.oponentBoardFrame,width=3,state='disabled').grid(row=i,column=j)
                ttk.Button(self.playerBoardFrame,width=3,state='disabled').grid(row=i,column=j)

                #text=str(i)+','+str(j)

        #place ships buttons size
        #self.shipSizeButtons = [] 
        #for i in range (5):
         #   self.shipSizeButtons.append(ttk.Button(self.placeshipsFrame,text=str(i+1),width=3,state='disabled'))
         #   self.shipSizeButtons[i].grid(column=i,row=0)
        

        
    

    def updateGUI(self):
        self.size = (2*(self.gridList.index(self.defListItem.get()))+4)
        Grid.make_grid(self,self.size)
        self.fileGameStateButton.configure(state='enable')
        

        #remove previous grid
        for child in self.oponentBoardFrame.winfo_children():
            child.destroy()
        for child in self.playerBoardFrame.winfo_children():
            child.destroy()

        MenuGUI.shipCount = 0
        MenuGUI.shipSize = 5

        self.rotateButton = ttk.Button(self.placeshipsFrame,text="Rotate 90",command = lambda:  Ships.rotate90(self))
        self.rotateButton.grid(column=1,row=1,columnspan=3)

        #create new grid of size n
        


        MenuGUI.playerGridButtons = []
        self.oponentGridButtons = []
        for i in range (self.size):
            
            MenuGUI.playerGridButtons.append ([])
            self.oponentGridButtons.append([])
            
            for j in range (self.size):
                ttk.Label(self.playerBoardFrame,text=Grid.get_letters(self,j)).grid(row=0,column=j+1)
                ttk.Label(self.oponentBoardFrame,text=Grid.get_letters(self,j)).grid(row=0,column=j+1)
                ttk.Label(self.playerBoardFrame,text=i+1).grid(row=i+1,column=0)
                ttk.Label(self.oponentBoardFrame,text=i+1).grid(row=i+1,column=0)
                ##(ADD FUNCTION)
                tempOponentButton = ttk.Button(self.oponentBoardFrame,width=3,state = 'disabled',image = self.smallEmptyImg, command = lambda i=i, j=j: Grid.playerFire(self,i,j))
                tempOponentButton.grid(row=i+1,column=j+1)
                self.oponentGridButtons[i].append(tempOponentButton)
                

                tempPlayerButton = ttk.Button(self.playerBoardFrame,width=3,image = self.emptyImg,command =  lambda i=i, j=j:  Ships.place_ship(self,i,j))
                tempPlayerButton.grid(row=i+1,column=j+1)
                MenuGUI.playerGridButtons[i].append(tempPlayerButton)


        

        

       
               
    def getSize(self):
        return self.size

    def getLetterNumber(self,letter):
        MenuGUI.columnNumber = self.letterList.index(letter)



    
    def twoPlayerBtn(self):
        self.updateGUI()
        #reset game stats
        MenuGUI.mode = 2
        MenuGUI.playerSunkList = []
        MenuGUI.oponentSunkList = []

        MenuGUI.playerMiss = 0
        MenuGUI.playerHit = 0
        MenuGUI.playerSunk = 0

        MenuGUI.oponentMiss = 0
        MenuGUI.oponentHit = 0
        MenuGUI.oponentSunk = 0 
        Grid.make_grid(self,self.size)

        MenuGUI.hintText1.set("Now select where your battleship of length %i is placed" % MenuGUI.shipSize)
        MenuGUI.hintText2.set("To load a file, select load Game from file")

        print("Player 2 Button Click. Grid size: " + str(self.size))
        print(Grid.playerGrid)

        #disable menu buttons 
        #add save to file button

    def onePlayerBtn(self):
        self.updateGUI()
        #reset game stats
        MenuGUI.mode = 1
        MenuGUI.playerSunkList = []
        MenuGUI.oponentSunkList = []

        MenuGUI.playerMiss = 0
        MenuGUI.playerHit = 0
        MenuGUI.playerSunk = 0

        MenuGUI.oponentMiss = 0
        MenuGUI.oponentHit = 0
        MenuGUI.oponentSunk = 0 
        Grid.make_grid(self,self.size)
        Ships.computer_place_ships(self)
        Grid.computerCoordinates = []
        count =(MenuGUI.getSize(self)*MenuGUI.getSize(self)-sum(row.count('0') for row in Grid.oponentGrid))
        print(f"There are {count} boat squares")
        MenuGUI.hintText1.set("Now select where your battleship of length %i is placed" % MenuGUI.shipSize)
        MenuGUI.hintText2.set("To load a file, select load Game from file")
        MenuGUI.hintText3.set("The computer successfully placed")
            

        #temp view
        # for x in range(self.size):
        #     for y in range (self.size):
        #         if 'B' in Grid.oponentGrid[x][y]:
        #             self.oponentGridButtons[x][y].configure(image=self.smallHitImg,state='enabled')
        #         elif 'M' in Grid.oponentGrid[x][y]:
        #             self.oponentGridButtons[x][y].configure(image=self.smallMissImg,state='enabled')
        
        return


    def disableBoatSquares(self):
        for x in range(self.size):
            for y in range(self.size):
                if 'B' in Grid.playerGrid[x][y]:
                    MenuGUI.playerGridButtons[x][y].configure(image=self.boatImg,state='disabled')
    def changePlayerSquareIcon(self):
        #'NoneType' object not subscriptable
        #ttk buttons cannot hold colours
        #ttk button image
        #MenuGUI.playerGridButtons[i+1][j+1].config()
        
        for x in range (self.size):
            for y in range (self.size):
                if Grid.playerGrid[x][y] == '0':
                    MenuGUI.playerGridButtons[x][y].configure(image=self.emptyImg,state='enabled')
                elif 'H' in Grid.playerGrid[x][y]:
                    MenuGUI.playerGridButtons[x][y].configure(image=self.hitImg,state='disabled')
                elif Grid.playerGrid[x][y] == 'M':
                    MenuGUI.playerGridButtons[x][y].configure(image=self.missImg,state='disabled')
                elif 'B' in Grid.playerGrid[x][y]:
                    self.playerGridButtons[x][y].configure(state='enabled')

    def changeOponentSquareIcon(self):
        for x in range(self.size):
            for y in range (self.size):
                if 'H' in Grid.oponentGrid[x][y]:
                    self.oponentGridButtons[x][y].configure(image=self.smallHitImg,state = 'disabled')
                elif Grid.oponentGrid[x][y] == '0':
                    self.oponentGridButtons[x][y].configure(image=self.smallEmptyImg,state = 'enabled')
                elif Grid.oponentGrid[x][y] == 'M':
                    self.oponentGridButtons[x][y].configure(image=self.smallMissImg,state = 'disabled')
                elif 'B' in Grid.oponentGrid[x][y]:
                    self.oponentGridButtons[x][y].configure(image=self.smallEmptyImg,state='enabled')
            

    def disableAllPlayerButtons(self):
        for i in range (self.size):
            for j in range (self.size):
                MenuGUI.playerGridButtons[i][j].configure(state='disabled')
        self.rotateButton.configure(state='disabled')
        print("Disabled additional buttons")

    def disableAllOponentButtons(self):
        for i in range (self.size):
            for j in range (self.size):
                self.oponentGridButtons[i][j].configure(state='disabled')

    def enableAllOponentButtons(self):
        for i in range (self.size):
            for j in range (self.size):
                self.oponentGridButtons[i][j].configure(state='enabled')

    def enableAllPlayerButtons(self):
        for i in range (self.size):
            for j in range (self.size):
                MenuGUI.playerGridButtons[i][j].configure(state='enabled')


class SaveState(Grid):
    #code written from https://www.youtube.com/watch?v=H8t4DJ3Tdrg
    #this class uses basic encryption to encrypt the text in the state of the game. This prevents players from cheating by looking at the game file
    

    def locateKeyOrCreateOne(self):
        #This function returns a .key file with an encryption key
        #I have changed this to utilise a password keyword instead so there are less files floating about

        if messagebox.askyesno(message='Would you like to find an existing crypto key?') == True:
            self.fileName = filedialog.askopenfilename(title='Locate Battleships.key',defaultextension='.key',initialfile='battleships.key')
            self.keyFile = open(self.fileName,'rb')
            self.Key = self.keyFile.read()
            self.keyFile.close()
            print("Opened crypto key from: ",self.fileName)
        else:
            self.fileName = filedialog.asksaveasfile(title='Save Battleships.key',defaultextension='.key',initialfile='battleships.key')
            self.keyFile = open(self.fileName.name,'wb')
            self.genKey = Fernet.generate_key()
            print(self.genKey)
            self.keyFile.write(self.genKey)
            self.keyFile.close()
            self.keyFile = open(self.fileName.name,'rb')
            self.Key = self.keyFile.read()
            self.keyFile.close()
            print("Saved crypto key to: ",self.fileName.name) 
        print(self.Key)

    def passwordEncryption(self):
        #this function returns a key generated by a password. 
        #Players can send their oponent a unique passphrase which will encrpyt the game state and can still be
        # unencrypted by the oponent remotely.
        #  
        self.passPhraseProvided = simpledialog.askstring(title="Passphrase",prompt="Enter you passphrase. (This needs to be the same as your oponent.)")
        self.password = self.passPhraseProvided.encode()
        self.salt = b'\xc4"et\x8e\xb7\x98\xce\xcc.\xb2\xdb\x07\x84\xc3\xbc'
        self.kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=self.salt,iterations=100000)
        self.key = base64.urlsafe_b64encode(self.kdf.derive(self.password))
        print(self.key) 
        MenuGUI.hintText2.set("Once you've placed your ships, click save and send the file to your oponent")

    def encryptMessageToFile(self):
        self.gameGrids = [Grid.playerGrid, Grid.oponentGrid]
        self.message = pickle.dumps(self.gameGrids)
        encodedMessage = self.message
        f = Fernet(self.key)
        self.encryptedMessage = f.encrypt(encodedMessage)
        print(self.encryptedMessage)
        self.fileName = filedialog.asksaveasfile(title='Save game file',defaultextension='.config',initialfile='battleships.config')
        self.gameFile = open(self.fileName.name,'wb')
        self.gameFile.write(self.encryptedMessage)
        self.gameFile.close()
        print("Saved game state to :",self.fileName.name)

        
    def saveGame(self):
        #SaveState.locateKeyOrCreateOne(self)
        SaveState.passwordEncryption(self)
        SaveState.encryptMessageToFile(self)
        MenuGUI.fileOpenButton.configure(state='enable')
        return

    def openOponentState(self):
        SaveState.passwordEncryption(self)
        self.fileName = filedialog.askopenfilename(title='Locate Oponent file',defaultextension='.config',initialfile='battleships.config')
        self.gameFile = open(self.fileName,'rb')
        self.encryptedOpen = self.gameFile.read()
        self.gameFile.close()
        f2 = Fernet(self.key)
        self.decrypted = f2.decrypt(self.encryptedOpen)
        self.pickledBoard = self.decrypted
        self.messageOpen = pickle.loads(self.pickledBoard)
        #Grid.playerGrid = self.messageOpen[1]
        Grid.oponentGrid = self.messageOpen[0]
        MenuGUI.enableAllOponentButtons(self)
        MenuGUI.changePlayerSquareIcon(self)
        MenuGUI.changeOponentSquareIcon(self)
        MenuGUI.enableAllPlayerButtons(self)
        MenuGUI.hintText1.set("You:")
        MenuGUI.hintText2.set("")
        MenuGUI.hintText3.set("0 Hits 0 Sinks 0 Misses")
        MenuGUI.hintText4.set("Oponent:")
        MenuGUI.hintText5.set("")
        MenuGUI.hintText6.set("0 Hits 0 Sinks 0 Misses")
        for i in range (MenuGUI.getSize(self)):
            for j in range (MenuGUI.getSize(self)):

                MenuGUI.playerGridButtons[i][j].configure(command = lambda i=i, j=j: Grid.oponentFire(self,i,j))

    def openGameState(self):
        SaveState.passwordEncryption(self)
        self.fileName = filedialog.askopenfilename(title='Locate game file',defaultextension='.config',initialfile='battleships.config')
        self.gameFile = open(self.fileName,'rb')
        self.encryptedOpen = self.gameFile.read()
        self.gameFile.close()
        f2 = Fernet(self.key)
        self.decrypted = f2.decrypt(self.encryptedOpen)
        self.pickledBoard = self.decrypted
        self.messageOpen = pickle.loads(self.pickledBoard)
        Grid.playerGrid = self.messageOpen[0]
        Grid.oponentGrid = self.messageOpen[1]
        MenuGUI.changePlayerSquareIcon(self)
        MenuGUI.changeOponentSquareIcon(self)
        
        MenuGUI.fileSaveButton.configure(state='enable')
        MenuGUI.fileOpenButton.configure(state='enable')




root = Tk()
menu_gui = MenuGUI(root)
root.mainloop()


