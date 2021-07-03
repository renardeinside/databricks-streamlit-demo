FROM continuumio/miniconda3:4.9.2

ARG DRIVER_MAJOR_VERSION="2.6.16"
ARG DRIVER_MINOR_VERSION=1019
ARG BUCKET_URI="https://databricks-bi-artifacts.s3.us-east-2.amazonaws.com/simbaspark-drivers/odbc"

ENV DRIVER_FULL_VERSION=${DRIVER_MAJOR_VERSION}.${DRIVER_MINOR_VERSION}
ENV FOLDER_NAME=SimbaSparkODBC-${DRIVER_FULL_VERSION}-Debian-64bit
ENV ZIP_FILE_NAME=${FOLDER_NAME}.zip

RUN mkdir /opt/drivers
WORKDIR /opt/drivers


RUN apt-get update -y && apt-get install -y unzip unixodbc-dev unixodbc-bin unixodbc make procps

RUN wget \
    ${BUCKET_URI}/${DRIVER_MAJOR_VERSION}/${ZIP_FILE_NAME}

RUN unzip ${ZIP_FILE_NAME} && rm -f ${ZIP_FILE_NAME}
RUN apt-get install -y ./${FOLDER_NAME}/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app



ADD environment.yml environment.yml

RUN --mount=type=cache,target=/opt/conda/pkgs conda env create -f environment.yml
ENV PATH /opt/conda/envs/databricks-streamlit-demo/bin:$PATH
RUN /bin/bash -c "source activate databricks-streamlit-demo"

ADD databricks_streamlit_demo databricks_streamlit_demo
ADD setup.py setup.py

RUN pip install -e .

ENV STREAMLIT_SERVER_PORT=8052

ENTRYPOINT ["streamlit", "run", "databricks_streamlit_demo/app.py","--logger.level=debug"]
