import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

def train_logistic_regression_model(data_path):
    # Load your dataset
    data = pd.read_csv(data_path)

    # Assuming 'HeartDisease' is the target variable and other columns are features
    X = data.drop(['HeartDisease','ST_Slope'], axis=1)
    y = data['HeartDisease']

    
    categorical_features = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina']
    numerical_features = [col for col in X.columns if col not in categorical_features]

    
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder())
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    
    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', LogisticRegression())])

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]  

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Model Accuracy: {accuracy}")
    print("Classification Report:\n", report)

    return model

def predict_heart_disease_probability(model, new_data):
    new_data_prob = model.predict_proba(new_data)[:, 1]
    print(f"Probability of Heart Disease: {new_data_prob}")
    a=new_data_prob[0]
    if a>0.5:
        b='Yes'
    else:
        b='No'

    return a,b







