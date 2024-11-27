import fitz
import re

class CurriculumAnalyzer:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = self._extract_text()
        self.skills = []
        self.skill_categories = {
            'Technical Skills': [
                'python', 'java', 'c++', 'javascript', 'html', 'css',
                'react', 'node.js', 'django', 'flask', 'sql', 'machine learning',
                'data analysis', 'tensorflow', 'keras', 'pandas', 'numpy'
            ],
            'Soft Skills': [
                'communication', 'teamwork', 'leadership', 'problem solving',
                'critical thinking', 'adaptability', 'creativity'
            ],
            'Professional Skills': [
                'project management', 'agile', 'scrum', 'customer service',
                'strategic planning', 'analytical skills'
            ]
        }
        self.stop_words = set([
            'the', 'and', 'is', 'in', 'to', 'of', 'a', 'on', 'for', 'with', 'by',
            'at', 'an', 'this', 'that', 'as', 'it', 'from', 'or', 'be', 'are'
        ])

    def _extract_text(self):
        """Extract text from PDF"""
        text = ""
        with fitz.open(self.pdf_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text.lower()

    def analyze_skills(self):
        """Identify skills from the document"""
        # Tokenize and remove stopwords
        words = re.findall(r'\b\w+\b', self.text)
        filtered_words = [word for word in words if word not in self.stop_words]

        # Find matching skills
        found_skills = {}
        for category, skill_list in self.skill_categories.items():
            matched_skills = [skill for skill in skill_list if skill in filtered_words]
            if matched_skills:
                found_skills[category] = matched_skills

        return found_skills

    def calculate_completeness(self):
        """Calculate curriculum completeness"""
        sections = {
            'Education': 0,
            'Experience': 0,
            'Skills': 0,
            'Projects': 0,
            'Achievements': 0
        }

        # Check for sections
        for section in sections.keys():
            if section.lower() in self.text:
                sections[section] = 1

        # Calculate overall completeness
        completeness = sum(sections.values()) / len(sections) * 100
        return completeness, sections

    def generate_recommendations(self):
        """Generate skill recommendations"""
        skills = self.analyze_skills()
        completeness, sections = self.calculate_completeness()

        print("\n===== Curriculum Analysis Report =====")
        print(f"Overall Curriculum Completeness: {completeness:.2f}%")

        print("\n--- Section Completeness ---")
        for section, present in sections.items():
            status = "✓ Present" if present else "✗ Missing"
            print(f"{section}: {status}")

        print("\n--- Identified Skills ---")
        for category, skill_list in skills.items():
            print(f"{category}:")
            for skill in skill_list:
                print(f"  - {skill}")

        print("\n--- Recommendations ---")
        if completeness < 50:
            print("🚨 Your curriculum needs significant improvement!")
        elif completeness < 75:
            print("🟡 Your curriculum is okay, but could use some enhancements.")
        else:
            print("🟢 Your curriculum looks strong!")

        # Suggest missing categories
        missing_sections = [section for section, present in sections.items() if not present]
        if missing_sections:
            print("\nConsider adding these missing sections:")
            for section in missing_sections:
                print(f"  - {section}")


def main():
    # Example usage
    pdf_path = 'ResumeCV.pdf'
    analyzer = CurriculumAnalyzer(pdf_path)
    analyzer.generate_recommendations()


if __name__ == "__main__":
    main()
