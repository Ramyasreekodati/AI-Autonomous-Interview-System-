import sys
import PyPDF2
import pandas as pd

def extract_pdf(file_path):
    try:
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages):
                text += f"\n--- Page {i+1} ---\n"
                text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF {file_path}: {e}"

def extract_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        return df.to_string()
    except Exception as e:
        return f"Error reading Excel {file_path}: {e}"

print("=== 5 week implementation plan.pdf ===")
print(extract_pdf("5 week implementation plan.pdf"))

print("\n\n=== Document 4.pdf ===")
print(extract_pdf("Document 4.pdf"))

print("\n\n=== Task Distribution.xlsx ===")
print(extract_excel("Task Distribution.xlsx"))
