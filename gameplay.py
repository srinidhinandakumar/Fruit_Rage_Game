import numpy as np
import datetime
import time
import minimax_agent
import homework3
#import homework
import random_agent
inputpath="input.txt"
outputpath="output.txt"

total_star_count=0
n=0
p=0
time_remaining_alphabeta=float(300)
time_remaining_alphabetaB=float(300)
time_remaining_random=float(300)
time_remaining_minimax=float(300)
score_alphabeta=0
score_alphabetaB=0
score_random=0
score_minimax=0
flag=0
flagAR=0 
flagAM=0
flagAB=0
def calculate_stars():
        starc=0
        matrix=None
        file_object1=open(outputpath,'r')
        lines=file_object1.read()
        input_data=lines.split("\n")
        #movemade=input_data[0]
        number=int(n)
        matrix = np.empty([number,number],dtype='<U1')
        for i in range(number):
            for j in range(number):
                matrix[i][j]=input_data[i+1][j]
                if(matrix[i][j]=="*"):
                    starc+=1
        return starc
def print_solution(state=np.empty([n,n],dtype='<U1')):
        temp=""
        message=""
        number=int(n)
        for i in range(number):
            for j in range(number):
                temp+=str(state[i][j])
            if(i<number-1):
                temp+="\n"
        message+=temp
        #message=column[moveColumnA]+str(moveRowA+1)+"\n"+message
        #print(message)
        return message
        #write_output(message) 
        
def write_output(message):
    file_object=open(outputpath,'w')
    file_object.write(message)
    file_object.close()


def run_random_agent():
    global n
    global p
    global time_remaining_random
    global total_star_count
    global score_random
    message=""
    starc=0
    matrix=None
    n=int(n)
    print("Total stars: ",total_star_count)
    #read from output written by alphabeta agent
    file_object1=open(outputpath,'r')
    lines=file_object1.read()
    input_data=lines.split("\n")
    #movemade=input_data[0]
    matrix = np.empty([n,n],dtype='<U1')
    for i in range(n):
        for j in range(n):
            matrix[i][j]=input_data[i+1][j]
            #if(matrix[i][j]=="*"):
                #starc+=1
            #print(input_data[i+3][j],end="")
        #print()
    #print_solution(matrix)
    #write to input file for random agent to read from
    file_object2=open(inputpath,"w")
    message1=str(n)+"\n"+str(p)+"\n"+str(time_remaining_random)+"\n"
    message2=print_solution(matrix)
    file_object2.write(message1+message2)
    #return matrix
    file_object1.close()
    file_object2.close()
    
    #run random agent
    start=datetime.datetime.now()
    #exec('python3 random_agent.py')
    random_agent.fruitrage()
    end=datetime.datetime.now()
    delta=end-start
    combined=float(delta.total_seconds())
    time_remaining_random=float(time_remaining_random)-combined
    
    starc=calculate_stars()
    score_random+=(int(starc)-int(total_star_count))**2
    print("Random agent score: ",score_random)
    total_star_count=starc
    
def run_minimax_agent():
    global n
    global p
    global time_remaining_minimax
    global total_star_count
    global score_minimax
    starc=0
    message=""
    matrix=None
    number=int(n)
    #read from output written by alphabeta agent
    file_object1=open(outputpath,'r')
    lines=file_object1.read()
    input_data=lines.split("\n")
    #movemade=input_data[0]
    matrix = np.empty([number,number],dtype='<U1')
    for i in range(number):
        for j in range(number):
            matrix[i][j]=input_data[i+1][j]
            #if(matrix[i][j]=="*"):
                #starc+=1
            #print(input_data[i+3][j],end="")
        #print()
    #print_solution(matrix)
    #write to input file for random agent to read from
    file_object2=open(inputpath,"w")
    message1=str(n)+"\n"+str(p)+"\n"+str(time_remaining_minimax)+"\n"
    message2=print_solution(matrix)
    file_object2.write(message1+message2)
    #return matrix
    file_object1.close()
    file_object2.close()
    
    #run random agent
    start=datetime.datetime.now()
    #exec('python3 inimax_agent.py')
    minimax_agent.fruitrage()
    end=datetime.datetime.now()
    delta=end-start
    combined=float(delta.total_seconds())
    time_remaining_minimax=float(time_remaining_minimax)-combined
    
    starc=calculate_stars()
    score_minimax+=(int(starc)-int(total_star_count))**2
    print("Minimax agent score: ",score_minimax)
    total_star_count=starc 

