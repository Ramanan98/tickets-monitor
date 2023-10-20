until python bms_theaters_server_one_time.py; do
    echo "Server crashed with exit code $?.  Respawning.." >&2
    sleep 5
done