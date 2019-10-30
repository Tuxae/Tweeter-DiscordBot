#!/bin/bash

name=tweeter-discordbot

docker rm -f $name
docker image rm $name
docker build --tag $name .
docker run -d --name $name $name
