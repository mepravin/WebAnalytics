import csv


# The list containing all data
import math

visit = list()

# All columns with name in visit
visit_columns = list()

# #visit_columns.append("\ufeffScreen Resolution")
visit_columns.append("Browser")
# visit_columns.append("Browser Version")
visit_columns.append("Device Type")
# #visit_columns.append("Device")
visit_columns.append("OS")
# visit_columns.append("OS Version")
# visit_columns.append("User Agent") Deleted because redundant information
# visit_columns.append("Traffic Source")
visit_columns.append("Returning Visitor")
# visit_columns.append("Hit Time")
visit_columns.append("User Language")
# visit_columns.append("URL")
# visit_columns.append("Referring URL")
# visit_columns.append("City")
# #visit_columns.append("Region")
visit_columns.append("Country")
visit_columns.append("Combination Id")
visit_columns.append("Converted")

# A dictionary with the indices of the columns
columnIndexes = dict()


# Format values to booleans or null
def formatValue(data):
    value_to_change = data

    if value_to_change == "TRUE":
        value_to_change = True

    if value_to_change == "FALSE":
        value_to_change = False

    if value_to_change == "Yes":
        value_to_change = True

    if value_to_change == "No":
        value_to_change = False

    if value_to_change == "":
        value_to_change = "null"

    if value_to_change == "unknown":
        value_to_change = "null"

    try:
        value_to_change = int(value_to_change)
    except ValueError:
        pass

    return value_to_change


# read data in and save to visit and column_names
with open('data-delimited.csv', 'r', encoding='utf-8') as csv_file:
    spam_reader = csv.reader(csv_file, delimiter=',', quotechar='"')

    i = 0
    # counter = 0
    for row in spam_reader:
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
        # TODO: delete
        readRow.append(i % 1210)

        if "null" not in readRow:
            # TODO change to 10
            # 1 is True = B, #0 is False = A
            readRow[0] = str(readRow[0])
            readRow[1] = str(readRow[1])
            readRow[2] = str(readRow[2])
            if "Windows" in readRow[2]:
                readRow[2] = "Windows"
            readRow[3] = True if readRow[3] == 1 else False
            readRow[4] = str(readRow[4])
            readRow[5] = str(readRow[5])
            readRow[6] = True if readRow[6] == 1 else False
            readRow[7] = True if readRow[7] == 1 else False

            visit.append(readRow)
        i += 1
    visit_columns.append("counter")


# Save data in new csv file
# with open('data_file.csv', mode='wb') as csvfile:
#     data_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     data_writer.writerow(visit_columns)
#     for row in visit:
#         data_writer.writerow(row)


# Method to get the data
def get_data():
    return visit

# Method to get the column names of the data
def get_column_names():
    return visit_columns
