from numpy import insert
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

# user to select priorities
st.text('Alternatively Pick your Desire outcome, Low sugar or low ..?')

#import requests

#create the repeatable code black 
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # st.text(fruityvice_response.json()) # no json() 200, with turns data to txt  
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


#new section to display API response
st.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.error("Please select a fruit to get information.")
    else:
        st.write('The user entered ', fruit_choice)
        back_from_function = get_fruityvice_data(fruit_choice)
        st.dataframe(back_from_function)
        
except URLError as e:
    st.error()

#don't run anything pas here while we troubleshoot
#st.stop()

#import snowflake.connector

# Query account data
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()") #return account info


st.header("View Our fruit List - Add Your Favorites!")
# snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("Select * from fruit_load_list")
        #my_data_row = my_cur.fetchone()
        return my_cur.fetchall()

# add button to load the fruit
if st.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    st.dataframe(my_data_rows)

#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    V_Count = 1
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('"+ new_fruit +"', " + V_Count + ")")
        return "Thanks for adding " + new_fruit

# Empty table

def truncate_row_snowflake():
   with my_cnx.cursor() as my_cur:
       my_cur.execute("truncate fruit_load_list")
       return "Thanks for Emplying the list"
     
add_my_fruit = st.text_input('What fruit would you like to add?','jackfruit')
add_wanted_fruit_low = add_my_fruit.lower()
my_availble_fruit = str(my_fruit_list.index).lower()


if add_wanted_fruit_low in my_availble_fruit or add_my_fruit == False:
   st.text('We have this fruit already, What else do you like?')
else:      
    if st.button('add a Fruit to the List'):
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        back_from_function = insert_row_snowflake(add_my_fruit)
        my_cnx.close()
        st.text(back_from_function)


if st.button('Reset List'):
        my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
        back_from_function = truncate_row_snowflake()
        my_cnx.close()
        st.text(back_from_function)




     