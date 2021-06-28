build:
	docker build -t databricks-streamlit-demo .

run: build
	docker run -it --env-file=.env databricks-streamlit-demo
