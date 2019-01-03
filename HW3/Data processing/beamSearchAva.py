import heapq
import math

from Tools.scripts.treesync import raw_input

import importData
import queue

definition_list = list()
amount_of_definitions = list()
targets = list()
descriptors = list()


class PriorityQueue:
    def __init__(self, length):
        self.items = []
        self.length = length

    def push(self, priority, x):
        if not self.inQueue(x):
            heapq.heappush(self.items, (-priority, x))
        while len(self.items) > self.length:
            minimum = self.items[0][0]
            location = 0
            for j in range(1, len(self.items)):
                smaller = self.items[j][0] > minimum
                minimum = self.items[j][0] if smaller else minimum
                location = j if smaller else location
            self.items[location] = self.items[0]
            heapq.heappop(self.items)
            heapq.heapify(self.items)

    def pop(self):
        priority, x = heapq.heappop(self.items)
        return -priority, x

    def empty(self):
        return not self.items

    def inQueue(self, x):
        for j in range(len(self.items)):
            if sorted(self.items[j][1][1]) == sorted(x[1]):
                return True
            else:
                return False

def sameDescriptors(descriptors, descriptorstocompare):
    for row in descriptors:
        inDescriptors = False
        for rowToCompare in descriptorstocompare:
            if row[0] == rowToCompare[0] and row[1] == rowToCompare[1] and row[2] == rowToCompare[2]:
                inDescriptors = True
                break
        if not inDescriptors:
            return False
    return True


def pause():
    program_pause = raw_input("Press the <ENTER> key to continue...")


def createNumericalData(data):
    global definition_list
    definition_list = [dict() for _ in column_names]
    global amount_of_definitions
    amount_of_definitions = [0 for _ in column_names]
    for row in data:
        counter = 0
        for col in row:
            column_definition_list = definition_list[counter]
            amount = amount_of_definitions[counter]
            if isinstance(col, str):
                if col not in column_definition_list:
                    column_definition_list[col] = amount
                    index = amount
                    amount_of_definitions[counter] = amount + 1
                else:
                    index = column_definition_list[col]
            elif isinstance(col, bool):
                if col not in column_definition_list:
                    if col:
                        column_definition_list[1] = 1
                    else:
                        column_definition_list[0] = 1
                        amount_of_definitions[counter] += 1
                index = 1 if col else 0
            else:
                #numeric
                if col not in column_definition_list:
                    column_definition_list[col] = col
                    amount_of_definitions[counter] += 1
                index = col
            row[counter] = index
            counter += 1
    return data

def refinement_positive(seed, counter, value):
    subset = list()
    for row in seed:
        if row[counter] == value:
            subset.append(row)
    return subset


def refinement_negative(seed, counter, value):
    subset = list()
    for row in seed:
        if row[counter] != value:
            subset.append(row)
    return subset

def refinement_larger(seed, counter, value):
    subset = list()
    for row in seed:
        if row[counter] >= value:
            subset.append(row)
    return subset

def refinement_smaller(seed, counter, value):
    subset = list()
    for row in seed:
        if row[counter] <= value:
            subset.append(row)
    return subset


def checkcounter(seed, counter):
    for j in range(len(seed[1])):
        if counter == seed[1][j][0]:
            print("hello")
            return(True)
    return(False)

#TODO Add numeric data
def refinement_operator(seed, data, bins):
    NumberTypes = (int, float, complex)
    global definition_list
    if len(seed) == 0:
        seed = [data, []]
    refinement_set = list()
    for counter in descriptors:
        print(counter)
        # if len(seed) == 2:
        if checkcounter(seed, counter):
            continue
        column_definition_list = definition_list[counter]
        for key, value in column_definition_list.items():
            if isinstance(key, NumberTypes):
                allvalues = list(column_definition_list.values())
                allvalues = allvalues.sort()
                print(allvalues)
                n = len(column_definition_list.items())
                for j in range(1, bins):
                    print(j)
                    Sj = allvalues[math.floor(j * (n / bins))]
                    description = [[counter, "<=", Sj]]
                    description = seed[1] + description
                    refinement_set.append([refinement_smaller(seed[0], counter, Sj), description])
                    description = [[counter, ">=", Sj]]
                    description = seed[1] + description
                    refinement_set.append([refinement_larger(seed[0], counter, Sj), description])
            else:
                description = [[counter, "==", value]]
                description = seed[1] + description
                    # if len(seed) == 2 else description
                refinement_set.append([refinement_positive(seed[0], counter, value), description])
                if not isinstance(key, bool):
                    description = [[counter, "!=", value]]
                    description = seed[1] + description
                        # if len(seed) == 2 else description
                    refinement_set.append([refinement_negative(seed[0], counter, value), description])
        print(counter)
    return refinement_set

