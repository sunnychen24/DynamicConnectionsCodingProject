#Sunny Chen
import math

#
#assumptions made: stackable pallets can be stacked across the top of multiple bottom pallets, regardless of varying height
#

def optimalLinearFootage(pallets, trailerwidth, trailerheight):

    #recursive function to calculate minimum linear footage given unstackable pallets
    def unstackableFootage(unstackablepallets, currentwidth, currentfootage):

        #base case, one pallet left
        if len(unstackablepallets) == 1:

            #if last pallet is able to be fit into remaining width, only increase linear footage if currently less than half trailer width is taken up, otherwise increase linear footage by length in ft /2
            if unstackablepallets[0].width <= trailerwidth-currentwidth:
                if currentwidth > trailerwidth/2:
                    return currentfootage + max(0, (unstackablepallets[0].length/12 - currentfootage)/2)
                else: return currentfootage + unstackablepallets[0].length/12/2

            #placing last pallet in new row, increase linear footage by half if it takes up less than half trailer width, otherwise increase by length in feet
            else:
                if unstackablepallets[0].width <= trailerwidth/2:
                    return currentfootage + unstackablepallets[0].length/12/2
                else: return currentfootage + unstackablepallets[0].length/12

        #create a list to assign each pallet the new linear footage amount if it were to be added
        newfootages = [0]*len(unstackablepallets)
        for i in range(0,len(unstackablepallets)):

            #if pallet is able to be fit into remaining width, only increase linear footage if currently less than half trailer width is taken up, otherwise increase linear footage by length in ft /2
            if unstackablepallets[i].width <= trailerwidth-currentwidth:
                if currentwidth > trailerwidth/2:
                    newfootages[i] = currentfootage + max(0, (unstackablepallets[i].length/12 - currentfootage)/2)
                else: newfootages[i] = currentfootage + unstackablepallets[i].length/12/2

            #placing pallet in new row, increase linear footage by half if it takes up less than half trailer width, otherwise increase by length in feet
            else:
                if unstackablepallets[i].width <= trailerwidth/2:
                    newfootages[i] = currentfootage + unstackablepallets[i].length/12/2
                else: newfootages[i] = currentfootage + unstackablepallets[i].length/12

        #find the index of the pallet to be used that will increase the linear footage by the least amount
        minIncreaseindex = newfootages.index(min(newfootages))

        #update the variable to track width taken up after most recent pallet addition
        if (currentwidth + unstackablepallets[minIncreaseindex].width) <= trailerwidth:
            currentwidth = currentwidth + unstackablepallets[minIncreaseindex].width
        else:
            currentwidth = unstackablepallets[minIncreaseindex].width

        #remove chosen pallet from future considerations
        unstackablepallets.pop(minIncreaseindex)

        #recursively call the function again with updated pallet list, working width, and current linear footage
        return unstackableFootage(unstackablepallets, currentwidth, newfootages[minIncreaseindex])


    #recursive function to calculate minimum linear footage given stackable pallets
    def stackableFootage(stackablepallets, currentwidth, currentfootage, currentheight, stackablelength, stackablewidth):

        #base, one pallet left
        if len(stackablepallets) == 1:

            #if last pallet is able to be stacked, do not increase linear footage
            if stackablelength >= stackablepallets[0].length and stackablewidth >= stackablepallets[0].width and trailerheight >= stackablepallets[0].height + currentheight:
                return currentfootage

            #if last pallet is able to be fit into remaining width, only increase linear footage if currently less than half trailer width is taken up, otherwise increase linear footage by length in ft /2
            if stackablepallets[0].width <= trailerwidth-currentwidth:
                if currentwidth > trailerwidth/2:
                    return currentfootage + max(0, (stackablepallets[0].length/12 - currentfootage)/2)
                else: return currentfootage + stackablepallets[0].length/12/2
            
            #placing last pallet in new row, increase linear footage by half if it takes up less than half trailer width, otherwise increase by length in feet
            else:
                if stackablepallets[0].width <= trailerwidth/2:
                    return currentfootage + stackablepallets[0].length/12/2
                else: return currentfootage + stackablepallets[0].length/12
            
        #create a list to assign each pallet the new linear footage amount if it were to be added
        newfootages = [0]*len(stackablepallets)
        stacked = False

        for i in range(0,len(stackablepallets)):
            #if pallet is able to be stacked, do not increase linear footage
            if stackablelength >= stackablepallets[0].length and stackablewidth >= stackablepallets[0].width and trailerheight >= stackablepallets[0].height + currentheight:
                newfootages[i] = currentfootage
                stacked = True

            #if pallet is able to be fit into remaining width, only increase linear footage if currently less than half trailer width is taken up, otherwise increase linear footage by length in ft /2
            elif stackablepallets[i].width <= trailerwidth-currentwidth:
                if currentwidth > trailerwidth/2:
                    newfootages[i] = currentfootage + max(0, (stackablepallets[i].length/12 - currentfootage)/2)
                else: newfootages[i] = currentfootage + stackablepallets[i].length/12/2

            #placing pallet in new row, increase linear footage by half if it takes up less than half trailer width, otherwise increase by length in feet
            else:
                if stackablepallets[i].width <= trailerwidth/2:
                    newfootages[i] = currentfootage + stackablepallets[i].length/12/2
                else: newfootages[i] = currentfootage + stackablepallets[i].length/12

        #find the index of the pallet to be used that will increase the linear footage by the least amount
        minIncreaseindex = newfootages.index(min(newfootages))

        #update the variables to track remaining stackable area if stacked
        if stacked:
            stackablelength -= stackablepallets[minIncreaseindex].length
            stackablewidth -= stackablepallets[minIncreaseindex].width
            currentheight += stackablepallets[minIncreaseindex].height

        #update the variable to track width taken up and new stackable area after most recent floor pallet addition
        else:
            if (currentwidth + stackablepallets[minIncreaseindex].width) <= trailerwidth:
                currentwidth = currentwidth + stackablepallets[minIncreaseindex].width
            else:
                currentwidth = stackablepallets[minIncreaseindex].width
            stackablelength += stackablepallets[minIncreaseindex].length
            stackablewidth = stackablepallets[minIncreaseindex].width
            currentheight = stackablepallets[minIncreaseindex].height

        #remove chosen pallet from future considerations
        stackablepallets.pop(minIncreaseindex)
            
        #recursively call the function again with updated pallet list, working width, current linear footage, and stackable area remaining
        return stackableFootage(stackablepallets, currentwidth, newfootages[minIncreaseindex], currentheight, stackablelength, stackablewidth)


    #split list of pallets into stackable and unstackable
    stackable = []
    unstackable = []
    for pallet in pallets:
        if pallet.stackable:
            stackable.append(pallet)
        else:
            unstackable.append(pallet)

    #add linear footage for both pallet types together and round to next whole number
    return math.ciel(unstackableFootage(unstackable, 0, 0) + stackableFootage(stackable, 0, 0, 0, 0, 0)) 