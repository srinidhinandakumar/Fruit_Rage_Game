import math
import copy
import numpy as np
import time
inputpath="input.txt"
outputpath="output.txt"
INF=math.inf
n=0#board size between 1 to 26 inclusive
p=0#number of fruit varieties 0 to 9
time_remaining=0
matrix=None
choice=''
count=0
moveRowA=-1
moveColumnA=-1
moveRowB=-1
moveColumnB=-1
starc=0
list_traversed=[]
nodesTravel=0
safe_time_remaining=0  
scores=[]
column=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
#print matrix output
def print_solution(state=np.empty([n,n],dtype='<U1')):
        temp=""
        message=""
        for i in range(n):
            for j in range(n):
                temp+=str(state[i][j])
            if(i<n-1):
                temp+="\n"
        message+=temp
        #message=column[moveColumnA]+str(moveRowA+1)+"\n"+message
        #print(message)
        
#write output to file
def print_final_solution(state=np.empty([n,n],dtype='<U1')):
        temp=""
        message=""
        for i in range(n):
            for j in range(n):
                temp+=str(state[i][j])
            if(i<n-1):
                temp+="\n"
        message+=temp
        message=column[moveColumnA]+str(moveRowA+1)+"\n"+message
        #print(message)
        write_output(message) 
#read from file        
def readinputfile():
    global n
    global p
    global time_remaining
    global safe_time_remaining
    global matrix
    global starc
    starc=0
    file_object=open(inputpath,'r')
    lines=file_object.read()
    #print(lines)
    input_data=lines.split("\n")
    n=int(input_data[0])
    p=int(input_data[1])
    time_remaining=float(input_data[2])
    matrix = np.empty([n,n],dtype='<U1')
    safe_time_remaining=time_remaining-2
    for i in range(n):
        for j in range(n):
            matrix[i][j]=input_data[i+3][j]
            if(matrix[i][j]=="*"):
                starc+=1
            #print(input_data[i+3][j],end="")
        #print()
    #print_solution(matrix)
    return matrix
    file_object.close()
#write message to output file
def write_output(message):
    file_object=open(outputpath,'w')
    file_object.write(message)
    file_object.close()
#perform gravity operation on given matrix 
def gravity(state=np.empty([n,n],dtype='<U1')):
    col=0
    row=0
    row_index=0
    while col<n:
        first_empty_space_index=0
        empty_space_count=0
        first_empty_space=0
        row=row_index
        fruit_count_above=0
        while row<n:
            if(state[row][col]!='*'):
                fruit_count_above+=1
            if(state[row][col]!='*' and empty_space_count>0):
                row_index=row
                break
            if(state[row][col]=='*'):
                empty_space_count+=1
                if(first_empty_space==0):
                    first_empty_space_index=row
                    first_empty_space=1
            row+=1
        if(empty_space_count==0):
            #no empty spaces 
            row_index=0
            col+=1
        elif(empty_space_count>0 and fruit_count_above==0):
            #no fruits above to shift
            row_index=0
            col+=1
        else:
            #print("Empty space count %s First empty space index %s" %(empty_space_count,first_empty_space_index))
            k=first_empty_space_index+empty_space_count-1
            j=first_empty_space_index-1
            while k>=empty_space_count and j>=0:
                state[k][col]=state[j][col]
                k-=1
                j-=1
            while(k>=0):
                state[k][col]='*'
                k-=1
        #print_solution(state)
    return state
#check for terminal state   
def terminal_state(state):
    for i in range(n):
        if(state[n-1][i]!="*"):
            return False
        
    return True
#heuristic function to compute depth for traversal
def heuristic(number,state,stars):
    global choice
    global count
    boardsizeby2=(n**2)/2
    #print(stars)
    #print(boardsizeby2)
    if(time_remaining<1):
        depth=0
    else:
        if(number<10):
            depth=3
        elif(number<14):
            if(time_remaining<1):
                depth=0
            elif(time_remaining<5):
                depth=1
            elif(time_remaining<50):
                depth=2
            else:
                depth=3
        elif(number<20):
            if(time_remaining<1):
                depth=0
            elif(time_remaining<30 and stars<boardsizeby2):
                depth=1
            elif(time_remaining<30 and stars>=boardsizeby2):
                depth=2
            elif(time_remaining<60 and stars<boardsizeby2):
                depth=2
            else:
                depth=3
        elif(number<23):
            if(time_remaining<2):
                depth=0
            elif(time_remaining<50 and stars<boardsizeby2):
                depth=1
            else:
                depth=2
        elif(number<=26):
            if(time_remaining<20):
                depth=0
            elif(time_remaining<120 and stars<boardsizeby2):
                depth=1
            else:
                depth=2
        #calculate density of current state by calcultaing children
        temp_state=np.empty([n,n],dtype='<U1')
        np.copyto(temp_state,state) 
        children_all=[]
        for i in range(n):
            for j in range(n):
                #print("%s %s"%(i,j))
                if(temp_state[i][j] == '*'):
                    continue
                else:
                    choice = temp_state[i][j]
                    count=0
                    temp_state = makemove(i,j,temp_state)
                    #print("Printing makemove")
                    #print_solution(temp_state)
                    children_all.append([i,j,count])
        #children_all.sort(key=lambda x: int(x[2]), reverse=True)
        l=len(children_all)
        #print("Number of chilren: ",l)
        if(l<20):
            depth=3
    return depth
