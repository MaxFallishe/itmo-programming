import csv
import os
from unittest import TestCase

from bayes import NaiveBayesClassifier


class TestNaiveBayesClassifier(TestCase):
    def test_score(self) -> None:
        with open(
            os.path.join(os.path.dirname(__file__), "data/SMSSpamCollection"), "r", encoding="utf-8"
        ) as f:
            data = list(csv.reader(f, delimiter="\t"))
        X, y = [], []
        for target, msg in data:
            X.append(msg)
            y.append(target)
        X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
        model = NaiveBayesClassifier(0.05)
        model.fit(X_train, y_train)
        score = model.score(X_test, y_test)
        print("Classifier accuracy: %f" % score)
        self.assertTrue(score > 0.9, "Classifier accuracy %f (< 0.9)" % score)