def setTarget(number):
    global targets
    targets = targets + [number]
    global descriptors
    descriptors = list(set(descriptors) - set(targets))

# def difference_lists
def calculateQuality(refinement_set, data_set, constraints):
    subgroup_set = refinement_set[0]
    descriptions = refinement_set[1]
    global data_size
    subgroup_size = len(subgroup_set)
    if subgroup_size < 1:
        return 0
    # Create nonsubgroup
    # seed = data_set
    # for row in descriptions:
    #     counter = row[0]
    #     operator = row[1]
    #     value = row[2]
    #
    #     if operator == "==":
    #         seed = refinement_negative(seed, counter, value)
    #     elif operator == "!=":
    #         seed = refinement_positive(seed, counter, value)
    #
    # nonsubgroup_set = seed
    # nonsubgroup_size = len(nonsubgroup_set)


    # n1 = A (row[target[0]] == 0) and NoClick (row[target[1]] == 0)
    # n2 = A (row[target[0]] == 0) and Click (row[target[1]] == 1)
    # n3 = B (row[target[0]] == 1) and NoClick (row[target[1]] == 0)
    # n4 = B (row[target[0]] == 1) and Click (row[target[1]] == 1)
    # y1 = nonsubgroup
    # row[targets[0]] = Combination Id --> 1 = B and 0 = A
    # row[targets[1]] = Converted --> No Click = 0 and Click = 1
    # 1 is True = B, #0 is False = A

    N1 = 0
    N2 = 0
    N3 = 0
    N4 = 0
    for row in subgroup_set:
        if row[targets[0]] == 0 and row[targets[1]] == 0:
            N1 += 1
        elif row[targets[0]] == 0 and row[targets[1]] == 1:
            N2 += 1
        elif row[targets[0]] == 1 and row[targets[1]] == 0:
            N3 += 1
        elif row[targets[0]] == 1 and row[targets[1]] == 1:
            N4 += 1

    if N1 * N4 + N2 * N3 == 0:
        return 0

    if N2 < constraints and N4 < constraints:
        return 0

    if N1 < constraints and N3 < constraints:
        return 0

    quality = (N1 * N4 - N2 * N3)/(N1 * N4 + N2 * N3)
    if quality == 1:
        print("hello")
    return quality

def beamSearch(data, q, d, w, bins, constraints):
    candidateQueue = queue.Queue()
    candidateQueue.put({})

    resultSet = PriorityQueue(q)
    for i in range(d):
        beam = PriorityQueue(w)
        while not candidateQueue.empty():
            seed = candidateQueue.get()
            if len(seed) == 3:
                seed = [seed[0], seed[1]]
            refinement_sets = refinement_operator(seed, data, bins)
            for j in range(len(refinement_sets)):
                refinement_set = refinement_sets[j]
                quality = calculateQuality(refinement_set, data, constraints)
                #TODO: Satisfy all conditions (figure out)
                if constraints <= len(refinement_set[0]) <= len(data) - constraints:
                    print(quality)
                    combinationId = ["A"] if quality <= 0 else ["B"]
                    refinement_set = refinement_set + combinationId
                    resultSet.push(abs(quality), refinement_set)
                    beam.push(abs(quality), refinement_set)
        while not beam.empty():
            _, candidate = beam.pop()
            candidateQueue.put(candidate)
    return resultSet


constraints = 20
w = 10
q = 5
d = 3
bins = 5

data = importData.get_data()
data_size = len(data)
amount_of_columns = len(data[0])
column_names = importData.get_column_names()
for i in range(len(data[0])):
    descriptors += [i]
# TODO change to 9 and 10
setTarget(6)
setTarget(7)
numericData = createNumericalData(data)
result = beamSearch(numericData, q, d, w, constraints, bins)
while not result.empty():
    quality, row = result.pop()
    end_description = ""
    begin = True
    for description in row[1]:
        if begin:
            begin = False
        else:
            end_description += " AND "
        name = column_names[description[0]]
        for key, value in definition_list[description[0]].items():
            if value == description[2]:
                equalTo = key
                continue
        end_description += str(name) + " " + description[1] + " " + str(equalTo)
    print(end_description)
    print(row[0])
    print(row[2])
    print(quality)
