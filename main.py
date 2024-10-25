    # Create a web app of weather forecast with some interactive feautures.

import streamlit as st
import plotly.express as px
from backend import get_data
import datetime

# Add title, text input, slider, selectbox, and subheader
st.title("Weather Forecast for the Next Days:")
place = st.text_input("Place:")

try:
    # Create a slider who allow ass to select between 1 ad 5 days, sliding a bar with the mouse.
    days = st.slider(
        "Forecast Days",
        min_value=1,
        max_value=5,
        help="Select the number of forecasted days",
    )

    option = st.selectbox("Select data to view", ("Temperature", "Sky"))
    st.subheader(
        f"{option} for the next {days} days in {place}:"
    )  # create dinamyc subheader

    if place:
        # Get the temperature/sky data
        filtered_data = get_data(place, days)

        if option == "Temperature":
            temperatures = [dict["main"]["temp"] for dict in filtered_data]
            temperatures = [temperature - 273 for temperature in temperatures]
            dates = [dict["dt_txt"] for dict in filtered_data]

            # Create an interactive and auto update temperature plot
            figure = px.line(
                x=dates,
                y=temperatures,
                labels={"x": "Date", "y": "Temperature (ºC)"},
            )
            st.plotly_chart(figure)

        if option == "Sky":

            images = {
                "Clear": "images/clear.png",
                "Clouds": "images/cloud.png",
                "Rain": "images/rain.png",
                "Snow": "images/snow.png",
            }
            sky_conditions = [
                dict["weather"][0]["main"] for dict in filtered_data
            ]
            image_paths = [images[condition] for condition in sky_conditions]

            # extract the dt_txt from filtred_data and, convert it into a datatime object to give it the formatt we want.
            day_hour = [
                datetime.datetime.strptime(
                    dict["dt_txt"], "%Y-%m-%d %H:%M:%S"
                ).strftime("%a, %d %b %H:%M")
                for dict in filtered_data
            ]

            st.image(image_paths, day_hour, width=140)
except KeyError:
    st.markdown(
        f"""<h4 style="text-align: center;">Please enter a valid City.</p>""",
        unsafe_allow_html=True,
    )
