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

    # Calibrated probabilities via CalibratedClassifierCV or model fallback
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(text_vector)[0]
    else:
        # Fallback to decision_function
        scores = model.decision_function(text_vector)[0]
        exp_scores = np.exp(scores - np.max(scores))
        probabilities = exp_scores / np.sum(exp_scores)

    # class labels
    classes = model.classes_

    # top 3 predictions
    top_indices = np.argsort(probabilities)[-3:][::-1]

    top_predictions = []

    # EXPLAINABILITY: Extract top TF-IDF features present in the resume
    feature_names = np.array(vectorizer.get_feature_names_out())
    non_zero_indices = text_vector.nonzero()[1]
    feature_scores = text_vector.data
    
    sorted_feat_indices = np.argsort(feature_scores)[::-1]
    top_influential_keywords = [
        feature_names[non_zero_indices[i]] for i in sorted_feat_indices[:5]
    ] if len(sorted_feat_indices) > 0 else []

    for idx in top_indices:
        role = classes[idx]
        raw_score = probabilities[idx] * 100
        confidence = round(raw_score, 2)
        if confidence < 1.0:
            confidence = 1.0

        top_predictions.append({
            "role": role,
            "confidence": confidence,
            "influential_keywords": top_influential_keywords
        })

    return top_predictions