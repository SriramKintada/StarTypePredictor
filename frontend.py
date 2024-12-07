import streamlit as st
import requests
import pandas as pd
from io import StringIO

# API endpoints
single_predict_url = "https://startype-predictor.onrender.com/predict/"
bulk_predict_url = "https://startype-predictor.onrender.com/bulk_predict/"

st.set_page_config(
    page_title="Star Type Predictor",
    page_icon="https://img.icons8.com/emoji/48/000000/star-emoji.png",  # You can use any online icon URL or a local file path.
)

# Footer Text
footer = """
<div style='position: fixed; left: 0; bottom: 0; width: 100%; background-color: white; text-align: center; padding: 10px;'>
    <p style='color: black; margin: 0;'>Made by <b>Sriram Kintada </b></p>
</div>
"""

# Custom CSS for background
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/5eae36e3-278f-4731-be00-1440d36eca76/d30idy4-9a4a96ed-33be-4941-99c1-8b77adb23288.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9jaiI6W1t7InBhdGgiOiIvZi81ZWFlMzZlMy0yNzhmLTQ3MzEtYmUwMC0xNDQwZDM2ZWNhNzYvZDMwaWR5NC05YTRhOTZlZC0zM2JlLTQ5NDEtOTljMS04Yjc3YWRiMjMyODguanBnIn1dXX0.urB7x7zyDCCRhro0z1HDVMWXZ9HJi9NgdXurlCon43Q");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
[data-testid="stAppViewContainer"] > .main {
    backdrop-filter: blur(5px);
}
</style>
'''

# Inject the background image CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title of the app
st.markdown("<h1 style='color:cyan;'>**** Star Type Predictor  ****</h1>", unsafe_allow_html=True)

# Page selection dropdown
page = st.selectbox("Choose a page:", ["Introduction", "Single Prediction Mode", "Bulk Prediction Mode"])

# Display Introduction Page if selected
if page == "Introduction":
    with st.container():
        st.markdown("""
        <div style='background-color: rgba(255, 235, 235, 0.8); padding: 20px; border-radius: 10px;'>
            <h3 style='color: maroon;'>Introduction to Project</h3>
            <p style='color:black;'><b>This web application helps you predict the type of stars based on their physical parameters. Using machine learning models, we analyze key attributes of stars such as <u>temperature</u>, <u>luminosity</u>, <u>radius</u>, and <u>absolute magnitude</u>, to classify them into different types.</b></p>
        </div>
        """, unsafe_allow_html=True)
    st.text(" ")
    with st.container():
        st.markdown("""
        <div style='background-color: rgba(230, 230, 250, 0.8); padding: 20px; border-radius: 10px;'>
            <h3 style='color: darkblue;'>How to Use This Web Application?</h3>
            <ul style='font-size: 16px; color:black;'>
                <li><strong>Select either Single Prediction Mode or Bulk Prediction Mode from the dropdown.</strong></li>
                <li><strong>Single Prediction can predict the type of a single star based on its properties.</strong></li>
                <li><strong>Bulk Prediction can predict the type of multiple stars based on properties in a CSV file.</strong></li>
                <li><strong>The respective page will guide you on how to use it.</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    st.text(" ")
    with st.container():
        st.markdown("""
        <div style='background-color: rgba(230, 250, 250, 0.8); padding: 20px; border-radius: 10px;'>
            <h3 style='color: darkgreen;'>Important Note</h3>
            <p style='color:black;'><b>If the app was idle for more than 15 minutes, you might face the <a href='https://en.wikipedia.org/wiki/Cold_start_(computing)'>cold start issue.</a></b></p>
        </div>
        """, unsafe_allow_html=True)
    st.text(" ")
    with st.container():
        st.markdown("""
        <div style='background-color: rgba(250, 250, 250, 0.8); padding: 20px; border-radius: 10px;'>
            <h3 style='color: purple;'>Get Started...</h3>
            <p style='color:black;'><b>Choose either the Single or Bulk Prediction mode from the menu to start exploring the stars!</b></p>
        </div>
        """, unsafe_allow_html=True)

# Display Single Prediction Page if selected
elif page == "Single Prediction Mode":
    st.markdown(footer, unsafe_allow_html=True)
    with st.container():
        st.markdown("""
        <div style='background-color: rgba(255, 205, 255, 0.8); padding: 20px; border-radius: 10px;'>
            <h3 style='color: maroon;'>Single Star Type Predictor Mode:</h3>
            <ul style='font-size: 16px; color: black;'>
                <li><strong>Provide properties of the star to predict its type!</strong></li>
                <li><strong>The default values are for the Sun. You can modify these to analyze other stars.</strong></li>
                <li><strong>Click the Predict button to get the predicted star type.</strong></li>
                <li><strong>Green (good), Yellow (ok), and Red (bad) status shows the confidence level of the model.</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    st.text(" ")
    
    # Input fields for user to enter star details
    temperature = st.number_input("Temperature (K):-", min_value=0, step=1, value=5770)
    luminosity = st.number_input("Luminosity wrt Sun (L/Lo):-", min_value=0.0, step=0.01, value=1.0)
    radius = st.number_input("Radius wrt Sun (R/Ro):-", min_value=0.0, step=0.01, value=1.0)
    magnitude = st.number_input("Absolute magnitude (Mv):-", step=0.01, value=4.83)

    # Trigger prediction when button is clicked
    if st.button("Predict"):
        with st.spinner('It may take a while if the app was idle for more than 15 mins...'):
            st.markdown(footer, unsafe_allow_html=True)
            # Prepare the payload for the API request
            payload = {
                "Temperature (K)": temperature,
                "Luminosity(L/Lo)": luminosity,
                "Radius(R/Ro)": radius,
                "Absolute magnitude(Mv)": magnitude
            }
            # Send a POST request to the FastAPI backend
            try:
                response = requests.post(single_predict_url, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    predicted_type = result.get("predicted_type")
                    probability = result.get("predicted_probability")
                    # Create a dynamic container for the prediction results
                    with st.container():
                        if probability >= 0.47:
                            background_color = "rgba(76, 175, 80, 0.8)"  # Green for good predictions
                            text_color = "white"
                            message = "Predicted Star Type: " + predicted_type
                        elif 0.27 <= probability < 0.47:
                            background_color = "rgba(255, 235, 59, 0.8)"  # Yellow for okayish predictions
                            text_color = "black"
                            message = "Predicted Star Type: " + predicted_type
                        else:
                            background_color = "rgba(244, 67, 54, 0.8)"  # Red for low confidence predictions
                            text_color = "white"
                            message = "Predicted Star Type: " + predicted_type
                        st.markdown(f"""
                            <div style="background-color: {background_color}; padding: 20px; border-radius: 10px;">
                                <h3 style="color: {text_color};">{message}</h3>
                                <h5 style="color: {text_color};">Confidence Level: {probability * 100:.2f}%</h5>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Error in prediction. Please try again later.")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred while connecting to the server: {e}")

# Display Bulk Prediction Page if selected
elif page == "Bulk Prediction Mode":
    st.markdown(footer, unsafe_allow_html=True)
    st.text(" ")
    with st.container():
        st.markdown("""
        <div style='background-color: rgba(255, 220, 220, 0.8); padding: 20px; border-radius: 10px;'>
            <h3 style='color: maroon;'>Bulk Prediction Mode:</h3>
            <ul style='font-size: 16px; color:black;'>
                <li><strong>Upload a CSV file with the same structure as shown above to predict the star types for multiple entries!</strong></li>
                <li><strong>The CSV file must have the following columns: <u>Temperature (K)</u>, <u>Luminosity(L/Lo)</u>, <u>Radius(R/Ro)</u>, <u>Absolute magnitude(Mv)</u>.</strong></li>
                <li><strong>Download sample CSV to see the correct format!</strong></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # File upload widget
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        st.text(" ")
        st.markdown("""
        <div style='background-color: rgba(255, 255, 255, 0.8); padding: 20px; border-radius: 10px;'>
            <h3 style='color: darkblue;'>Preview of Your CSV File:</h3>
        </div>
        """, unsafe_allow_html=True)
        file_data = uploaded_file.read().decode("utf-8")
        df = pd.read_csv(StringIO(file_data))
        st.write(df.head())  # Display the first few rows of the CSV file
        st.text(" ")
        # Button to trigger prediction
        if st.button("Predict All Star Types"):
            with st.spinner('Predicting star types...'):
                st.markdown(footer, unsafe_allow_html=True)
                # Send the CSV data to the backend API for bulk prediction
                try:
                    response = requests.post(bulk_predict_url, files={"file": uploaded_file})
                    if response.status_code == 200:
                        result_df = pd.read_csv(StringIO(response.text))
                        st.write(result_df)  # Display the result DataFrame
                    else:
                        st.error("Error in bulk prediction. Please try again.")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred while connecting to the server: {e}")


    #Summary
# In no scalling we just run logistic regression on our data frame and claculate validation and r2score using test dataframe
# In standard we standardise the data and run logistic regression on our data frame and claculate validation and r2score using test dataframe
# In minmaxscaller we operate minmaxscaler on the data and run logistic regression on our data frame and claculate validation and r2score using test dataframe
# In hyperparameter we use GridSearchCVto find best hyperparameter which give better result in prediction
# then we create data frame to make comparision in between these methods
# In fitting we use just basic elif condition on validation score and r2 score to identify fitting