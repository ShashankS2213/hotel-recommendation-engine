import pandas as pd
import pyodbc
from sklearn.neighbors import NearestNeighbors
import joblib
from preprocessor import preprocessing
# Connect using pyodbc
conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=hotels-database.database.windows.net,1433;DATABASE=hotels-data;UID=shashank@hotels-database;PWD=Snowy@123')

# Read from the SQL database into a pandas DataFrame
df = pd.read_sql("SELECT * FROM offerings", conn)
print(f"Loaded {len(df)} records from database.")


def train_model():
    processed_df, scaled_features, ohe, scaler, kmeans = preprocessing(df)

    # Train KNN model
    knn = NearestNeighbors(n_neighbors=5, metric='euclidean')
    knn.fit(scaled_features)

    # Save models and encoders - if you want, save scaler, ohe, kmeans separately
    joblib.dump(knn, 'knn_model.pkl')

    print("Model is saved.")

train_model()