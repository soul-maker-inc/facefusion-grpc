FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-devel

RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone
RUN apt update -y && apt install --no-install-recommends -y tzdata ffmpeg git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN pip3 --no-cache-dir install -i https://mirrors.aliyun.com/pypi/simple -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

ENV PORT 50051

VOLUME [ "/data" ]

CMD ["python3", "facefusion_grpc.py"]
