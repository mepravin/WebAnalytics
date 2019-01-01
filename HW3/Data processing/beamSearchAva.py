from Tools.scripts.treesync import raw_input

import importData
import queue

definition_list = list()
amount_of_definitions = list()
import asyncio


def pause():
    program_pause = raw_input("Press the <ENTER> key to continue...")

def createList(q):
    mylist = []
    for i in range(q):
        mylist.append(i)
    return mylist

def createNumericalData(data):
    definition_list = [dict() for _ in column_names]
    amount_of_definitions = [0 for _ in column_names]
    for row in data:
        counter = 0
        for col in row:
            if isinstance(col, str):
                column_definition_list = definition_list[counter]
                amount = amount_of_definitions[counter]
                if col not in column_definition_list:
                    column_definition_list[col] = amount
                    index = amount
                    amount_of_definitions[counter] = amount + 1
                else:
                    index = column_definition_list[col]
                row[counter] = index
            counter += 1

class PriorityQueue:
    def __init__(self):
        self.items = []

    def push(selfself, priority, x):
        heapq.heappush(self.items, ())

def beamSearch(data, q, d):
    candidateQueue = queue.Queue()
    candidateQueue.put({})

    # FIFO Queue
    resultSet = asyncio.PriorityQueue()

q = 5
d = 5

data = importData.get_data()
column_names = importData.get_column_names()
numericData = createNumericalData(data)
beamSearch(numericData, q, d)
