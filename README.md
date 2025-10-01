# Nova: Loan Eligibility Checker

Nova is a web-based application that predicts loan eligibility for partners (Merchants and Drivers) using a machine learning model. The system provides a simple user interface for a single-entry prediction or a bulk prediction via a CSV file upload. The backend is a Flask API that serves the predictions, and all user data submitted is logged for future model retraining.
Features

Single-Entry Prediction: Check eligibility for one user by manually entering their data.

Bulk CSV Prediction: Upload a CSV file with multiple user data points to get predictions for all of them.

Model Performance Metrics: Displays key metrics (Accuracy, Precision, Recall, F1-Score) of the trained model.

Data Logging: All submitted data is logged to an online_testcases.csv file, which can be used to retrain and improve the model over time.

## Demo
<img width="1919" height="995" alt="image" src="https://github.com/user-attachments/assets/9d71a554-3d22-46ac-ad6d-5d3394f7cf98" />
<img width="1919" height="993" alt="image" src="https://github.com/user-attachments/assets/5b2f943d-c673-491f-8899-a7aef9b981af" />
<img width="1919" height="993" alt="image" src="https://github.com/user-attachments/assets/fc3a6177-22f8-41ee-bf50-157fea60d166" />
<img width="1919" height="993" alt="image" src="https://github.com/user-attachments/assets/4662683b-cb48-4e42-8e53-cd0214537613" />
<img width="830" height="818" alt="image" src="https://github.com/user-attachments/assets/4d5864a6-4125-4e61-86df-eb4d41533507" />
<img width="1919" height="993" alt="image" src="https://github.com/user-attachments/assets/33f0d466-db55-4c11-a1b9-64e5fb1d5ba5" />


## Technologies Used

Frontend: HTML, JavaScript, and Tailwind CSS

Backend: Python (Flask)

Machine Learning: Scikit-learn, XGBoost, Pandas, NumPy

Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Prerequisites

Make sure you have Python 3.x and pip installed.

python --version
pip --version

## Installation

Clone the repository:

    git clone https://github.com/AyushMann29/GrabHack-Project-Nova
    cd GrabHack-Project-Nova

Then, install the dependencies:

    pip install -r requirements.txt

    Create the training data file. The backend expects a CSV file named catalyst_train.csv to exist in the same directory. You'll need to add your training dataset here.

## Usage

Run the Flask backend server:

    python main.py

Open the frontend in your web browser by navigating to the index.html file located in the root directory.

 Use the application by selecting either the "Single Entry" or "Upload CSV" tab and submitting your data. The predictions and model metrics will be displayed directly on the page.

Project Structure

├── catalyst_train.csv          
├── online_testcases.csv        
├── main.py     
├── index.html                
└── requirements.txt            

Author

Ayush Mann - Initial work - https://github.com/AyushMann29/GrabHack-Project-Nova

## Badges

[![GitHub stars](https://img.shields.io/github/stars/AyushMann29/GrabHack-Project-Nova?style=social)](https://github.com/AyushMann29/GrabHack-Project-Nova/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/AyushMann29/GrabHack-Project-Nova?style=social)](https://github.com/AyushMann29/GrabHack-Project-Nova/network/members)
[![GitHub issues](https://img.shields.io/github/issues/AyushMann29/GrabHack-Project-Nova)](https://github.com/AyushMann29/GrabHack-Project-Nova/issues)
[![License](https://img.shields.io/github/license/AyushMann29/GrabHack-Project-Nova)](https://github.com/AyushMann29/GrabHack-Project-Nova/blob/main/LICENSE)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
