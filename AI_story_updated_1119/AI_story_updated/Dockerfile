# Copyright (c) 2022 NVIDIA Corporation.  All rights reserved.

# To build the docker container, run: $ sudo docker build -t nimdemo/aistory:v1 .
# To run: $ docker run -d -v $PWD:/works --name nimstory nimdemo/aistory:v1
# Enter docker container: docker exec -it nimstory bash
# Start streamlit: streamlit run AI_story_streamlit.py  
# If you want customize the port, you can use this command: streamlit run AI_story_streamlitß.py --server.port=8080
# Finally, open http://IP:8080/   
#
# Before we start, we need to modify the API Link of two files to the local service:
# 1. File names: story_module1.py, story_module2.py
# 2. Modify line 4 to the local service link, and replace the api_key on line 5

# Select Base Image
ARG ROOT_CONTAINER=brokyz/notebook_hub:latest
FROM $ROOT_CONTAINER

USER root
COPY . /AI_story_updated
WORKDIR /AI_story_updated/

# install Vim
RUN apt-get update && \
    apt-get install -y vim ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install ipywidgets and openai
RUN pip install streamlit pydub ipywidgets requests openai

ENTRYPOINT [ "streamlit", "run", "AI_story_streamlit.py" ]

# start JupyterLab
#CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
