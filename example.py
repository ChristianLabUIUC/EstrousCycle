# -*- coding: utf-8 -*-
"""
Created on Thu May 23 13:16:17 2019

@author: Jiang Li
"""

from pyEstrousCycle import plotCycles, plotAllofThem, analysis

# input args: 
# fileDir = directory for the input excel file,
# animalID = the unique identifier for a animal, the code will generate the graph for this animal 
# saveFile = true, will save plot to .png in the current folder, 
# resolution = dpi of the plot, 
# time = select time for making plot. arg should be a list
# color = select color for making plot. arg should be a list

plotCycles(fileDir='test.xlsx', animalID= 233, saveOutPutFile = True, resolution = 300, time = [1,2] , colors=['black','red'])

plotAllofThem(fileDir='test.xlsx', saveOutPutFile = True, resolution = 300, time = [1,2] , colors=['black','red'])

percentage_table = analysis('test.xlsx', saveOutPutFile = True)

print(percentage_table)
