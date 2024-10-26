    # Create a web app of weather forecast with some interactive feautures.

import streamlit as st
import plotly.express as px
from backend import get_data
import datetime

# Add title, text input, slider, selectbox, and subheader
st.title("Weather Forecast for the Next Days:")
place = st.text_input("City:")


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

# In case there is typed an inexistent city, the program shows a friendly message instead a tecnical error:
try:
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
                labels={"x": "Date", "y": "Temperature (°C)"},
            )

            st.plotly_chart(figure)

        if option == "Sky":

            # put the images paths in a dictionary with keywords asosiated to each weather condition:
            images = {
                "Clear": "images/clear.png",
                "Clouds": "images/cloud.png",
                "Rain": "images/rain.png",
                "Snow": "images/snow.png",
            }

            # to create image paths is join the weahter condition in dictionary filtered_data with images before created and configurated:
            sky_conditions = [
                dict["weather"][0]["main"] for dict in filtered_data
            ]
            image_paths = [images[condition] for condition in sky_conditions]

            # extract the dt_txt from filtred_data and, convert it into a datatime object to give it the format we want:
            day_hours = [datetime.datetime.strptime(
                    dict["dt_txt"], "%Y-%m-%d %H:%M:%S"
                ).strftime("%a, %d %b %H:%M")
                for dict in filtered_data
            ]

            # extract temperatures from dict on keyword main and inside main from keyword temp, and give them the format:
            temperatures = [dict["main"]["temp"] for dict in filtered_data]
            temperatures = [
                f"{int(temperature - 273)}°C"
                for temperature in temperatures
            ]

            # join strings lists day_hours and temperatures in one string list and finally
            temp_hours = [
                f"{day_hour}  {temperature}"
                for day_hour, temperature in zip(day_hours, temperatures)
            ]

            # display the list temp_hours under each weather symbol:
            st.image(image_paths, temp_hours, width=125)

except KeyError:
    st.markdown(
        f"""<h4 style="text-align: center;">Please enter a valid City.</p>""",
        unsafe_allow_html=True
    )