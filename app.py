from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
db = SQLAlchemy(app)

# Database model for Patient
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    chronic_conditions = db.Column(db.String(200), nullable=False)
    input_data = db.Column(db.JSON, nullable=False)

# Function to stratify risk
def stratify_risk(patient_data):
    # Dummy model - replace with your trained model
    model = LogisticRegression()
    # Assume patient_data is a DataFrame with relevant features
    features = patient_data[['age', 'some_other_features']]
    return model.predict(features)

# Route for patient input
@app.route('/api/patient', methods=['POST'])
def add_patient():
    data = request.json
    new_patient = Patient(
        name=data['name'],
        age=data['age'],
        chronic_conditions=data['chronic_conditions'],
        input_data=data['input_data']
    )
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({"message": "Patient added successfully"}), 201

# Route for risk stratification
@app.route('/api/risk-stratification/<int:patient_id>', methods=['GET'])
def risk_stratification(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    # Convert input data to DataFrame
    patient_data = pd.DataFrame([{
        'age': patient.age,
        'some_other_features': ...  # Extract more features from input_data
    }])
    
    risk_score = stratify_risk(patient_data)
    return jsonify({"patient_id": patient_id, "risk_score": risk_score.tolist()}), 200

# Run the app
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
