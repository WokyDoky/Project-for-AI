import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import numpy as np


class DiagnosticAgentGUI:
    def __init__(self, data_path):
        # Load and preprocess data
        self.data = pd.read_csv(data_path)
        self.symptoms = list(self.data.columns[:-1])
        self.conditions = list(self.data[self.data.columns[-1]].unique())

        # Calculate probabilities
        self.prior_probs = self.calculate_prior_probs()
        self.conditional_probs = self.calculate_conditional_probs()

        # Setup main window
        self.root = tk.Tk()
        self.root.title("Diagnostic Agent")
        self.root.geometry("600x500")

        # Symptom tracking
        self.observed_symptoms = {}
        self.asked_symptoms = set()

        # Create GUI elements
        self.setup_gui()

        # Add keyboard bindings
        self.setup_keyboard_bindings()

    def calculate_prior_probs(self):
        return self.data[self.data.columns[-1]].value_counts(normalize=True).to_dict()

    def calculate_conditional_probs(self):
        conditional_probs = {}
        for condition in self.conditions:
            condition_data = self.data[self.data[self.data.columns[-1]] == condition]
            conditional_probs[condition] = (condition_data[self.symptoms].sum(axis=0) / len(condition_data)).to_dict()
        return conditional_probs

    def infer_condition(self, observed_symptoms):
        probabilities = {}
        for condition in self.conditions:
            prob = self.prior_probs[condition]
            for symptom, value in observed_symptoms.items():
                if value == 1:
                    prob *= self.conditional_probs[condition].get(symptom, 1e-6)
                elif value == 0:
                    prob *= (1 - self.conditional_probs[condition].get(symptom, 1e-6))
            probabilities[condition] = prob

        # Normalize probabilities
        total_prob = sum(probabilities.values())
        if total_prob == 0:
            return {condition: 1 / len(self.conditions) for condition in self.conditions}

        for condition in probabilities:
            probabilities[condition] /= total_prob

        return probabilities

    def select_next_question(self, asked_symptoms):
        remaining_symptoms = [symptom for symptom in self.symptoms if symptom not in asked_symptoms]
        if not remaining_symptoms:
            return None

        symptom_variance = {
            symptom: np.var([self.conditional_probs[cond].get(symptom, 0) for cond in self.conditions])
            for symptom in remaining_symptoms
        }
        return max(symptom_variance, key=symptom_variance.get)

    def setup_keyboard_bindings(self):
        # Bind Left Arrow to Yes (1)
        self.root.bind('<Left>', lambda event: self.record_symptom(1))
        # Bind Right Arrow to No (0)
        self.root.bind('<Right>', lambda event: self.record_symptom(0))
        # Bind End key to show final diagnosis
        self.root.bind('<End>', lambda event: self.show_final_diagnosis())

    def setup_gui(self):
        # Question Label
        self.question_label = tk.Label(self.root, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)

        # Keyboard Instructions Label
        self.instructions_label = tk.Label(
            self.root,
            text="Use Left Arrow for Yes, Right Arrow for No, End to finish",
            font=("Arial", 10)
        )
        self.instructions_label.pack(pady=5)

        # Button Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        # Yes Button
        self.yes_button = tk.Button(button_frame, text="Yes (Left Arrow)", command=lambda: self.record_symptom(1),
                                    width=15)
        self.yes_button.pack(side=tk.LEFT, padx=10)

        # No Button
        self.no_button = tk.Button(button_frame, text="No (Right Arrow)", command=lambda: self.record_symptom(0),
                                   width=15)
        self.no_button.pack(side=tk.LEFT, padx=10)

        # End Questionnaire Button
        self.end_button = tk.Button(button_frame, text="End Questionnaire (End Key)", command=self.show_final_diagnosis,
                                    width=20)
        self.end_button.pack(side=tk.LEFT, padx=10)

        # Results Frame
        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack(pady=10, expand=True, fill='both')

        # Start the diagnostic process
        self.ask_next_question()

    def ask_next_question(self):
        # Select next symptom to ask about
        next_symptom = self.select_next_question(self.asked_symptoms)

        if next_symptom is None:
            self.show_final_diagnosis()
            return

        # Update question label
        formatted_symptom = next_symptom.replace('_', ' ').capitalize()
        self.question_label.config(text=f"Do you have {formatted_symptom}?")

    def record_symptom(self, value):
        # Check if buttons are active
        if (self.yes_button['state'] == tk.DISABLED or
                self.no_button['state'] == tk.DISABLED):
            return

        # Get current symptom
        current_symptom = self.select_next_question(self.asked_symptoms)

        if current_symptom is None:
            return

        # Record symptom
        self.observed_symptoms[current_symptom] = value
        self.asked_symptoms.add(current_symptom)

        # Calculate current probabilities
        probabilities = self.infer_condition(self.observed_symptoms)
        most_likely_condition = max(probabilities, key=probabilities.get)

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Show current most likely condition
        current_result_label = tk.Label(
            self.results_frame,
            text=f"Most likely condition: {most_likely_condition}\n" +
                 f"Probability: {probabilities[most_likely_condition]:.2f}",
            font=("Arial", 12)
        )
        current_result_label.pack()

        # Ask next question
        self.ask_next_question()

    def show_final_diagnosis(self):
        # Disable buttons
        self.yes_button.config(state=tk.DISABLED)
        self.no_button.config(state=tk.DISABLED)
        self.end_button.config(state=tk.DISABLED)

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Calculate final probabilities
        probabilities = self.infer_condition(self.observed_symptoms)

        # Sort conditions by probability
        sorted_conditions = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)

        # Show final diagnosis results
        self.question_label.config(text="Final Diagnosis")
        self.instructions_label.config(text="")  # Clear instructions

        # Create a treeview for results
        columns = ('Condition', 'Probability')
        results_tree = ttk.Treeview(self.results_frame, columns=columns, show='headings')
        results_tree.heading('Condition', text='Condition')
        results_tree.heading('Probability', text='Probability')

        # Configure column widths
        results_tree.column('Condition', width=400, anchor='w')
        results_tree.column('Probability', width=100, anchor='e')

        # Insert all conditions with their probabilities
        for condition, prob in sorted_conditions:
            results_tree.insert('', 'end', values=(condition, f"{prob:.4f}"))

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=results_tree.yview)
        results_tree.configure(yscroll=scrollbar.set)

        # Pack treeview and scrollbar
        results_tree.pack(side=tk.LEFT, expand=True, fill='both')
        scrollbar.pack(side=tk.RIGHT, fill='y')

    def run(self):
        self.root.mainloop()


# Usage
if __name__ == "__main__":
    # Replace with your actual data path
    agent_gui = DiagnosticAgentGUI('C:/Users/jdben/Downloads/SymbiPredict/SymbiPredict/symbipredict_2022.csv')
    agent_gui.run()