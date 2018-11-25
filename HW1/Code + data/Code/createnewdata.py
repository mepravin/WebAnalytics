import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

path = '..\Data\speed-dating-null-as-questionmark-no-header.csv'

df = pd.read_csv(path, delim_whitespace=False, header=None, names=
['id', 'date nr', 'date position', 'date same race', 'date subject met before', 'date partner met before',
 'date subject prob receive yes', 'date partner prob receive yes', 'date subject rates partner',
 'date partner rates subject', 'date partner decision', 'date match', 'subject local id', 'subject gender id',
 'subject position_start', 'subject hometown', 'subject hometown zipcode', 'subject field',
 'subject school undergraduate', 'subject intended career', 'subject intended career category',
 'subject importance of race', 'subject importance of religion', 'subject date frequency', 'subject go out frequency',
 'subject speeddate reason', 'subject expected_happy', 'subject month after call', 'subject month after called',
 'subject n_matches_estimation', 'subject interest art', 'subject interest clubbing', 'subject interest concerts',
 'subject interest dining', 'subject interest exercise', 'subject interest gaming', 'subject interest hiking',
 'subject interest movies', 'subject interest museums', 'subject interest music', 'subject interest reading',
 'subject interest shopping', 'subject interest sports', 'subject interest theater', 'subject interest tv',
 'subject interest watching_sports', 'subject interest yoga', 'subject judgement on date length',
 'subject judgement on n dates', 'subject satisfied_with dates', 'subject during date ambition',
 'subject during date attractive', 'subject during date funny', 'subject during date intellect',
 'subject during date sincere', 'subject guesses_how_perceived_by_others ambition',
 'subject guesses_how_perceived_by_others attractive', 'subject guesses_how_perceived_by_others funny',
 'subject guesses_how_perceived_by_others intellect', 'subject guesses_how_perceived_by_others sincere',
 'subject during date preference ambition', 'subject during date preference attractive',
 'subject during date preference funny', 'subject during date preference intellect',
 'subject during date preference shared interests', 'subject during date preference sincere',
 'subject day after preference ambition', 'subject day after preference attractive',
 'subject day after preference funny', 'subject day after preference intellect',
 'subject day after preference shared interests', 'subject day after preference sincere',
 'subject month after preference ambition', 'subject month after preference attractive',
 'subject month after preference funny', 'subject month after preference intellect',
 'subject month after preference shared interests', 'subject month after preference sincere',
 'subject during date rating ambition', 'subject during date rating attractive', 'subject during date rating funny',
 'subject during date rating intellect', 'subject during date rating shared interests',
 'subject during date rating sincere', 'subject guesses opposite sex preference date ambition',
 'subject guesses opposite sex preference date attractive', 'subject guesses opposite sex preference date funny',
 'subject guesses opposite sex preference date intellect',
 'subject guesses opposite sex preference date shared interests',
 'subject guesses opposite sex preference date sincere',
 'subject day after guesses opposite sex preference date ambition',
 'subject day after guesses opposite sex preference date attractive',
 'subject day after guesses opposite sex preference date funny',
 'subject day after guesses opposite sex preference date intellect',
 'subject day after guesses opposite sex preference date shared interests',
 'subject day after guesses opposite sex preference date sincere',
 'subject month after guesses opposite sex preference date ambition',
 'subject month after guesses opposite sex preference date attractive',
 'subject month after guesses opposite sex preference date funny',
 'subject month after guesses opposite sex preference date intellect',
 'subject month after guesses opposite sex preference date shared interests',
 'subject month after guesses opposite sex preference date sincere',
 'subject guesses fellow men women preference partner ambition',
 'subject guesses fellow men women preference partner attractive',
 'subject guesses fellow men women preference partner funny',
 'subject guesses fellow men women preference partner intellect',
 'subject guesses fellow men women preference partner shared interests',
 'subject guesses fellow men women preference partner sincere',
 'subject day after guesses fellow men women preference partner ambition',
 'subject day after guesses fellow men women preference partner attractive',
 'subject day after guesses fellow men women preference partner funny',
 'subject day after guesses fellow men women preference partner intellect',
 'subject day after guesses fellow men women preference partner shared interests',
 'subject day after guesses fellow men women preference partner sincere',
 'subject month after guesses fellow men women preference partner ambition',
 'subject month after guesses fellow men women preference partner attractive',
 'subject month after guesses fellow men women preference partner funny',
 'subject month after guesses fellow men women preference partner intellect',
 'subject month after guesses fellow men women preference partner shared interests',
 'subject month after guesses fellow men women preference partner sincere', 'subject day after importance ambition',
 'subject day after importance attractive', 'subject day after importance funny',
 'subject day after importance intellect', 'subject day after importance shared interests',
 'subject day after importance sincere', 'subject month after importance ambition',
 'subject month after importance attractive', 'subject month after importance funny',
 'subject month after importance intellect', 'subject month after importance shared interests',
 'subject month after importance sincere', 'partner local id', 'partner preference ambition',
 'partner preference attractive', 'partner preference funny', 'partner preference intellect',
 'partner preference shared interests', 'partner preference sincere', 'partner during date rating ambition',
 'partner during date rating attractive', 'partner during date rating funny', 'partner during date rating intellect',
 'partner during date rating shared interests', 'partner during date rating sincere', 'wave nr', 'wave n people',
 'wave condition', 'date subject decision', 'date interests correlate d', 'date age difference d',
 'date age abs difference d', 'date subject younger', 'date subject richer hometown', 'date subject richer school',
 'date same field category', 'date subject smarter school', 'date same importance of race',
 'date same importance of religion', 'date subject expects more interested in him her', 'subject global id',
 'subject gender', 'subject age d', 'subject race', 'subject hometown income d', 'subject field category',
 'subject school tuition d', 'subject school median sat d', 'subject ambition d', 'subject attractive d',
 'subject funny d', 'subject intellect d', 'subject sincere d', 'subject preference ambition d',
 'subject preference attractive d', 'subject preference funny d', 'subject preference intellect d',
 'subject preference sincere d', 'subject preference shared interests d', 'partner global id', 'partner gender',
 'partner age d', 'partner race', 'partner hometown income d', 'partner field category', 'partner school tuition d',
 'partner school median sat d', 'partner ambition d', 'partner attractive d', 'partner funny d', 'partner intellect d',
 'partner sincere d', 'partner preference ambition d', 'partner preference attractive d', 'partner preference funny d',
 'partner preference intellect d', 'partner preference sincere d', 'partner preference shared interests d'],
                 na_values='?')

