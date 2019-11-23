#!/bin/bash
# weatherRP start              Inicia el servicio remoto
# weatherRP stop               Detiene el servicio remoto
# weatherRP local start/stop   Idem, pero en local
# weatherRP local restart      Reinicia en local
# weatherRP sync               Copia y ejecuta en remoto

SERVER="raspberrypi.lan"
USER="pi"
LOCAL_DIR=$(pwd)
LOG_FILE="/home/pi/weather/weatherRP.log"
DATE=$(date)

if [ $1 = "local" ]
then
    if [ $2 = "stop" ]
    then
        echo "Deteniendo servicio local"
        pkill -f weatherRP.py
        echo "Local stop at $DATE" >> $LOG_FILE
    elif [ $2 = "start" ]
    then
        echo "Arrancando servicio local"
        python3 /home/pi/weather/weatherRP.py &
        echo "Local start at $DATE" >> $LOG_FILE
    elif [ $2 = "restart" ]
    then
        pkill -f weatherRP.py
        echo "Pausa de 10 segundos"
        sleep 10
        python3 /home/pi/weather/weatherRP.py &
        echo "Local restart at $DATE" >> $LOG_FILE
    fi
    
elif [ $1 = "stop" ]
then
    echo "Deteniendo servicio remoto"
    ssh $USER@$SERVER pkill -f weatherRP.py
    ssh $USER@$SERVER "echo "Remote stop at $DATE" >> $LOG_FILE"
elif [ $1 = "sync" ]
then
    echo "Deteniendo servicio remoto"
    ssh $USER@$SERVER pkill -f weatherRP.py
    sleep 3
    echo "Actualizando servicio remoto"
    scp $LOCAL_DIR/*.* $USER@$SERVER:/home/pi/weather/
    echo "Arrancando servicio remoto"
    ssh $USER@$SERVER python3 /home/pi/weather/weatherRP.py &
    ssh $USER@$SERVER "echo "Remote sync at $DATE" >> $LOG_FILE"
elif [ $1 = "start" ]
then
    echo "Arrancando servicio remoto"
    ssh $USER@$SERVER python3 /home/pi/weather/weatherRP.py &
    ssh $USER@$SERVER "echo "Remote start at $DATE" >> $LOG_FILE"
fi
