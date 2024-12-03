FROM python:3.10-slim
WORKDIR /app
EXPOSE 8501

# Définir les variables d'environnement pour Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
COPY . .
RUN apt-get update && apt-get install -y --no-install-recommends \
    dos2unix curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN find . -type f \( -name "*.sh" -o -name "*.py" \) -exec dos2unix {} +
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN chmod +x bin/install.sh bin/menu.sh bin/launch.sh bin/launch_app.sh
RUN mkdir -p /app/data
ENTRYPOINT ["bash", "bin/menu.sh"]