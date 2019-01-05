import csv


# The list containing all data
import math

visit = list()

# All columns with name in visit
visit_columns = list()

# string - 0 - doesn't seem to make difference + large
visit_columns.append("\ufeffScreen Resolution")
# string - 1
visit_columns.append("Browser")
# visit_columns.append("Browser Version")

# string - 2
visit_columns.append("Device Type")
# string - 3
visit_columns.append("Device")
# string - removed, doesnt seem to make a difference
# visit_columns.append("OS")
# visit_columns.append("OS Version")
# visit_columns.append("User Agent") Deleted because redundant information
# visit_columns.append("Traffic Source")

# boolean - 5
visit_columns.append("Returning Visitor")
# visit_columns.append("Hit Time")

# string - 6
visit_columns.append("User Language")
# visit_columns.append("URL")
# visit_columns.append("Referring URL")
# visit_columns.append("City")

# string - 7, removed too many variations
# visit_columns.append("Region")

# string - 8
visit_columns.append("Country")

#boolean - 9
visit_columns.append("Combination Id")
#boolean - 10
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
    counter = 0
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
        # JUI - add the data here (by doing readRow.append(gender)
        # For gender I recommend True False
        if "null" not in readRow:
            # 1 is True = B, #0 is False = A
            height = (round(int(readRow[0].split('x')[0]) / 100)) * 100
            length = (round(int(readRow[0].split('x')[1]) / 100)) * 100
            readRow[0] = str(height) + 'x' + str(length)
            readRow[0] = str(readRow[0])
            readRow[1] = str(readRow[1])
            readRow[2] = str(readRow[2])
            readRow[3] = str(readRow[3])
            if "Samsung" in readRow[3]:
                readRow[3] = "Samsung"
            elif "Lenovo" in readRow[3]:
                readRow[3] = "Lenovo"
            elif "LG" in readRow[3]:
                readRow[3] = "LG"
            elif "Moto" in readRow[3]:
                readRow[3] = "Motorola"
            elif "ONEPLUS" in readRow[3]:
                readRow[3] = "OnePlus"
            elif "Pixel" in readRow[3]:
                readRow[3] = "Pixel"
            elif "HTC" in readRow[3]:
                readRow[3] = "HTC"
            elif "Asus" in readRow[3]:
                readRow[3] = "Asus"
            elif "HUAWEI" in readRow[3]:
                readRow[3] = "HUAWEI"
            elif "iPhone" in readRow[3]:
                readRow[3] = "iPhone"
            elif "iPad" in readRow[3]:
                readRow[3] = "iPad"
            elif "XiaoMi" in readRow[3]:
                readRow[3] = "XiaoMi"
            elif "Nexus" in readRow[3]:
                readRow[3] = "Nexus"
            elif "Mi" in readRow[3]:
                readRow[3] = "Mi"
            elif "Generic Smartphone" in readRow[3]:
                readRow[3] = "Generic Smartphone"
            elif "Other" in readRow[3]:
                readRow[3] = "Other"
            else:
                counter += 1
                continue
            # if "Windows" in readRow[4]:
            #      readRow[4] = "Windows"
            # readRow[4] = str(readRow[4])
            readRow[4] = True if readRow[4] == 1 else False
            readRow[5] = str(readRow[5])
            readRow[6] = str(readRow[6])
            # readRow[7] = str(readRow[7])
            readRow[7] = True if readRow[7] == 1 else False
            readRow[8] = True if readRow[8] == 1 else False

            visit.append(readRow)
        i += 1
    print(counter)
    print(len(visit))
    # JUI, add the column_name (in the same order as you appended the data before.
    # e.g. visit_columns.append("Gender")
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
