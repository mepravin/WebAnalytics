import csv
import numpy as np

def formatValue(data):
    value = data

    if ":" in value and "/" in value and "-" in value:
        value = value[1:2]

    if value == "TRUE":
        value = 1

    if value == "FALSE":
        value = 0

    if value == "male":
        value = 1

    if value == "female":
        value = 0

    try:
        value = int(value)
    except ValueError:
        pass

    return value

table = list()

date = dict()
subject = dict()

subject_id = "subject global id"
date_id = "id"

subject_columns = list()
subject_columns.append("subject gender")
subject_columns.append("subject age d")
subject_columns.append("subject hometown income d")
subject_columns.append("subject school tuition d")
subject_columns.append("subject school median sat d")
subject_columns.append("subject ambition d")
subject_columns.append("subject attractive d")
subject_columns.append("subject funny d")
subject_columns.append("subject intellect d")
subject_columns.append("subject sincere d")
subject_columns.append("subject preference ambition d")
subject_columns.append("subject preference attractive d")
subject_columns.append("subject preference funny d")
subject_columns.append("subject preference intellect d")
subject_columns.append("subject preference sincere d")
subject_columns.append("subject preference shared interests d")


#subject_columns.append("subject hometown")
#subject_columns.append("subject hometown zipcode")
#subject_columns.append("subject school undergraduate")
#subject_columns.append("subject intended career")
#subject_columns.append("subject intended career category")
subject_columns.append("subject importance of race")
subject_columns.append("subject importance of religion")
subject_columns.append("subject expected_happy")
subject_columns.append("subject n_matches_estimation")
subject_columns.append("subject interest art")
subject_columns.append("subject interest clubbing")
subject_columns.append("subject interest concerts")
subject_columns.append("subject interest dining")
subject_columns.append("subject interest exercise")
subject_columns.append("subject interest gaming")
subject_columns.append("subject interest hiking")
subject_columns.append("subject interest movies")
subject_columns.append("subject interest music")
subject_columns.append("subject interest reading")
subject_columns.append("subject interest shopping")
subject_columns.append("subject interest sports")
subject_columns.append("subject interest theater")
subject_columns.append("subject interest tv")
subject_columns.append("subject interest watching_sports")
subject_columns.append("subject interest yoga")

date_columns = list()
date_columns.append("subject global id")
date_columns.append("partner global id")
date_columns.append("date subject decision")
date_columns.append("date partner decision")
date_columns.append("date partner rates subject")
date_columns.append("date subject rates partner")
date_columns.append("date partner prob receive yes")
date_columns.append("date subject prob receive yes")
date_columns.append("date subject met before")
date_columns.append("date partner met before")
date_columns.append("date position")
date_columns.append("date nr")

columnIndexes = dict()

categoricalUnits = dict()


with open('speed-dating.csv', 'r') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')

     i = 0
     counter = 0
     for row in spamreader:
         if i == 0:
             j = 0
             for col in row:
                columnIndexes[col] = j
                j += 1
             i+=1
             continue
         readRow = list()

         for name in subject_columns:
             value = formatValue(row[columnIndexes[name]])
             readRow.append(value)
         if "null" not in readRow:
             subject[row[columnIndexes[subject_id]]] = readRow
         else:
             counter = counter + 1

         readRow = list()
         for name in date_columns:
             value = formatValue(row[columnIndexes[name]])
             readRow.append(value)
         date[row[columnIndexes[date_id]]] = readRow

         i += 1

for date in date_columns:
    subjectid = date[0]
    partnerid = date[1]
    subjectInfo = subject[subjectid]
    partnerInfo = subject[partnerid]
    np.concatenate(date, subjectInfo, partnerInfo)


for row in subject:
    print(subject[row])





