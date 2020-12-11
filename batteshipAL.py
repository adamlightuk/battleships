import random


class main():

    def __init__(self):

        self.primaryGridP1 = []
        self.trackingGridP1 = []

        self.primaryGridP2 = []
        self.trackingGridP2 = []

        for i in range(0,11): #start loop for making table
            hold=[i]#create a holding column to be added to the array
            if i == 0: #create the first column for the letters
                for row in 'ABCDEFGHIJ' : 
                    hold.append(row) #add the letters in turn to the holding list
                self.primaryGridP1.append(hold)#add the holding row of letters to the array
                self.trackingGridP2.append(hold)#the same for the tracking grid
                self.primaryGridP2.append(hold)
                self.trackingGridP2.append(hold)
            else:
                hold=[i]
                for j in range (0,10): #remaining columns
                   hold.append(0) #make the remaining columns 0s
                self.primaryGridP1.append(hold) #add the hold row to the array
                self.trackingGridP1.append(hold) #same for tracking grid
                self.primaryGridP2.append(hold)
                self.trackingGridP2.append(hold)
                
                #after this process, we have a '2d' array of lists with the first
                #column consisting of letters A -J , the top row being numbers 1 - 10
                #this is for both boards, the one the player places their own ships on
                #and the one that they fire at


        

                
                
                            
                
                    
                    
                
            