#alpha beta pruning technique applied to choose next move
def alphabeta(alpha,beta,star_count,cummulative_score,depth,player,state=np.empty([n,n],dtype='<U1')):
    global choice
    global count
    global moveRowA
    global moveColumnA
    global moveRowB
    global moveColumnB
    children=[]
    children_all=[]
    temp_state=np.empty([n,n],dtype='<U1')
    bestval=-INF
    val=-1
    #print(time.time()-start_time)
    if(time.time()-start_time>=(safe_time_remaining)):
     	return -1
    if(depth<0 or star_count==n**2):
    #if(depth<0 or terminal_state(state)):
        """terminal_state(state)==True"""
        #print("Depth reached of terminal state")
        #print("Depth:%s Score: %s"%(depth,cummulative_score))
        return cummulative_score
    #print("Current State:-")
    #print_solution(state)
    #generating all children of current state
    np.copyto(temp_state,state) 
    for i in range(n):
        for j in range(n):
            if(temp_state[i][j] == '*'):
                continue
            else:
                choice = temp_state[i][j]
                count=0
                temp_state = makemove(i,j,temp_state)
                children_all.append([i,j,count])
    #sort children in descending order
    children_all.sort(key=lambda x: int(x[2]), reverse=True)  
    l=len(children_all)#number of children
    #determine branching factor for states with board size greater than 15
    if(n>=23 and l>200):
        #print("Len ",l)
        k=int(np.ceil(0.4*l))
        #print("K: %s "%(k))
        children=children_all[0:k-1]
    elif(n>=20 and l>150):
        #print("Len ",l)
        k=int(np.ceil(0.5*l))
        #print("K: %s "%(k))
        children=children_all[0:k-1]
    elif(n>15 and l>100):
        #print("Len ",l)
        k=int(np.ceil(0.6*l))
        #print("K: %s "%(k))
        children=children_all[0:k-1]
    else:
        children=children_all
    #print("Children to this state: ",children)
    #print()
    cummulative_score_copy=cummulative_score
    if(player==1):#PlayerA
        #print("**Player A**")  
        bestVal=-INF
        for child in children:
            stars=star_count
            cummulative_score_copy=cummulative_score
            np.copyto(temp_state,state)
            #to get the fruit to choose
            row = child[0]
            col = child[1]
            choice = temp_state[row][col]
            count=0
            temp_state = gravity(makemove(row,col,temp_state))
            #print("A Successor state: \n")
            #print_solution(temp_state)
            cummulative_score_copy+=count**2
            stars+=count
            #print("A Cummulative score at %s %s is %s"%(row,col,cummulative_score_copy))
            val=alphabeta(alpha,beta,stars,cummulative_score_copy,depth-1,0,temp_state)
            if(val==-1):
                 return -1
            #print("A Value returned at %s %s is %s and alpha is %s"%(row,col,val,alpha))
            #print("A Move made from")
            #print("A Current state: \n")
            #print_solution(state)
            #print("A To")
            #print("A Successor state: \n")
            #print_solution(temp_state)
            #print("Star count after return from A val: %s Stars : %s"%(star_count,stars))
            if(val>bestVal):
                bestVal=val
                #moveRowA=row
                #moveColumnA=col
            if(bestVal>alpha):
                alpha=bestVal
                moveRowA=row
                moveColumnA=col
            if(beta<=alpha):
                #print("A Alpha %s moveRowA %s moveColA %s: "%(alpha,moveRowA,moveColumnA))
                #print("A Alpha cut off at %s %s"%(row,col))
                break
        #print("Just before return A alpha %s moveRowA %s moveColA %s: "%(alpha,moveRowA,moveColumnA))        
        return bestVal
    elif(player==0):#PlayerB
       #print("**Player B**")  
        bestVal=+INF
        for child in children:
            stars=star_count
            cummulative_score_copy=cummulative_score
            np.copyto(temp_state,state)
            row = child[0]
            col = child[1]
            choice = temp_state[row][col]
            count=0
            temp_state = gravity(makemove(row,col,temp_state))
            #print("B Successor state: \n")
            #print_solution(temp_state)
            cummulative_score_copy-=count**2
            stars+=count
            #print("B Cummulative score at %s %s is %s"%(row,col,cummulative_score_copy))
            val=alphabeta(alpha,beta,stars,cummulative_score_copy,depth-1,1,temp_state)
            if(val==-1):
                 return -1
            #print("B Value returned at %s %s is %s and beta is %s"%(row,col,val,beta))
            #print("B Move made from")
            #print("B Current state: \n")
            #print_solution(state)
            #print("B To")
            #print("B Successor state: \n")
            #print_solution(temp_state)
            #print("Star count after return from B val: %s Stars : %s"%(star_count,stars))
            if(val<bestVal):
                bestVal=val
                #moveRowB=row
                #moveColumnB=col
            if(bestVal<beta):
                beta=bestVal
                moveRowB=row
                moveColumnB=col
            if(alpha>=beta):
                #print("B beta %s moveRowB %s moveColB %s: "%(beta,moveRowB,moveColumnB))
                #print("B Alpha cut off at %s %s"%(row,col))
                break
        #print("Just before return B beta %s moveRowB %s moveColB %s: "%(beta,moveRowB,moveColumnB))    
        return bestVal
