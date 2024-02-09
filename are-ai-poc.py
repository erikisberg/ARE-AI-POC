import streamlit as st
import requests
import pandas as pd
import datetime
import json

today = datetime.datetime.now()
next_year = today.year
jan_1 = datetime.date(next_year, 1, 1)
dec_31 = datetime.date(next_year, 12, 31)

min_year = 2020
max_year = 2030
min_date = datetime.date(min_year, 1, 1)
max_date = datetime.date(max_year, 12, 31)

# Streamlit UI Components
st.title("Åre Destination AI-POC")
st.subheader("Planera ditt besök i Åre med hjälp av AI")
st.write("Berätta mer om din vistelse i Åre och ditt sällskap så hjälper vi dig att hitta rätt aktiviteter och upplevelser.")
user_input = st.text_area("Vilka är ni och vad vill ni hitta på?")
st.markdown("""
* _Aa_
* _Aa_
* _Aa_
""", unsafe_allow_html=True)
number_of_people = st.slider('Hur många personer är det i ert sällskap?', min_value=1, max_value=30)
arrival_dates = st.date_input(
    "När kommer ni till Åre?",
    value=(jan_1, datetime.date(next_year, 1, 7)),
)
huvudfokus_semester = st.selectbox('Vad är huvudfokus för er semester?', ["Nöjen och äventyr", "Relax och avslappning", "Äldre människor som vill uppleva Åre", "Romantisk getaway med min partner", "Romantik"])
submit_button = st.button('Hitta aktiviteter')

# POST Request API
def send_post_request(input_text, number_of_people, arrival_dates, huvudfokus_semester):
    url = "https://api.retool.com/v1/workflows/b61838af-a3b6-40ee-bbe1-15ea6bc2fbd6/startTrigger?workflowApiKey=retool_wk_548bed49009e4b1e8967211445ce07c9"
    headers = {'Content-Type': 'application/json'}
    data = {
        "body": input_text, 
        "number_of_people": "Beskrivning från användare: " + str(number_of_people), 
        "arrival_start_date": "Datum för ankomst: " + arrival_dates[0].strftime("%Y-%m-%d"),  
        "arrival_and_end_date": "Datum för avfärd: " + arrival_dates[1].strftime("%Y-%m-%d"),  
        "huvudfokus_semester": "Huvudkategori:" + huvudfokus_semester
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
        data_field = send_post_request(user_input, number_of_people, arrival_dates, huvudfokus_semester)
        st.write("Response Data:")
        st.write(data_field)
    else:
        st.error("Du måste ju skriva något...")


st.divider()    
st.title("Lista på URL:er")
# Send GET request to API
url = "https://api.retool.com/v1/workflows/643e51d9-8a0f-4721-b65e-6de2787414f5/startTrigger?workflowApiKey=retool_wk_cbbfe6b6719545999f2eee687382b0f9"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    # Convert the list into a DataFrame
    df = pd.DataFrame(data, columns=["URLs"])

    # Display the data in a table
    st.table(df)
else:
    st.error("Failed to fetch data from API")