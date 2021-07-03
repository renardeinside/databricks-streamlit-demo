from plotly.missing_ipywidgets import FigureWidget
from databricks_streamlit_demo.data_provider import TaxiDataProvider
import streamlit as st
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from databricks_streamlit_demo.utils import write_aligned_header, custom_spinner


class Plotter:
    def __init__(self, provider: TaxiDataProvider) -> None:
        self.provider = provider
        px.set_mapbox_access_token(self.provider.get_mapbox_token())

    def add_counter_plot(self, chosen_date: dt.date) -> None:
        with custom_spinner("Loading total count ..."):
            cnt = self.provider._get_data(
                f"""
            select count(1) as cnt 
            from streamlit_demo_db.nyctaxi_yellow
            where to_date(pickup_datetime) = "{chosen_date}"
            """
            ).loc[0, "cnt"]
            fig = go.Figure(
                go.Indicator(
                    mode="number",
                    value=cnt,
                    align="center",
                    title={"text": "Total pickups"},
                )
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    def add_minute_plot(self, chosen_date: dt.date) -> None:
        write_aligned_header("Number of trips per minute", alignment="right")
        with custom_spinner("Loading minute plot ..."):
            data = self.provider.get_trips_by_minute(chosen_date)
            fig = px.area(
                data,
                x="dt",
                y="amount_of_trips",
                labels={"dt": "time", "amount_of_trips": "Number of Trips"},
                height=500,
            )
            st.plotly_chart(fig, use_container_width=True)

    def _get_density_map(
        self,
        chosen_date: dt.date,
        date_filter_column: str,
        lat_col: str,
        lon_col: str,
        frame_col: str,
        zoom: int = 10,
    ) -> FigureWidget:
        data = self.provider.get_raw_trips(date_filter_column, chosen_date)
        fig = px.density_mapbox(
            data_frame=data,
            lat=lat_col,
            lon=lon_col,
            zoom=zoom,
            z="trip_distance",
            radius=10,
            opacity=0.7,
            mapbox_style="dark",
            animation_frame=frame_col,
            center={"lat": 40.7359, "lon": -73.9911},  # NY Central Park Coordinates
            height=600,
            labels={"pickup_hour": "Pickup Hour", "dropoff_hour": "Dropoff Hour"}
        )
        return fig

    def add_pickup_density_map(self, chosen_date: dt.date) -> None:
        write_aligned_header("Pickups density map")
        with custom_spinner("Loading pickup density map ..."):
            fig = self._get_density_map(
                chosen_date,
                "pickup_datetime",
                "pickup_latitude",
                "pickup_longitude",
                "pickup_hour",
                zoom=11,
            )
            st.plotly_chart(fig, use_container_width=True)

    def add_dropoff_density_map(self, chosen_date: dt.date) -> None:
        write_aligned_header("Dropoffs density map", alignment="right")
        with custom_spinner("Loading dropoff density map ..."):
            fig = self._get_density_map(
                chosen_date,
                "dropoff_datetime",
                "dropoff_latitude",
                "dropoff_longitude",
                "dropoff_hour",
                zoom=9,
            )
            st.plotly_chart(fig, use_container_width=True)
