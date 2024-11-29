# Copyright (c) 2022 NVIDIA Corporation.  All rights reserved.

# To build the docker container, run: $ sudo docker build -t nimdemo/tts:v1 .
# To run: $ docker run -d -v $PWD:/works --name jupyter1 nimdemo/tts:v1
# Enter docker container: docker exec -it nimtts bash
# Start streamlit: streamlit run TTS.py
# If you want customize the port, you can use this command: streamlit run TTS.py --server.port=8080
# Finally, open http://IP:8080/
#
# Before we start, we need to modify the API Link of two files to the local service:
# 1. File names: text_apps/AItext.py
# 2. Modify line 57 to the local service link

# Select Base Image
ARG ROOT_CONTAINER=brokyz/notebook_hub:latest
FROM $ROOT_CONTAINER

USER root
COPY . /AI_tts_1119
WORKDIR /AI_tts_1119/

# install Vim
RUN apt-get update && \
    apt-get install -y vim ffmpeg && \
    apt-get install -y python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install streamlit and pydub
RUN pip install streamlit pydub

# install ipywidgets and openai
RUN pip install -r https://raw.githubusercontent.com/nvidia-riva/python-clients/main/requirements.txt
RUN pip install --force-reinstall git+https://github.com/nvidia-riva/python-clients.git
#RUN git clone https://github.com/nvidia-riva/python-clients.git
RUN pip install ipywidgets requests

ENTRYPOINT [ "streamlit", "run", "TTS.py" ]
# start JupyterLab
#CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
