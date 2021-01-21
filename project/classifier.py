import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer


class Classifier:

    def __init__(self):
        self.text_clf = Pipeline([('vect', CountVectorizer()),
                                  ('tfidf', TfidfTransformer()),
                                  ('clf', OneVsRestClassifier(SGDClassifier(random_state=42, max_iter=5, tol=None)))])
        temp_df = pd.read_csv('data/enron_with_categories/data.csv')
        self.mlb = MultiLabelBinarizer()

        temp_df["category"] = temp_df["category"].apply(lambda i: eval(i))
        y = self.mlb.fit_transform(temp_df['category'])
        x_training, y_training = (temp_df['body'], y)
        self.text_clf.fit(x_training, y_training)

    def guess(self, contents: str) -> list:
        return self.mlb.inverse_transform(self.text_clf.predict([contents]))
