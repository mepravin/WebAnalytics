import csv

import numpy as np
import pydotplus
from sklearn import neighbors, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


# import graphviz


def formatValue(data):
    value = data

    if value == "TRUE":
        value = 1

    if value == "FALSE":
        value = 0

    if value == "Yes":
        value = 1

    if value == "No":
        value = 0

    if value == "":
        value = "null"

    try:
        value = int(value)
    except ValueError:
        pass

    return value


table = list()

visit = list()
visit_target = list()
date_info = list()
date_info_columns = list()

visit_id = "id"

visit_columns = list()

visit_columns.append("\xef\xbb\xbfScreen Resolution")
visit_columns.append("Browser")
visit_columns.append("Browser Version")
visit_columns.append("Device Type")
visit_columns.append("Device")
visit_columns.append("OS")
visit_columns.append("OS Version")
visit_columns.append("User Agent")
visit_columns.append("Traffic Source")
visit_columns.append("Returning Visitor")
visit_columns.append("Hit Time")
visit_columns.append("User Language")
visit_columns.append("URL")
visit_columns.append("Referring URL")
visit_columns.append("City")
visit_columns.append("Region")
visit_columns.append("Country")
visit_columns.append("Combination Id")
visit_columns.append("Converted")

columnIndexes = dict()
categoricalUnits = dict()

with open('data-delimited.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

    i = 0
    counter = 0
    totalcounter = 0
    missingcounter = 0
    for row in spamreader:
        if i == 0:
            j = 0
            for col in row:
                columnIndexes[col] = j
                j += 1
            i += 1
            continue
        readRow = list()

        for name in visit_columns:
            value = formatValue(row[columnIndexes[name]])
            readRow.append(value)
        if "null" in readRow:
            if readRow[6] == "null" and "Windows" in readRow[5]:
                value = readRow[5][8:]
                readRow[5] = "Windows"
                readRow[6] = value
            if readRow[6] == "null" and "Linux" in readRow[5]:
                readRow[6] = 0
            if readRow[6] == "null" and "Ubuntu" in readRow[5]:
                readRow[6] = 0

        if "null" not in readRow:
            readRow[17] = "A" if readRow[17] == 1 else "B"
            missingcounter += 1
            visit.append(readRow)
        i += 1
        totalcounter += 1

print("start")

with open('data_file.csv', mode='wb') as csvfile:
    data_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writerow(visit_columns)
    for row in visit:
        data_writer.writerow(row)

print(missingcounter)
print(totalcounter)