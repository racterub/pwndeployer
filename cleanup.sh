#!/bin/bash

if [ -f docker-compose.yml ]; then
    rm docker-compose.yml;
else
    echo "Docker-compose config not found, this needs to recover manually";
    exit;
fi

for d in `find chal/* -type d -maxdepth 0`; do
    for f in `find ${d}/* -type f -maxdepth 0`; do
        rm ${f};
    done;
    mv ${d}/bin/* ${d}/;
    rm -r ${d}/bin;
done;

if [ -d libc ]; then
    sudo rm -r libc/;
fi
