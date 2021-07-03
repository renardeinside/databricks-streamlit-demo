# Demo of Streamlit application with Databricks SQL Endpoint

Table of Contents
=================

   * [Demo of Streamlit application with Databricks SQL Endpoint](#demo-of-streamlit-application-with-databricks-sql-endpoint)
      * [Prerequisites](#prerequisites)
      * [Quick demo](#quick-demo)
      * [How to](#how-to)
      * [References](#references)

## Prerequisites

- Databricks SQL endpoint
- Locally: Docker, Makefile

## Quick demo

![demo](./raw/demo.gif)

## How to 

1. Create or start an existing SQL endpoint of any size in your Databricks workspace
2. Create new query and define the database and table:

```
create database if not exists streamlit_demo_db;
create table if not exists
streamlit_demo_db.nyctaxi_yellow 
using delta
location "dbfs:/databricks-datasets/nyctaxi/tables/nyctaxi_yellow";
```

3. On local machine, clone the repository and create `.env` file in the repository directory. Follow the `.env.sample` for instructions. 
4. On local machine, launch `make run` to start the server
5. Open http://localhost:8052 and enjoy the new application :) 

## References

- [Databricks SQL](https://databricks.com/product/databricks-sql)
- [Streamlit](https://streamlit.io/)
- [Mapbox](https://www.mapbox.com/)
- [NYC Taxi Dataset](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Markdown TOC](https://github.com/ekalinin/github-markdown-toc)