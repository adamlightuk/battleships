#gui module
#from tkinter import *
from tkinter import ttk, Frame,Tk, StringVar, N,E,S,W, PhotoImage,Label
from tkinter import messagebox
from tkinter import filedialog 
import tkinter.simpledialog as simpledialog
import tkinter

import sys
import random
import copy
#crypto
#
from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#file saving
#pickle can save objects as str and turn them back into objects
import pickle
#
from PIL import Image

#alphabet module
import string 

class Grid():
    def make_grid(self,size): #makes 2D list for the size given by the user when the game is started
        self.newGrid = [['0' for i in range(size)]for j in range(size)]
        Grid.playerGrid = self.newGrid
        self.oNewGrid= [['0' for i in range(size)]for j in range(size)]
        Grid.oponentGrid = self.oNewGrid
        #return (self.newGrid)              
                
    def get_letters(self,a):
        self.letters = string.ascii_uppercase #stores the letters of the alphabet in uppercase 
        return self.letters[a]

    def playerFire(self,i,j):
        print("You have fired at ", i , j )
        if Grid.oponentGrid[i][j] =='B':
            Grid.oponentGrid[i][j] ='H'
            print("it's a hit")
            MenuGUI.changeOponentSquareIcon(self)
        elif Grid.oponentGrid[i][j]== '0':
            print("It's a miss")
            Grid.oponentGrid[i][j] = 'M'
            MenuGUI.changeOponentSquareIcon(self)

    def oponentFire(self):
        i = MenuGUI.getOponentColumns(self)
        j = MenuGUI.getOponentRows(self)
        print("Oponent fired at ", i , j )
        if Grid.playerGrid[i][j] =='B':
            Grid.playerGrid[i][j] ='H'
            print("it's a hit")
            MenuGUI.changePlayerSquareIcon(self)
        elif Grid.playerGrid[i][j]== '0':
            print("It's a miss")
            Grid.playerGrid[i][j] = 'M'
            MenuGUI.changePlayerSquareIcon(self)


        




class Ships(Grid):
    
    #function when a square is clicked and boat is placed

    
        
    def place_ship(self,i,j):
        
        print()
        while True:
            try:
        

                self.tempPlayerGrid = copy.deepcopy(Grid.playerGrid)
                
                self.tempShip=[]
                self.tempList = []
                self.selectedI = i
                self.selectedJ = j
                for n in range(MenuGUI.shipSize):
                    if Grid.playerGrid[i+n][j] == '0': 
                        Grid.playerGrid[i+n][j] = 'B'
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
                self.shipCount =sum(row.count('B') for row in Grid.playerGrid)
                print("Square ( %i,%i ) = "%(i,j)   , Grid.playerGrid[i][j] , ". Ship count: " , self.shipCount)
                print(self.tempShip)
                if self.shipCount >=15:
                    MenuGUI.disableAllPlayerButtons(self)
                    MenuGUI.fileSaveButton.configure(state='enable')
                    
                    MenuGUI.hintText1.set("Thank You. Please now select a square to playerFire at your oponent")
                else:
                    MenuGUI.hintText1.set("Now select where your battleship of length %i is placed" % MenuGUI.shipSize)

                break
        
            except:
                    messagebox.showerror("Outside of Range","You have entered a square outside the grid, please enter again")
                    Grid.playerGrid = copy.deepcopy(self.tempPlayerGrid)
                    break
                
    def computer_place_ships(self):
        while True:
            try:

                for n in range(5):
                    i = random.randint(0,(MenuGUI.getSize(self)))
                    j = random.randint(0,MenuGUI.getSize(self))
                    for m in range(n):
                        Grid.oponentGrid[i+n][j] = 'B'
                        
                break
            except:
                messagebox.showerror("Outside of Range","You have entered a square outside the grid, please enter again")
                
                break



            

                    
    def rotate90(self):
        while True:
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
                        Grid.playerGrid[x][y]='B'
                    else:
                        messagebox.showerror("Overlap","You have entered a square that will result in a ship overlap. Please enter again")
                        Grid.playerGrid = copy.deepcopy(self.tempPlayerGrid)
                        break

                    
                MenuGUI.changePlayerSquareIcon(self)
                print(self.tempShip)
                break
            except:
                messagebox.showerror("Outside of Range","You have entered a square outside the grid, Please enter again")
                Grid.playerGrid = copy.deepcopy(self.tempPlayerGrid)
                break
                


        #tempButton = MenuGUI.playerGridButtons[i][j]
        #tempButton.config(bg='red')



