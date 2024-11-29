# Copyright (c) 2022 NVIDIA Corporation.  All rights reserved.

# To build the docker container, run: $ sudo docker build -t nimdemo/asr:v1 .
# To run: $ docker run -d -v $PWD:/works --name nimasr nimdemo/asr:v1
# Enter docker container: docker exec -it nimasr bash
# Start streamlit: streamlit run AI_asr/web.py  
# If you want customize the port, you can use this command: streamlit run web.py --server.port=8080
# Finally, open http://IP:8080/   
#
# Before we start, we need to modify the API Link of two files to the local service:
# 1. File names: mic_apps/web.py
# 2. Modify line 52 to the local service link

# Select Base Image
ARG ROOT_CONTAINER=brokyz/notebook_hub:latest
FROM $ROOT_CONTAINER

USER root
COPY . /AI_asr
WORKDIR /AI_asr/

# install Vim and ffmpeg
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
# RUN git clone https://github.com/nvidia-riva/python-clients.git
RUN pip install ipywidgets requests

ENTRYPOINT [ "streamlit", "run", "web.py" ]

# start JupyterLab
#CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
