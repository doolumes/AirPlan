import streamlit as st
import requests
import pandas as pd
import numpy as np
import random
import base64
import webbrowser
from pymongo import MongoClient
from gridfs import GridFS

@st.cache
def load_data(date):
    x = requests.get(f"http://localhost:4000/flights?date={date}")
    df = pd.read_json(x.text)
    return df

#Import the required Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#import airportsdata




 

# print (data)    
# # calling head() method  
# # storing in new variable 
# data_top = data.head() 


st.set_page_config(layout="wide")

# Functions for each of the pages
def home():
    """### gif from local file"""
    file_ = open("Air-plan.gif", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" width="1000" height="1000">',
        unsafe_allow_html=True,
    )

    # video_file = open('Air-plan.gif', 'rb')
    # video_bytes = video_file.read()

    # st.video(video_bytes)
    
def data_summary():
    #get date from user
    user_input_date = st.text_input("Enter Date in format YYYY-MM-DD", "2020-01-01")

    df = load_data(user_input_date)

    user_input_flight = st.text_input("Enter your flight number", "2020")

    user_input_lastname = st.text_input("Enter your last name", "Phatak")


    flightNumbers = []

    for row in range(len(df)):
        flightNumbers.append(df["flightNumber"][row])

    #print(flightNumbers)


    user_input_flight = int(user_input_flight)

    if user_input_flight in flightNumbers:
        st.write("Your Flight information is: ")
        row = flightNumbers.index(user_input_flight)
        st.write("Origin: " + df["origin"][row]['city'])
        st.write("Destination: " + df["destination"][row]['city'])
        st.write("Departure Time: " + df["departureTime"][row])
        st.write("Aircraft Information: " + df["aircraft"][row]["model"])
        
        gate_letter = random.randint(65,70)
        gate_num = random.randint(1,19)

        st.write("Gate Information: " + chr(gate_letter) + str(gate_num))

    else:
        if (user_input_flight < 2000):
            st.write("Your flight was cancelled :( please check available flights on the next day!")
        else:
            st.write("Invalid Flight Number. Please try again!")


def data_header():
    # st.header('Header of Dataframe')
    # st.write(df.head())
    data = pd.read_csv("airports.csv") 
    option = st.selectbox('Choose your location',data["name"])
    if option=="George Bush Intcntl/Houston Airport":
        url = "https://www.fly2houston.com/iah/overview?utm_source=IAH&utm_medium=WIFI&utm_campaign=WIFI"
        #st.write("Click here to proceed to the airport website!(%s)" % url)
        #st.button("Click here to proceed to the airport website!(%s)" % url)
        if st.button("Click here to proceed to the airport website!"):
            webbrowser.open_new_tab(url)


    elif option=="Aero B Ranch Airport":
        url = "http://airnav.com/airport/00AA"
        if st.button("Click here to proceed to the airport website!"):
            webbrowser.open_new_tab(url)

    elif option=="Dallas-Fort Worth International Airport":
        url = "https://www.dfwairport.com/"
        if st.button("Click here to proceed to the airport website!"):
            webbrowser.open_new_tab(url)

    elif option=="Epps Airpark":
        url = "https://www.aopa.org/destinations/airports/00AL/details"
        if st.button("Click here to proceed to the airport website!"):
            webbrowser.open_new_tab(url)

    elif option=="Indira Gandhi International Airport":
        url = "https://www.newdelhiairport.in/"
        if st.button("Click here to proceed to the airport website!"):
            webbrowser.open_new_tab(url)

    elif option=="Lowell Field":
        url = "https://www.airnav.com/airport/9GA5"
        if st.button("Click here to proceed to the airport website!"):
            webbrowser.open_new_tab(url)
    elif option=="Arland Airport":
        url = "https://www.swedavia.se/arlanda/"
        if st.button("Click here to proceed to the airport website!"):
            webbrowser.open_new_tab(url)



    elif option =="Grass Patch Airport":
        url = "https://www.airnav.com/airport/VA62"
        if st.button("Click here to proceed to the airport website!"):
            webbrowser.open_new_tab(url)

    elif option=="York Airport":
        url = "https://www.york-aviation.com/"
        if st.button("Click here to proceed to the airport website!"):
            webbrowser.open_new_tab(url)

def displayplot():
    # st.header('Plot of Data')
    
    # fig, ax = plt.subplots(1,1)
    # ax.scatter(x=df['Depth'], y=df['Magnitude'])
    # ax.set_xlabel('Depth')
    # ax.set_ylabel('Magnitude')
    
    # st.pyplot(fig)
    #upload_file = st.file_uploader("Upload a picture of your luggage!", type=['png','jpeg'], accept_multiple_files=True, key=None, help="JPG, PNG only", on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    numluggage = st.number_input("Enter the number of check-in luggage: ", min_value = 0, step= 1)
    for i in range(0, numluggage):
        upload_file = st.file_uploader("Upload a picture of your {} luggage!".format(i+1), type=['png','jpeg','image','jpg'], accept_multiple_files=True, key=None, help="JPG, PNG only", on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
    client = MongoClient('mongodb://localhost:27017/')
    db = client['AIRLINESDB']
    fs = GridFS(db)

    # open the image file
    with open('myimage.jpg', 'rb') as f:
        # create a new GridFS file
        file_id = fs.put(f, filename='luggage.jpg')

    print(f'Successfully uploaded image with ID: {file_id}')
#     if numluggage>=1:
#         st.button("Done", on_click=save())

#Sidebar navigation

def explore():
    user_input = st.text_input("Enter Date in format YYYY-MM-DD", "2020-01-01")
    #df = load_data(user_input)
    x = requests.get(f"http://localhost:4000/flights?date={user_input}")
    df = pd.read_json(x.text)
    lat_and_long = [[],[]]


    for row in range(len(df)):
        lat_and_long[0].append(df["origin"][row]['location']["latitude"])
        lat_and_long[1].append(df["origin"][row]["location"]["longitude"])

    lat_and_long_r = np.array(lat_and_long)
    lat_and_long_c = np.array(lat_and_long)
    lat_and_long_c = np.transpose(lat_and_long_c)

    #print(f"C: {lat_and_long_c}")


    lat_df = pd.DataFrame(lat_and_long_c, columns=['lat', 'lon'])

    #print(lat_df)

    #print(long)
    st.write("Check out this day's busiest cities!")
    st.map(lat_df)

def contact():
    st.write("Contact Us Form: ")
    with st.form(key = "form1"):
        name = st.text_input("Please enter your name.")
        email = st.text_input("Please enter your email.")
        message = st.text_input("Please enter your message.")
        submit_button = st.form_submit_button(label = "Submit")
    
    if (submit_button):
        st.success("Thank you for submitting your message. We will get back to you as soon as possible!")

# Add a title and intro text
st.markdown("<h1 style='text-align: center; color: white;'>Air-plan</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>See the world with us!</h1>", unsafe_allow_html=True)


# Sidebar setup
st.sidebar.title('Options')

options = st.sidebar.radio('', ['Home', 'Flight Information', 'Airport Navigation', 'Luggage \'Drop\'', 'Explore', 'Contact Us!'])


# Navigation options
if options == 'Home':
    home()
elif options == 'Flight Information':
    data_summary()
elif options == 'Airport Navigation':
    data_header()
elif options == 'Luggage \'Drop\'':
    displayplot()
elif options == 'Explore':
    explore()
elif options == 'Contact Us!':
    contact()

# tab1, tab2, tab3, tab4 = st.tabs(["Flight Information", "Aiport Navigation", "Luggage Drop", "Contact Us"])

# # Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
