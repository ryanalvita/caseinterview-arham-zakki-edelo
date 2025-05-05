[ ![docs](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://vanoord.github.io/pyramid-app-voice/docs/) [ ![coverage](https://github.com/VanOord/pyramid-app-voice/blob/gh-pages/coverage/coverage.svg)](https://vanoord.github.io/pyramid-app-voice/coverage/) [![CICD - ACR - Python](https://github.com/VanOord/pyramid-app-caseinterview/actions/workflows/action.yml/badge.svg)](https://github.com/VanOord/pyramid-app-caseinterview/actions/workflows/action.yml)



# caseinterview
A pyramid app for case interview with opentelemetry

# Installation and running caseinterview

Install the environment:

```bash
rebuild and reopen in docker container
```

Input Grafana Cloud Credentials in config.alloy:

```bash
otelcol.exporter.otlphttp "grafana" {
  client {
    endpoint = "ENDPOINT" << REPLACE ENDPOINT
    auth = otelcol.auth.basic.grafanacloud.handler
  }
}

otelcol.auth.basic "grafanacloud" {
  username = "INSTANCE" << REPLACE INSTANCE
  password = "API-KEY" << REPLACE API-KEY
}
```

Run the application with alloy

```bash
./otel.sh alloy
```
When we open "Traces" Drilldown in Grafana Cloud we see that traces are seperated
