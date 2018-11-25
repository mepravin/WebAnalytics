import csv
import numpy as np
from sklearn.model_selection import train_test_split


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
date_result = dict()
date_info = dict()

subject_id = "subject global id"
date_id = "id"
date_result_id = "id"
date_info_id = "id"

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

# subject_columns.append("subject hometown")
# subject_columns.append("subject hometown zipcode")
# subject_columns.append("subject school undergraduate")
# subject_columns.append("subject intended career")
# subject_columns.append("subject intended career category")
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
date_columns.append("date partner decision")
date_columns.append("date subject decision")
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
            i += 1
            continue
        readRow = list()

        for name in subject_columns:
            value = formatValue(row[columnIndexes[name]])
            readRow.append(value)
        if "null" not in readRow:
            subject[row[columnIndexes[subject_id]]] = readRow

        readRow = list()
        for name in date_columns:
            value = formatValue(row[columnIndexes[name]])
            readRow.append(value)
        if "null" not in readRow:
            date[row[columnIndexes[date_id]]] = readRow

        i += 1


for row in date:
    subjectId = date[row][0]
    partnerId = date[row][1]
    subjectInfo = subject.get(str(subjectId))
    partnerInfo = subject.get(str(partnerId))
    if (subjectInfo is None) or (partnerInfo is None):
        continue
    else:
        index = date_columns.index("date partner decision")
        partner_preference = date[row].pop(index)
        index = date_columns.index("date subject decision")
        subject_preference = date[row].pop(index)
        date_result[row] = 1 if ((partner_preference == 1) and (subject_preference == 1)) else 0

        new_row = np.append(date[row], (subjectInfo, partnerInfo))
        date_info[row] = new_row

for row in date_info:
    print(row)
    print(date_info[row])