class MenuGUI(Frame,Ships,Grid):
    def __init__(self,root): 
        
        root.title("Battleships")#sets the title of the window
        


        #setup file save encryption

        #self.key = Fernet.generate_key()
        #self.keyFile = open('key.key','wb')
        #self.keyFile.write(self.key)
        #self.keyFile.close()

        #sets the icon for the UI
        path = "D:/BBC Apprenticeship/University/Semester 3/Programming/COURSEWORK/Icons/"

        self.icon = PhotoImage(file= path + "ship.png")
        root.iconphoto(False,self.icon)

        self.battleshipImage = PhotoImage(file=path + "logo.png")
        
        

        #imports photo icons
        self.hitImg = PhotoImage(file= path + "hit.png" )
        self.emptyImg = PhotoImage(file= path + "empty.png")
        self.boatImg = PhotoImage(file= path + "ship_body.png")

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
        ttk.Button(self.mainMenuFrame,text="1 Player",state='disabled').grid(row=6,column=2,sticky=(W,E))        

        #2player  button 
        ttk.Button(self.mainMenuFrame,text="2 Player",command=self.twoPlayerBtn).grid(row=6,column=3,sticky=(W,E))

        #instruction text label
        MenuGUI.hintText1=tkinter.StringVar()
        MenuGUI.hintText1.set("Select Grid size then select 1 or 2 players")
        MenuGUI.hintLbl1 = ttk.Label(self.mainMenuFrame,textvariable=self.hintText1).grid(row=7,column=1,columnspan=3)

        MenuGUI.hintText2=tkinter.StringVar()
        MenuGUI.hintText2.set("To load a file, create a game with the correct grid size")
        MenuGUI.hintLbl2 = ttk.Label(self.mainMenuFrame,textvariable=self.hintText2).grid(row=8,column=1,columnspan=3)  
       
        for child in self.mainMenuFrame.winfo_children():#adds padding
            child.grid_configure(padx=2, pady=5)

        #tempory player and oponent board frame GUI elements (both)
        for i in range (2*(self.gridList.index(self.defListItem.get()))+4):
            for j in range (2*(self.gridList.index(self.defListItem.get()))+4):
                ttk.Button(self.oponentBoardFrame,width=3,state='disabled').grid(row=i,column=j)
                ttk.Button(self.playerBoardFrame,width=3,state='disabled').grid(row=i,column=j)

                #text=str(i)+','+str(j)

        #place ships buttons size
        self.shipSizeButtons = [] 
        for i in range (5):
            self.shipSizeButtons.append(ttk.Button(self.placeshipsFrame,text=str(i+1),width=3,state='disabled'))
            self.shipSizeButtons[i].grid(column=i,row=0)
        

        
    

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
        


        self.playerGridButtons = []
        self.oponentGridButtons = []
        for i in range (self.size):
            
            self.playerGridButtons.append ([])
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
                self.playerGridButtons[i].append(tempPlayerButton)


        #spinbox for selectin the grid square that the oponent has fired at
        MenuGUI.rowSpinVar = StringVar(value=1)

        self.letterList = []
        for n in range(self.size):
            self.letterList.append(Grid.get_letters(self,n))

        MenuGUI.columnSpinVar = StringVar(value=self.letterList[0])

        self.rowSpinBox = ttk.Spinbox(self.rightFrame, from_=1, to=self.size,textvariable= MenuGUI.rowSpinVar)
        self.rowSpinBox.grid(column=0,row=1)
        

        self.columnSpinBox = ttk.Spinbox(self.rightFrame, values=self.letterList,textvariable= MenuGUI.columnSpinVar)
        self.columnSpinBox.grid(column=0,row=2)

        
####
        self.fireButton = ttk.Button(self.rightFrame,text="Oponent Fire!", command = lambda: Grid.oponentFire(self))
        self.fireButton.grid(column=0,row=3)
#####

    def getOponentColumns(self):
        return int(self.rowSpinBox.get())

    def getOponentRows(self):
        return  (self.getLetterNumber(self.columnSpinBox.get()))           
               
    def getSize(self):
        return self.size

    def getLetterNumber(self,letter):
        MenuGUI.columnNumber = self.letterList.index(letter)



    
    def twoPlayerBtn(self):
        self.updateGUI()
        
        Grid.make_grid(self,self.size)

        MenuGUI.hintText1.set("Now select where your battleship of length %i is placed" % MenuGUI.shipSize)
        MenuGUI.hintText2.set("To load a file, select load Game from file")

        print("Player 2 Button Click. Grid size: " + str(self.size))
        print(Grid.playerGrid)

        #disable menu buttons 
        #add save to file button

    def changePlayerSquareIcon(self):
        #'NoneType' object not subscriptable
        #ttk buttons cannot hold colours
        #ttk button image
        #MenuGUI.playerGridButtons[i+1][j+1].config()
        for x in range (self.size):
            for y in range (self.size):
                if Grid.playerGrid[x][y] == 'B':
                    self.playerGridButtons[x][y].configure(image=self.boatImg,state='disabled')
                elif Grid.playerGrid[x][y] == '0':
                    self.playerGridButtons[x][y].configure(image=self.emptyImg,state='enabled')
                elif Grid.playerGrid[x][y] == 'H':
                    self.playerGridButtons[x][y].configure(image=self.hitImg,state='disabled')
    def changeOponentSquareIcon(self):
        for x in range(self.size):
            for y in range (self.size):
                if Grid.oponentGrid[x][y]== 'H':
                    self.oponentGridButtons[x][y].configure(image=self.smallHitImg,state = 'disabled')
                elif Grid.oponentGrid[x][y] == '0':
                    self.oponentGridButtons[x][y].configure(image=self.smallEmptyImg,state = 'enabled')
                elif Grid.oponentGrid[x][y] == 'M':
                    self.oponentGridButtons[x][y].configure(image=self.smallMissImg,state = 'disabled')
                elif Grid.oponentGrid[x][y] =='B':
                    self.oponentGridButtons[x][y].configure(image=self.smallEmptyImg,state='enabled')
            

    def disableAllPlayerButtons(self):
        for i in range (self.size):
            for j in range (self.size):
                self.playerGridButtons[i][j].configure(state='disabled')
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

        

        

        return

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
        MenuGUI.disableAllPlayerButtons(self)

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
        MenuGUI.disableAllPlayerButtons(self)
        MenuGUI.fileSaveButton.configure(state='enable')
        MenuGUI.fileOpenButton.configure(state='enable')




root = Tk()
menu_gui = MenuGUI(root)
root.mainloop()


