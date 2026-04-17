import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os
import numpy as np
from tensorflow.keras.models import load_model

def plot_all():
    os.makedirs('outputs/graphs', exist_ok=True)
    
    # Load data
    df = pd.read_csv('data/maharashtra_material_dataset.csv')
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    # Load Models and Encoders
    rf_model = joblib.load('outputs/models/random_forest.pkl')
    lstm_model = load_model('outputs/models/lstm_model.h5')
    scaler = joblib.load('outputs/models/scaler.pkl')
    le_brand = joblib.load('outputs/models/le_brand.pkl')
    le_city = joblib.load('outputs/models/le_city.pkl')
    le_material = joblib.load('outputs/models/le_material.pkl')
    le_category = joblib.load('outputs/models/le_category.pkl')

    # Encode for RF
    df['brand_encoded'] = le_brand.transform(df['brand'])
    df['city_encoded'] = le_city.transform(df['city'])
    df['material_encoded'] = le_material.transform(df['material'])
    df['category_encoded'] = le_category.transform(df['category'])

    # 1. Separate Forecasts (Horizontal Bar Graph - Correct Price Ranges)
    for material in ['Cement', 'Steel']:
        pred_path = f'outputs/predictions/{material.lower()}_prices.csv'
        if not os.path.exists(pred_path):
            continue
            
        future_df = pd.read_csv(pred_path)
        future_df['date'] = pd.to_datetime(future_df['date'])
        future_df['date_str'] = future_df['date'].dt.strftime('%d %b')

        plt.figure(figsize=(12,8))
        
        # Determine specific colors for materials
        color = 'skyblue' if material == 'Cement' else 'lightcoral'
        edge = 'navy' if material == 'Cement' else 'darkred'

        bars = plt.barh(future_df['date_str'], future_df['predicted_price'], color=color, edgecolor=edge, alpha=0.8)
        
        # Add labels to the end of each bar
        for bar in bars:
            width = bar.get_width()
            plt.text(width + (width*0.005), bar.get_y() + bar.get_height()/2, 
                     f'₹{int(width):,}', va='center', fontsize=10, fontweight='bold')

        # Set X-axis range based on material (as requested for Cement)
        if material == 'Cement':
            plt.xlim(280, 360) # Range around the 290-350 shown in user image
        else:
            plt.xlim(55000, 75000)

        plt.title(f'Next 7 Days {material} Price Forecast', fontsize=14, pad=20)
        plt.xlabel('Predicted Price (₹)', fontsize=12)
        plt.ylabel('Forecast Date', fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.4)
        
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(f'outputs/graphs/{material.lower()}_forecast.png')
        plt.close()

    # 2. Model Comparison Plot (Predictions Only)
    comparison_df = df[(df['material'] == 'Cement') & (df['city'] == 'Mumbai')].copy().tail(50)
    X_rf = comparison_df[['brand_encoded', 'city_encoded', 'material_encoded', 'category_encoded']]
    y_rf = rf_model.predict(X_rf)
    
    # LSTM Predictions
    scaled_prices = scaler.transform(df[['price']])
    X_lstm = []
    indices = comparison_df.index
    for idx in indices:
        if idx >= 10:
            X_lstm.append(scaled_prices[idx-10:idx])
        else:
            X_lstm.append(np.zeros((10, 1)))
    
    y_lstm_scaled = lstm_model.predict(np.array(X_lstm).reshape(-1, 10, 1))
    y_lstm = scaler.inverse_transform(y_lstm_scaled)

    plt.figure(figsize=(14,7))
    plt.plot(comparison_df['date'], y_rf, label='RF Prediction', color='red', linestyle='--', linewidth=2)
    plt.plot(comparison_df['date'], y_lstm, label='LSTM Prediction', color='green', linestyle='-.', linewidth=2)
    plt.title('Model Comparison: Random Forest vs LSTM (Predictions Only)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('outputs/graphs/model_comparison.png')
    plt.close()

    # 3. Parameter Bubble Plot
    params_df = pd.read_csv('outputs/parameters.csv')
    params_df['Accuracy'] = params_df['Accuracy (R2 Score)'].str.replace('%', '').astype(float)
    params_df['MAE'] = params_df['Mean Absolute Error'].astype(float)
    
    plt.figure(figsize=(10,6))
    colors = ['red', 'green']
    for i, row in params_df.iterrows():
        plt.scatter(row['MAE'], row['Accuracy'], 
                    s=row['Training Samples']*0.5, 
                    alpha=0.6, label=row['Model'], color=colors[i])
        plt.text(row['MAE'], row['Accuracy'], row['Model'], fontsize=12, fontweight='bold')

    plt.title('Parameter Analysis: Accuracy vs Error')
    plt.xlabel('Mean Absolute Error (Lower is Better)')
    plt.ylabel('Accuracy Score (Higher is Better)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.savefig('outputs/graphs/parameter_bubble_plot.png')
    plt.close()

    print("\nUpdated material-specific forecasts saved to outputs/graphs/")

if __name__ == "__main__":
    plot_all()
