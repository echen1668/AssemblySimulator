import re
#Compare flag
flag = 0 #for cmp, jeq, and jnq. Value is obtained by subtracting the two inputed numbers in cmp. If flag is 0, jeq is true, else, jnq is true

#Line for file
line = None

#Registars
r1 = 0
r2 = 0
r3 = 0
r4 = 0
r5 = 0
lr = 0 #return address register
stack = [] #stack array
data = [] #array for data section
ip = 1 #instruction pointer

#Helper functions
def getBhelper(b): #derefernce [b]
    global stack
    global data
    for i in range(len(data)):
        if data[i][0] == b[1:len(b) - 1]: #finds b in section .data
            return data[i][1]
    if "sp" in b: #if b is a stack pointer
        sp = len(stack) - 1 #sp points at the rightmost side of the stack array
        pointer = sp - int(b[4]) #get index of stack
        return stack[pointer]

def convertstringtoint(a):
    global r1
    global r2
    global r3
    global r4
    global r5
    if a[1] == "r1":
        if isinstance(r1,str): #checks if r1 is a string before converting it to int
            r1 = int(r1)
        elif isinstance(r1,int): #if r1 is already an int, subtract 48 normally
            r1 -= 48
    elif a[1] == "r2":
        if isinstance(r2, str):
            r2 = int(r2)
        elif isinstance(r2, int):
            r2 -= 48
    elif a[1] == "r3":
        if isinstance(r3, str):
            r3 = int(r3)
        elif isinstance(r3, int):
            r3 -= 48
    elif a[1] == "r4":
        if isinstance(r4, str):
            r4 = int(r4)
        elif isinstance(r4, int):
            r4 -= 48
    elif a[1] == "r5":
        if isinstance(r5, str):
            r5 = int(r5)
        elif isinstance(r5, int):
            r5 -= 48
    else:
        if isinstance(a[1], str):
            a[1] = int(a[1])
        elif isinstance(a[1], int):
            a[1] -= 48

def convertinttostring(a):
    global r1
    global r2
    global r3
    global r4
    global r5
    if a[1] == "r1":
        if isinstance(r1,int): #check if registar or vaule is a int, if not, nothing happens
            r1 = str(r1)
    elif a[1] == "r2":
        if isinstance(r2, int):
            r2 = str(r2)
    elif a[1] == "r3":
        if isinstance(r3, int):
            r3 = str(r3)
    elif a[1] == "r4":
        if isinstance(r4, int):
            r4 = str(r4)
    elif a[1] == "r5":
        if isinstance(r5, int):
            r5 = str(r5)
    else:
        if isinstance(a[1], int):
            a[1] = str(a[1])


def helperB(b):
    if isinstance(b,int): #checks if b is a int number then returns it
        return b
    elif b.isnumeric(): #coverts b into a int number if it is a number but is a string
        b = int(b)
        return b
    else:
        return b #returns b if not number


def subhelperA(a,b):
    global r1
    global r2
    global r3
    global r4
    global r5
    if a[1] == "r1":
        r1 -= b
    elif a[1] == "r2":
        r2 -= b
    elif a[1] == "r3":
        r3 -= b
    elif a[1] == "r4":
        r4 -= b
    elif a[1] == "r5":
        r5 -= b
    else:
        if isinstance(a[1], int):  # checks if a is a int number, then subtracts
            a[1] -= b
        elif a[1].isnumeric():  # coverts string a into a int number, then subtracts
            a[1] = int(a[1])
            a[1] -= b



def addhelperA(a,b):
    global r1
    global r2
    global r3
    global r4
    global r5
    if a[1] == "r1":
        r1 += b
    elif a[1] == "r2":
        r2 += b
    elif a[1] == "r3":
        r3 += b
    elif a[1] == "r4":
        r4 += b
    elif a[1] == "r5":
        r5 += b
    else:
        if isinstance(a[1], int):  # checks if a is a int number, then adds
            a[1] += b
        elif a[1].isnumeric():  # coverts string a into a int number, then adds
            a[1] = int(a[1])
            a[1] += b

