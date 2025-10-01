# Nova: AI-Powered Loan Eligibility Platform

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-FF6B35?style=for-the-badge)](https://xgboost.readthedocs.io)
[![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)

**An intelligent creditworthiness assessment system for Grab's merchant and driver partners**

[🎯 Features](#-features) • [🚀 Quick Start](#-quick-start) • [📊 Demo](#-demo) • [🏗️ Architecture](#️-architecture) • [📖 API Documentation](#-api-documentation)

</div>

---

## Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Demo Screenshots](#-demo)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [Project Architecture](#️-architecture)
- [API Documentation](#-api-documentation)
- [Data Features](#-data-features)
- [Model Performance](#-model-performance)
- [Contributing](#-contributing)
- [License](#-license)

## Overview

**Nova** is an enterprise-grade machine learning platform designed to assess loan eligibility for Grab's ecosystem partners. Built with fairness and transparency in mind, Nova provides real-time creditworthiness predictions while maintaining ethical AI practices through comprehensive bias detection and mitigation.

The platform serves two primary user groups:
- **Merchants**: Restaurant owners, retail partners, and service providers
- **Drivers**: Transportation partners across various vehicle categories

## Key Features

### **Intelligent Prediction Engine**
- **Single Entry Prediction**: Real-time eligibility assessment through intuitive web interface
- **Bulk CSV Processing**: High-throughput batch processing for enterprise operations
- **XGBoost ML Model**: State-of-the-art gradient boosting with 95%+ accuracy

### **Comprehensive Analytics Dashboard**
- **Model Performance Metrics**: Real-time accuracy, precision, recall, and F1-score tracking
- **Fairness Assessment**: Bias detection across demographic groups using Fairlearn
- **Interactive Data Visualization**: Rich charts and tables for decision transparency

### **Enterprise-Grade Features**
- **Data Validation**: Robust input sanitization and anomaly detection
- **Audit Trail**: Complete logging of all predictions for compliance
- **RESTful API**: Production-ready endpoints with CORS support
- **Responsive Design**: Mobile-first UI with Tailwind CSS

### **Fairness & Bias Mitigation**
- **Algorithmic Fairness**: Equal opportunity and selection rate monitoring
- **Group Parity Analysis**: Performance comparison across partner types
- **Bias Reporting**: Automated fairness violation detection and recommendations

## Demo

<div align="center">

### Main Dashboard
<img width="1919" alt="Nova Dashboard" src="https://github.com/user-attachments/assets/9d71a554-3d22-46ac-ad6d-5d3394f7cf98" />

### Single Entry Prediction
<img width="1919" alt="Single Entry Form" src="https://github.com/user-attachments/assets/5b2f943d-c673-491f-8899-a7aef9b981af" />

### Bulk CSV Processing
<img width="1919" alt="CSV Upload Interface" src="https://github.com/user-attachments/assets/fc3a6177-22f8-41ee-bf50-157fea60d166" />

### Performance Metrics
<img width="1919" alt="Model Metrics Dashboard" src="https://github.com/user-attachments/assets/4662683b-cb48-4e42-8e53-cd0214537613" />

### Fairness Analysis
<img width="830" alt="Fairness Metrics" src="https://github.com/user-attachments/assets/4d5864a6-4125-4e61-86df-eb4d41533507" />

### Results Visualization
<img width="1919" alt="Results Table" src="https://github.com/user-attachments/assets/33f0d466-db55-4c11-a1b9-64e5fb1d5ba5" />

</div>

## 🛠 Technology Stack

### **Backend**
- **Framework**: Flask 2.0+ with CORS support
- **ML Engine**: XGBoost, Scikit-learn, Pandas, NumPy
- **Fairness Library**: Fairlearn, AIF360
- **Model Serialization**: Joblib
- **Data Processing**: Pandas, NumPy

### **Frontend**
- **UI Framework**: Vanilla JavaScript with modern ES6+
- **Styling**: Tailwind CSS 3.0+
- **Visualization**: Chart.js for interactive charts
- **Design**: Responsive, mobile-first architecture

### **Infrastructure**
- **Deployment**: Render.com (Production: `https://grabhack-project-nova.onrender.com`), Local development
- **Data Storage**: CSV-based with audit logging
- **API**: RESTful design with JSON responses
- **CORS**: Enabled for cross-origin requests

## Quick Start

### Prerequisites

Ensure you have Python 3.8+ installed:

```bash
python --version  # Should be 3.8+
pip --version
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ANAS727189/GrabHack-Project-Nova.git
cd GrabHack-Project-Nova
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Prepare training data**
   - The system includes `catalyst_train.csv` with 10,000+ synthetic records
   - For custom datasets, ensure CSV follows the required schema (see [Data Features](#-data-features))

### Running the Application

#### Option 1: Full Application (Recommended)
```bash
python main.py
```
- Trains model automatically on startup
- Starts Flask server on `http://127.0.0.1:5000`
- Open `index.html` in your browser (or serve on port 5500+ via Live Server)

#### Option 2: Pre-trained Model Server
```bash
# First, train and export the model
python train_and_export_model.py

# Then run the lightweight server
python app.py
```

#### Option 3: Interactive Mode
```bash
# Single prediction with user input
python main-ask.py

# Batch processing mode
python main-many.py
```

### Usage

1. **Start the backend server**: Run `python main.py` (starts on `http://127.0.0.1:5000`)
2. **Open the web interface**: 
   - **Option A**: Double-click `index.html` to open in browser
   - **Option B**: Use Live Server extension in VS Code (typically serves on `http://127.0.0.1:5500`)
3. **Choose prediction mode**:
   - **Single Entry**: Fill the form with partner details
   - **Upload CSV**: Use sample files like `user_input_many.csv`
4. **View results** with model confidence and fairness metrics

### Troubleshooting

#### **Port Configuration & Common Issues**

**Understanding the Setup:**
- **Backend API**: Runs on `http://127.0.0.1:5000` (Flask server with `/predict` and `/predict_csv` endpoints)
- **Frontend**: Serves on different port (e.g., `http://127.0.0.1:5500` via Live Server)
- **Communication**: Frontend makes API calls to backend on port 5000

**Recommended Development Setup:**
```bash
# Terminal 1: Start the backend
python main.py
# Should show: "Running on http://127.0.0.1:5000"

# Terminal 2 or VS Code: Serve the frontend
# Use Live Server extension or open index.html directly
# Frontend typically runs on http://127.0.0.1:5500
```

## Architecture

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API     │    │   ML Pipeline   │
│   (index.html)  │────│   (main.py)     │────│   (XGBoost)     │
│                 │    │                 │    │                 │
│ • Form UI       │    │ • /predict      │    │ • Data Prep     │
│ • CSV Upload    │    │ • /predict_csv  │    │ • Model Train   │
│ • Visualizations│    │ • CORS Support  │    │ • Predictions   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                        ┌─────────────────┐
                        │   Data Layer    │
                        │                 │
                        │ • Training CSV  │
                        │ • Audit Logs    │
                        │ • Model Assets  │
                        └─────────────────┘
```

### File Structure

```
GrabHack-Project-Nova/
├── Frontend
│   └── index.html                      # Main web interface
├── Backend APIs
│   ├── main.py                         # Primary Flask application
│   ├── app.py                          # Lightweight pre-trained model server
│   ├── main-ask.py                     # Interactive single prediction
│   └── main-many.py                    # Batch processing script
├── ML Pipeline
│   ├── train_and_export_model.py       # Model training and export
│   ├── dataset.py                      # Synthetic data generation
│   └── model.pkl                       # Trained model (generated)
├── Data Assets
│   ├── catalyst_train.csv              # Training dataset (10K+ records)
│   ├── catalyst_test.csv               # Test dataset
│   ├── user_input.csv                  # Single prediction sample
│   ├── user_input_many.csv             # Bulk prediction sample
│   └── online_testcases.csv            # Audit log (generated)
├── Model Artifacts
│   ├── xgboost_credit_model.joblib     # Serialized XGBoost model
│   ├── train_features_columns.joblib   # Feature schema
│   └── evaluation_metrics.joblib       # Performance metrics
├── Configuration
│   ├── requirements.txt                # Python dependencies
│   ├── metadata.txt                    # Model metadata
│   └── README.md                       # This file
└── Documentation
    ├── CODE_OF_CONDUCT.md              # Community guidelines
    └── Contribute.md                   # Contribution guide
```

## API Documentation

### Endpoints

> - For **local development**: `http://127.0.0.1:5000`
> - For **production**: `https://grabhack-project-nova.onrender.com`

#### `POST /predict`
**Single partner eligibility prediction**

**Production URL**: `https://grabhack-project-nova.onrender.com/predict`
**Local URL**: `http://127.0.0.1:5000/predict`

**Request Body:**
```json
{
  "Partner Type": "Merchant",
  "Earnings (Value)": 2500,
  "Earnings (Stability Type)": "Stable",
  "Perf. Rating (Avg)": 4.5,
  "Time on Platform (Months)": 24,
  "Order/Trip Volume": 450,
  "Financial Activity (Score)": 0.75,
  "Earnings Volatility": 0.15,
  "On-Time Loan Repayments": 12,
  "Operational Anomaly Score": 0.08
}
```

**Response:**
```json
{
  "prediction": "Eligible",
  "metrics": {
    "accuracy": 0.9890,
    "precision": 0.9892,
    "recall": 0.9892,
    "f1_score": 0.9892
  }
}
```

#### `POST /predict_csv`
**Bulk prediction from CSV upload**

**Production URL**: `https://grabhack-project-nova.onrender.com/predict_csv`
**Local URL**: `http://127.0.0.1:5000/predict_csv`

**Request:** Multipart form data with CSV file

**Response:**
```json
{
  "predictions": [
    {
      "Partner ID": "00001",
      "Partner Type": "Driver",
      "Earnings (Value)": 1800,
      "Earnings (Stability Type)": "Stable",
      "Perf. Rating (Avg)": 4.5,
      "Time on Platform (Months)": 27,
      "Order/Trip Volume": 447,
      "Financial Activity (Score)": 0.6,
      "Earnings Volatility": 0.1,
      "On-Time Loan Repayments": 12,
      "Operational Anomaly Score": 0.03,
      "Creditworthy_Prediction": "Eligible"
    }
  ],
  "metrics": {
    "accuracy": 0.9890,
    "precision": 0.9892,
    "recall": 0.9892,
    "f1_score": 0.9892
  },
  "fairness_metrics": {
    "selection_rate": {
      "Driver": 0.72,
      "Merchant": 0.68
    },
    "equal_opportunity": {
      "Driver": 0.94,
      "Merchant": 0.91
    }
  },
  "fairness_observation": "Driver group approval rate is 4.00% higher than Merchant group."
}
```

### Input Validation

The API includes comprehensive validation:
- **Range Checks**: Earnings (0-100,000), Number of Trips (0-1,000)
- **Type Validation**: Categorical values from predefined sets
- **Data Sanitization**: SQL injection and XSS prevention
- **Schema Validation**: Required fields and data types
- **Business Rules**: Partner type validation, performance rating bounds (1.0-5.0)
- **Score Validation**: Financial Activity Score and Volatility (0.0-1.0)

## Data Features

### Input Schema

| Feature | Type | Description | Example Values |
|---------|------|-------------|----------------|
| `Partner Type` | Categorical | Business relationship | `"Merchant"`, `"Driver"` |
| `Earnings (Value)` | Numeric | Monthly earnings (USD) | `500 - 50000` |
| `Earnings (Stability Type)` | Categorical | Income consistency | `"Stable"`, `"Variable"`, `"Seasonal"` |
| `Perf. Rating (Avg)` | Numeric | Platform performance score | `1.0 - 5.0` |
| `Time on Platform (Months)` | Numeric | Partnership duration | `1 - 120` |
| `Order/Trip Volume` | Numeric | Monthly transaction count | `10 - 2000` |
| `Financial Activity (Score)` | Numeric | Financial engagement metric | `0.0 - 1.0` |
| `Earnings Volatility` | Numeric | Income stability coefficient | `0.0 - 1.0` |
| `On-Time Loan Repayments` | Numeric | Historical repayment count | `0 - 50` |
| `Operational Anomaly Score` | Numeric | Risk assessment metric | `0.0 - 1.0` |

### Target Variable

- **`Creditworthy`**: Binary classification (`0` = Not Eligible, `1` = Eligible)

## Model Performance

### Current Metrics (Training Set Performance)

| Metric | Score | Description |
|--------|-------|-------------|
| **Accuracy** | 98.9% | Overall correct predictions |
| **Precision** | 98.9% | True positives / All positive predictions |
| **Recall** | 98.9% | True positives / All actual positives |
| **F1-Score** | 98.9% | Harmonic mean of precision and recall |

### Fairness Metrics

The system monitors fairness across partner types:
- **Selection Rate Parity**: Ensures equal approval rates
- **Equal Opportunity**: Monitors true positive rates across groups
- **Demographic Parity**: Tracks prediction distributions

### Model Features

- **Algorithm**: XGBoost Classifier with hyperparameter optimization
- **Training Size**: 10,000+ synthetic records based on real-world patterns
- **Validation**: 80/20 train-test split with stratification
- **Feature Engineering**: One-hot encoding for categorical variables
- **Regularization**: Built-in L1/L2 regularization in XGBoost

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](Contribute.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request


## 👥 Authors & Acknowledgments

- **AyushMann29** - *Project Lead & Development* - [GitHub](https://github.com/AyushMann29)

<div align="center">

**🌟 Star this repository if you found it helpful!**

[Report Bug](https://github.com/AyushMann29/GrabHack-Project-Nova/issues) • [Request Feature](https://github.com/AyushMann29/GrabHack-Project-Nova/issues)

</div>
