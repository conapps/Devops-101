#!/bin/bash

# Comando que simplifica el envío de comandos al router de cisco.

if [[ -z "$AUTH" ]]; then
  echo "No ha configurado sus credenciales."
  echo "Registrelas mediante el siguiente comando:"
  echo ""
  echo "export AUTH='conatel:conatel'"
  exit 1
fi

if [[ -z "$API" ]]; then
  echo "No se configuro la API."
  echo "Registrela mediante el siguiente comando:"
  echo "export API='https://10.X.254.254'"
  echo ""
  echo "OBS: La 'X' corresponde al número de su pod."
  exit 1
fi

if [[ -z "$METHOD" ]]; then
  export METHOD="GET"
fi

curl -u $AUTH \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Accept: application/yang-data+json, application/yang-data.errors+json' \
  -X "$METHOD" \
  -k -s "$API/$1" | jq