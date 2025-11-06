import random #to generate random numbers and make choices

def randomInt(level):
    if level == "Easy":
        return random.randint(1, 9), random.randint(1,9) #generates two numbers between 1 and 9
    elif level == "Moderate":
        return random.randint(10, 99), random.randint(10,99) #generates two numbers between 10 and 99
    else: #for advanced
        return random.randint(1000, 9999), random.randint(1000,9999)  #generates two numbers between 1000 and 9999
    
def decideOperation():
    return random.choice(['+', '-']) #randomly chooses a math operation

def isCorrect(answer, num1, num2, operation): #to check if the players answer is correct
    if operation == '+':
        return answer == num1 + num2 #return True if the answer they gave matches sum, else False
    return answer == num1 - num2 #otherwise if the operation is subtraction return True 