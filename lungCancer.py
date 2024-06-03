import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

def load_data(file_path):
    # Load the dataset
    return pd.read_csv(file_path)

def preprocess_data(data):
    # Preprocess categorical data
    label_encoder = LabelEncoder()
    data['GENDER'] = label_encoder.fit_transform(data['GENDER'])
    data['LUNG_CANCER'] = label_encoder.fit_transform(data['LUNG_CANCER'])
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
    if new_prediction[0] >= 0.5:
        b='Yes'
    else:
        b='No'
    return a,b

def main ( gender,age,smoking,yellow_fingers,anxiety,peer_pressure,chronic_disease,fatigue,allergy,weezing,alcohol_consumption,coughing,shortness_of_breath,swallowing_difficulty,chest_pain ) :
    # Load and preprocess the data
    data = load_data('survey lung cancer.csv')
    data.rename(columns = {'FATIGUE ':'FATIGUE'}, inplace = True)
    data.rename(columns = {'ALLERGY ':'ALLERGY'}, inplace = True)
    data = preprocess_data(data)

    # Define features (X) and target variable (y)
    X = data[['GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC DISEASE', 'FATIGUE', 'ALLERGY', 'WHEEZING', 'ALCOHOL CONSUMING', 'COUGHING', 'SHORTNESS OF BREATH', 'SWALLOWING DIFFICULTY', 'CHEST PAIN']]
    y = data['LUNG_CANCER']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    #evaluate_model(model, X_test, y_test)

    # Make predictions on new data
    new_data = pd.DataFrame({'GENDER': [gender], 'AGE': [age], 'SMOKING': [smoking], 'YELLOW_FINGERS': [yellow_fingers], 'ANXIETY': [anxiety], 'PEER_PRESSURE': [peer_pressure],
                             'CHRONIC DISEASE': [chronic_disease], 'FATIGUE': [fatigue], 'ALLERGY': [allergy], 'WHEEZING': [weezing], 'ALCOHOL CONSUMING': [alcohol_consumption],
                             'COUGHING': [coughing], 'SHORTNESS OF BREATH': [shortness_of_breath], 'SWALLOWING DIFFICULTY': [swallowing_difficulty], 'CHEST PAIN': [chest_pain]})
    return make_predictions(model, new_data)


