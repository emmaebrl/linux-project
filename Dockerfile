FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN mkdir -p /home/mosef
RUN apt update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /home/mosef
COPY . .
RUN chmod +x ./install.sh ./bin/*.sh ./data_loader/*.sh
RUN bash ./bin/install.sh
RUN python3 -m pip install --no-cache-dir -r requirements.txt
CMD bash -c "cd bin && ./run.sh"
