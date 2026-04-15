# 🚀 Asorex AI Chat Assistant

### AI-Powered Construction Material Pricing & Prediction System

---

## 📌 Overview

The **Asorex AI Chat Assistant** is an intelligent chatbot that provides real-time and predictive insights for construction materials such as **Cement** and **Steel**.

The system integrates:

* Natural Language Processing (NLP)
* Machine Learning (LSTM & Random Forest)
* Web Scraping
* Data Analytics

to deliver **accurate, context-aware, and future price predictions**.

---

## 🎯 Key Features

* 🧱 Cement & Steel price tracking
* 📍 City-wise pricing across Maharashtra
* 🏷️ Brand-based filtering (ACC, UltraTech, SAIL, JSW, etc.)
* 📊 Historical data analysis (past days)
* 📅 Date-based queries ("price on 10 April")
* 🔮 ML-based future prediction
* 📈 Multi-day prediction (next 3–7 days)
* 🔁 Comparison across cities & brands
* 🤖 Context-aware chatbot
* ⚠️ Smart fallback (scraping + estimation)

---

## 🧠 Machine Learning Models

* 🔵 **LSTM Model** → Time-series forecasting
* 🟢 **Random Forest** → Price prediction comparison
* ⚙️ **Scaler + Encoders** → Data preprocessing

---

## 📂 Project Structure

```bash
Asorex Assistant/
│
├── app/                         # Chatbot & backend logic
│   ├── app.py
│   ├── chatbot.py
│   ├── model_utils.py
│   ├── nlp_utils.py
│   ├── scraper_utils.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
│
├── models/                      # ML models & training
│   ├── lstm_model.py
│   ├── random_forest.py
│   ├── train.py
│   ├── predict.py
│   ├── preprocess.py
│   └── visualize.py
│
├── outputs/                     # Generated outputs
│   ├── graphs/
│   │   ├── cement_forecast.png
│   │   ├── steel_forecast.png
│   │   └── model_comparison.png
│   ├── models/
│   │   ├── lstm_model.h5
│   │   ├── random_forest.pkl
│   │   ├── scaler.pkl
│   │   └── encoders (.pkl files)
│   └── predictions/
│       ├── cement_prices.csv
│       ├── steel_prices.csv
│       └── future_prices.csv
│
├── scraper/                     # Data scraping scripts
│   ├── cement_scraper.py
│   └── steel_scraper.py
│
├── pipeline/                    # Dataset generation
│   ├── build_dataset.py
│   └── simulate_history.py
│
├── data/                        # Dataset storage
│
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/asorex-ai-chat-assistant.git
cd asorex-ai-chat-assistant
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run Application

```bash
python app/app.py
```

---

### 5️⃣ Open in Browser

```
http://127.0.0.1:5000
```

---

## 💬 Example Queries

* Cement price in Pune today
* Steel price tomorrow Fe500
* Cement price last 3 days
* Steel price on 20 April
* Compare cement price across cities
* Next 5 days steel price

---

## 🔍 Prediction Logic

* Based on **current market price**
* Uses **controlled growth model**
* Avoids unrealistic fluctuations
* Material-specific behavior:

  * Cement → stable trend
  * Steel → slightly volatile

---

## 📊 Output Reports

* 📈 Forecast graphs (cement & steel)
* 📉 Model comparison charts
* 📋 Classification & parameter reports

---

## 🔮 Future Enhancements

* 📊 Interactive graph visualization
* 🧠 Advanced deep learning models
* 🌍 Multi-state expansion
* ☁️ Cloud deployment (AWS/Render)
* 📱 Mobile application

---

