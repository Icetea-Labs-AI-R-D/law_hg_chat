FROM python:3.10

# Set the working directory
WORKDIR /app

COPY ./backend ./backend
COPY ./frontend ./frontend
COPY ./.env ./.env
COPY ./run_backend_local.sh ./run_backend_local
COPY ./run_frontend_local.sh ./run_frontend_local
COPY ./requirements.txt ./requirements.txt

# Install dependencies
RUN apk add --no-cache dbus-x11

RUN pip install -r requirements.txt \
    && bash run_backend_local.sh \
    && bash run_frontend_local.sh

# Expose the port
EXPOSE 11001
EXPOSE 11002