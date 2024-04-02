# Use Python 3.11 Slim image as the base
FROM python:3.11-slim

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg fonts-dejavu-core && \
    # Clean up to keep the image slim
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy the requirements file into the image
COPY ./requirements.txt /requirements.txt
COPY ./DejaVuSansCondensed.ttf /DejaVuSansCondensed.ttf
COPY ./DejaVuSansCondensed-Bold.ttf /DejaVuSansCondensed-Bold.ttf

# switch working directory
WORKDIR /

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

EXPOSE 8501

# install the dependencies and packages in the requirements file
RUN pip3 install -r requirements.txt
RUN pip3 install openai-whisper

# copy every content from the local file to the image
COPY ./ /

# configure the container to run in an executed manner
ENTRYPOINT [ "streamlit", "run" ]
CMD [ "server.py", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]