def run_alphabeta_agent():
    global n
    global p
    global time_remaining_alphabeta
    global total_star_count
    global score_alphabeta
    starc=0
    message=""
    #read from output written by alphabeta agent
    global flag
    if(flag==0):
        file_object=open(inputpath,'r')
        lines=file_object.read()
        input_data=lines.split("\n")
        n=input_data[0]
        p=input_data[1]
        time_remaining_alphabeta=input_data[2]
        file_object.close()
    elif(flag==1):
        file_object1=open(outputpath,'r')
        lines=file_object1.read()
        input_data=lines.split("\n")
        #movemade=input_data[0]
        number=int(n)
        matrix = np.empty([number,number],dtype='<U1')
        for i in range(number):
            for j in range(number):
                matrix[i][j]=input_data[i+1][j]
                #if(matrix[i][j]=="*"):
                 #   starc+=1
                #print(input_data[i+3][j],end="")
            #print()
        #print_solution(matrix)
        #write to input file for random agent to read from
        file_object2=open(inputpath,"w")
        message1=str(number)+"\n"+str(p)+"\n"+str(time_remaining_alphabeta)+"\n"
        message2=print_solution(matrix)
        file_object2.write(message1+message2)
        #return matrix
        file_object1.close()
        file_object2.close()
    
    #run alphabeta agent
    start=datetime.datetime.now()
    #print(start)
    #exec('python3 alphabeta_agent.py')
    homework3.fruitrage()
    end=datetime.datetime.now()
    delta=end-start
    combined=float(delta.total_seconds())
    time_remaining_alphabeta=float(time_remaining_alphabeta)-combined
    starc=calculate_stars()
    #print(np.dtype(starc)+" "+np.dtype(total_star_count)+" "+np.dtype(score_alphabeta))
    score_alphabeta+=(int(starc)-int(total_star_count))**2
    print("AlphaBeta agent score: ",score_alphabeta)
    total_star_count=starc
    print("Total stars: ",total_star_count)
    if(flag==0):
        flag=1
def run_alphabetaB_agent():
    global n
    global p
    global time_remaining_alphabetaB
    global total_star_count
    global score_alphabetaB
    matrix=None
    starc=0
    message=""
    #read from output written by alphabeta agent
    global flag
    if(flag==0):
        file_object=open(inputpath,'r')
        lines=file_object.read()
        input_data=lines.split("\n")
        n=input_data[0]
        p=input_data[1]
        time_remaining_alphabetaB=input_data[2]
        file_object.close()
    elif(flag==1):
        file_object1=open(outputpath,'r')
        lines=file_object1.read()
        input_data=lines.split("\n")
        #movemade=input_data[0]
        number=int(n)
        matrix = np.empty([number,number],dtype='<U1')
        for i in range(number):
            for j in range(number):
                matrix[i][j]=input_data[i+1][j]
                #if(matrix[i][j]=="*"):
                 #   starc+=1
                #print(input_data[i+3][j],end="")
            #print()
        #print_solution(matrix)
        #write to input file for random agent to read from
        file_object2=open(inputpath,"w")
        message1=str(number)+"\n"+str(p)+"\n"+str(time_remaining_alphabetaB)+"\n"
        message2=print_solution(matrix)
        file_object2.write(message1+message2)
        #return matrix
        file_object1.close()
        file_object2.close()
    
    #run alphabeta agent
    start=datetime.datetime.now()
    #print(start)
    #exec('python3 alphabeta_agent.py')
    homework3.fruitrage()
    end=datetime.datetime.now()
    delta=end-start
    combined=float(delta.total_seconds())
    time_remaining_alphabetaB=float(time_remaining_alphabetaB)-combined
    starc=calculate_stars()
    #print(np.dtype(starc)+" "+np.dtype(total_star_count)+" "+np.dtype(score_alphabeta))
    score_alphabetaB+=(int(starc)-int(total_star_count))**2
    print("AlphaBeta B agent score: ",score_alphabetaB)
    total_star_count=starc
    print("Total stars: ",total_star_count)
    total_star_count=starc
    if(flag==0):
        flag=1
      
