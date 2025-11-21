import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import os

st.title("Testimonial Generator")

# Load Excel
excel_path = "students_storage.xlsx"
if os.path.exists(excel_path):
    df = pd.read_excel(excel_path, engine="openpyxl")
else:
    df = pd.DataFrame(columns=["Serial", "ID", "Name", "Father", "Mother", "Class", "Session", "DOB"])

# Form input
st.subheader("Student Details")
with st.form("student_form"):
    sn = st.text_input("S/N", value=str(len(df)+1))
    date = st.text_input("Date (DD/MM/YYYY)", value=datetime.today().strftime("%d/%m/%Y"))
    student_id = st.text_input("ID No")
    student_class = st.text_input("Class")
    session = st.text_input("Session")
    name = st.text_input("Student Name")
    father = st.text_input("Father's Name")
    mother = st.text_input("Mother's Name")
    dob = st.text_input("DOB (DD/MM/YYYY)")
    gender = st.selectbox("Gender", ["Male", "Female"])
    submitted = st.form_submit_button("Generate PDF")
    
if submitted:
    if not all([sn, date, student_id, name]):
        st.warning("Please fill at least S/N, Date, ID and Name.")
    else:
        # Add/update Excel
        df.loc[df["ID"]==student_id, :] = [sn, student_id, name, father, mother, student_class, session, dob]
        df.to_excel(excel_path, index=False, engine="openpyxl")
        
        # Generate PDF
        pdf_path = f"testimonial_{student_id}.pdf"
        c = canvas.Canvas(pdf_path, pagesize=A4)
        W,H = A4
        c.drawString(50, H-50, f"Testimonial Certificate for {name}")
        c.save()
        st.success(f"PDF Generated: {pdf_path}")
        st.download_button("Download PDF", pdf_path)
