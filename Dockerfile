FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y dos2unix
RUN find . -type f \( -name ".sh" -o -name ".txt" -o -name ".csv" -o -name ".py" -o -name "Dockerfile" -o -name "requirements.txt" \) -exec dos2unix {} +
RUN chmod +x bin/install.sh bin/launch.sh bin/run.sh
RUN bash bin/install.sh
CMD ["bash", "bin/launch.sh"]
ENTRYPOINT ["bash", "bin/launch.sh"]