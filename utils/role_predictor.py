import pickle
import re
import numpy as np

# load trained model
model = pickle.load(
    open(
        "ml_models/resume_classifier.pkl",
        "rb"
    )
)

# load vectorizer
vectorizer = pickle.load(
    open(
        "ml_models/vectorizer.pkl",
        "rb"
    )
)

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9 ]",
        " ",
        text
    )

    return text

def predict_role(resume_text):

    # clean resume text
    cleaned_text = clean_text(resume_text)

    # vectorize
    text_vector = vectorizer.transform([cleaned_text])

    # raw decision scores
    scores = model.decision_function(text_vector)[0]

    # class labels
    classes = model.classes_

    # convert to pseudo probabilities
    exp_scores = np.exp(scores - np.max(scores))

    probabilities = exp_scores / np.sum(exp_scores)

    # top 3 predictions
    top_indices = np.argsort(
        probabilities
    )[-3:][::-1]

    top_predictions = []

    for idx in top_indices:
       
        role = classes[idx]

        # scaled display score
        raw_score = probabilities[idx] * 100
        confidence = round(
            min(
                95,raw_score * 1.8
            ),2
        )

        top_predictions.append({
            "role": role,
            "confidence": confidence
        })

    # keep minimum score visible
    for pred in top_predictions:

        if pred["confidence"] < 1:

            pred["confidence"] = 1.0

    return top_predictions