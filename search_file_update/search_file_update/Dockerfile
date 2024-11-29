# Copyright (c) 2022 NVIDIA Corporation.  All rights reserved.

# To build the docker container, run: $ sudo docker build -t nimdemo/aifile:v1 .
# To run: $ docker run -d -v $PWD:/works --name nimfile nimdemo/aifile:v1
# Enter docker container: docker exec -it nimfile bash
# Start streamlit: streamlit run streamlit-update.py  
# If you want customize the port, you can use this command: streamlit run streamlit-update.py --server.port=8080
# Finally, open http://IP:8080/   
#
# Before we start, we need to modify the API Link of two files to the local service:
# 1. File names: streamlit-update.py
# 2. Modify line 36 to the local service link, and replace the api_key on line 37

# Select Base Image
ARG ROOT_CONTAINER=brokyz/notebook_hub:latest
FROM $ROOT_CONTAINER

USER root

COPY . /search_file_update
WORKDIR /search_file_update/

# install Vim
RUN apt-get update && \
    apt-get install -y vim ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install ipywidgets and openai
RUN pip install streamlit pydub ipywidgets requests openai

ENTRYPOINT [ "streamlit", "run", "streamlit-update.py" ]

# start JupyterLab
#CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
