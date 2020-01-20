#!/bin/bash

apt-get update -qq \
&& apt-get install -y --no-install-recommends build-essential \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
    
