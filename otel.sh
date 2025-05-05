#!/bin/bash

if [ "$1" == "console" ]; then
  EXPORTER="console"
  ENDPOINT=""
  echo "🪵 Running with console exporter"

elif [ "$1" == "alloy" ]; then
  EXPORTER="otlp"
  ENDPOINT="--exporter_otlp_endpoint=http://collector-alloy:4317"
  echo "🪨  Running with Alloy exporter"

else
  EXPORTER="otlp"
  ENDPOINT="--exporter_otlp_endpoint=http://otel-collector:4317"
  echo "🚀 Running with OTLP exporter"
fi

opentelemetry-instrument \
  --traces_exporter=$EXPORTER \
  --metrics_exporter=none \
  --logs_exporter=none \
  --service_name=pyramid-app \
  $ENDPOINT \
  pserve development-docker.ini