noColumn = df.drop(['subject school undergraduate', 'subject month after call', 'subject month after called',
                    'subject day after preference ambition', 'subject day after preference attractive',
                    'subject day after preference funny', 'subject day after preference intellect',
                    'subject day after preference shared interests', 'subject day after preference sincere',
                    'subject month after preference ambition', 'subject month after preference attractive',
                    'subject month after preference funny', 'subject month after preference intellect',
                    'subject month after preference shared interests', 'subject month after preference sincere',
                    'subject day after guesses opposite sex preference date ambition',
                    'subject day after guesses opposite sex preference date attractive',
                    'subject day after guesses opposite sex preference date funny',
                    'subject day after guesses opposite sex preference date intellect',
                    'subject day after guesses opposite sex preference date shared interests',
                    'subject day after guesses opposite sex preference date sincere',
                    'subject month after guesses opposite sex preference date ambition',
                    'subject month after guesses opposite sex preference date attractive',
                    'subject month after guesses opposite sex preference date funny',
                    'subject month after guesses opposite sex preference date intellect',
                    'subject month after guesses opposite sex preference date shared interests',
                    'subject month after guesses opposite sex preference date sincere',
                    'subject day after guesses fellow men women preference partner ambition',
                    'subject day after guesses fellow men women preference partner attractive',
                    'subject day after guesses fellow men women preference partner funny',
                    'subject day after guesses fellow men women preference partner intellect',
                    'subject day after guesses fellow men women preference partner shared interests',
                    'subject day after guesses fellow men women preference partner sincere',
                    'subject month after guesses fellow men women preference partner ambition',
                    'subject month after guesses fellow men women preference partner attractive',
                    'subject month after guesses fellow men women preference partner funny',
                    'subject month after guesses fellow men women preference partner intellect',
                    'subject month after guesses fellow men women preference partner shared interests',
                    'subject month after guesses fellow men women preference partner sincere',
                    'subject day after importance ambition', 'subject day after importance attractive',
                    'subject day after importance funny', 'subject day after importance intellect',
                    'subject day after importance shared interests', 'subject day after importance sincere',
                    'subject month after importance ambition', 'subject month after importance attractive',
                    'subject month after importance funny', 'subject month after importance intellect',
                    'subject month after importance shared interests', 'subject month after importance sincere'],
                   axis=1)

filledMean = noColumn.fillna(noColumn.mean())



for row in filledMean.columns:
    filledMean[row].fillna(filledMean[row].mode()[0], inplace=True)
    # for value in filledMean[row]:
    #     if isinstance(value, basestring) and ":" in value and "/" in value:
    #         string = value
    #         filledMean.replace(value, string[1:2], inplace=True)
filledMean.to_csv('removedColumns.csv')