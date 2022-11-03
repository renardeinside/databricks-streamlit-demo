FROM continuumio/miniconda3:4.12.0

ARG DRIVER_MAJOR_VERSION="2.6.26"
ARG DRIVER_MINOR_VERSION=1045
ARG BUCKET_URI="https://databricks-bi-artifacts.s3.us-east-2.amazonaws.com/simbaspark-drivers/odbc"

ENV DRIVER_FULL_VERSION=${DRIVER_MAJOR_VERSION}.${DRIVER_MINOR_VERSION}
ENV FOLDER_NAME=SimbaSparkODBC-${DRIVER_FULL_VERSION}-Debian-64bit
ENV ZIP_FILE_NAME=${FOLDER_NAME}.zip

WORKDIR /opt/drivers


RUN apt-get update -y && \
    apt-get install -y unzip unixodbc-dev unixodbc build-essential cmake make procps && \
    wget ${BUCKET_URI}/${DRIVER_MAJOR_VERSION}/${ZIP_FILE_NAME} && \
    unzip ${ZIP_FILE_NAME} && rm -f ${ZIP_FILE_NAME} && \
    apt-get install -y ./*.deb

WORKDIR /usr/src/app

ADD environment.yml environment.yml

ENV CONDA_ENV_NAME=databricks-streamlit-demo
ENV PATH /opt/conda/envs/${CONDA_ENV_NAME}/bin:$PATH
RUN --mount=type=cache,target=/opt/conda/pkgs conda env create -f environment.yml && \
    echo "source activate ${CONDA_ENV_NAME}" > ~/.bashrc

ADD databricks_streamlit_demo databricks_streamlit_demo
ADD setup.py setup.py

RUN pip install -e .

ENV STREAMLIT_SERVER_PORT=8052

ENTRYPOINT ["streamlit", "run", "databricks_streamlit_demo/app.py","--logger.level=debug", "--server.address", "0.0.0.0"]
