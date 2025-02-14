import json
from xai_assistant_cls import XAIAssistant
from icecream import ic
import streamlit as st
import os
import datetime
import uuid
from utils import clean_latex_formatting, save_state_json
from welcome import welcome_page
#from survey import survey
from german_survey import survey
from chat import chat_page
from images import get_images
from decision_popover import decision
from thanks import thank_you_page
from config import ASSISTANT_ID
from images import save_upload_images
from sciebo_uploader import Sciebo

#
# def set_page_styling():
#     st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
#
#     html, body, [class*="css"]  {
#         font-family: 'Roboto', sans-serif;
#     }
#
#     .stTextInput, .stNumberInput, .stSelectSlider {
#         margin-bottom: 20px;
#     }
#
#     .stTextInput input, .stNumberInput input {
#         padding: 10px;
#         border: 1px solid #ddd;
#         border-radius: 4px;
#     }
#
#     .stSelectSlider {
#         padding: 10px 0;
#     }
#     .StyledThumbValue.st-emotion-cache-132r2mp.ew7r33m2 {
#         font-family: 'Roboto', sans-serif;
#         color: darkgrey;
#     }
#
#     .st-emotion-cache-1inwz65.ew7r33m0 {
#         font-family: 'Roboto', sans-serif;
#         color: darkgrey.
#     }
#
#     .st-emotion-cache-1s3l9q9.e1nzilvr5 {
#         font-family: 'Roboto', sans-serif;
#         color: black.
#     }
#
#     .stButton button:hover {
#         background-color: #45a049.
#     }
#
#     h1 {
#         font-weight: 700.
#     }
#
#     label {
#         font-weight: 400.
#         color: #333.
#     }
#     </style>
#     """, unsafe_allow_html=True)
#

def initialize(image_path):
    if "user_uuid" not in st.session_state:
        #set_page_styling()
        user_uuid = str(uuid.uuid4())
        start_time = datetime.datetime.now().isoformat()

        if not "assistant" in st.session_state:
            if os.environ.get("SMOKE_TEST"):
                st.session_state["assistant"] = None
            else:
                st.session_state["assistant"] = XAIAssistant(assistant_id=ASSISTANT_ID)
            # Initialize the assistant
            survey_data = st.session_state.get("survey", {})
            st.session_state["assistant"].frame_with_survey_data(survey_data)

        assistant = st.session_state["assistant"]
        print(f'Selected Image path during AI intialization: {image_path}')

        assistant_response = assistant.initialize_assistant(image_path)
        # Store the assistant's response or any other relevant information in the session state
        st.session_state["user_uuid"] = user_uuid
        st.session_state["start_time"] = start_time
        st.session_state["assistant_response"] = assistant_response
        st.session_state["saved_image"] = image_path

        #save_state_json()


def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "welcome"

    if st.session_state["page"] == "welcome":
        welcome_page()

    elif st.session_state["page"] == "survey":
        survey()
        save_state_json()
    elif st.session_state["page"] == "chat":
        survey_data = st.session_state.get("survey", {})
        skin_color = survey_data.get("skin_color", "default")  # Assuming "skin_color" is the key for the skin color data
        #image_path = get_images(skin_color)
        if 'file_uploaded' not in st.session_state:
                st.session_state['file_uploaded'] = False

        #this is a the chat container with only title , header and image uploader
        with st.container():
                print('Inside chat page container with only title , header and image uploader')
                st.title("🤖 Medical Diagnostic Assistant")
                #col1, col2 = st.columns([1, 1]) #making two columns one for image upload and one for camera input
                st.subheader("Diagnose your skin condition with the Medical Assistant", divider="gray")
                image_placeholder=st.empty() #this is a placeholder for image upload
                with image_placeholder:
                    print('inside image placeholder')
                    #uploaded_file_1 = st.file_uploader("Upload from Files", type=["png", "jpg", "jpeg"])
                    uploaded_file_1=st.camera_input("Upload your Image here",label_visibility="collapsed")
                    if uploaded_file_1:
                         st.session_state["file_uploaded"] = True

                    uploaded_file=uploaded_file_1


                    if uploaded_file:
                        print('before save upload images')
                        save_upload_images(uploaded_file) #saved image into uploaded_images folder
                        image_path = st.session_state["saved_image"] #update state.saved_image with image path
                        initialize(image_path)  #Pass the image path during initialization
        if st.session_state['file_uploaded']:
            st.subheader("Describe your situation to the assistant. You can also book an appointment with our doctor", divider="grey")
            decision() #this loads the chat and buttons
            image_placeholder.empty()
            chat_page()

            save_state_json()
    elif st.session_state["page"] == "thanks":
        image_path = st.session_state["saved_image"]
        uuid = st.session_state.get("user_uuid")
        Sciebo.upload_image(image_path,uuid)
        Sciebo.upload_state_data(uuid)
        save_state_json()
        thank_you_page()


if __name__ == "__main__":
    main()
