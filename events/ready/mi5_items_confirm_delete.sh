#!/bin/sh

sendevent /dev/input/event4 3 53 601
sendevent /dev/input/event4 3 54 $1
sendevent /dev/input/event4 3 58 48
sendevent /dev/input/event4 3 48 3
sendevent /dev/input/event4 1 330 1
sendevent /dev/input/event4 0 0 0
sendevent /dev/input/event4 3 58 33
sendevent /dev/input/event4 3 48 2
sendevent /dev/input/event4 0 0 0
sendevent /dev/input/event4 3 57 4294967295
sendevent /dev/input/event4 1 330 0
sendevent /dev/input/event4 0 0 0
