# 模板

## Springboot

```yaml
FROM java:8

MAINTAINER {{author}} {{email}}

EXPOSE 8080

ADD target/{{JARNAME}} app.jar

RUN bash -c 'touch /app.jar'

ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom", "-jar", "/app.jar"]
```

