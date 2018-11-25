import csv
from tkinter import Image

import numpy as np
import pydotplus as pydotplus
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import neighbors
import graphviz


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
date_result = list()
date_info = list()
date_info_columns = list()

subject_id = "subject global id"
date_id = "id"

partner_columns = list()
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

for i in range(len(subject_columns)):
    new_value = "partner" + subject_columns[i][7:]
    partner_columns.append(new_value)

date_columns = list()
date_columns.append("subject global id")
date_columns.append("partner global id")
date_columns.append("date match")
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
        index = date_columns.index("date match")
        match = date[row].pop(index)
        date_result.append(match)

        new_row = np.append(date[row], (subjectInfo, partnerInfo))
        date_info.append(new_row)

date_columns.remove("date match")
date_info_columns = np.append(date_columns, (subject_columns, partner_columns))

# --------------------------------Divide Train Test Set -------------------------------------
X_train, X_test, y_train, y_test = train_test_split(date_info, date_result, test_size=0.25)

# -------------------------Decision Tree --------------------------------------------

# for i in range(1, 11):
#     dt = tree.DecisionTreeClassifier(max_depth=i)
#     dt.fit(X_train, y_train)
#     dot_data = tree.export_graphviz(dt, out_file=None, feature_names=date_info_columns, class_names=["No Date", "Date"],
#                                     filled=True, rounded=True, special_characters=True)
#
#     # Visualise decision tree
#     graph = pydotplus.graph_from_dot_data(dot_data)
#     graph.write_pdf("outcome" + str(i) + ".pdf")
#
#     # Check accuracy
#     y_pred_train = dt.predict(X_train)
#     y_pred_test = dt.predict(X_test)
#     accuracy_dt_train = accuracy_score(y_train, y_pred_train) * 100
#     accuracy_dt_test = accuracy_score(y_test, y_pred_test) * 100
#
#     print(str(i) + " & " + str(accuracy_dt_train) + " & " + str(accuracy_dt_test))

# -------------------------Random Forest--------------------------------------------
# Instantiate model with 1000 decision trees
for i in range(10, 26):
    rf = RandomForestClassifier(n_estimators=1000, random_state=42, max_depth=i)

    # Train the model on training data
    rf.fit(X_train, y_train)

    # Check accuracy
    y_pred_train = rf.predict(X_train)
    y_pred_test = rf.predict(X_test)
    accuracy_rf_train = accuracy_score(y_train, y_pred_train) * 100
    accuracy_rf_test = accuracy_score(y_test, y_pred_test) * 100

    print(str(i) + " & " + str(accuracy_rf_train) + " & " + str(accuracy_rf_test))

# -------------------------Linear Regression--------------------------------------------
# K_Nearest = neighbors.KNeighborsClassifier()
# K_Nearest.fit(X_train, y_train)
#
# y_pred_train = K_Nearest.predict(X_train)
# for i in range(len(y_pred_train)):
#     y_pred_train[i] = 0 if y_pred_train[i] < 0.5 else 1
# y_pred_test = K_Nearest.predict(X_test)
# for i in range(len(y_pred_test)):
#     y_pred_test[i] = 0 if y_pred_test[i] < 0.5 else 1
# accuracy_K_Nearest_train = accuracy_score(y_train, y_pred_train) * 100
# accuracy_K_Nearest_test = accuracy_score(y_test, y_pred_test) * 100
#
# print("K_Nearest - Accuracy Train Set: " + str(accuracy_K_Nearest_train))
# print("K_Nearest - Accuracy Test Set: " + str(accuracy_K_Nearest_test))
