#!/usr/bin/python

import os

DEVICE = '/dev/input/event1'

def convert_c(file_name):
    f = open(file_name, 'r')
    fw = open (file_name + ".sh", 'w')
    
    isFirst = True
    
    for line in f:
        global DEVICE
        
        if len(line) <= 3:
            continue
        tokens = line.split(' ')
        
        if isFirst:
            lout = ''
            isFirst = False
        else:
            lout = ';'
            
        for t in tokens:
            lout = lout + t.rstrip()
        
        fw.write(lout)
    f.close()
    fw.close()

def convert_file(file_name):
    f = open(file_name, 'r')
    fw = open (file_name + ".sh", 'w')
    
    fw.write('#!/bin/sh\n')
     
    for line in f:
        global DEVICE
        
        if len(line) <= 3:
            continue
        tokens = line.split(' ')
        lout = 'sendevent ' + DEVICE
        for t in tokens:
            v = int(t, 16)
            lout = lout + ' ' + str(v)
        fw.write(lout + '\n')
    f.close()
    fw.close() 

def convert_file_adb(file_name):
    f = open(file_name, 'r')
    fw = open (file_name + ".sh", 'w')
    
    fw.write('#!/bin/bash\n')
    
    for line in f:
        global DEVICE
        
        if len(line) <= 3:
            continue
        tokens = line.split(' ')
        lout = 'adb shell sendevent ' + DEVICE
        for t in tokens:
            v = int(t, 16)
            lout = lout + ' ' + str(v)
        fw.write(lout + '\n')
    f.close()
    fw.close() 


path = "../events/"

results = list();

for f in os.listdir(path):
    if f.endswith('.txt'):
        print f
        convert_c(os.path.join(path, f));
        #convert_file(os.path.join(path, f));
        #convert_file_adb(os.path.join(path, f));

