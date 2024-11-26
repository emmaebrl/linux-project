#!/bin/bash
echo "Starting the application..."
streamlit run app/app.py --server.port 8080 --server.enableCORS false --server.address 0.0.0.0
