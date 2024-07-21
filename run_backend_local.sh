ENVIRONMENT=DEV
nohup python ./backend/main.py > output.log &

# ps ax | grep ./backend/main.py