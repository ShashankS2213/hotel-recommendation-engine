# preprocessor.py
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.cluster import KMeans

class CustomPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=10, random_state=42)
        self.fitted = False
        self.mean_price = None

    def fit(self, X, y=None):
        df = X.copy()
        
        # Calculate and store mean price
        self.mean_price = df['price'].mean()
        df['price'] = df['price'].fillna(self.mean_price)
        
        # Feature engineering
        df['normalized_rating'] = df['rating'] / 5.0

        # Price category
        def price_category(price):
            if pd.isnull(price):
                return 'Unknown'
            elif price < 30:
                return 'Budget'
            elif price < 100:
                return 'Midrange'
            else:
                return 'Premium'
        df['price_category'] = df['price'].apply(price_category)

        # Rating category
        def rating_category(rating):
            if pd.isnull(rating):
                return 'Unrated'
            elif rating >= 4.5:
                return 'Excellent'
            elif rating >= 4.0:
                return 'Good'
            elif rating >= 3.0:
                return 'Average'
            else:
                return 'Poor'
        df['rating_category'] = df['rating'].apply(rating_category)

        # One-hot encode categorical features
        categorical_cols = ['location', 'price_category', 'rating_category']
        self.ohe.fit(df[categorical_cols])
        categorical_encoded = self.ohe.transform(df[categorical_cols])

        categorical_df = pd.DataFrame(
            categorical_encoded, 
            columns=self.ohe.get_feature_names_out(categorical_cols),
            index=df.index
        )
        
        # Only using normalized_rating & price (no num_reviews)
        features = pd.concat([
            df[['normalized_rating', 'price']].fillna(0),
            categorical_df
        ], axis=1)
        
        # Scale features
        self.scaler.fit(features)
        scaled_features = self.scaler.transform(features)
        
        # Fit KMeans clustering
        self.kmeans.fit(scaled_features)
        
        self.fitted = True
        return self

    def transform(self, X):
        if not self.fitted:
            raise RuntimeError("You must fit the preprocessor before transform.")
        
        df = X.copy()
        
        # Impute using stored mean price
        df['price'] = df['price'].fillna(self.mean_price)
        
        # Feature engineering
        df['normalized_rating'] = df['rating'] / 5.0

        def price_category(price):
            if pd.isnull(price):
                return 'Unknown'
            elif price < 30:
                return 'Budget'
            elif price < 100:
                return 'Midrange'
            else:
                return 'Premium'
        df['price_category'] = df['price'].apply(price_category)

        def rating_category(rating):
            if pd.isnull(rating):
                return 'Unrated'
            elif rating >= 4.5:
                return 'Excellent'
            elif rating >= 4.0:
                return 'Good'
            elif rating >= 3.0:
                return 'Average'
            else:
                return 'Poor'
        df['rating_category'] = df['rating'].apply(rating_category)

        # One-hot encode categorical features
        categorical_cols = ['location', 'price_category', 'rating_category']
        categorical_encoded = self.ohe.transform(df[categorical_cols])
        categorical_df = pd.DataFrame(
            categorical_encoded, 
            columns=self.ohe.get_feature_names_out(categorical_cols),
            index=df.index
        )
        
        # Only normalized_rating & price (no num_reviews)
        features = pd.concat([
            df[['normalized_rating', 'price']].fillna(0),
            categorical_df
        ], axis=1)
        
        # Scale features
        scaled_features = self.scaler.transform(features)
        
        # Predict cluster
        df['cluster'] = self.kmeans.predict(scaled_features)
        
        return df, scaled_features
