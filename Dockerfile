#FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-devel
FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel

RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN apt update -y && apt install --no-install-recommends -y tzdata ffmpeg git && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/facefusion/jobs

COPY requirements.txt /tmp/
RUN pip3 --no-cache-dir install -i https://mirrors.aliyun.com/pypi/simple -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

ENV PORT=50051
ENV LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/opt/conda/lib/python3.11/site-packages/nvidia/cudnn/lib

VOLUME [ "/var/facefusion" ]

CMD ["python3", "grpc_server.py"]
