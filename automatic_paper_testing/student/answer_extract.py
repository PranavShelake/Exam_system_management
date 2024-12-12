import re
import fitz  # PyMuPDF library for extracting text from PDFs

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

def parse_answers_to_mapping(text):

    question_pattern = re.compile(r"^Q(\d+)([a-zA-Z]?)[-]")  # Matches Q1-, Q1a-, Q2-, Q2a-, etc.
   
    lines = text.splitlines()
    answers_mapping = {}
    current_answer = ""
    current_key = None

    for line in lines:
        line = line.strip()
        match = question_pattern.match(line)
       
        if match:  # New question or sub-question detected
            if current_answer and current_key is not None:  # Save previous answer
                answers_mapping[current_key] = current_answer.strip()
           
            question_number = match.group(1)  # Extract main question number (e.g., 1 from Q1)
            subquestion = match.group(2)  # Extract subquestion part (e.g., a from Q1a)
           
            # Generate the new key for the mapping (e.g., "1", "1.1", "2", "2.1", etc.)
            if subquestion:
                current_key = f"{question_number}.{ord(subquestion.lower()) - ord('a') + 1}"
            else:
                current_key = f"{question_number}"
           
            current_answer = line[match.end():].strip()  # Start new answer, exclude the question prefix
        else:  # Continuation of the current answer
            current_answer += " " + line

    # Add the last answer to the mapping
    if current_answer and current_key is not None:
        answers_mapping[current_key] = current_answer.strip()
   
    return answers_mapping

# Example usage
pdf_path = r"C:\Users\prana\Desktop\final project\automatic_paper_testing\media\student_answers\student_answers.pdf"
pdf_text = extract_text_from_pdf(pdf_path)
answers_mapping = parse_answers_to_mapping(pdf_text)

# Print or use the mapping
print(answers_mapping)

