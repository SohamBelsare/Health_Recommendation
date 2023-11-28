import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

def load_data(file_path):
    # Load the dataset
    return pd.read_csv('diabetes_prediction_dataset.csv')

def preprocess_data(data):
    # Preprocess categorical data (e.g., gender)
    label_encoder = LabelEncoder()
    data['gender'] = label_encoder.fit_transform(data['gender'])
    return data

def train_model(X_train, y_train):
    # Initialize the logistic regression model
    model = LogisticRegression(solver='liblinear')

    # Train the model
    model.fit(X_train, y_train)

    return model

def evaluate_model(model, X_test, y_test):
    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Calculate accuracy on the test set
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy:.2f}')

    # Print classification report
    print(classification_report(y_test, y_pred))

def make_predictions(model, new_data):
    # Make predictions on new data
    new_prediction = model.predict_proba(new_data)[:, 1]
    
    a=new_prediction[0]
    if new_prediction[0] >= 0.5 :
        b='Yes'
    else:
        b='No'
    return a,b

def main(gender,age,hypertension,heartDisease,bmi,HbA1c_level,blood_glucose_level):
    # Load and preprocess the data
    data = load_data('your_dataset.csv')
    data = preprocess_data(data)

    # Define features (X) and target variable (y)
    X = data[['gender', 'age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']]
    y = data['diabetes']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    #evaluate_model(model, X_test, y_test)

    # Make predictions on new data
    new_data = pd.DataFrame({'gender': [gender], 'age': [age], 'hypertension': [hypertension], 'heart_disease': [heartDisease], 'bmi': [bmi], 'HbA1c_level': [HbA1c_level], 'blood_glucose_level': [blood_glucose_level]})
    print(make_predictions(model, new_data))
    print(new_data)
    return make_predictions(model, new_data)

