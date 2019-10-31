#!/bin/bash

name=twitter-discordbot

docker rm -f $name
docker image rm $name
docker build --tag $name .
docker run -d --name $name $name
