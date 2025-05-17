import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics.pairwise import euclidean_distances
from preprocessor import CustomPreprocessor

# Load models
@st.cache_resource
def load_models():
    preprocessor = joblib.load('utils/hotel_preprocessor.pkl')  # Local file, no DB
    knn_model = joblib.load('utils/knn_model.pkl')  # Still loading, no retrain
    return preprocessor, knn_model

# Load offerings data from local pickle
@st.cache_data
def load_offerings():
    df = joblib.load('utils/offerings.pkl')  # Local file, no DB
    return df

# Load models & data
preprocessor, knn_model = load_models()
offerings_df = load_offerings()

# Streamlit UI
st.title("Hotel Recommendation Engine")
st.markdown("Get top 5 hotel recommendations based on your preferences.")

location = st.selectbox("Location", sorted(offerings_df['location'].unique()))
price = st.slider("Price", 10, 500, 100)
rating = st.slider("Rating", 0.0, 5.0, 4.0, step=0.1)
num_reviews = st.number_input("Number of Reviews", min_value=0, value=50)

if st.button("Get Recommendations"):
    # Prepare input data
    input_data = pd.DataFrame([{
        'location': location,
        'price': price,
        'rating': rating,
        'num_reviews': num_reviews
    }])

    # Preprocess input data
    processed_input_df, scaled_input_features = preprocessor.transform(input_data)

    # Filter offerings to selected location only
    filtered_offerings_df = offerings_df[offerings_df['location'] == location]

    if filtered_offerings_df.empty:
        st.warning(f"No hotels found in {location}. Please select a different location.")
    else:
        # Preprocess filtered offerings data
        processed_filtered_df, scaled_filtered_features = preprocessor.transform(filtered_offerings_df)

        # Compute distances manually (euclidean)
        distances = euclidean_distances(scaled_input_features, scaled_filtered_features)[0]

        # Get indices of top 5 closest hotels
        top_indices = np.argsort(distances)[:5]

        # Display results
        st.subheader("🔍 Top 5 Recommendations:")

        for idx, index in enumerate(top_indices, 1):
            hotel = filtered_offerings_df.iloc[index]
            processed_hotel = processed_filtered_df.iloc[index]
            distance = distances[index]

            st.markdown(f"""
            **{idx}. {hotel['name']}**
            - Location: {hotel['location']}
            - Price: ${hotel['price']}
            - Rating: {hotel['rating']} ({hotel['num_reviews']} reviews)
            - Price Category: {processed_hotel['price_category']}
            - Rating Category: {processed_hotel['rating_category']}
            - Distance Score: {distance:.2f}
            """)
