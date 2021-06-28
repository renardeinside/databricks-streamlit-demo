import streamlit as st

import pandas as pd
import logging
import datetime as dt
from databricks_streamlit_demo.data_provider import TaxiDataProvider

logger = logging.getLogger("databricks-streamlit-demo")
data_provider = TaxiDataProvider(logger)


st.set_page_config(layout="wide")

st.write(
    """
# Databricks Streamlit Demo
This Streamlit application connects to Databricks SQL Endpoint, based on the [NYC Taxi Dataset](#https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
"""
)

st.sidebar.write("## Please choose the date")
chosen_date = st.sidebar.date_input("", dt.date(2019,1,24))
data = data_provider.get_trips_by_hour(chosen_date)
st.area_chart(data)