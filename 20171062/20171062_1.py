import sys
import os
from collections import OrderedDict

# Global Initializations
answer = ""
database = OrderedDict()
memory = OrderedDict()
registers = {}
id_command = {}
transaction_ids = []

def init_value(line):
    ''' Initialize value in database'''
    line = line.split()
    for i in range(0, len(line), 2):
        database[line[i].strip()] = int(line[i+1].strip())
    
def read(path):
    ''' Read contents of file'''
    num = 0
    transaction_id = None
    flag = False
    with open(path,'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not flag:
                init_value(line)
                flag = True
                continue
            if line == "":
                continue
            if num:
                id_command[transaction_id].append(line)
                num-=1
            else:
                transaction_id, num = line.split()
                transaction_id = transaction_id.strip()
                num  = int(num.strip())
                if transaction_id in id_command:
                    sys.exit("Repeated Transaction")
                else:
                    transaction_ids.append(transaction_id)
                    id_command[transaction_id] = []

def output_status():
    ''' Outputs final answer to file'''
    global answer
    
    sorted_memory = sorted(memory)
    len_sort_mem = len(sorted_memory)
    for i, var in enumerate(sorted_memory):
        answer += "{} {}".format(var, memory[var])
        if i != len_sort_mem - 1:
            answer += " "
    answer += "\n"

    sorted_database = sorted(database)
    len_sort_database = len(sorted_database)
    for i, var in enumerate(sorted_database):
        answer += "{} {}".format(var, database[var])
        if i != len_sort_database - 1:
            answer += " "
    answer += "\n"

def database_execute(cmd, op, transaction_id):
    ''' Execute database operation(read,write,output)'''
    global answer
    cmd = cmd[:-1].split('(')[1].strip()
    if ',' in cmd:
        var, tmp = cmd.split(',')
        var, tmp = var.strip(), tmp.strip()
    if op.lower() == "read":
        if var in memory:
            registers[tmp] = memory[var]
        else:
            registers[tmp] = database[var]
            memory[var] = database[var]
    
    elif op.lower() == "write":
        answer += "<{}, {}, ".format(transaction_id, var)
        if var not in memory:
            memory[var] = database[var]
        answer += "{}>\n".format(memory[var])
        memory[var] = registers[tmp]
        output_status()
    
    elif op.lower() == "output":
        if cmd in memory:
            database[cmd] = memory[cmd]
        else:
            memory[cmd] = database[cmd]


def operand_check(inp):
    ''' Helper function for arithmetic_execute()'''
    try:
        return int(inp)
    except:
        return registers[inp]

def arithmetic_execute(c, a, b, op):
    ''' Function to execute arithmetic operations'''
    a, b = operand_check(a), operand_check(b)
    if op == "+":
        registers[c] = a + b
    elif op == "-":
        registers[c] = a - b
    elif op == "*":
        registers[c] = a * b
    elif op == "/":
        if b==0:
            sys.exit("Error: Divide by zero")
        else:
            registers[c] = a / b
    

def execute(transaction_id, start, end):
    ''' Function to execute all transactions'''

    database_operations = ["read", "write", "output"]
    arithmetic_operations = ["+", "-", "*", "/"]

    for i in range(start, end):
        flag = False
        cmd = id_command[transaction_id][i]
        for op in database_operations:
            if op in cmd.lower():
                database_execute(cmd, op, transaction_id)
                flag = True
                break
        # if flag is true then a database operation occured, continue to next iteration    
        if flag:
            continue
        cmd = cmd.strip().split(":=")
        cmd[1] = cmd[1].strip()
        c = cmd[0].strip()
        for op in arithmetic_operations:
            if op in cmd[1]:
                a, b = cmd[1].split(op)
                a, b = a.strip(), b.strip()
                arithmetic_execute(c, a, b, op)
                break

def compute(rr_x):
    ''' Computes all transactions in a round robin fashion'''
    global answer
    l = 0
    while True:
        count = 0
        start = l * rr_x
        for transaction_id in transaction_ids:
            num = len(id_command[transaction_id])
            if start == 0:
                answer += "<START {}>\n".format(transaction_id)
                output_status()
            if num <= start:
                count+=1
                continue
            end = min((l+1)*rr_x, num)
            execute(transaction_id, start, end)
            if end == num:
                answer += "<COMMIT {}>\n".format(transaction_id)
                output_status()
        l += 1
        if count == len(transaction_ids):
            break

if __name__ == "__main__":
    path = sys.argv[1]
    read(path)

    rr_x = int(sys.argv[2])
    compute(rr_x)

    with open("20171062_1.txt","w") as fl:
        fl.write(answer)