def runfunction():
    global line
    global ip
    count = ip
    while line[count] != "ret": #get all the lines between the label adn ret
        count += 1
    #Run each line in the function
    while ip < count:
        if line[ip] == 'syscall': #instruction syscall
            syscall()
        elif "sub" in line[ip]: #instruction sub a, b
            command = line[ip].split(',')
            sub(command[0], command[1])
        elif "add" in line[ip]: #instruction add a, b
            command = line[ip].split(',')
            add(command[0], command[1])
        elif "cmp" in line[ip]: #instruction cmp a, b
            command = line[ip].split(',')
            cmp(command[0], command[1])
        elif "jmp" in line[ip]: #instruction jmp
            command = line[ip].split(" ")
            ip = jmp(command[1])
        elif "jeq" in line[ip]: #instruction jeq
            command = line[ip].split(" ")
            ip = jeq(command[1])
        elif "jnq" in line[ip]: #instruction jnq
            command = line[ip].split(" ")
            ip = jnq(command[1])
        elif "call" in line[ip]: #instruction jnq
            command = line[ip].split(" ")
            ip = call(command[1])
        elif "mov" in line[ip]:
            command = line[ip].split(',')
            if '[' and ']' in command[1]: #instruction mov a,[b]
                movB(command[0], command[1])
            elif '[' and ']' in command[0]: #instruction mov [a],b
                movA(command[0], command[1])
            elif command[1] in ["r1","r2","r3","r4","r5"]: #instruction mov a,b
                mov(command[0],command[1])
            else:
                mov0000(command[0],command[1]) #instruction mov a,#0000
        ip += 1 #moves to the next line


# System calls
def syscall():
    global r1
    global r2
    global r3
    global r4
    global r5
    size = None
    if r1 == 0: #system write
        if r3 == None: #if r3 is None, default to 0
            size = 0
        elif isinstance(r3,int): #checks if r3 is a number then makes it the size of the input
            size = r3
        elif r3.isnumeric():
            size = int(r3)
        else: #if r3 is a variable, data .section is check to see what the variable is equal to
            for index3 in range(len(data)):
                if r3 == data[index3][0]:
                    size = int(data[index3][1])
        enterInput = input() #user input is entered
        for index1 in range(len(data)):
            if r2 in data[index1]: #move user input into variable
                data[index1][1] = enterInput[:size]
                return
    if r1 == 1: #system read
        if r3 == None: #if r3 is None, default to 0
            size = 0
        elif isinstance(r3,int): #checks if r3 is a number then makes it the size of the output
            size = r3
        elif r3.isnumeric():
            size = int(r3)
        else: #if r3 is a variable, data .section is check to see what the variable is equal to
            for index3 in range(len(data)):
                if r3 == data[index3][0]:
                    size = int(data[index3][1])
        if r2 == None: #if r3 is None, default to printing nothing
            print(end='')
            return
        for index2 in range(len(data)):  # if r2 is a variable, it find the variable in the data .section and prints its value
            if r2 == data[index2][0]:
                printOut = data[index2][1]
                if isinstance(printOut, int): #if output is an int, it prints nothing
                    print(end='')
                    return
                print(printOut[0:size],end='')
                return
        if isinstance(r2,int): #if r2 is an intenger, not a string, nothing is printed
            return
        printOut = r2
        print(printOut[0:size],end='')


#Instructions

#mov a, b
def mov(a,b):
    global r1
    global r2
    global r3
    global r4
    global r5
    if (b == "r1" or b == "r2" or b == "r3" or b == "r4" or b == "r5"): #get value from registar in b
        if b == "r1":
            b = r1
        if b == "r2":
            b = r2
        if b == "r3":
            b = r3
        if b == "r4":
            b = r4
        if b == "r5":
            b = r5
    if a == "mov r1": #assigns value of registar from b to register in a
        r1 = b
    if a == "mov r2":
        r2 = b
    if a == "mov r3":
        r3 = b
    if a == "mov r4":
        r4 = b
    if a == "mov r5":
        r5 = b

