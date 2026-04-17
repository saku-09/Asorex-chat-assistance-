import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, explained_variance_score
import joblib

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from preprocess import prepare_data, create_sequences
from lstm_model import build_lstm_model
from random_forest import train_rf

def main():
    print("--- Starting ML Training Phase ---")
    csv_path = 'data/maharashtra_material_dataset.csv'
    
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    # 1. Preprocess
    df, X_rf, y_rf, scaler = prepare_data(csv_path)
    
    # 2. Random Forest Training
    X_train_rf, X_test_rf, y_train_rf, y_test_rf = train_test_split(X_rf, y_rf, test_size=0.2, random_state=42)
    rf_model = train_rf(X_train_rf, y_train_rf)
    
    rf_preds = rf_model.predict(X_test_rf)
    rf_r2 = r2_score(y_test_rf, rf_preds)
    rf_mae = mean_absolute_error(y_test_rf, rf_preds)
    rf_rmse = np.sqrt(mean_squared_error(y_test_rf, rf_preds))
    rf_evs = explained_variance_score(y_test_rf, rf_preds)
    
    joblib.dump(rf_model, 'outputs/models/random_forest.pkl')
    
    # 3. LSTM Training
    seq_length = 10
    prices_scaled = df['price_scaled'].values
    X_lstm, y_lstm = create_sequences(prices_scaled, seq_length)
    X_lstm = np.reshape(X_lstm, (X_lstm.shape[0], X_lstm.shape[1], 1))
    
    X_train_lstm, X_test_lstm, y_train_lstm, y_test_lstm = train_test_split(X_lstm, y_lstm, test_size=0.2, shuffle=False)
    
    lstm_model = build_lstm_model((X_train_lstm.shape[1], 1))
    lstm_model.fit(X_train_lstm, y_train_lstm, epochs=20, batch_size=32, verbose=0)
    
    lstm_preds_scaled = lstm_model.predict(X_test_lstm)
    lstm_r2 = r2_score(y_test_lstm, lstm_preds_scaled)
    
    # Inverse transform for real price metrics
    y_test_lstm_real = scaler.inverse_transform(y_test_lstm.reshape(-1, 1))
    lstm_preds_real = scaler.inverse_transform(lstm_preds_scaled)
    lstm_mae = mean_absolute_error(y_test_lstm_real, lstm_preds_real)
    lstm_rmse = np.sqrt(mean_squared_error(y_test_lstm_real, lstm_preds_real))
    lstm_evs = explained_variance_score(y_test_lstm_real, lstm_preds_real)
    
    lstm_model.save('outputs/models/lstm_model.h5')
    
    # 4. Save Comprehensive Parameters Table
    params = {
        'Model': ['Random Forest', 'LSTM'],
        'R2 Score': [rf_r2, lstm_r2],
        'MAE': [rf_mae, lstm_mae],
        'RMSE': [rf_rmse, lstm_rmse],
        'Expl. Variance': [rf_evs, lstm_evs],
        'Samples': [len(X_train_rf), len(X_train_lstm)]
    }
    
    params_df = pd.DataFrame(params)
    os.makedirs('outputs', exist_ok=True)
    params_df.to_csv('outputs/parameters.csv', index=False)
    
    print("\n--- Training Results (Detailed) ---")
    print(params_df)

if __name__ == "__main__":
    main()
