import random
import logging
from typing import Dict, List, Tuple
from datetime import datetime


class MedicalDiagnosticPrediction:
    def __init__(self):
        """
        Initialize the Medical Diagnostic Prediction system with enhanced diagnostics
        and safety features.
        """
        # Enhanced illness definitions with weighted symptoms
        self.illnesses = {
            "Upper Respiratory Tract Infection": {
                "symptoms": {
                    "cough": 3,
                    "sore throat": 3,
                    "runny nose": 2,
                    "fever": 3,
                    "fatigue": 2
                },
                "risk_factors": ["close contact with sick people", "weakened immune system"]
            },
            "Hypertension": {
                "symptoms": {
                    "headaches": 2,
                    "dizziness": 3,
                    "blurred vision": 2,
                    "shortness of breath": 3
                },
                "risk_factors": ["age over 40", "family history", "obesity"]
            },
            "Digestive Issues": {
                "symptoms": {
                    "nausea": 2,
                    "abdominal pain": 3,
                    "excessive thirst": 3,
                    "frequent urination": 3,
                    "unexplained weight loss": 2
                },
                "risk_factors": ["family history of diabetes", "sedentary lifestyle"]
            },
            "Allergies": {
                "symptoms": {
                    "sneezing": 2,
                    "itchy eyes": 2,
                    "rash": 3,
                    "runny nose": 2,
                    "swelling": 3
                },
                "risk_factors": ["seasonal changes", "environmental exposure"]
            },
            "Mental Health Conditions": {
                "symptoms": {
                    "anxiety": 3,
                    "depression": 3,
                    "fatigue": 2,
                    "difficulty concentrating": 2,
                    "insomnia": 3
                },
                "risk_factors": ["chronic stress", "traumatic experiences"]
            }
        }

        # Configure logging
        logging.basicConfig(
            filename='medical_diagnostic_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )

    def validate_input(self, response: str) -> bool:
        """
        Validate user input to ensure only valid responses.

        Args:
            response (str): User's input response

        Returns:
            bool: Whether the input is valid
        """
        return response.lower() in ['yes', 'no']

    def get_validated_input(self, question: str) -> str:
        """
        Continuously prompt user until valid input is received.

        Args:
            question (str): Question to be asked

        Returns:
            str: Validated user response
        """
        while True:
            response = input(f"{question} (yes/no): ").strip()
            if self.validate_input(response):
                return response.lower()
            print("Invalid input. Please respond with 'yes' or 'no'.")

    def calculate_diagnosis_score(self, user_symptoms: Dict[str, int]) -> List[Tuple[str, float]]:
        """
        Calculate diagnostic scores with more nuanced probability assessment.

        Args:
            user_symptoms (Dict[str, int]): Symptoms reported by user

        Returns:
            List[Tuple[str, float]]: Ranked illnesses with their scores
        """
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
        """
        Log diagnostic session for record-keeping and potential future analysis.

        Args:
            user_symptoms (Dict[str, int]): Symptoms reported
            results (List[Tuple[str, float]]): Diagnostic results
        """
        log_entry = f"\nDiagnostic Session: {datetime.now()}\n"
        log_entry += f"Reported Symptoms: {user_symptoms}\n"
        log_entry += "Top Potential Diagnoses:\n"
        for illness, score in results[:3]:
            log_entry += f"- {illness}: {score:.2f}\n"

        logging.info(log_entry)

    def medical_diagnostic_prediction(self):
        """
        Main diagnostic prediction method with comprehensive symptom assessment.
        """
        print("\n===== Medical Diagnostic Prediction System =====")
        print("Disclaimer: This is a preliminary screening tool.")
        print("Always consult a healthcare professional for accurate diagnosis.\n")

        user_symptoms = {}

        # Comprehensive symptom questionnaire
        symptom_questions = [
            ("Do you have a persistent cough?", "cough"),
            ("Are you experiencing a sore throat?", "sore throat"),
            ("Do you have headaches?", "headaches"),
            ("Are you feeling dizzy?", "dizziness"),
            ("Have you noticed unexplained weight changes?", "unexplained weight loss"),
            # Add more targeted questions
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
        print("\n===== Preliminary Diagnostic Assessment =====")
        for illness, score in diagnostic_results[:3]:
            print(f"{illness}: Potential Match (Confidence: {score:.2f})")
            risk_factors = self.illnesses[illness]["risk_factors"]
            print(f"  Risk Factors: {', '.join(risk_factors)}\n")

        print("IMPORTANT: These results are NOT a definitive diagnosis.")
        print("Consult a healthcare professional for comprehensive medical advice.")


def main():
    """
    Main function to run the Medical Diagnostic Prediction system.
    """
    try:
        mdp = MedicalDiagnosticPrediction()
        mdp.medical_diagnostic_prediction()
    except Exception as e:
        logging.error(f"Critical system error: {e}")
        print("An unexpected error occurred. Please try again or contact support.")


if __name__ == "__main__":
    main()