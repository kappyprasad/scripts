#!/usr/bin/env bash

mailman.py \
    -s \
    -j "Test Subject" \
    -b "Test Body" \
    -t eddo888@tpg.com.au david.edson@gmail.com \
    -f _test/DavidEdson-CorpratePhoto.png _test/DavidEdson-hand.jpeg
