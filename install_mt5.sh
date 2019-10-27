wine mt5setup.exe &

sleep 10

xdotool key Return

export COMMON='/headless/.wine/drive_c/Program Files/MetaTrader 5/Config/common.ini'
while :
do
  if test -f "$COMMON"
  then
    break
  fi
  sleep 2
done

echo 'waiting for mt5 to finish install'

sleep 600

echo 'done'
