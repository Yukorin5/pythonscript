#!/usr/bin/env python
# -*- coding: utf-8 -*-

from turtle import *

for i in range(5):
    setposition(0,i*30)
    for i in range(2):
        forward(180)
        left(90)
        forward(30)
        left(90)

for i in range(6):
    setposition(i*30,0)
    for i in range(2):
        forward(30)
        left(90)
        forward(150)
        left(90)


input()
