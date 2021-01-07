import math
import os
from collections import Counter

import pandas as pd
import spacy
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

nlp = spacy.load('en_core_web_sm')

convert = eval(input("Create csv with count(True/False): "))
if not os.path.exists('bbc_TFIDF.csv'):
    print('bbc_TFIDF.csv file does not exist. Create csv with count.')
    convert = True
if convert:
    array = []
    if not os.path.exists('csv'):
        os.mkdir('csv')
    for catalog in os.listdir('bbc'):
        for file in os.listdir(f'bbc\\{catalog}'):
            with open(f'bbc\\{catalog}\\{file}', 'r') as f:
                array.append({
                    'CLASS': catalog,
                    'FILE': file,
                    **Counter([
                        word.lemma_
                        for word in nlp(' '.join(f.readlines()))
                        if not word.is_stop and word.is_alpha
                    ])
                })

        df = pd.DataFrame(array)
        df.to_csv(f'csv\\bbc_{catalog}.csv')
        array = []
        print(f"Finished bbc_{catalog}.csv")

    df = None
    for index, file in enumerate(os.listdir('csv')):
        if index == 0:
            df = pd.read_csv(f'csv\\{file}')
        else:
            df = df.append(pd.read_csv(f'csv\\{file}'), ignore_index=True)
    df = df.drop('Unnamed: 0', axis=1)
    df.to_csv('bbc_finished.csv', index=False)
    print("Finished")

    for column in df.columns:
        if column != 'CLASS' and column != 'FILE':
            df[column] = df[column].apply(lambda i: i * math.log(len(df.index) / df[column].count(), 10))
    df.to_csv('bbc_TFIDF.csv', index=False)
    print("Finished bbc_TFIDF.csv")
else:
    df = pd.read_csv('bbc_TFIDF.csv')

df = df.fillna(0)
y = df.CLASS
x = df.drop('CLASS', axis=1)
x = x.drop('FILE', axis=1)

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.5)
print(x_train.head(), x_test.head(), y_train.head(), y_test.head())

clf = LogisticRegression(random_state=0).fit(x_train, y_train)
print(round(clf.score(x_test, y_test) * 100, 2))

test = plot_confusion_matrix(
    clf,
    x_test,
    y_test,
    display_labels=[
        'business',
        'entertainment',
        'politics',
        'sport',
        'tech'
    ])
test.ax_.set_title('Macierz pomyłek dla danych testowych')
fig = plt.figure()
ax = plt.subplot(111)
plt.show()

training = plot_confusion_matrix(
    clf,
    x_train,
    y_train,
    display_labels=[
        'business',
        'entertainment',
        'politics',
        'sport',
        'tech'
    ])
training.ax_.set_title('Macierz pomyłek dla danych treningowych')
plt.show()