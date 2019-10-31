# docker-mt5
Docker image running mt5 platform on vnc

# USAGE

```
docker run -it --rm -p 5901:5901 -p 8080:8080 -e MT5_PASSWORD=YOUR_PASSWORD_HERE -e MT5_LOGIN=YOUR_LOGIN_HERE -e MT5_SERVER=YOUR_SERVER_HERE mt5:latest
```

The default vnc password is `vncpassword`
