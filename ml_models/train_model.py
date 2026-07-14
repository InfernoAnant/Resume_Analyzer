import pandas as pd
import pickle
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns

# CLEAN TEXT
def clean_text(text):

    text = str(text).lower()
    # keep words + numbers only
    text = re.sub(
        r"[^a-zA-Z0-9 ]",
        " ",
        text
    )

    # remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )
    return text.strip()

# LOAD DATASET (V3)
df = pd.read_csv(
    "dataset/resume_dataset_v3.csv"
)

print("\nDataset loaded successfully")
print("Total dataset size:", len(df))
print("Total classes:", df["category"].nunique())

# PREPROCESS
df["resume_text"] = df[
    "resume_text"
].apply(
    clean_text
)

X = df["resume_text"]
y = df["category"]

# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X,y,test_size=0.20,random_state=42,stratify=y
)


print("\nTrain size:", len(X_train))
print("Test size:", len(X_test))

# TF-IDF VECTORIZER
vectorizer = TfidfVectorizer(

    stop_words="english",
    ngram_range=(1, 3),
    max_features=20000,
    min_df=1,
    max_df=0.90,
    sublinear_tf=True
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

print("\nVocabulary size:", len(vectorizer.vocabulary_))

# MODEL
model = LinearSVC(
    C=2.0,class_weight="balanced",random_state=42,max_iter=5000
)

# CROSS VALIDATION
cv_scores = cross_val_score(
    model,X_train_vec,y_train,cv=5
)

print("\nCross Validation Accuracy:")
print(round(cv_scores.mean(), 4))

# TRAIN MODEL
model.fit(
    X_train_vec,y_train
)

# PREDICT
predictions = model.predict(
    X_test_vec
)

# EVALUATION
accuracy = accuracy_score(
    y_test,predictions
)

print("\nFinal Accuracy:")
print(round(accuracy, 4))
print("\nClassification Report:\n")
print(
    classification_report(
        y_test,predictions
    )
)

# CONFUSION MATRIX
cm = confusion_matrix(
    y_test,predictions
)

print("\nConfusion Matrix:\n")
print(cm)

# show graph
plt.figure(figsize=(14, 10))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    xticklabels=model.classes_,
    yticklabels=model.classes_
)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# SHOW CLASSES
print("\nModel Classes:\n")
print(model.classes_)

# SAVE MODEL
pickle.dump(
    model,
    open(
        "ml_models/resume_classifier.pkl",
        "wb"
    )
)

pickle.dump(
    vectorizer,
    open(
        "ml_models/vectorizer.pkl",
        "wb"
    )
)

print("\nModel saved successfully")
print("\nTraining completed successfully")