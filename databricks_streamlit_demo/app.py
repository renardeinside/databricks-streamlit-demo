import streamlit as st
import logging
import datetime as dt
from databricks_streamlit_demo.data_provider import TaxiDataProvider
from databricks_streamlit_demo.plotter import Plotter
from databricks_streamlit_demo.utils import write_aligned_header

logger = logging.getLogger("databricks-streamlit-demo")
data_provider = TaxiDataProvider(logger)
plotter = Plotter(data_provider)

st.set_page_config(layout="wide")

st.write(
    """
# Databricks Streamlit Demo :fire:
This Streamlit application connects to Databricks SQL Endpoint, based on the [NYC Taxi Dataset](#https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
"""
)

filter_box, minute_dynamic_box = st.beta_columns([1, 4])

with filter_box:
    write_aligned_header("Please choose the date")
    chosen_date = st.date_input("", dt.date(2016, 6, 30))
    plotter.add_counter_plot(chosen_date)


with minute_dynamic_box:
    plotter.add_minute_plot(chosen_date)

pickups_map, dropoffs_map = st.beta_columns(2)


with pickups_map:
    plotter.add_pickup_density_map(chosen_date)

with dropoffs_map:
    plotter.add_dropoff_density_map(chosen_date)
