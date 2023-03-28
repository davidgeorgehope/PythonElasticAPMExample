#!/bin/bash
# load_test.sh

url="http://localhost:5001"

for i in {1..1000}
do
  curl -s -o /dev/null $url
  sleep 0.1
done

