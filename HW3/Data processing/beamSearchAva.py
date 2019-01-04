import heapq
import math
import importData
import queue

definition_list = list()
amount_of_definitions = list()
targets = list()
descriptors = list()

# !!!User can define the minimum set size of the result (constraints), the width, the depth, the amount of bins and
# the amount of results
minimum_set_size = 25
width = 15
depth = 3
bins = 5
result_amount = 8

# Define the data and the column names. Important is that a column should be either binary, numeric or nominal.
# It cannot be a combination
data = importData.get_data()
# The names of the columns.
column_names = importData.get_column_names()




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
                        amount_of_definitions[counter] += 1
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
    print(amount_of_definitions)
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
def refinement_not_equal_to(seed, counter, value_to_compare_with):
    subset = list()
    for line in seed:
        if line[counter] != value_to_compare_with:
            subset.append(line)
    return subset

# Find all rows in which value of the counter'ed column is larger than (or equal to) the value_to_compare_with
# Return these rows as subset
def refinement_larger(seed, counter, value_to_compare_with):
    subset = list()
    for line in seed:
        if line[counter] >= value_to_compare_with:
            subset.append(line)
    return subset

# Find all rows in which value of the counter'ed column is smaller than (or equal to) the value_to_compare_with
# Return these rows as subset
def refinement_smaller(seed, counter, value_to_compare_with):
    subset = list()
    for line in seed:
        if line[counter] <= value_to_compare_with:
            subset.append(line)
    return subset

# Check whether the counter'ed column has already been used as description and therefore
def check_counter(seed, counter):
    for j in range(len(seed)):
        seed_to_compare = seed[j][0]
        if counter == seed_to_compare:
            return True
    return False


def remove_duplicates(k):
    k.sort()
    dedup = [k[i] for i in range(len(k)) if i == 0 or k[i] != k[i - 1]]
    return dedup

'''
Save all descriptions possible based on the seed
If the seed is empty, all descriptions possible are added
Otherwise, all descriptions are added, except for the columns of which a descriptions already exists
'''


def refinement_operator(seed, bins_amount):
    global definition_list
    description_set = list()

    for counter in descriptors:
        # if len(seed) == 2:
        # check whether a descr has already been defined for the counter'ed column
        if check_counter(seed, counter):
            continue

        # take the definition list of a specific column
        column_definition_list = definition_list[counter]
        for definition_key, definition_value in column_definition_list.items():
            # if the column contains integers, then add the descriptors for all possible values
            # break out of the for loop
            if isinstance(definition_key, (int, float, complex)) and not isinstance(definition_key, bool):
                #make a list of all values in the numeric counter'ed column
                all_values = list(column_definition_list.values())
                all_values.sort()
                n = len(column_definition_list.items())
                for j in range(1, bins_amount):
                    Sj = all_values[math.floor(j * (n / bins_amount))]

                    # add the new descriptor to the already defined descriptors in the seed
                    descr = [[counter, "<=", Sj]]
                    descr = seed + descr
                    description_set.append(descr)

                    # add the new descriptor to the already defined descriptors in the seed
                    descr = [[counter, ">=", Sj]]
                    descr = seed + descr
                    description_set.append(descr)
                break
            else:
                # the column is not numeric, thus it is a boolean or nominal, first we add the description equal to
                # add the new descriptor to the already defined descriptors in the seed
                descr = [[counter, "==", definition_value]]
                descr = seed + descr
                description_set.append(descr)

                # the column is nominal, thus we add the description not equal to
                if not isinstance(definition_key, bool):
                    descr = [[counter, "!=", definition_value]]
                    descr = seed + descr
                        # if len(seed) == 2 else descr
                    description_set.append(descr)
        print("counter:" + str(counter))
    #make sure that there are no duplicates, to avoid overhead
    description_set = remove_duplicates(description_set)
    return description_set

# Set the targets of the dataset by providing the number of the column. These 'numbers' will be deleted from the
# descriptor set
def setTarget(number):
    global targets
    targets = targets + [number]
    global descriptors
    descriptors = list(set(descriptors) - set(targets))

# Create subgroup using the description_set

def createSubgroup(description_set, data_set):
    result_set = data_set
    for line in description_set:
        counter = line[0]
        operator = line[1]
        value_to_compare_with = line[2]

        if operator == "==":
            result_set = refinement_equal_to(result_set, counter, value_to_compare_with)
        elif operator == "!=":
            result_set = refinement_not_equal_to(result_set, counter, value_to_compare_with)
        elif operator == ">=":
            result_set = refinement_larger(result_set, counter, value_to_compare_with)
        elif operator == "<=":
            result_set = refinement_smaller(result_set, counter, value_to_compare_with)

    return result_set


