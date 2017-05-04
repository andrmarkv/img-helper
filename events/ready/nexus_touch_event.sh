#!/bin/sh
sendevent /dev/input/event1 3 57 470
sendevent /dev/input/event1 3 53 $1
sendevent /dev/input/event1 3 54 $2
sendevent /dev/input/event1 3 58 47
sendevent /dev/input/event1 0 0 0
sendevent /dev/input/event1 3 57 -1
sendevent /dev/input/event1 0 0 0
