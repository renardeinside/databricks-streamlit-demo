from logging import Logger
import os
from dataclasses import dataclass
import pandas as pd
import os
import pyodbc
import datetime as dt


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
            ]
        )
        return connection_string

    def _get_data(self, query: str) -> pd.DataFrame:
        self.logger.debug(f"Running SQL query: {query}")
        data = pd.read_sql(query, self.connection)
        self.logger.debug("Query executed, returning the result")
        return data


class TaxiDataProvider(DataProvider):
    def get_trips_by_hour(self, dt: dt.date) -> pd.DataFrame:
        query = f"""
        select 
            date_trunc('minute', pickup_datetime) as dt, 
            count(1) as amount_of_trips
        from streamlit_demo_db.nyctaxi_yellow
        where to_date(pickup_datetime) = "{dt}"
        group by 1
        order by 1
        """
        data = self._get_data(query).set_index("dt")
        return data
