import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score, recall_score

from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC
from sklearn.neighbors import RadiusNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

result_dict = {}

def summarize_classification(y_test, y_pred):
    acc = accuracy_score(y_test, y_pred, normalize=True)
    num_acc = accuracy_score(y_test, y_pred, normalize=False)  # accurate count

    prec = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    return {
        'accuracy': acc,
        'precision': prec,
        'recall': recall,
        'accuracy_count': num_acc
    }


def build_model(classifier_fn,
                name_of_y_col,
                name_of_x_cols,
                dataset,
                test_frac=0.2
                ):
    X = dataset[name_of_x_cols]
    Y = dataset[name_of_y_col]

    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=test_frac)

    model = classifier_fn(x_train, y_train)
    y_pred = model.predict(x_test)

    y_pred_train = model.predict(x_train)

    train_summary = summarize_classification(y_train, y_pred_train)
    test_summary = summarize_classification(y_test, y_pred)

    pred_results = pd.DataFrame({
        'y_test': y_test,
        'y_pred': y_pred
    })

    model_crosstab = pd.crosstab(pred_results.y_pred, pred_results.y_test)

    return {
        'training': train_summary,
        'test': test_summary,
        'confusion_matrix': model_crosstab
    }


def compare_results():
    for key in result_dict:
        print('Classification: ', key)
        print()
        print('Training data')
        for score in result_dict[key]['training']:
            print(score, result_dict[key]['training'][score])

        print()
        print('Test data')
        for score in result_dict[key]['test']:
            print(score, result_dict[key]['test'][score])

        print()



