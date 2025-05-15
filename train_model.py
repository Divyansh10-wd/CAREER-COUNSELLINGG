import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the dataset from data.csv (Ensure this file is in the same folder)
df = pd.read_csv('data.csv')

# Encode categorical variables
label_encoder = LabelEncoder()

# Encoding the categorical columns
df['personality'] = label_encoder.fit_transform(df['personality'])
df['thinking'] = label_encoder.fit_transform(df['thinking'])
df['perception'] = label_encoder.fit_transform(df['perception'])
df['thought'] = label_encoder.fit_transform(df['thought'])
df['career'] = label_encoder.fit_transform(df['career'])

# Split dataset into features (X) and target (y)
X = df[["personality", "thinking", "perception", "thought", "LRscore"]]
y = df["career"]

# Train the model
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Save the trained model
joblib.dump(model, 'careermodel.pkl')

# Save the label encoder so you can use it in the front-end for the same data transformations
joblib.dump(label_encoder, 'label_encoder.pkl')

print("Model training complete and saved!")
