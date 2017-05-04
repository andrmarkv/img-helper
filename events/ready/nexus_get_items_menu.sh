#!/bin/sh
sendevent /dev/input/event1 3 57 100
sendevent /dev/input/event1 3 53 557
sendevent /dev/input/event1 3 54 1608
sendevent /dev/input/event1 0 0 0
sendevent /dev/input/event1 3 57 -1
sendevent /dev/input/event1 0 0 0

sleep 2

sendevent /dev/input/event1 3 57 101
sendevent /dev/input/event1 3 53 848
sendevent /dev/input/event1 3 54 1432
sendevent /dev/input/event1 0 0 0
sendevent /dev/input/event1 3 57 -1
sendevent /dev/input/event1 0 0 0

