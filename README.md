# hotel-recommendation-engine
A Machine Learning-based Hotel Recommendation System that provides personalized hotel suggestions based on user preferences using KNN & Streamlit, powered by Azure SQL Database.

**Project Objective**
To develop an intelligent Hotel Recommendation Engine that suggests top hotels based on user-defined preferences such as location, price, rating, and number of reviews, using machine learning models with a simple, interactive Streamlit UI.

**Demo Preview**
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)

**Project Architecture**
    UserInput["User Inputs (Location, Price, Rating, Reviews)"] -->|Frontend| StreamlitApp["Streamlit Web App"]
    StreamlitApp --> LoadData["Load Offerings"]
    StreamlitApp --> LoadModels["Load Preprocessor & KNN Model"]
    StreamlitApp --> Preprocess["Preprocess Input & Offerings Data"]
    Preprocess --> Recommend["Compute Similarity (Euclidean Distance)"]
    Recommend --> Display["Show Top 5 Recommendations"]

**Tech Stack**
Frontend -> Streamlit
Backend -> Python, Scikit-learn, Pandas
Database -> Azure SQL Database, SQLAlchemy, pyodbc
Modeling -> K-Nearest Neighbors, Custom Preprocessing
Deployment -> Local / Streamlit Cloud / Azure App Svc
Serialization -> joblib (for .pkl files)

**Installation & Usage**
**1]Clone the Repository**
[git clone https://github.com/yourusername/hotel-recommendation.git]
cd hotel-recommendation
**2]Install Dependencies**
pip install -r requirements.txt
**3]Run the Streamlit App**
streamlit run app.py
