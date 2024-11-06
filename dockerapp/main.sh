echo "Starting the application"

echo "--------------Data Loader--------------"
bash collect_data.sh
echo "                                        "

echo "--------------Transform Data--------------"
bash run_prediction.sh