from setuptools import find_packages, setup
from databricks_streamlit_demo import __version__

setup(
    name="databricks_streamlit_demo",
    packages=find_packages(exclude=["tests", "tests.*"]),
    setup_requires=["wheel"],
    version=__version__,
    description="Databricks Streamlit Demo",
    author="Ivan Trusov",
)