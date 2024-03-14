import streamlit as st
#import snowflake.connector
from snowflake.snowpark.functions import col
import requests
import pandas as pd

st.title("Zena\'s Amazing Athleisure Catalog")

# connect to snowflake
my_cnx = st.connection("snowflake")
session = my_cnx.session()

# run a snowflake query and put it all in a var called my_catalog
#my_cnx.execute("select color_or_style from catalog_for_website")
#my_catalog = my_cur.fetchall()

my_dataframe = session.table("catalog_for_website").select(col('color_or_style'))
#st.dataframe(data=my_dataframe,use_container_width=True)

# put the dafta into a dataframe
pd_df = my_dataframe.to_pandas()

# temp write the dataframe to the page so I Can see what I am working with
# st.dataframe(pd_df)

# put the first column into a list
#color_list = pd_df[0].values.tolist()
# print(color_list)

# Let's put a pick list here so they can pick the color
option = st.selectbox('Pick a sweatsuit color or style:', my_dataframe)

# We'll build the image caption now, since we can
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# use the option selected to go back and get all the info from the database
#my_cur.execute("select direct_url, price, size_list, upsell_product_desc from catalog_for_website where
#color_or_style = '" + option + "';")

#info_dataframe = session.sql("select direct_url, price, size_list, upsell_product_desc from catalog_for_website where color_or_style = '" + option + "';")
#info_dataframe.show()
info_dataframe = session.table("catalog_for_website").select(col('color_or_style'), col('direct_url'), col('price'), col('size_list'), col('upsell_product_desc'))
info_dataframe.filter(col(0) == "'" + option + "'").collect()
st.write( """Checking if code so far is working.""")

#df2 = my_cur.fetchone()
#streamlit.image(
#df2[0],
#width=400,
#caption= product_caption
#)
#streamlit.write('Price: ', df2[1])
#streamlit.write('Sizes Available: ',df2[2])
#streamlit.write(df2[3])
