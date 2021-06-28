build:
	docker build -t databricks-streamlit-demo .

run: build
	docker run -it -p 8052:8052 --env-file=.env databricks-streamlit-demo
