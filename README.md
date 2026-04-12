# 💳 Real-Time Credit Card Fraud Detection System

An end-to-end **production-grade Machine Learning system** that detects fraudulent transactions in real-time using streaming data.

This project simulates real-world fintech systems using **Kafka-based streaming**, **XGBoost modeling**, and **Dockerized deployment on AWS**.

---

## 🚀 Overview

Fraud detection is a highly imbalanced and cost-sensitive problem.  
This system is designed to:

- Detect fraudulent transactions with high recall
- Minimize financial loss using business-aware thresholding
- Process streaming data in real-time

---

## 🏗️ Architecture


::contentReference[oaicite:0]{index=0}


### 🔁 Pipeline Flow

```

User / Dataset
↓
Kafka Producer (Streaming transactions)
↓
Kafka Topic (fraud_topic)
↓
Kafka Consumer
↓
Inference Pipeline (XGBoost Model)
↓
Fraud Prediction (Probability + Threshold)
↓
FastAPI (Prediction API)
↓
Flask UI (Dashboard)
↓
Storage (CSV / BI layer)

```

---

## ⚙️ Tech Stack

- Python  
- XGBoost  
- Apache Kafka  
- FastAPI  
- Flask  
- Docker & Docker Compose  
- AWS EC2  
- MLflow  

---

## 🧠 Machine Learning Highlights

- Handled **extreme class imbalance (~0.07% fraud rate)**
- Performed **feature engineering** using:
  - Transaction time (hour, day)
  - User age
  - Behavioral features
- Removed **data leakage features**:
  - `cc_num`, `unix_time`, geo-coordinates
- Implemented **modular ML pipeline**:
  - Data Ingestion → Preprocessing → Feature Engineering → Training → Inference

---

## 🎯 Threshold Optimization (Key Feature)

Implemented **dual threshold strategy**:

### 1️⃣ F1-based Threshold
- Optimizes model performance
- Balanced precision and recall

### 2️⃣ Cost-based Threshold (Production)
- Minimizes business loss
- Penalizes false negatives more than false positives

Additionally:
- Constrained threshold range to avoid overly aggressive predictions
- Ensured realistic production behavior

---

## 📊 Model Performance

```

Confusion Matrix:
[[110664     52]
[     5     75]]

```

- ✅ Recall: ~94% (fraud detection)
- ✅ Precision: ~59%
- ✅ Very low false negatives (critical in fraud systems)

---

## 🔄 Real-Time Pipeline

1. Kafka Producer streams transaction data  
2. Kafka Consumer reads data in real-time  
3. Inference pipeline processes transactions  
4. Model predicts fraud probability  
5. Threshold applied for classification  
6. Results stored in `data/bi/predictions.csv`  
7. Flask UI displays predictions  

---

## 🐳 Deployment

- Fully containerized using Docker  
- Multi-service system:
  - API (FastAPI)
  - UI (Flask)
  - Kafka + Zookeeper  
- Deployed on AWS EC2  

---

## 📁 Project Structure

```

credit-card-fraud-detection-project/
│
├── api_engine/        # FastAPI backend
├── app_ui/            # Flask UI
├── kafka/             # Producer & Consumer
├── src/               # ML pipeline (modular)
│   ├── ingestion/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── model/
│   └── pipeline/
├── models/            # Saved artifacts
├── data/              # Raw + BI data
├── config/            # Config files
├── docker-compose.yml

```

---

## 🧪 How to Run

### 1️⃣ Clone the repo

```

git clone <https://github.com/abhikdas98/credit-card-fraud-detection>
cd credit-card-fraud-detection-project

```

### 2️⃣ Start services

```

docker-compose up --build

```

### 3️⃣ Access

- API → http://localhost:8001  
- UI → http://localhost:5001  

---

## 🚀 Future Improvements

- Replace CSV storage with S3 / Data Warehouse  
- Add SHAP model explainability  
- Real-time monitoring dashboard  
- Model drift detection  
- Alerting system  

---

## 💼 Key Learnings

- Designing real-time ML systems with Kafka  
- Handling highly imbalanced datasets  
- Avoiding data leakage in ML pipelines  
- Balancing business vs model metrics  
- Deploying containerized ML systems on AWS  

---

## ⭐ Conclusion

This project demonstrates a **production-ready fraud detection system** combining:

- Machine Learning  
- Streaming Architecture  
- Backend APIs  
- Cloud Deployment  

---

## 📬 Connect

If you found this useful, feel free to connect or provide feedback!

```