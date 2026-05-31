import streamlit as st
import requests

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the Fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

conn = st.connection("snowflake")
my_dataframe = conn.query("SELECT FRUIT_NAME FROM smoothies.public.fruit_options")

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order)
                        VALUES ('{ingredients_string}', '{name_on_order}')"""

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        conn.query(my_insert_stmt)
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")

smoothiefroot_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
