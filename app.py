from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np

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
    risk_score = db.Column(db.Float)
    care_plan = db.Column(db.JSON)

# Function to simulate training and return a risk score
def stratify_risk(patient_data):
    # Simulate a trained model using dummy data
    model = LogisticRegression()
    # Dummy data for training the model
    X_train = np.array([[50], [60], [70], [80], [90]])  # Example ages
    y_train = np.array([0, 0, 1, 1, 1])  # Example risk labels (0: low, 1: high)
    model.fit(X_train, y_train)
    
    # Assume patient_data is a DataFrame with relevant features
    features = patient_data[['age']]  # Add more features as necessary
    return model.predict_proba(features)[:, 1]  # Return probability of high risk

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
    return jsonify({"message": "Patient added successfully", "patient_id": new_patient.id}), 201

# Route for risk stratification
@app.route('/api/risk-stratification/<int:patient_id>', methods=['GET'])
def risk_stratification(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient_data = pd.DataFrame([{
        'age': patient.age,
        # Extract additional features from input_data as needed
    }])
    
    risk_score = stratify_risk(patient_data)
    patient.risk_score = risk_score
    db.session.commit()
    
    return jsonify({"patient_id": patient_id, "risk_score": risk_score[0]}), 200

# Route for creating a personalized care plan
@app.route('/api/care-plan/<int:patient_id>', methods=['POST'])
def create_care_plan(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    # Simple logic to create a care plan based on risk score and conditions
    care_plan = {
        "recommendations": [],
        "follow_up_schedule": []
    }
    
    if patient.risk_score > 0.7:
        care_plan["recommendations"].append("Intensive follow-up required.")
        care_plan["follow_up_schedule"].append("Weekly follow-ups recommended.")
    else:
        care_plan["recommendations"].append("Regular monitoring is sufficient.")
        care_plan["follow_up_schedule"].append("Monthly follow-ups recommended.")

    patient.care_plan = care_plan
    db.session.commit()
    
    return jsonify({"patient_id": patient_id, "care_plan": care_plan}), 200

# Route for self-management support
@app.route('/api/self-management/<int:patient_id>', methods=['GET'])
def self_management_support(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    # Provide self-management resources based on conditions
    resources = {
        "education": "Link to chronic condition management resources.",
        "tools": ["Medication reminder app", "Symptom tracker"]
    }
    
    return jsonify({"patient_id": patient_id, "resources": resources}), 200

# Route for monitoring and follow-up
@app.route('/api/follow-up/<int:patient_id>', methods=['GET'])
def follow_up(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    # Generate follow-up schedule based on risk score
    follow_up_schedule = {
        "next_follow_up": "In 1 month" if patient.risk_score <= 0.7 else "In 1 week",
        "reminders": ["Check blood pressure weekly"] if patient.risk_score > 0.7 else ["Check blood pressure monthly"]
    }
    
    return jsonify({"patient_id": patient_id, "follow_up_schedule": follow_up_schedule}), 200

# Route for outcome evaluation
@app.route('/api/outcome-evaluation/<int:patient_id>', methods=['POST'])
def outcome_evaluation(patient_id):
    data = request.json
    patient = Patient.query.get_or_404(patient_id)
    # Implement logic to evaluate outcomes based on data submitted
    evaluation_results = {
        "symptoms_improved": data.get("symptoms_improved", False),
        "medication_adherence": data.get("medication_adherence", False)
    }
    
    # Here, you might store evaluation results in the database or process them further
    return jsonify({"patient_id": patient_id, "evaluation_results": evaluation_results}), 200

# Route for quality improvement feedback
@app.route('/api/quality-improvement/<int:patient_id>', methods=['POST'])
def quality_improvement(patient_id):
    data = request.json
    patient = Patient.query.get_or_404(patient_id)
    feedback = {
        "patient_feedback": data.get("feedback"),
        "suggestions": data.get("suggestions")
    }
    # Here you would implement logic to collect feedback and implement improvements
    return jsonify({"patient_id": patient_id, "feedback_received": True, "feedback": feedback}), 200

# Run the app
if __name__ == '__main__':
    db.create_all()  # Creates the database if it doesn't exist
    app.run(debug=True)
