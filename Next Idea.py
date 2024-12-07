import random
import logging
from typing import Dict, List, Tuple
from datetime import datetime
from tabulate import tabulate
from termcolor import colored


# IMPORTANT INFORMATION
# Please install the following library to run this program
# pip install tabulate termcolor

class MedicalDiagnosticPrediction:
    def __init__(self):
        """
        Initialize the Medical Diagnostic Prediction system with comprehensive illness definitions.
        """
        # Enhanced illness definitions with weighted symptoms
        self.illnesses = {
            # Respiratory
            "Upper Respiratory Tract Infection": {
                "symptoms": {
                    "cough": 3, "sore throat": 3, "runny nose": 2,
                    "fever": 3, "fatigue": 2
                },
                "risk_factors": ["close contact with sick people", "weakened immune system"],
                "description": "A common viral infection affecting the upper respiratory tract."
            },
            "Pneumonia": {
                "symptoms": {
                    "cough": 4, "chest pain": 3, "fever": 3,
                    "difficulty breathing": 4, "chills": 2
                },
                "risk_factors": ["age extremes", "smoking", "weakened immune system"],
                "description": "Infection causing inflammation in the air sacs of the lungs."
            },
            "Chronic Bronchitis": {
                "symptoms": {
                    "persistent cough": 4, "mucus production": 3,
                    "wheezing": 2, "chest discomfort": 3
                },
                "risk_factors": ["smoking", "air pollution exposure", "advanced age"],
                "description": "Long-term inflammation of the bronchial tubes."
            },

            # Cardiovascular
            "Hypertension": {
                "symptoms": {
                    "headaches": 2, "dizziness": 3, "blurred vision": 2,
                    "shortness of breath": 3
                },
                "risk_factors": ["age over 40", "family history", "obesity", "high salt intake"],
                "description": "Chronic condition of elevated blood pressure."
            },
            "Heart Disease": {
                "symptoms": {
                    "chest pain": 4, "shortness of breath": 3,
                    "irregular heartbeat": 3, "fatigue": 2
                },
                "risk_factors": ["high cholesterol", "diabetes", "smoking", "sedentary lifestyle"],
                "description": "Range of conditions affecting heart function."
            },
            "Arrhythmia": {
                "symptoms": {
                    "irregular heartbeat": 4, "dizziness": 3,
                    "fainting": 3, "chest discomfort": 2
                },
                "risk_factors": ["heart disease", "high blood pressure", "stress"],
                "description": "Abnormal heart rhythm or heartbeat pattern."
            },

            # Digestive
            "Digestive Issues": {
                "symptoms": {
                    "nausea": 2, "abdominal pain": 3, "excessive thirst": 3,
                    "frequent urination": 3, "unexplained weight loss": 2
                },
                "risk_factors": ["family history of diabetes", "sedentary lifestyle"],
                "description": "Various conditions affecting the digestive system."
            },
            "Gastroesophageal Reflux Disease (GERD)": {
                "symptoms": {
                    "heartburn": 4, "chest pain": 2, "difficulty swallowing": 3,
                    "chronic cough": 2
                },
                "risk_factors": ["obesity", "smoking", "pregnancy"],
                "description": "Chronic acid reflux condition affecting the digestive tract."
            },
            "Irritable Bowel Syndrome (IBS)": {
                "symptoms": {
                    "abdominal pain": 4, "bloating": 3, "constipation": 2,
                    "diarrhea": 2, "mucus in stool": 2
                },
                "risk_factors": ["stress", "diet", "hormonal changes"],
                "description": "Disorder affecting the large intestine with various symptoms."
            },

            # Neurological
            "Migraine": {
                "symptoms": {
                    "severe headache": 4, "sensitivity to light": 3,
                    "nausea": 2, "visual disturbances": 3
                },
                "risk_factors": ["family history", "stress", "hormonal changes"],
                "description": "Neurological condition causing intense headaches."
            },
            "Multiple Sclerosis": {
                "symptoms": {
                    "vision problems": 3, "numbness": 3, "weakness": 3,
                    "balance issues": 2, "fatigue": 3
                },
                "risk_factors": ["autoimmune conditions", "family history", "age"],
                "description": "Chronic condition affecting the central nervous system."
            },
            "Epilepsy": {
                "symptoms": {
                    "seizures": 4, "temporary confusion": 3,
                    "staring spells": 2, "uncontrollable jerking": 3
                },
                "risk_factors": ["genetic factors", "brain injury", "developmental disorders"],
                "description": "Neurological disorder causing recurrent seizures."
            },

            # Allergies
            "Allergies": {
                "symptoms": {
                    "sneezing": 2, "itchy eyes": 2, "rash": 3,
                    "runny nose": 2, "swelling": 3
                },
                "risk_factors": ["seasonal changes", "environmental exposure", "genetic predisposition"],
                "description": "Immune system response to specific triggers."
            },
            "Lupus": {
                "symptoms": {
                    "joint pain": 3, "skin rash": 3, "fatigue": 3,
                    "fever": 2, "hair loss": 2
                },
                "risk_factors": ["female gender", "autoimmune conditions", "genetic factors"],
                "description": "Chronic autoimmune disease affecting multiple body systems."
            },
            "Rheumatoid Arthritis": {
                "symptoms": {
                    "joint pain": 4, "morning stiffness": 3,
                    "swelling": 3, "fatigue": 2
                },
                "risk_factors": ["age", "family history", "smoking"],
                "description": "Inflammatory disorder affecting joint linings."
            },

            # Mental
            "Mental Health Conditions": {
                "symptoms": {
                    "anxiety": 3, "depression": 3, "fatigue": 2,
                    "difficulty concentrating": 2, "insomnia": 3
                },
                "risk_factors": ["chronic stress", "traumatic experiences", "genetic predisposition"],
                "description": "Various conditions affecting mental and emotional well-being."
            },
            "Generalized Anxiety Disorder": {
                "symptoms": {
                    "excessive worry": 4, "restlessness": 3,
                    "difficulty concentrating": 3, "sleep problems": 2
                },
                "risk_factors": ["stress", "family history", "personality type"],
                "description": "Persistent and excessive anxiety about various things."
            },
            "Depression": {
                "symptoms": {
                    "persistent sadness": 4, "loss of interest": 3,
                    "changes in sleep": 3, "fatigue": 3
                },
                "risk_factors": ["life events", "chemical imbalances", "chronic illness"],
                "description": "Mood disorder causing persistent feelings of sadness."
            },

            # Endocrine
            "Diabetes": {
                "symptoms": {
                    "excessive thirst": 3, "frequent urination": 3,
                    "unexplained weight loss": 3, "fatigue": 2
                },
                "risk_factors": ["obesity", "family history", "age", "sedentary lifestyle"],
                "description": "Metabolic disorder affecting blood sugar regulation."
            },
            "Thyroid Disorders": {
                "symptoms": {
                    "weight changes": 3, "fatigue": 3,
                    "temperature sensitivity": 2, "hair loss": 2
                },
                "risk_factors": ["autoimmune conditions", "family history", "gender"],
                "description": "Conditions affecting thyroid hormone production."
            },

            # Extra
            "Chronic Fatigue Syndrome": {
                "symptoms": {
                    "extreme fatigue": 4, "muscle pain": 3,
                    "sleep problems": 3, "cognitive difficulties": 2
                },
                "risk_factors": ["viral infections", "immune system issues", "hormonal imbalances"],
                "description": "Complex disorder characterized by extreme fatigue."
            }
        }

        # Configure logging
        logging.basicConfig(
            filename='medical_diagnostic_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )

    def validate_input(self, response: str) -> bool:
        """Validate user input to ensure only valid responses."""
        return response.lower() in ['yes', 'no']

    def get_validated_input(self, question: str) -> str:
        """Continuously prompt user until valid input is received."""
        while True:
            response = input(colored(f"{question} (yes/no): ", 'cyan')).strip()
            if self.validate_input(response):
                return response.lower()
            print(colored("Invalid input. Please respond with 'yes' or 'no'.", 'red'))

    def calculate_diagnosis_score(self, user_symptoms: Dict[str, int]) -> List[Tuple[str, float]]:
        """Calculate diagnostic scores with more nuanced probability assessment."""
        illness_scores = {}

        for illness, illness_data in self.illnesses.items():
            score = 0
            for symptom, weight in illness_data["symptoms"].items():
                if symptom in user_symptoms:
                    score += weight * user_symptoms[symptom]

            # Add a random factor to simulate medical uncertainty
            score += random.uniform(0, 1)
            illness_scores[illness] = score

        # Sort illnesses by score in descending order
        ranked_illnesses = sorted(
            illness_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked_illnesses

    def log_diagnostic_session(self, user_symptoms: Dict[str, int], results: List[Tuple[str, float]]):
        """Log diagnostic session for record-keeping and potential future analysis."""
        log_entry = f"\nDiagnostic Session: {datetime.now()}\n"
        log_entry += f"Reported Symptoms: {user_symptoms}\n"
        log_entry += "Top Potential Diagnoses:\n"
        for illness, score in results[:3]:
            log_entry += f"- {illness}: {score:.2f}\n"

        logging.info(log_entry)

    def medical_diagnostic_prediction(self):
        """Main diagnostic prediction method with comprehensive symptom assessment."""
        print(colored("\n===== Medical Diagnostic Prediction System =====", 'green'))
        print(colored("Disclaimer: This is a preliminary screening tool.", 'yellow'))
        print(colored("Always consult a healthcare professional for accurate diagnosis.\n", 'yellow'))

        user_symptoms = {}

        # Comprehensive symptom questionnaire
        symptom_questions = [
            ("Do you have a persistent cough?", "cough"),
            ("Are you experiencing a sore throat?", "sore throat"),
            ("Do you have headaches?", "headaches"),
            ("Are you feeling dizzy?", "dizziness"),
            ("Have you noticed unexplained weight changes?", "unexplained weight loss"),
            ("Are you experiencing chest pain?", "chest pain"),
            ("Do you have joint pain?", "joint pain"),
            ("Are you feeling excessive fatigue?", "fatigue"),
            ("Have you noticed changes in sleep patterns?", "sleep problems"),
            ("Are you experiencing digestive issues?", "abdominal pain"),
            ("Do you have difficulty concentrating?", "difficulty concentrating"),
            ("Are you experiencing muscle weakness?", "weakness"),
            ("Have you noticed vision problems?", "vision problems"),
            ("Do you have frequent urination?", "frequent urination"),
            ("Are you experiencing anxiety or excessive worry?", "anxiety"),
            ("Do you have skin rashes or itching?", "rash"),
            ("Are you experiencing temperature sensitivity?", "temperature sensitivity"),
            ("Do you have swelling in any part of your body?", "swelling"),
            ("Have you noticed any sensory changes like numbness?", "numbness"),
            ("Are you experiencing persistent sadness?", "persistent sadness")
        ]

        for question, symptom in symptom_questions:
            response = self.get_validated_input(question)
            if response == 'yes':
                user_symptoms[symptom] = 1

        # Calculate diagnostic scores
        diagnostic_results = self.calculate_diagnosis_score(user_symptoms)

        # Log the diagnostic session
        self.log_diagnostic_session(user_symptoms, diagnostic_results)

        # Present results
        print(colored("\n===== Preliminary Diagnostic Assessment =====", 'green'))

        table_data = []
        for illness, score in diagnostic_results[:5]:
            risk_factors = ', '.join(self.illnesses[illness]["risk_factors"])
            description = self.illnesses[illness]["description"]
            table_data.append([
                colored(illness, 'cyan'),
                f"{score:.2f}",
                colored(risk_factors, 'yellow'),
                description
            ])

        # Print table
        headers = [
            colored("Potential Diagnosis", 'magenta'),
            colored("Confidence", 'magenta'),
            colored("Risk Factors", 'magenta'),
            colored("Description", 'magenta')
        ]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

        print("\n" + colored("IMPORTANT: These results are NOT a definitive diagnosis.", 'red'))
        print(colored("Consult a healthcare professional for comprehensive medical advice.", 'red'))


def main():
    """Main function to run the Medical Diagnostic Prediction system."""
    try:
        mdp = MedicalDiagnosticPrediction()
        mdp.medical_diagnostic_prediction()
    except Exception as e:
        logging.error(f"Critical system error: {e}")
        print(colored("An unexpected error occurred. Please try again or contact support.", 'red'))


if __name__ == "__main__":
    main()