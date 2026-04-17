import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import joblib
import os

def prepare_data(csv_path):
    df = pd.read_csv(csv_path)
    
    # Sort by date
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Label Encoding for categorical features
    le_brand = LabelEncoder()
    le_city = LabelEncoder()
    le_material = LabelEncoder()
    le_category = LabelEncoder()
    
    df['brand_encoded'] = le_brand.fit_transform(df['brand'])
    df['city_encoded'] = le_city.fit_transform(df['city'])
    df['material_encoded'] = le_material.fit_transform(df['material'])
    df['category_encoded'] = le_category.fit_transform(df['category'])
    
    # Save encoders for later use in prediction
    os.makedirs('outputs/models', exist_ok=True)
    joblib.dump(le_brand, 'outputs/models/le_brand.pkl')
    joblib.dump(le_city, 'outputs/models/le_city.pkl')
    joblib.dump(le_material, 'outputs/models/le_material.pkl')
    joblib.dump(le_category, 'outputs/models/le_category.pkl')
    
    # Features for Random Forest
    rf_features = ['brand_encoded', 'city_encoded', 'material_encoded', 'category_encoded']
    X_rf = df[rf_features]
    y_rf = df['price']
    
    # Scaling for LSTM
    scaler = MinMaxScaler()
    df['price_scaled'] = scaler.fit_transform(df[['price']])
    joblib.dump(scaler, 'outputs/models/scaler.pkl')
    
    return df, X_rf, y_rf, scaler

def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:(i + seq_length)])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)