#The modelClass, in our case we use association
def model_class(subgroup_set):

    """
    N1 = A (line[target[0]] == 0) and NoClick (line[target[1]] == 0)
    N2 = A (line[target[0]] == 0) and Click (line[target[1]] == 1)
    N3 = B (line[target[0]] == 1) and NoClick (line[target[1]] == 0)
    N4 = B (line[target[0]] == 1) and Click (line[target[1]] == 1)
    line[targets[0]] = Combination Id --> 1 = B and 0 = A
    line[targets[1]] = Converted --> No Click = 0 and Click = 1
    1 is True = B, #0 is False = A
    """

    N1 = 0
    N2 = 0
    N3 = 0
    N4 = 0

    for line in subgroup_set:
        if line[targets[0]] == 0 and line[targets[1]] == 0:
            N1 += 1
        elif line[targets[0]] == 0 and line[targets[1]] == 1:
            N2 += 1
        elif line[targets[0]] == 1 and line[targets[1]] == 0:
            N3 += 1
        elif line[targets[0]] == 1 and line[targets[1]] == 1:
            N4 += 1

     return N1, N2, N3, N4


#We use Yule's Q
def quality_method(N1, N2, N3, N4, constraint):
    # Return 0 if the denominator is 0, since then only one version is present or only clicks/no clicks
    if N1 * N4 + N2 * N3 == 0:
        return 0

    # return 0 if the size of the subsets of the associations are not significant
    if N2 < constraint and N4 < constraint:
        return 0

    if N1 < constraint and N3 < constraint:
        return 0

    return (N1 * N4 - N2 * N3) / (N1 * N4 + N2 * N3)


# calculate the quality of each description set
def calculateQuality(description_set, data_set, constraint):
    subgroup_set = createSubgroup(description_set, data_set)
    subgroup_size = len(subgroup_set)
    if subgroup_size < 1:
        return 0, 0

    N1, N2, N3, N4 = model_class(subgroup_set)
    quality = quality_method(N1, N2, N3, N4, constraint)
    return len(subgroup_set), quality

# the beamsearch as explained in the paper Exceptional Model Mining # Supervised descriptive local pattern
# mining with complex target # concepts
def beamSearch(beam_data, beam_result_length, beam_depth, beam_width, beam_bins, beam_constraint):
    # create queue for the candidates
    candidateQueue = queue.Queue()
    candidateQueue.put([])

    # create result Set: this is a priority queue with length beam_result_length
    resultSet = PriorityQueue(beam_result_length)
    for _ in range(beam_depth):
        # create the beam: this is a priority queue with length beam_width
        beam = PriorityQueue(beam_width)
        while not candidateQueue.empty():
            # take a seed
            seed = candidateQueue.get()
            # seed can contain both the descriptions and the version, if so, only save the description
            if len(seed) == 2:
                seed = seed[0]

            # define the descriptions using the seed and the bins
            description_sets = refinement_operator(seed, beam_bins)

            # for each set of descriptions, calculate the quality and put in the beam and resultset
            for j in range(len(description_sets)):
                description_set = description_sets[j]
                subgroup_set_size, quality = calculateQuality(description_set, beam_data, beam_constraint)
                if j % 100 == 0:
                    print(str(j) + ": " + str(len(description_sets)))
                #TODO: Satisfy all conditions (figure out)
                if beam_constraint <= subgroup_set_size <= len(beam_data) - beam_constraint:
                    #Also remember the combination ID at which was clicked most often
                    combinationId = ["A"] if quality <= 0 else ["B"]
                    description_set = [description_set] + combinationId
                    resultSet.push(abs(quality), description_set)
                    beam.push(abs(quality), description_set)
        # add all beams to the candidate_queue
        while not beam.empty():
            _, candidate = beam.pop()
            candidateQueue.put(candidate)
    return resultSet


def print_result(result):
    while not result.empty():
        quality, row = result.pop()
        end_description = ""
        begin = True
        for description in row[0]:
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
        print(createSubgroup(row[0], numericData))
        print(row[1])
        print(quality)


for i in range(len(data[0])):
    descriptors += [i]
setTarget(9)
setTarget(10)
numericData = createNumericalData(data)
result = beamSearch(numericData, result_amount, depth, width, bins, minimum_set_size)
print_result(result)