#make move on board for given row and column
def makemove(row,col,state=np.empty([n,n],dtype='<U1')):
    global choice
    global count
    global star_count
    if(row>=n or col>=n or row<0 or col<0):
        #print("Makemove return Row %s Col %s:"%(row,col))
        return state
    #print(int(state[row][col]))
    #print("Type Choice %s ,choice %s"%(type(choice),choice))
    #print("Type State %s val %s"%(type(state[row][col]),state[row][col]))
    if(state[row][col]==choice):
        #print("Chosen fruit in row %s col %s" %(row,col))
        state[row][col]='*'
        #print_solution(state)
        count+=1
        list_traversed.append([row,col])
        
        #print("Traverse down")
        np.copyto(state,makemove(row+1,col,state))
        #print("Traverse right")
        np.copyto(state,makemove(row,col+1,state))
        #print("Traverse up")
        np.copyto(state,makemove(row-1,col,state))
        #print("Traverse left")
        np.copyto(state,makemove(row,col-1,state))
    elif(state[row][col]=='*'):
        return state
    #print_solution(state)    
    return state
def random_play(state=np.empty([n,n],dtype='<U1')):
    global moveRowA
    global moveColumnA
    global choice
    children=[]
    children_all=[]
    temp_state=np.empty([n,n],dtype='<U1')
    np.copyto(temp_state,state) 
    for i in range(n):
        for j in range(n):
            #print("%s %s"%(i,j))
            if(temp_state[i][j] == '*'):
                continue
            else:
                choice = temp_state[i][j]
                count=0
                temp_state = makemove(i,j,temp_state)
                #print("Printing makemove")
                #print_solution(temp_state)
                children_all.append([i,j,count])
    #children_all.sort(key=lambda x: int(x[2]), reverse=True)  
    children_all.sort(key=lambda x: int(x[2]), reverse=True)  
    child=children_all[0]
    moveRowA=child[0]
    moveColumnA=child[1]
    return 0 
#play game
def gameplay(state=np.empty([n,n],dtype='<U1')):
    global valueA
    global valueB
    global moveRowA
    global moveColumnA
    global choice
    global nodesTravel
    alpha=-INF
    beta=INF
    valueA=0
    valueB=0
    if(time_remaining<0.1):#if very less time is left, randomly choose a child and return
            depth=0
            random_play(state)
    else:
        star_count=starc
        depth=heuristic(n,state,star_count)
        player=1#MY AGENT
        cummulative_score=0
        
        #depth=3
        #print("Depth: ",depth)
        alphabeta(alpha,beta,star_count,cummulative_score,depth,player,state)
    
    if(moveRowA==-1 or moveColumnA==-1):
          random_play(state)
    #print("Make the move: %s %s"%(moveRowA,moveColumnA))
    choice=state[moveRowA][moveColumnA]
    print_final_solution(gravity(makemove(moveRowA,moveColumnA,state)))
    #print("ValueA: %s ValueB: %s Path: %s" %(value[0],value[1],value[2]))
    #print("Value of A %s Value of B %s Node to be chosen %s %s"%(value[0],value[1],value[2]))
#final function to implement gameplay()
def fruitrage():
    global choice
    global moveRowA
    global moveColumnA
    global count
    state=readinputfile()
    gameplay(state)
        
#call fucntion and tract time taken
start_time=time.time()
#readinputfile()
#print_solution(matrix)
fruitrage()
end=time.time()
#print(end-start_time)