def alphabetaVSminimax(agent):
    global flagAM
    print("total stars: %s flagAM: %s"%(total_star_count,flagAM))
    if(total_star_count>=int(n)**2 and flagAM==1):
        print("Score AlphaBeta: %s Score Minimax: %s "%(score_alphabeta,score_minimax))
        if(score_alphabeta>score_minimax):
            print("AlphaBeta agent wins!")
            return True
        elif(score_alphabeta<score_minimax):
            print("Minimax agent wins!")
            return True
        else:
            print("It's a tie!")
            return True
    elif(time_remaining_alphabeta<=0):
        print("AlphaBeta agent loses. Time limit reached.")
        return False
    elif(time_remaining_minimax<=0):
        print("Minimax agent loses. Time limit reached.")
        return False
    else:
        
        if(agent=="A"):
            print("********Running Alphabeta agent********")        
            run_alphabeta_agent()
            time.sleep(5)
            flagAM=1
            val=alphabetaVSminimax("M")
        else:
            print("********Running Minimax agent********")         
            run_minimax_agent()
            time.sleep(5)
            #flagAR=1
            val=alphabetaVSminimax("A")
    
    return True

def alphabetaVSrandom(agent):
    global flagAR
    if(total_star_count==int(n)**2 and flagAR==1):
        print("Score AlphaBeta: %s Score Random: %s "%(score_alphabeta,score_random))
        if(score_alphabeta>score_random):
            print("AlphaBeta agent wins!")
            return True
        elif(score_alphabeta<score_random):
            print("Random agent wins!")
            return True
        else:
            print("It's a tie!")
            return True
    elif(time_remaining_alphabeta<=0):
        print("AlphaBeta agent loses. Time limit reached.")
        return False
    elif(time_remaining_random<=0):
        print("Random agent loses. Time limit reached.")
        return False
    else:
        
        if(agent=="A"):
            print("********Running Alphabeta agent********")
            run_alphabeta_agent()
            time.sleep(5)
            flagAR=1
            val=alphabetaVSrandom("R")
            
        else:
            print("********Running Random agent********")
            run_random_agent()
            time.sleep(5)
            val=alphabetaVSrandom("A")
    
    return True

def alphabetaVSalphabeta(agent):
    global flagAB
    print("total stars: %s flagAB: %s"%(total_star_count,flagAB))
    if(total_star_count>=int(n)**2 and flagAB==1):
        print("Score AlphaBetaA : %s Score AlphaBetaB: %s "%(score_alphabeta,score_alphabetaB))
        if(score_alphabeta>score_alphabetaB):
            print("AlphaBeta A agent wins!")
            return True
        elif(score_alphabeta<score_alphabetaB):
            print("Alphabeta B agent wins!")
            return True
        else:
            print("It's a tie!")
            return True
    elif(time_remaining_alphabeta<=0):
        print("AlphaBeta A agent loses. Time limit reached.")
        return False
    elif(time_remaining_alphabetaB<=0):
        print("AlphaBeta B agent loses. Time limit reached.")
        return False
    else:
        
        if(agent=="A"):
            print("********Running Alphabeta A agent********")
            print("Time Agent A: ",time_remaining_alphabeta)
            run_alphabeta_agent()
            time.sleep(5)
            flagAB=1
            val=alphabetaVSalphabeta("B")
        else:
            print("********Running Alphabeta B agent********") 
            print("Time Agent B: ",time_remaining_alphabetaB)
            run_alphabetaB_agent()
            time.sleep(5)
            #flagAR=1
            val=alphabetaVSalphabeta("A")
    
    return True
   

#alphabetaVSrandom("A")        
#alphabetaVSminimax("A")
print("**********Game Play**************")
alphabetaVSalphabeta("A")        