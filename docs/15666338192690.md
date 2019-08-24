```shell
#!/bin/bash
jar=$2
start(){
echo "run $jar ..."
nohup java -jar -Xmn128 -Xms256m -Xmx512m $jar &
}
stop(){
#kill 
PID=$(ps -ef | grep $jar | grep -v grep | awk '{ print $2 }')
if [ -z "$PID" ]
then
echo Application is already stopped
else
echo kill $PID
kill $PID
fi
}
case $1 in
start)
start
;;
stop)
stop
;;
restart)
$0 stop
sleep 2
$0 start
;;
*)
echo "Usage: {start|stop|restart}"
;;
esac
exit 0

```

