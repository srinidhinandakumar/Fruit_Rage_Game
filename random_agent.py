import math
import copy
import numpy as np
import time
from operator import itemgetter, attrgetter, methodcaller
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
    
scores=[]
column=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

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
        print(message)
        #write_output(message) 
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
        print(message)
        write_output(message) 
        
def readinputfile():
    global n
    global p
    global time_remaining
    global matrix
    global starc
    matrix=None
    file_object=open(inputpath,'r')
    lines=file_object.read()
    input_data=lines.split("\n")
    n=int(input_data[0])
    p=int(input_data[1])
    time_remaining=float(input_data[2])
    matrix = np.empty([n,n],dtype='<U1')
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

def write_output(message):
    file_object=open(outputpath,'w')
    file_object.write(message)
    file_object.close()

def gravity(state=np.empty([n,n],dtype='<U1')):
    col=0
    row=0
    row_index=0
    
    while col<n:
        
        #print()
        first_empty_space_index=0
        empty_space_count=0
        first_empty_space=0
        row=row_index
        fruit_count_above=0
        while row<n:
            #print("Col %s Row %s Value %s" %(col,row,state[row][col]))
            #print("Value: ",state[row][col])
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
    """Changed"""
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
    i=np.random.randint(0,l)
    child=children_all[i]
    moveRowA=child[0]
    moveColumnA=child[1]
    return 0

def makemove(row,col,state=np.empty([n,n],dtype='<U1')):
    global choice
    global count
    global star_count
    if(row>=n or col>=n or row<0 or col<0):
        return state
    #make move applies chosen move to state
    #print(int(state[row][col]))
    #print("Type Choice %s ,choice %s"%(type(choice),choice))
    #print("Type State %s val %s"%(type(state[row][col]),state[row][col]))
    
    if(state[row][col]==choice):
        #print("Chosen fruit in row %s col %s" %(row,col))
        state[row][col]='*'
        #print_solution(state)
        count+=1
        #star_count+=1
        list_traversed.append([row,col])
        #print("Traverse down")
        np.copyto(state,makemove(row+1,col,state))
        """Changed"""
        #state=copy.deepcopy(makemove(row+1,col,state))#traverse down
        #print("After traverse down")
        #print_solution(state)
        #print("Traverse right")
        np.copyto(state,makemove(row,col+1,state))
        """Changed"""
        #state=copy.deepcopy(makemove(row,col+1,state))#traverse right
        #print("After traverse right")
        #print_solution(state)
        #print("Traverse up")
        np.copyto(state,makemove(row-1,col,state))
        """Changed"""
        #state=copy.deepcopy(makemove(row-1,col,state))#traverse up
        #print("After traverse up")
        #print_solution(state)
        #print("Traverse left")
        np.copyto(state,makemove(row,col-1,state))
        """Changed"""
        #state=copy.deepcopy(makemove(row,col-1,state))#traverse left
        #print("After traverse left")
        #print_solution(state)
        #state=copy.copy(state)
    elif(state[row][col]=='*'):
        return state
    #print_solution(state)    
    return state
def gameplay(state=np.empty([n,n],dtype='<U1')):
    global moveRowA
    global moveColumnA
    global choice
    random_play(state)
    print("Make the move: %s %s"%(moveRowA,moveColumnA))
    choice=state[moveRowA][moveColumnA]
    print_final_solution(gravity(makemove(moveRowA,moveColumnA,state)))
    
def fruitrage():
    state=readinputfile()
    gameplay(state)
        
"""
start=time.time()
fruitrage()
end=time.time()
print(end-start)
"""