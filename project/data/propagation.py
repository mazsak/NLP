import math
import os
from collections import Counter
from os import path

import matplotlib.pyplot as plt
import pandas as pd
import spacy
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from type.type_data import TypeData

nlp = spacy.load("en_core_web_sm")

first_catalog = 'enron_with_categories'

type_data = TypeData.BODY

if not path.exists(f'{first_catalog}/data.csv'):
    def parse_raw_message(lines, category, file_name):
        email = {}
        message = ''
        keys_to_extract = ['subject']
        for line in lines:
            if ':' not in line:
                message += ' ' + line.strip()
                email['body'] = message
            else:
                pairs = line.split(':')
                key = pairs[0].lower()
                val = pairs[1].strip()
                if key in keys_to_extract:
                    email[key] = val
        email['category'] = category
        email['file_name'] = file_name
        return email


    mails = []
    for folder in os.listdir(first_catalog):
        if path.isdir(f'{first_catalog}/{folder}'):
            for file in os.listdir(f'{first_catalog}/{folder}'):
                if file.endswith(".txt"):
                    with open(f'{first_catalog}/{folder}/{file.replace(".txt", ".cats")}', 'r') as cats:
                        lines = cats.readlines()
                    category = [line.strip()[:-2].replace(',', '.') for line in lines]
                    with open(f'{first_catalog}/{folder}/{file}', 'r') as txt:
                        lines = txt.readlines()
                    mails.append(parse_raw_message(lines, category, file))

    df = pd.DataFrame(mails)
    df.to_csv(f'{first_catalog}/data.csv', index=False)
    print("File generate: " + f'{first_catalog}/data.csv')
else:
    print("File exists: " + f'{first_catalog}/data.csv')

if not path.exists(f'{first_catalog}/data_clean' + (
'' if type_data == TypeData.ALL else '_subject' if type_data == TypeData.SUBJECT else '_body') + '.csv'):
    df = pd.read_csv(f'{first_catalog}/data.csv')

    for row in df.iloc:
        if type_data == TypeData.SUBJECT or type_data == TypeData.ALL:
            tokens_subject = [token.lemma_ for token in nlp(str(row['subject'])) if
                              token.is_alpha and not token.is_stop]
            row['subject'] = tokens_subject
        if type_data == TypeData.BODY or type_data == TypeData.ALL:
            tokens_body = [token.lemma_ for token in nlp(str(row['body'])) if token.is_alpha and not token.is_stop]
            row['body'] = tokens_body

    df.to_csv(f'{first_catalog}/data_clean' + (
        '' if type_data == TypeData.ALL else '_subject' if type_data == TypeData.SUBJECT else '_body') + '.csv',
              index=False)
    print("File generate: " + f'{first_catalog}/data_clean' + (
        '' if type_data == TypeData.ALL else '_subject' if type_data == TypeData.SUBJECT else '_body') + '.csv')
else:
    print("File exists: " + f'{first_catalog}/data_clean' + (
        '' if type_data == TypeData.ALL else '_subject' if type_data == TypeData.SUBJECT else '_body') + '.csv')

if not path.exists(f'{first_catalog}/data_tfidf' + (
'' if type_data == TypeData.ALL else '_subject' if type_data == TypeData.SUBJECT else '_body') + '.csv'):
    df = pd.read_csv(f'{first_catalog}/data_clean' + (
        '' if type_data == TypeData.ALL else '_subject' if type_data == TypeData.SUBJECT else '_body') + '.csv')
    array = []
    for row in df.iloc:
        if type_data == TypeData.SUBJECT or type_data == TypeData.ALL:
            tf_idf_data = eval(row['subject'])
        if type_data == TypeData.ALL:
            tf_idf_data.extend(eval(row['body']))
        if type_data == TypeData.BODY:
            tf_idf_data = eval(row['body'])
        array.append({
            'CATEGORY': row['category'],
            'FILE': row['file_name'],
            **Counter(tf_idf_data)
        })
    df_tfidf = pd.DataFrame(array)
    for column in df_tfidf.columns:
        if column != 'CATEGORY' and column != 'FILE':
            df_tfidf[column] = df_tfidf[column].apply(
                lambda i: i * math.log(len(df_tfidf.index) / df_tfidf[column].count(), 10))

    df_tfidf = df_tfidf.fillna(0)
    df_tfidf.to_csv(f'{first_catalog}/data_tfidf' + (
        '' if type_data == TypeData.ALL else '_subject' if type_data == TypeData.SUBJECT else '_body') + '.csv',
                    index=False)
    print("File generate: " + f'{first_catalog}/data_tfidf' + (
        '' if type_data == TypeData.ALL else '_subject' if type_data == TypeData.SUBJECT else '_body') + '.csv')
else:
    print("File exists: " + f'{first_catalog}/data_tfidf' + (
        '' if type_data == TypeData.ALL else '_subject' if type_data == TypeData.SUBJECT else '_body') + '.csv')

if input("Test data(yes, no)?").lower() == 'yes':
    df = pd.read_csv(f'{first_catalog}/data_tfidf' + (
        '' if type_data == TypeData.ALL else '_subject' if type_data == TypeData.SUBJECT else '_body') + '.csv')
    df["CATEGORY"] = df["CATEGORY"].apply(lambda i: eval(i)[0])
    y = df.CATEGORY
    x = df.drop('CATEGORY', axis=1).drop('FILE', axis=1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.9)
    print(x_train.head(), x_test.head(), y_train.head(), y_test.head())

    classifiers = [KNeighborsClassifier(3), SVC(kernel="linear", C=0.025), SVC(gamma=2, C=1),
                   DecisionTreeClassifier(max_depth=5),
                   RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
                   MLPClassifier(alpha=1, max_iter=1000), AdaBoostClassifier(), GaussianNB(),
                   QuadraticDiscriminantAnalysis()]
    names = ["Nearest Neighbors", "Linear SVM", "RBF SVM",
             "Decision Tree", "Random Forest", "Neural Net", "AdaBoost",
             "Naive Bayes", "QDA"]
    for i, classifier in enumerate(classifiers):
        classifier.fit(x_train, y_train)
        print(names[i],round(classifier.score(x_test, y_test) * 100, 2))
        test = plot_confusion_matrix(
            classifier,
            x_test,
            y_test,
            display_labels=[
                '1.1',
                '1.2',
                '1.3',
                '1.4',
                '1.5',
                '1.6',
                '1.7',
                '1.8',
            ])

        test.ax_.set_title('Macierz pomyłek dla danych testowych ' + names[i])
        plt.show()
