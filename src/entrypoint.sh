export VNC_RESOLUTION=800x600

export MT5_LOGIN=${MT5_LOGIN:?variable MT5_LOGIN not defined}
export MT5_PASSWORD=${MT5_PASSWORD:?variable MT5_PASSWORD not defined}
export MT5_SERVER=${MT5_SERVER:?variable MT5_SERVER not defined}

/dockerstartup/vnc_startup.sh &

wine '/headless/.wine/drive_c/Program Files/MetaTrader 5/terminal64.exe' &

while :
do

sleep 5

if [ "$(iconv -f utf-16 -t utf-8 '/headless/.wine/drive_c/Program Files/MetaTrader 5/Config/common.ini' | grep $MT5_LOGIN)" ]; then break ; else echo 'not connected yet'; fi

sleep 5

xdotool key Alt+F+L
xdotool key Ctrl+A
xdotool type $MT5_LOGIN
xdotool key Tab
xdotool key Ctrl+A
xdotool type $MT5_PASSWORD
xdotool key Tab
xdotool key Tab
xdotool key Ctrl+A
xdotool type $MT5_SERVER
xdotool key Tab
xdotool key Return

done

echo 'connected'

echo 'starting webserver'

wine uvicorn --host 0.0.0.0 --port 8080 --reload main:app

