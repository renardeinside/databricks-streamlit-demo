# Demo of Streamlit application with Databricks SQL Endpoint


## Prerequisites

- Databricks SQL endpoint
- Locally: Docker, Makefile

## Quick demo

![demo](./videos/demo.webm)

## How to 

1. Createnw or start an existing SQL endpoint of any size in your Databricks workspace
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




