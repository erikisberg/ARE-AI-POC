import streamlit as st
import requests
import datetime
import json

today = datetime.datetime.now()
next_year = today.year + 1
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

# Streamlit UI Components
st.title("Åre Destination AI-POC")
st.subheader("Planera ditt besök i Åre med hjälp av AI")
st.write("Berätta mer om din vistelse i Åre och ditt sällskap så hjälper vi dig att hitta rätt aktiviteter och upplevelser.")
user_input = st.text_area("Berätta om din semester och vad ni vill göra i Åre...")
st.markdown("""
* _Aa_
* _Aa_
* _Aa_
""", unsafe_allow_html=True)
number_of_people = st.slider('Hur många personer är det i ert sällskap?', min_value=1, max_value=30)
d = st.date_input(
    "När kommer ni till Åre?",
    value=(jan_1, datetime.date(next_year, 1, 7)),
    min_value=jan_1,
    max_value=dec_31,
    format="DD.MM.YYYY",
)

st.write('Anländer:', d)
st.divider()
submit_button = st.button("Skicka")

# POST Request API
def send_post_request(input_text, workout_length, number_of_people, arrival_date):
    url = "https://api.retool.com/v1/workflows/49b9ad64-b79c-4433-8dbc-d591e1016fa7/startTrigger?workflowApiKey=retool_wk_8f83ae0a17bb46d0a45ee6382cece909"
    headers = {'Content-Type': 'application/json'}
    data = {
        "body": input_text, 
        "workout_length": workout_length, 
        "number_of_people": number_of_people, 
        "arrival_date": arrival_date.strftime("%Y-%m-%d")  # Assuming arrival_date is a datetime object
    }
    
    with st.spinner('Vi letar aktiviteter och rekommendationer...'):
        response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()

        data_field = response_data.get("data", "")
        
        return data_field
    else:
        return "Error in API response"

# Button Click
if submit_button:
    if user_input:
        data_field = send_post_request(user_input, workout_length, number_of_people, d[0])
        st.write("Response Data:")
        st.write(data_field)
    else:
        st.error("Du måste ju skriva något...")