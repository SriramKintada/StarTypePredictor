from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import GridSearchCV

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://starsize.streamlit.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def default():
    """
    Default endpoint to check if the application is running.

    Returns:
        dict: A simple message indicating the application is running.
    """
    return {"App": "Running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Reading the uploaded file
    contents = await file.read()

    # Load the CSV data into a DataFrame
    df = pd.read_csv(io.BytesIO(contents))

    x = df.iloc[:, :-1]
    y = df.iloc[:, -1:]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.3, random_state=0
    )

    reg = LogisticRegression()
    reg.fit(X_train, y_train)

    # Base Model
    a = np.mean(cross_val_score(reg, X_train, y_train, cv=10))
    r2_score = reg.score(X_test, y_test)

    # StandardScaler
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    reg.fit(X_train_scaled, y_train)
    b = np.mean(cross_val_score(reg, X_train_scaled, y_train, cv=10))
    r2_score_stand = reg.score(X_test_scaled, y_test)

    # MinMaxScaler
    scaler = MinMaxScaler()
    scaler.fit(X_train)
    X_train_scaled_min = scaler.transform(X_train)
    X_test_scaled_min = scaler.transform(X_test)
    reg.fit(X_train_scaled_min, y_train)
    c = np.mean(cross_val_score(reg, X_train_scaled_min, y_train, cv=10))
    r2_score_min = reg.score(X_test_scaled_min, y_test)

    # Hyperparameter Tuning
    param_grid = [
        {
            "penalty": ["l1", "l2", "elasticnet", "none"],
            "C": np.logspace(-4, 4, 20),
            "solver": ["lbfgs", "newton-cg", "liblinear", "sag", "saga"],
        }
    ]
    clg = GridSearchCV(reg, param_grid=param_grid, cv=10, verbose=True, n_jobs=-1)
    clg.fit(X_train, y_train)
    r2_score_hyper = clg.score(X_test, y_test)
    d = np.mean(cross_val_score(clg, X_train, y_train, cv=10))

    # Fitting analysis
    def determine_fit(cv_score, val_score):
        if cv_score + 0.5 < val_score:
            return "overfitting"
        elif cv_score - 0.5 > val_score:
            return "underfitting"
        else:
            return "good fit"

    k = determine_fit(a, r2_score)
    l = determine_fit(b, r2_score_stand)
    m = determine_fit(c, r2_score_min)
    n = determine_fit(d, r2_score_hyper)

    # Creating DataFrame for results
    data = {
        "Changes made": ["No Scalar", "MinMax Scalar", "Standard Scalar", "Hyperparameter Tuning"],
        "Training accuracy": [a, b, c, d],
        "Validation Accuracy": [r2_score, r2_score_min, r2_score_stand, r2_score_hyper],
        "Fitting": [k, l, m, n],
    }

    df1 = pd.DataFrame(data)

    # Convert the DataFrame with predictions to CSV format
    output = df1.to_csv(index=False).encode("utf-8")

    # Return the CSV file as a streaming response
    return StreamingResponse(
        io.BytesIO(output),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=predictions.csv"},
    )

#Summary
# In no scalling we just run logistic regression on our data frame and claculate validation and r2score using test dataframe
# In standard we standardise the data and run logistic regression on our data frame and claculate validation and r2score using test dataframe
# In minmaxscaller we operate minmaxscaler on the data and run logistic regression on our data frame and claculate validation and r2score using test dataframe
# In hyperparameter we use GridSearchCVto find best hyperparameter which give better result in prediction
# then we create data frame to make comparision in between these methods
# In fitting we use just basic elif condition on validation score and r2 score to identify fitting