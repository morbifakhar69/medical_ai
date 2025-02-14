import streamlit as st
from tipi import calculate_scores
import json

def submit_survey():
    st.session_state["survey_completed"] = True
    st.session_state["tipi_scores"] = calculate_scores(st.session_state["survey"])
    st.session_state["page"] = "chat"

def survey():
    if "survey" not in st.session_state:
        st.session_state["survey"] = {}

    file_path = "questionarre/deutsch_questionarre.json"

    st.title("📋 Survey")
    st.subheader("Demographics", divider='gray')

    # Apply custom CSS for borders
    st.markdown("""
        <style>
        .question-box {
            border: 2px solid #f0f0f0;
            border-radius: 10px;
            background-color: #c5c7c6;
            align: center;
        
        }
        .question-text {
            font:  Helvetica;
            font-weight: bold;
            font-size: 16px;
            color: #000000;
            text-align: left;
            margin: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # User Inputs
    st.text("Please enter your name")
    name = st.text_input("Name", value=st.session_state["survey"].get("name", ""))
    st.text("Please select your age from the dropdown")

    age = st.number_input("Age", value=st.session_state["survey"].get("age", 18), min_value=0, max_value=100)

    st.text("Please select the gender")
    gender = st.radio("Gender", ["Male", "Female"],
                      index=0 if st.session_state["survey"].get("gender", "Male") == "Male" else 1)

    skin_color = st.radio("Skin Color", ["White", "Black"],
                          index=0 if st.session_state["survey"].get("skin_color", "White") == "White" else 1)

    # Load questions from JSON
    questions = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            questions = json.load(file)  # Read JSON file
    except FileNotFoundError:
        st.error("❌ Die Datei wurde nicht gefunden. Bitte überprüfen Sie den Pfad.")
        return
    except json.JSONDecodeError:
        st.error("❌ Fehler beim Laden der JSON-Datei. Bitte überprüfen Sie das Format.")
        return

    # Store responses
    if "responses" not in st.session_state:
        st.session_state["survey"]["responses"] = {}

    st.subheader("Questionnaire", divider='gray')
    st.text("Below there are 14 questions with 4 options each thats fits for you. \nPlease select what is more appropiate for you")
    with st.form(key="questionnaire_form"):

        for idx, q in enumerate(questions):
            # Apply border for each question using HTML & CSS
            st.markdown(f'<div class="question-box">'+f'<p class="question-text">Q{idx + 1}: {q["question"]}</p>', unsafe_allow_html=True)
            #st.markdown(f'<p class="question-text">Q{idx + 1}: {q["question"]}</p>', unsafe_allow_html=True)

            selected_option = st.radio(f"q{idx+1}", q["options"],
                                       index=st.session_state["survey"]["responses"].get(f"q{idx + 1}", 0),
                                       key=f"q{idx + 1}",label_visibility="collapsed")
            st.session_state["survey"]["responses"][f"q{idx + 1}"] = selected_option
            st.subheader("",divider='gray')
            # Closing the box

        # Submit button
        submit_button = st.form_submit_button("Absenden ✉️")

    if submit_button:
        st.session_state["survey"]["name"] = name
        st.session_state["survey"]["age"] = age
        st.session_state["survey"]["gender"] = gender
        st.session_state["survey"]["skin_color"] = skin_color

        st.success("🎉 Vielen Dank für Ihre Antworten!")
        st.write("### Ihre Auswahl:")

        for idx, q in enumerate(questions):
            selected_options = st.session_state["survey"]["responses"].get(f"q{idx + 1}", [])
            st.write(f"**Q{idx + 1}:** {', '.join(selected_options) if selected_options else 'Keine Auswahl'}")

        st.session_state["page"] = "chat"
        st.rerun()
