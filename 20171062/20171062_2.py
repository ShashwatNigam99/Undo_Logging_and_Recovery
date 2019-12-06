import sys
import os, copy
from collections import OrderedDict

database = OrderedDict()

def initialize_values(line):
    temp = {}
    line = line.split()
    for i in range(0, len(line), 2):
        temp[line[i].strip()] = int(line[i+1].strip())
    for i in sorted(temp):
        database[i] = temp[i]

def read(path):
    ''' Read contents of file'''
    flag = False
    data = []
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not flag:
                initialize_values(line)
                flag = True
                continue
            if line== "":
                continue
            data.append(line)
    return data

def left_transactions(cmd, done_trans):
    ''' Deal with left over transactions'''
    ret_trans = []
    cmd = cmd.split('(')[1].split(')')[0]
    transactions = list(map(lambda x: x.strip(), cmd.split(',')))
    for transaction in transactions:
        if transaction in done_trans:
            continue
        ret_trans.append(transaction)
    return ret_trans

def recover(data):
    ''' Function to recover'''
    end_ckpt = False
    start_ckpt = False
    data = data[-1::-1]
    done_trans = []
    trans = []
    cnt = 0
    for command in data:
        if command == "<END CKPT>":
            end_ckpt = True
        elif "<START CKPT" in  command:
            if end_ckpt:
                break
            trans = copy.deepcopy(left_transactions(command, done_trans))
            start_ckpt = True
            cnt = 0
        elif "<COMMIT" in command:
            transactions = command.split()[1][:-1]
            done_trans.append(transactions)
        elif "<START" in command:
            if start_ckpt:
                transactions = command.split()[1][:-1]
                if transactions in trans:
                    cnt+=1
                if cnt == len(trans):
                    break
        else:
            [transactions, var, val] = list(map(lambda x: x.strip(), command[1:-1].split(',')))
            if transactions not in done_trans:
                database[var] = val

def output():
    ''' Final output to file'''
    answer = ""
    len_db = len(database)
    for i, var in enumerate(database):
        answer += str(var)+" "+str(database[var])
        if i != len_db - 1:
            answer += " "
    answer += "\n"
    with open('20171062_2.txt', 'w') as fl:
        fl.write(answer)

if __name__ == "__main__":
    path = sys.argv[1]
    data = read(path)
    recover(data)
    output()