#mov a, #0000
def mov0000(a, b):
    global r1
    global r2
    global r3
    global r4
    global r5
    b = helperB(b) #gets vaule of b
    if a == "mov r1": #assigns value of b to register in a
        r1 = b
    if a == "mov r2":
        r2 = b
    if a == "mov r3":
        r3 = b
    if a == "mov r4":
        r4 = b
    if a == "mov r5":
        r5 = b

#mov a, [b]
def movB(a,b):
    global r1
    global r2
    global r3
    global r4
    global r5
    b = getBhelper(b) #derefences b
    if a == "mov r1": #find b in data .section and move its vaule into a
        r1 = b
    if a == "mov r2":
        r2 = b
    if a == "mov r3":
        r3 = b
    if a == "mov r4":
        r4 = b
    if a == "mov r5":
        r5 = b

#mov [a], b
def movA(a,b):
    global r1
    global r2
    global r3
    global r4
    global r5
    if (b == "r1" or b == "r2" or b == "r3" or b == "r4" or b == "r5"): #get value from registar in b
        if b == "r1":
            b = r1
        if b == "r2":
            b = r2
        if b == "r3":
            b = r3
        if b == "r4":
            b = r4
        if b == "r5":
            b = r5
    else: #if b is not a registar
        b = helperB(b)

    a = a.split(" ")
    a = a[1]
    for i in range(len(data)): #finds a in data .section and moves b into there
        if data[i][0] == a[1:len(a)-1]:
            data[i][1] = b

#add a, b
def add(a,b):
    global r1
    global r2
    global r3
    global r4
    global r5
    a = a.split(" ")
    if (b == "r1" or b == "r2" or b == "r3" or b == "r4" or b == "r5"): #get value from registar in b
        if b == "r1":
            b = r1
        if b == "r2":
            b = r2
        if b == "r3":
            b = r3
        if b == "r4":
            b = r4
        if b == "r5":
            b = r5
    else:
        b = helperB(b) #if b is not a registar checks if b is an int.
    if b == 48: #if 48, a is converted to a string
        convertinttostring(a)
    else:
        addhelperA(a,b)


#sub a, b
def sub(a,b):
    global r1
    global r2
    global r3
    global r4
    global r5
    a = a.split(" ")
    if (b == "r1" or b == "r2" or b == "r3" or b == "r4" or b == "r5"): #get value from registar in b
        if b == "r1":
            b = r1
        if b == "r2":
            b = r2
        if b == "r3":
            b = r3
        if b == "r4":
            b = r4
        if b == "r5":
            b = r5
    else:
        b = helperB(b) #if b is not a registar checks if b is an int.
    if b == 48: #if 48, a is converted to a int
        convertstringtoint(a)
    else:
        subhelperA(a, b)



def cmp(a,b):
    global r1
    global r2
    global r3
    global r4
    global r5
    global flag
    if (a == "cmp r1" or a == "cmp r2" or a == "cmp r3" or a == "cmp r4" or a == "cmp r5"): #get value from registar in a
        if a == "cmp r1":
            a = r1
        if a == "cmp r2":
            a = r2
        if a == "cmp r3":
            a = r3
        if a == "cmp r4":
            a = r4
        if a == "cmp r5":
            a = r5
    else:
        a = a.split(" ") #if a is a pure number, get the number from string "cmp x"
        a = a[1]
    if (b == "r1" or b == "r2" or b == "r3" or b == "r4" or b == "r5"): #get value from registar in b
        if b == "r1":
            b = r1
        if b == "r2":
            b = r2
        if b == "r3":
            b = r3
        if b == "r4":
            b = r4
        if b == "r5":
            b = r5
    num1 = None #defualt values
    num2 = None
    if isinstance(a, int): #check is a and b are int, convert to int if numbers but strings
        num1 = a
    elif a.isnumeric():
        num1 = int(a)
    if isinstance(b, int):
        num2 = b
    elif b.isnumeric():
        num2 = int(b)
    flag = num1 #flag = a - b
    flag -= num2

#jmp label
def jmp(label):
    global line
    global ip
    lr = ip #return address registar holds the original instruction pointer
    for index in range(0,len(line)): #finds label in section .txt and makes return address register = the new intrustion pointer
        if line[index][0:len(line[index])-1] == label:
            lr = index
    return lr


