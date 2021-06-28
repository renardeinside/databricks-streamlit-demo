include .env
export

build:
	docker build -t databricks-streamlit-demo .

run: build
	docker run -it -p 8052:8052 --env-file=.env databricks-streamlit-demo

debug-in-docker:
	streamlit run databricks_streamlit_demo/app.py \
		--server.port=8052 \
		--logger.level=debug \
		--logger.messageFormat="[%(asctime)s][%(levelname)s][%(name)s][%(funcName)s][%(message)s]"