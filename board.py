def make_triangle(size,node): #Helperfunction
    lst = []
    for i in range(1,size+1):
            row = [node]*i
            lst.append(row)
    return lst

class  Board: 
   


    def __init__(self,type,size): 
        if (type == "t" and (size not in [4,5,6,7,8]) or type == "d" and (size not in [3,4,5,6]) ):
            return "wrong initialization" 
        node = 1
        
        if type == "t":
            self.board = make_triangle(size,node)
        
        elif type == "d":
            lst = make_triangle(size,node)
            lst.append(make_triangle(size,node)[:-1][::-1]) #trim of mid part and flip list on head
            self.board = lst


#t4 = Board("t",4)
#print(t4.board) 
#d5 = Board("d",5)
#print(d5.board)