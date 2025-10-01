

<div align="center">

<h1>Nova: AI-Powered Loan Eligibility Platform</h1>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-FF6B35?style=for-the-badge)](https://xgboost.readthedocs.io)


[![GitHub stars](https://img.shields.io/github/stars/AyushMann29/GrabHack-Project-Nova?style=social)](https://github.com/AyushMann29/GrabHack-Project-Nova/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/AyushMann29/GrabHack-Project-Nova?style=social)](https://github.com/AyushMann29/GrabHack-Project-Nova/network/members)
[![GitHub issues](https://img.shields.io/github/issues/AyushMann29/GrabHack-Project-Nova)](https://github.com/AyushMann29/GrabHack-Project-Nova/issues)

**An intelligent creditworthiness assessment system for Grab's merchant and driver partners**

</div>

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Live Application Preview](#live-application-preview)
- [Technology Stack](#-technology-stack)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Data Features](#data-features)
- [Model Performance](#model-performance)
- [Contributing](#contributing)
- [Authors & Acknowledgments](#authors--acknowledgments)

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

## Live Application Preview

<div align="center">

### **Interactive Dashboard**
*Clean, intuitive interface designed for financial professionals*

<img width="1919" alt="Nova's main dashboard featuring modern UI with model performance metrics and navigation" src="https://github.com/user-attachments/assets/9d71a554-3d22-46ac-ad6d-5d3394f7cf98" />

<br>

### **Single Partner Assessment** 
*Individual loan eligibility evaluation with instant results*

<img width="1919" alt="User-friendly form interface for entering partner details with real-time validation" src="https://github.com/user-attachments/assets/5b2f943d-c673-491f-8899-a7aef9b981af" />

<br>

### **Enterprise Batch Processing**
*High-volume CSV upload and processing for operational efficiency*

<img width="1919" alt="Professional CSV upload interface with drag-and-drop functionality and progress tracking" src="https://github.com/user-attachments/assets/fc3a6177-22f8-41ee-bf50-157fea60d166" />

<br>

### **Model Performance Analytics**
*Real-time monitoring of ML model accuracy and reliability metrics*

<img width="1919" alt="Comprehensive analytics dashboard showing model performance with accuracy, precision, recall, and F1-score" src="https://github.com/user-attachments/assets/4662683b-cb48-4e42-8e53-cd0214537613" />

<br>

### **AI Fairness & Bias Detection**
*Ethical AI implementation with comprehensive bias monitoring and reporting*

<img width="830" alt="Advanced fairness metrics visualization showing selection rates and equal opportunity across demographic groups" src="https://github.com/user-attachments/assets/4d5864a6-4125-4e61-86df-eb4d41533507" />

<br>

### **Intelligent Results Display**
*Professional data visualization with exportable comprehensive reports*

<img width="1919" alt="Clean, organized results table with prediction outcomes and detailed partner information" src="https://github.com/user-attachments/assets/33f0d466-db55-4c11-a1b9-64e5fb1d5ba5" />

---

</div>

## Technology Stack

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

```bash
python main.py
```
- Trains model automatically on startup
- Starts Flask server on `http://127.0.0.1:5000`
- Open `index.html` in your browser (or serve on port 5500+ via Live Server)


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

## API Documentation

### Base URLs

| Environment | Base URL | Description |
|-------------|----------|-------------|
| **Local Development** | `http://127.0.0.1:5000` | Local Flask development server |
| **Production** | `https://grabhack-project-nova.onrender.com` | Deployed production instance |

---

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

## Contributing

We welcome contributions! Please see our [Contributing Guide](Contribute.md) and [Code of Conduct](CODE_OF_CONDUCT.md).

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit: `git commit -m 'Add amazing feature'`
5. Push: `git push origin feature/amazing-feature`
6. Open a Pull Request


## Contributors

Thanks to all our amazing contributors for their support and code!

<a href="https://github.com/AyushMann29/GrabHack-Project-Nova/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=AyushMann29/GrabHack-Project-Nova" />
</a>

<div align="center">

**🌟 Star this repository if you found it helpful!**

[Report Bug](https://github.com/AyushMann29/GrabHack-Project-Nova/issues) • [Request Feature](https://github.com/AyushMann29/GrabHack-Project-Nova/issues)

</div>