# jeq label
def jeq(label):
    global line
    global ip
    global flag
    lr = ip
    if flag == 0: #jumps if the compare of two numbers is equal (flag = 0)
        for index in range(0,len(line)):
            if line[index][0:len(line[index])-1] == label:
                lr = index
    return lr

# jnq label
def jnq(label):
    global line
    global ip
    global flag
    lr = ip
    if flag != 0: #jumps if the compare of two numbers are not equal (flag != 0)
        for index in range(0,len(line)):
            if line[index][0:len(line[index])-1] == label:
                lr = index
    return lr

#call label
def call(label):
    global ip
    global r1
    global r2
    global r3
    global r4
    global r5
    global flag
    global stack
    lr = ip #make return address the orginal instruction pointer
    stack.append(r5)  # push registar into stack
    stack.append(r4)  # push registar into stack
    stack.append(r3) # push registar into stack
    stack.append(r2)  # push registar into stack
    stack.append(r1)  # push registar into stack
    ip = jmp(label) #make new instruction pointer location of label/function
    runfunction() #runs the label/function
    r1 = stack.pop() #pops the orginal registars back in
    r2 = stack.pop()
    r3 = stack.pop()
    r4 = stack.pop()
    r5 = stack.pop()
    stack = [] #clears stack
    return lr

if __name__ == "__main__":
    isData = 0
    fileName = input("Enter file name ")
    with open(fileName) as f:
        line = f.read().splitlines()
    #Get Data from Section.Data
    for i in line:
        if i[0:2] == "DW": #Get string message
            value = ""
            lineDW = i.split(" ")
            lineDW2 = i.split('"')
            if "\\n" in lineDW2[1]:  #Takes account for the new line symbol
                lineDW2[1] = lineDW2[1].replace("\\n",'\n') #Replace all occurence of string \n with actual \n (newline symbol)
            elif "\\n" == lineDW2[1]: #Takes account for the new line symbol being by itself
                lineDW2[1] = '\n'
            data.append([lineDW[1], lineDW2[1]])

        if i[0:2] == "DD": #Get string size
            value = 0
            lineDD = i.split(" ")
            lenMessage = lineDD[2]
            for k in range(0,len(data)):
                if data[k][0] in lenMessage:
                    value = len(data[k][1])
            data.append([lineDD[1],value])

        if i[0:4] == "resb": #Get resb variable
            value = 0
            lineResb = i.split(" ")
            value = lineResb[2]
            data.append([lineResb[1],value])
    count = len(line) #get the number of lines in the file
    for index in range(0, len(line)): #set instruction pointer to begining of section text
        if line[index] == "Section .Text":
            ip = index
    #Run each line in Section .Text
    while ip < count:
        if line[ip] == 'syscall': #instruction syscall
            syscall()
        elif "sub" in line[ip]: #instruction sub a, b
            command = line[ip].split(',')
            sub(command[0], command[1])
        elif "add" in line[ip]: #instruction add a, b
            command = line[ip].split(',')
            add(command[0], command[1])
        elif "cmp" in line[ip]: #instruction cmp a, b
            command = line[ip].split(',')
            cmp(command[0], command[1])
        elif "jmp" in line[ip]: #instruction jmp
            command = line[ip].split(" ")
            ip = jmp(command[1])
        elif "jeq" in line[ip]: #instruction jeq
            command = line[ip].split(" ")
            ip = jeq(command[1])
        elif "jnq" in line[ip]: #instruction jnq
            command = line[ip].split(" ")
            ip = jnq(command[1])
        elif "call" in line[ip]: #instruction jnq
            command = line[ip].split(" ")
            ip = call(command[1])
        elif "mov" in line[ip]:
            command = line[ip].split(',')
            if '[' and ']' in command[1]: #instruction mov a,[b]
                movB(command[0], command[1])
            elif '[' and ']' in command[0]: #instruction mov [a],b
                movA(command[0], command[1])
            elif command[1] in ["r1","r2","r3","r4","r5"]: #instruction mov a,b
                mov(command[0],command[1])
            else:
                mov0000(command[0],command[1]) #instruction mov a,#0000
        ip += 1 #moves to the next line