import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import ttkbootstrap as tb


class DiagnosticAgentGUI:
    def __init__(self, data_path):
        # Load and preprocess data
        self.data = pd.read_csv(data_path)
        self.symptoms = list(self.data.columns[:-1])
        self.conditions = list(self.data[self.data.columns[-1]].unique())

        # Calculate probabilities
        self.prior_probs = self.calculate_prior_probs()
        self.conditional_probs = self.calculate_conditional_probs()

        # Setup main window with dark theme
        self.root = tb.Window(themename="darkly")  # Using a dark theme
        self.root.title("Diagnostic Agent")
        self.root.geometry("700x600")

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
        self.root.bind('<Left>', lambda event: self.record_symptom(1))
        self.root.bind('<Right>', lambda event: self.record_symptom(0))
        self.root.bind('<End>', lambda event: self.show_final_diagnosis())

    def setup_gui(self):
        # Main container frame
        container = ttk.Frame(self.root, padding=20)
        container.pack(expand=True, fill="both")

        # Question Label
        self.question_label = ttk.Label(
            container,
            text="",
            wraplength=500,
            font=("Helvetica", 16, "bold"),
            anchor="center",
            style="info.TLabel"
        )
        self.question_label.pack(pady=20)

        # Button Frame
        button_frame = ttk.Frame(container)
        button_frame.pack(pady=10)

        # Yes Button
        self.yes_button = ttk.Button(
            button_frame,
            text="Yes (Left Arrow)",
            command=lambda: self.record_symptom(1),
            style="success.TButton",
            width=20
        )
        self.yes_button.pack(side=tk.LEFT, padx=10)

        # No Button
        self.no_button = ttk.Button(
            button_frame,
            text="No (Right Arrow)",
            command=lambda: self.record_symptom(0),
            style="danger.TButton",
            width=20
        )
        self.no_button.pack(side=tk.LEFT, padx=10)

        # End Questionnaire Button
        self.end_button = ttk.Button(
            button_frame,
            text="End Questionnaire (End Key)",
            command=self.show_final_diagnosis,
            style="warning.TButton",
            width=25
        )
        self.end_button.pack(side=tk.LEFT, padx=10)

        # Results Frame
        self.results_frame = ttk.Frame(container)
        self.results_frame.pack(pady=10, expand=True, fill="both")

        # Start the diagnostic process
        self.ask_next_question()

    def ask_next_question(self):
        next_symptom = self.select_next_question(self.asked_symptoms)
        if next_symptom is None:
            self.show_final_diagnosis()
            return
        formatted_symptom = next_symptom.replace('_', ' ').capitalize()
        self.question_label.config(text=f"Do you have {formatted_symptom}?")

    def record_symptom(self, value):
        if (self.yes_button['state'] == tk.DISABLED or
                self.no_button['state'] == tk.DISABLED):
            return
        current_symptom = self.select_next_question(self.asked_symptoms)
        if current_symptom is None:
            return
        self.observed_symptoms[current_symptom] = value
        self.asked_symptoms.add(current_symptom)
        probabilities = self.infer_condition(self.observed_symptoms)
        most_likely_condition = max(probabilities, key=probabilities.get)
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        current_result_label = ttk.Label(
            self.results_frame,
            text=f"Most likely condition: {most_likely_condition}\n" +
                 f"Probability: {probabilities[most_likely_condition]:.2f}",
            font=("Helvetica", 12),
            style="info.TLabel"
        )
        current_result_label.pack()
        self.ask_next_question()

    def show_final_diagnosis(self):
        self.yes_button.config(state=tk.DISABLED)
        self.no_button.config(state=tk.DISABLED)
        self.end_button.config(state=tk.DISABLED)
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        probabilities = self.infer_condition(self.observed_symptoms)
        sorted_conditions = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
        self.question_label.config(text="Final Diagnosis")
        columns = ('Condition', 'Probability')
        results_tree = ttk.Treeview(self.results_frame, columns=columns, show='headings')
        results_tree.heading('Condition', text='Condition')
        results_tree.heading('Probability', text='Probability')
        results_tree.column('Condition', width=400, anchor='w')
        results_tree.column('Probability', width=100, anchor='e')
        for condition, prob in sorted_conditions:
            results_tree.insert('', 'end', values=(condition, f"{prob:.4f}"))
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=results_tree.yview)
        results_tree.configure(yscroll=scrollbar.set)
        results_tree.pack(side=tk.LEFT, expand=True, fill='both')
        scrollbar.pack(side=tk.RIGHT, fill='y')

    def run(self):
        self.root.mainloop()


# Usage
if __name__ == "__main__":
    agent_gui = DiagnosticAgentGUI('symbipredict_2022.csv')
    agent_gui.run()