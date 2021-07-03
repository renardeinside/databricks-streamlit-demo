from logging import Logger
import os
from dataclasses import dataclass
import pandas as pd
import os
import pyodbc
import datetime as dt
import streamlit as st
import functools


@dataclass
class EndpointInfo:
    host: str
    token: str
    http_path: str
    driver_path: str


class DataProvider:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        endpoint_info = self._get_endpoint_info()
        self.connection = pyodbc.connect(
            self.get_connection_string(endpoint_info), autocommit=True
        )

    @staticmethod
    def _get_endpoint_info() -> EndpointInfo:
        for var in ["DATABRICKS_HOST", "DATABRICKS_TOKEN", "DATABRICKS_HTTP_PATH"]:
            if var not in os.environ:
                raise Exception(f"Environment variable {var} is not defined")

        _host = os.environ["DATABRICKS_HOST"]
        _token = os.environ["DATABRICKS_TOKEN"]
        _http_path = os.environ["DATABRICKS_HTTP_PATH"]
        _driver_path = os.environ.get(
            "SIMBA_DRIVER_PATH", "/opt/simba/spark/lib/64/libsparkodbc_sb64.so"
        )  # default location on Debian
        return EndpointInfo(_host, _token, _http_path, _driver_path)

    @staticmethod
    def get_mapbox_token() -> str:
        token = os.environ.get("MAPBOX_TOKEN")
        if not token:
            raise Exception(
                "Mapbox token is not provided, please create one for free at https://studio.mapbox.com/"
            )
        return token

    @staticmethod
    def get_connection_string(endpoint_info: EndpointInfo) -> str:
        connection_string = "".join(
            [
                f"DRIVER={endpoint_info.driver_path}",
                f";Host={endpoint_info.host}",
                ";PORT=443",
                f";HTTPPath={endpoint_info.http_path}",
                ";AuthMech=3",
                ";Schema=default",
                ";SSL=1",
                ";ThriftTransport=2",
                ";SparkServerType=3",
                ";UID=token",
                f";PWD={endpoint_info.token}",
                ";RowsFetchedPerBlock=3000000",
            ]
        )
        return connection_string

    def _get_data(self, query: str) -> pd.DataFrame:
        self.logger.debug(f"Running SQL query: {query}")
        start_time = dt.datetime.now()
        data = pd.read_sql(query, self.connection)
        end_time = dt.datetime.now()
        time_delta = end_time - start_time
        self.logger.debug(
            f"Query executed, returning the result. Total query time: {time_delta}"
        )
        return data


class TaxiDataProvider(DataProvider):
    def get_trips_by_minute(self, dt: dt.date) -> pd.DataFrame:
        query = f"""
        select 
            date_trunc('minute', pickup_datetime) as dt, 
            count(1) as amount_of_trips
        from streamlit_demo_db.nyctaxi_yellow
        where to_date(pickup_datetime) = "{dt}"
        group by 1
        order by 1
        """
        data = self._get_data(query)
        return data

    def get_raw_trips(self, date_filter_column: str, dt: dt.date) -> pd.DataFrame:
        query = f"""
        select 
            {date_filter_column},
            date_trunc('hour', pickup_datetime) as pickup_hour, 
            date_trunc('hour', dropoff_datetime) as dropoff_hour, 
            pickup_longitude,
            pickup_latitude,
            dropoff_longitude,
            dropoff_latitude,
            trip_distance
        from streamlit_demo_db.nyctaxi_yellow
        where 
            to_date({date_filter_column}) = "{dt}"
            and pickup_longitude is not null
            and pickup_latitude is not null
            and dropoff_longitude is not null
            and dropoff_latitude is not null
        """
        data = self._get_data(query)

        data["pickup_hour"] = pd.to_datetime(data["pickup_hour"]).dt.strftime("%H")
        data["dropoff_hour"] = pd.to_datetime(data["dropoff_hour"]).dt.strftime("%H")
        data.sort_values(by=date_filter_column, inplace=True)
        return data
