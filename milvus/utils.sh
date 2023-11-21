#!/bin/bash

COLOR_OFF='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BROWN='\033[0;33m'
BLUE='\033[0;34m'

if [ $1 == 'start' ]
then
  printf "${GREEN}Starting milvus${COLOR_OFF}\n"
  docker compose up -d
elif [ $1 == 'connection' ]
then
  printf "${BROWN}Connection details:${COLOR_OFF}\n"
  docker port milvus-standalone 19530/tcp
elif [ $1 == 'stop' ]
then
  printf "${BLUE}Stopping containers${COLOR_OFF}\n"
  docker compose down
elif [ $1 == 'clean' ]
then
  printf "${RED}Cleaning up containers${COLOR_OFF}\n"
  rm -rf volumes
elif [ $1 == 'purge' ]
then
  printf "${RED}Purging containers and images${COLOR_OFF}\n"
fi
