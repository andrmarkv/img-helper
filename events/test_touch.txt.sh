#!/bin/sh
sendevent /dev/input/event1 3 57 1522
sendevent /dev/input/event1 3 53 353
sendevent /dev/input/event1 3 54 474
sendevent /dev/input/event1 1 330 1
sendevent /dev/input/event1 0 0 0
sendevent /dev/input/event1 3 57 4294967295
sendevent /dev/input/event1 1 330 0
sendevent /dev/input/event1 0 0 0
