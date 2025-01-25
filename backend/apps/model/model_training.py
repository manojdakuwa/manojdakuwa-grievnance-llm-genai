import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv('grievances.csv')

# Preprocess and split data
X = df['description']
y = df['category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature extraction
vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train model
clf = RandomForestClassifier()
clf.fit(X_train_vec, y_train)

# Evaluate model
y_pred = clf.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# Save model and vectorizer
import joblib
joblib.dump(clf, 'grievance_classifier.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
