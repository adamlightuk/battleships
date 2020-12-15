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
    
class MenuGUI(Frame):
    def __init__(self,root): 
        
        root.title("Battleships")    
        
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)	

        #setup for dropdown list
        self.gridList = ['6x6','8x8','10x10','12x12','14x14','16x16']
        self.defListItem = StringVar(root)
        self.defListItem.set(self.gridList[2]) #default value
    
        #gui elements

        #image
        ##insert image code here##

        #name label
        self.nameLbl = ttk.Label(mainframe, text= "Battelships!").grid(row=2,column=2,sticky=(W,E))        

        #dropdown description label
        self.dropDownLbl = ttk.Label(mainframe, text= "Grid Size:").grid(row=3,column=1,sticky=(W,E))

        #dropdown grid size selection
        self.gridDropDown = ttk.OptionMenu(mainframe,self.defListItem,*self.gridList).grid(row=3,column=2,sticky=(W,E))

        #load game button ##add command##
        self.loadGameBtn = ttk.Button(mainframe,text="Load Game").grid(row=4,column=2,sticky=(W,E)) 

        #player number label new game
        self.newGameLbl = ttk.Label(mainframe, text= "New Game:").grid(row=5,column=1,sticky=(W,E))

        #1 player  button ##add command##
        self.onePlayBtn = ttk.Button(mainframe,text="1 Player").grid(row=5,column=2,sticky=(W,E))        

        #2player  button ##add command##
        self.twoPlayBtn = ttk.Button(mainframe,text="2 Player").grid(row=5,column=3,sticky=(W,E))      
       
        for child in mainframe.winfo_children():
            child.grid_configure(padx=2, pady=5)

class PlaceShips(Frame):
    def __init__(self,root):
        Frame.__init__(self,root)
        self.root = root
        root.title("Place Ships")

        self.pageNameLbl = ttk.Label(root,text="Place Ships")
        self.submitBtn = ttk.Button(root,text="Submit")
        self.pageNameLbl.pack()

root = Tk()
menu_gui = MenuGUI(root)
root.mainloop()

    
class Main():

    def __init__(self):
        return
