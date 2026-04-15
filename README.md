# 🚀 Asorex AI Chat Assistant

### AI-Powered Construction Material Pricing & Prediction System

---

## 📌 Overview

The **Asorex AI Chat Assistant** is an intelligent conversational system designed to provide real-time insights into construction material prices such as **Cement** and **Steel**.

The system combines **Natural Language Processing (NLP)**, **Machine Learning**, and **Web Scraping** to deliver accurate, context-aware, and future price predictions based on user queries.

---

## 🎯 Key Features

* 🧱 **Cement & Steel Price Tracking**
* 📍 **City-wise Pricing (Maharashtra)**
* 🏷️ **Brand-based Filtering (ACC, UltraTech, JSW, SAIL, etc.)**
* 📊 **Past, Current & Future Price Prediction**
* 📅 **Date-wise Query Handling (e.g., "price on 10 April")**
* 🔮 **ML-based Future Forecasting**
* 📈 **Multi-day Predictions (next 3 days, next week)**
* 📉 **Historical Analysis (last 3 days, past week)**
* 🔄 **Web Scraping Fallback (Real-time data)**
* 🤖 **Context-aware Chatbot (Remembers previous inputs)**
* ⚙️ **Error Handling & Data Fallback System**

---

## 🧠 How It Works

1. User enters a query (e.g., *"cement price tomorrow in Pune"*)
2. NLP module extracts:

   * Material
   * City
   * Brand
   * Category/Grade
   * Time context (past / present / future)
3. System processes request:

   * 📊 Past → Dataset
   * 💰 Current → Dataset
   * 📈 Future → ML Model
4. If data unavailable:

   * 🔄 Web scraping is triggered
   * ⚠️ Fallback estimation is applied

---

## 🛠️ Tech Stack

* **Frontend**: HTML, CSS, JavaScript
* **Backend**: Python (Flask)
* **Machine Learning**: Trend-based forecasting model
* **NLP**: Regex-based entity extraction
* **Web Scraping**: BeautifulSoup, Requests
* **Data Handling**: Pandas

---

## 📂 Project Structure

```bash
Asorex-Assistant/
│
├── app/
│   ├── app.py              # Flask app entry point
│   ├── chatbot.py          # Chatbot logic
│   ├── nlp_utils.py        # NLP processing
│   ├── model_utils.py      # ML prediction logic
│
├── scraper/
│   ├── cement_scraper.py
│   ├── steel_scraper.py
│
├── data/
│   ├── maharashtra_material_dataset.csv
│
├── static/
│   ├── style.css
│   ├── script.js
│
├── templates/
│   ├── index.html
│
├── requirements.txt
└── README.md
```

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/asorex-ai-chat-assistant.git
cd asorex-ai-chat-assistant
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Application

```bash
python app/app.py
```

---

### 5️⃣ Open in Browser

```bash
http://127.0.0.1:5000
```

---

## 💬 Example Queries

* "Cement price in Pune today"
* "Steel price tomorrow Fe500"
* "Cement price last 3 days"
* "Steel price on 20 April"
* "Compare cement price across cities"
* "Next 5 days cement price"

---

## 🔍 Prediction Logic

* Based on **current price trend**
* Uses **controlled growth rate**
* Ensures:

  * ✔ No unrealistic drop
  * ✔ Smooth price variation
  * ✔ Material-specific behavior

---

## 🔥 Future Improvements

* 📈 Graph visualization for trends
* 🧠 Advanced ML models (LSTM, ARIMA)
* 🌍 Multi-state support
* 📱 Mobile app integration
* ☁️ Cloud deployment

---
