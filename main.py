#gui module
from tkinter import *
from tkinter import ttk
#alphabet module
import string 

class Grid():
    def make_grid(self,size):

        self.newGrid = []
        self.letters = string.ascii_uppercase #stores the letters of the alphabet in uppercase

        

        for i in range(0,size+1): #start loop for making table
            hold=[i]#create a holding column to be added to the array
            if i == 0: #create the first column for the letters
                for row in range (0,size): 
                    hold.append(self.letters[row]) #add the letters in turn to the holding list by selecting the 'row'th letter on the list
                self.newGrid.append(hold)#add the holding row of letters to the array
                
            else:
                hold=[i]
                for j in range (0,size): #remaining columns
                   hold.append(0) #make the remaining columns 0s
                self.newGrid.append(hold) #add the hold row to the array
                
                
                #after this process, we have a '2d' array of lists with the first
                #column consisting of letters A -J , the top row being numbers 1 - 10
                #this is for both boards, the one the player places their own ships on
                #and the one that they fire at
    def get_letters(self,a):
         return self.letters[a]
    
class MenuGUI(Frame):
    def __init__(self,root): 
        
        root.title("Battleships")#sets the title of the window    

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
        ttk.Button(self.mainMenuFrame,text="Load Game from file").grid(row=4,column=2,sticky=(W,E)) 

        #player number label new game
        ttk.Label(self.mainMenuFrame, text= "New Game:").grid(row=5,column=1,sticky=(W,E))

        #1 player  button ##add command##
        ttk.Button(self.mainMenuFrame,text="1 Player").grid(row=5,column=2,sticky=(W,E))        

        #2player  button ##add command##
        ttk.Button(self.mainMenuFrame,text="2 Player",command=self.twoPlayerBtn).grid(row=5,column=3,sticky=(W,E))      
       
        for child in self.mainMenuFrame.winfo_children():#adds padding
            child.grid_configure(padx=2, pady=5)

        #player and oponent board frame GUI elements (both)
        for i in range (2*(self.gridList.index(self.defListItem.get()))+4):
            for j in range (2*(self.gridList.index(self.defListItem.get()))+4):
                ttk.Button(self.oponentBoardFrame,width=3).grid(row=i,column=j)
                ttk.Button(self.playerBoardFrame,width=3).grid(row=i,column=j)

                #text=str(i)+','+str(j)

        #place ships buttons
        for i in range (5):
            ttk.Button(self.placeshipsFrame,text=str(i+1),width=3).grid(column=i,row=0)
        ttk.Button(self.placeshipsFrame,text="Rotate 90").grid(column=1,row=1,columnspan=3)

        #fire button
        ttk.Button(self.rightFrame,text="Fire!").grid(column=0,row=1)

    def updateGUI(self):
        self.size = (2*(self.gridList.index(self.defListItem.get()))+4)
        Grid.make_grid(self,self.size)

        #remove previous grid
        for child in self.oponentBoardFrame.winfo_children():
            child.destroy()
        for child in self.playerBoardFrame.winfo_children():
            child.destroy()

        #create new grid of size n
        for i in range (self.size):
            for j in range (self.size):
                ttk.Label(self.playerBoardFrame,text=Grid.get_letters(self,j)).grid(row=0,column=j+1)
                ttk.Label(self.oponentBoardFrame,text=Grid.get_letters(self,j)).grid(row=0,column=j+1)
                ttk.Label(self.playerBoardFrame,text=i+1).grid(row=i+1,column=0)
                ttk.Label(self.oponentBoardFrame,text=i+1).grid(row=i+1,column=0)
                ttk.Button(self.oponentBoardFrame,width=3).grid(row=i+1,column=j+1)
                ttk.Button(self.playerBoardFrame,width=3).grid(row=i+1,column=j+1)



    
    def twoPlayerBtn(self):
        self.updateGUI()
        Player.make_human()

        print("Player 2 Button Click. Grid size: " + str(self.size))





class Player():
    def make_human():
       return()

    def make_cpu():
        return()



root = Tk()
menu_gui = MenuGUI(root)
root.mainloop()

def main():
    return
