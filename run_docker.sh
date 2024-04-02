##!/bin/bash

docker build --build-arg OPENAI_API_KEY='' -t fbellame/audio_to_pdf:1.0 .
docker run --gpus all -e OPENAI_API_KEY= -it --rm -v /media/farid/data/projects/audio_to_pdf/tmp:/data fbellame/audio_to_pdf:1.0