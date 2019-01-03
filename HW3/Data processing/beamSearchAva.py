import heapq
import math
import importData
import queue

definition_list = list()
amount_of_definitions = list()
targets = list()
descriptors = list()


''' 
Class which represents the priority queue where a high priority represents a better quality
In these priority queues, the length is already preserved
Input: length (integer)
Functions:
    push (priority, x): put an element in the queue with a priority and a value (x). If the lenght of the priority queue
    is exceeded, the element with smallest priority is deleted
    
    pop: returns the element and priority of the element with highest priority
    
    empty: returns True if PriorityQueue is empty, False if it is not empty
    
    inQueue: returns True if item x is already in the priority queue, False if it is not in the priority queue 
'''


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


# Check whether the both lists of descriptors are exactly the same
def sameDescriptors(descriptor_list1, descriptor_list2):
    for line in descriptor_list1:
        inDescriptors = False
        for lineToCompare in descriptor_list2:
            if line[0] == lineToCompare[0] and line[1] == lineToCompare[1] and line[2] == lineToCompare[2]:
                inDescriptors = True
                break
        if not inDescriptors:
            return False
    return True


'''
Create numerical data of the input. There are several distinct cases:
If the column only contains string values, then all string values are changed to integers and the string value is saved 
    in a dictionary with the following format {key String: value integer}
If the column only contains booleans, then False is saved as 0 and True as 1. The dictionary looks as follows:
    {False: 0, True: 1} 
If the column only contains integers, then the integers are kept in the list. For the dictionary are the key and value
the same, namely the integer x
'''


def createNumericalData(data_to_enumerate):
    # Create the definition list with the correct amount of dictionaries
    global definition_list
    definition_list = [dict() for _ in column_names]

    # Keep track for each column, how many definitions are saved in the dictionary
    global amount_of_definitions
    amount_of_definitions = [0 for _ in column_names]

    for line in data_to_enumerate:
        counter = 0
        for col in line:
            # Take the corresponding definition list and amount
            column_definition_list = definition_list[counter]
            amount = amount_of_definitions[counter]
            if isinstance(col, str):
                # If col not defined in the column_definition_list, add to the definition list and
                # plus one to the amount
                if col not in column_definition_list:
                    column_definition_list[col] = amount
                    index = amount
                    amount_of_definitions[counter] = amount + 1
                # IF col already defined, take the value corresponding to this col
                else:
                    index = column_definition_list[col]
            elif isinstance(col, bool):
                # If col not defined in the column_definition_list, add to the definition list and
                # plus one to the amount.
                # If col = True, then the corresponding integer is 1, else 0
                if col not in column_definition_list:
                    if col:
                        column_definition_list[col] = 1
                    else:
                        column_definition_list[col] = 0
                        amount_of_definitions[counter] += 1
                index = 1 if col else 0
            # Col is numeric
            else:
                # If col not defined in the column_definition_list, add to the definition list and
                # plus one to the amount
                if col not in column_definition_list:
                    column_definition_list[col] = col
                    amount_of_definitions[counter] += 1
                index = col
            # Change col to the index aka the value in the dictionary
            line[counter] = index
            # Go to next column
            counter += 1
    # Return the enumerated data
    return data_to_enumerate


# Find all rows in which value of the counter'ed column is equal to the value_to_compare_with
# Return these rows as subset
def refinement_equal_to(seed, counter, value_to_compare_with):
    subset = list()
    for line in seed:
        if line[counter] == value_to_compare_with:
            subset.append(line)
    return subset


# Find all rows in which value of the counter'ed column is NOT equal to the value_to_compare_with
# Return these rows as subset
def refinement_negative(seed, counter, value_to_compare_with):
    subset = list()
    for line in seed:
        if line[counter] != value_to_compare_with:
            subset.append(line)
    return subset


def refinement_larger(seed, counter, value_to_compare_with):
    subset = list()
    for line in seed:
        if line[counter] >= value_to_compare_with:
            subset.append(line)
    return subset


def refinement_smaller(seed, counter, value_to_compare_with):
    subset = list()
    for line in seed:
        if line[counter] <= value_to_compare_with:
            subset.append(line)
    return subset


def check_counter(seed, counter):
    for j in range(len(seed[1])):
        if counter == seed[1][j][0]:
            return True
    return False


# TODO Add numeric data
def refinement_operator(seed, data, bins):
    NumberTypes = (int, float, complex)
    global definition_list
    if len(seed) == 0:
        seed = [data, []]
    refinement_set = list()
    for counter in descriptors:
        # if len(seed) == 2:
        if check_counter(seed, counter):
            continue
        column_definition_list = definition_list[counter]
        for key, value in column_definition_list.items():
            if isinstance(key, NumberTypes) and not isinstance(key, bool):
                print("integer")
                all_values = list(column_definition_list.values())
                all_values.sort()
                n = len(column_definition_list.items())
                for j in range(1, bins):
                    Sj = all_values[math.floor(j * (n / bins))]
                    description = [[counter, "<=", Sj]]
                    description = seed[1] + description
                    refinement_set.append([refinement_smaller(seed[0], counter, Sj), description])
                    description = [[counter, ">=", Sj]]
                    description = seed[1] + description
                    refinement_set.append([refinement_larger(seed[0], counter, Sj), description])
                    print([refinement_larger(seed[0], counter, Sj), description])
            else:
                description = [[counter, "==", value]]
                description = seed[1] + description
                    # if len(seed) == 2 else description
                refinement_set.append([refinement_equal_to(seed[0], counter, value), description])
                if not isinstance(key, bool):
                    description = [[counter, "!=", value]]
                    description = seed[1] + description
                        # if len(seed) == 2 else description
                    refinement_set.append([refinement_negative(seed[0], counter, value), description])
        print("counter:" + str(counter))
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
