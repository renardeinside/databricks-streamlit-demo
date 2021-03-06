"""
Application entrypoint for streamlit. 
"""
import streamlit as st
import logging
import datetime as dt
from databricks_streamlit_demo.data_provider import TaxiDataProvider
from databricks_streamlit_demo.plotter import Plotter
from databricks_streamlit_demo.utils import write_aligned_header, empty_date_warning


logger = logging.getLogger("databricks-streamlit-demo")
data_provider = TaxiDataProvider(logger)
plotter = Plotter(data_provider)

st.set_page_config(
    layout="wide", page_title="Databricks Streamlit Demo", page_icon=":fire:" # :fire: will be transformed into emoji 
)

st.write(
    """
# Databricks Streamlit Demo :fire:

This Streamlit application connects to Databricks SQL Endpoint and creates some visualizations based on the [NYC Taxi Dataset](#https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
"""
)

empty_date_warning()

filter_box, minute_dynamic_box = st.beta_columns([1, 4])

with filter_box:
    write_aligned_header("Please choose the date")
    chosen_date = st.date_input("", dt.date(2016, 6, 30))
    plotter.add_counter_plot(chosen_date)


with minute_dynamic_box:
    plotter.add_minute_plot(chosen_date)

pickups_map, dropoffs_map = st.beta_columns(2)


with pickups_map:
    plotter.add_density_map(chosen_date, name="pickup", zoom=11)

with dropoffs_map:
    plotter.add_density_map(chosen_date, name="dropoff", zoom=9, alignment="right")
