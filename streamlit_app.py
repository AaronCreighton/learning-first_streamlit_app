import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

st.title('my Parents new Diner')

st.header('Breakfast Menu')

st.text('🥣 Omega 3 & Blueberry Oatmeal')

st.text('🥗 Kale, Spinach & Rocket Smoothie') 

st.text('🐔 Hard-Boulded Free-Range Egg')

st.text('🥑🍞 Avocado toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the Options on the page.
st.dataframe(my_fruit_list)

# Display the Results on the page.
st.dataframe(fruits_to_show)

#new section to display API response
st.header("Fruityvice Fruit Advice!")

#import requests

fruit_choice = st.text_input('What fruit would you like information about?','Kiwi')
st.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# st.text(fruityvice_response.json()) # no json() 200, with turns data to txt 



# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
st.dataframe(fruityvice_normalized)

#don't run anything pas here while we troubleshoot
st.stop()

#import snowflake.connector


# Query account metadata
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()") #return account info
my_cur.execute("Select * from fruit_load_list")
#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()
st.header("the fruit Load list contains:")
st.dataframe(my_data_rows)

#Allow the end user to add a fruit to the list
add_my_fruit = st.text_input('What fruit would you like to add?','jackfruit')
st.write('thank you for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")