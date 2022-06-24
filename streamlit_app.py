import streamlit as st

st.title('my Parents new Diner')

st.header('Breakfast Menu')

st.text('🥣 Omega 3 & Blueberry Oatmeal')

st.text('🥗 Kale, Spinach & Rocket Smoothie') 

st.text('🐔 Hard-Boulded Free-Range Egg')

st.text('🥑🍞 Avocado toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])

# Display the table on the page.
st.dataframe(my_fruit_list)