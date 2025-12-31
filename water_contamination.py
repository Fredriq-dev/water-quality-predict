import joblib as jb
import streamlit as st
import sklearn
from openai import OpenAI

model = jb.load('water_quality_model.pkl')

st.title('Water Quality detector')
st.subheader('Enter parameters of the water sample to predict the safety of the water')


pH_value = st.number_input('Enter pH value(0.0-10.0)', min_value=0.0, max_value=10.0)
hardness = st.number_input('Enter Hardness level(100-300)', min_value=100.0, max_value=300.0)
solids = st.number_input('Enter number of Solids(0-50000)', min_value=0.0, max_value=50000.0)
chloramines = st.number_input('Enter Chloramine level(0.0-10.0)', min_value=0.0, max_value=10.0)
sulphate = st.number_input('Enter Sulphate level(100-1000)', min_value=100.0, max_value=1000.0)
conductivity = st.number_input('Enter Conductivity level(100-1000)', min_value=100.0, max_value=1000.0)
organic_carbon = st.number_input('Enter Total organic carbon level(0.0-20.0)', min_value=0.0, max_value=20.0)
tlms = st.number_input('Enter Trihalomethanes level(0.0-100.0)', min_value=0.0, max_value=100.0)
turbidity = st.number_input('Enter Turbidity level(0.0-10.0)', min_value=0.0, max_value=10.0)


if st.button('Predict'):
    newData = [[pH_value,hardness,solids,chloramines,sulphate,conductivity,organic_carbon,tlms,turbidity]]
    prediction = model.predict(newData)

    if prediction == 0:
        st.success('The water is unsafe for drinking and cooking but can be used for other activities')
    elif prediction == 1:
        st.success('The water is safe for drinking and cooking.')


# chatbot
client = OpenAI(api_key=st.secrets['OPEN_AI_API_KEY'])

#chat history
messages = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = st.chat_input('Say something')
if prompt:
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message('assistant'):
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({'role': 'assistant', 'content': response})




