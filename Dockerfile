FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y dos2unix
RUN find . -type f \( -name "*.sh" -o -name "*.txt" -o -name "*.csv" -o -name "*.py" -o -name "Dockerfile" -o -name "requirements.txt" \) -exec dos2unix {} +
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN mkdir -p data logs
RUN chmod +x bin/launch.sh bin/run.sh
ENTRYPOINT ["bash", "bin/launch.sh"]
