# -*- coding: utf-8 -*-
"""
Created on Thu May 23 13:03:28 2019

@author: Jiang Li
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

def plotCycles(fileDir, animalID, saveOutPutFile = False, resolution = 80, time = [] , colors=[]):
	# input args: 
	# fileDir = directory for the input excel file, id = mouse id, 
	# saveFile = true, will save plot to .png in the current folder, resolution = dpi of the plot, 
	# time = select time for analysis.
	
	# read data from the check if the column "Time" exists in the dataframe
	data=pd.read_excel(fileDir)
	if 'Time' not in data.columns:
		data.loc[:,'Time'] = 1; # if not exist, assign all data to group 1
   
	# select the cycle data belong to the specified mouse
	mouse_data = pd.DataFrame()
	mice_list = data['Mouse_id'].unique().tolist()
	mouse_id = animalID
	if mouse_id not in mice_list:
		print('Mouse not found!')
	else:
		if not time: # if the time is not specified, take all the data from this mouse
			mouse_data = data.loc[data['Mouse_id']==mouse_id].copy()
		else:
			mouse_data = data.loc[(data['Mouse_id']==mouse_id) & (data['Time'].isin(time))].copy()
			
	# check if input args time is empty. If empty, generate values based on the data
	num_of_period = mouse_data['Time'].nunique()
	if len(time)!=num_of_period:
		if len(time) > num_of_period:
			print(str(mouse_id) + 'ERROR: too many time inputs')
		time = mouse_data['Time'].unique().tolist()
	# check if input args colors has the same length as the real time group data. Otherwise generate default values
	if len(colors)!=num_of_period:
		colors = ['black']*num_of_period
		   
	# lambda input function for convert cycle stage to numbers
	# cycle stages can only be 'E', 'M', 'D', 'FEW' or 'No data'
	def cycleToNum(row):
		if row['CycleStage'] == 'E':
			val = 1
		elif row['CycleStage'] == 'M':
			val = 2
		elif row['CycleStage'] == 'D' or row['CycleStage'] == 'FEW':
			val = 3
		elif row['CycleStage'] == 'P':
			val = 4
		elif row['CycleStage'] == 'No data': 
			val = 0
		else:
			val = -1 # if contains invalid cycle stages
			print(row + ' contains invalid cycle stage')
		return val
	mouse_data.loc[:,'CycleNumeric'] = mouse_data.apply(cycleToNum, axis = 1)
	mouse_data = mouse_data.loc[mouse_data['CycleNumeric']!=-1] # remove the invalid cycle data

	# generate fake data for the days with 'No data'
	for index, row in mouse_data.iterrows():
		if row['CycleNumeric'] == 0:
			cycle_diff = mouse_data.loc[index+1,'CycleNumeric'] - mouse_data.loc[index-1,'CycleNumeric']
			if cycle_diff == 1 or cycle_diff == 0:
				mouse_data.loc[index,'CycleNumeric'] = mouse_data.loc[index-1,'CycleNumeric']
			elif cycle_diff == 2:
				mouse_data.loc[index,'CycleNumeric'] = mouse_data.loc[index-1,'CycleNumeric'] +1
			elif mouse_data.loc[index+1,'CycleNumeric']== 1 and mouse_data.loc[index-1,'CycleNumeric'] == 3:
				mouse_data.loc[index,'CycleNumeric'] = 4
			elif mouse_data.loc[index+1,'CycleNumeric']== 2 and mouse_data.loc[index-1,'CycleNumeric'] == 4:
				mouse_data.loc[index,'CycleNumeric'] = 1
			else:
				mouse_data.loc[index,'CycleNumeric'] = mouse_data.loc[index-1,'CycleNumeric']               
    # make plot
	labels = ['E', 'M', 'D', 'P']
	first_day = mouse_data.loc[mouse_data.index[0],'CycleDate']
	last_day = mouse_data.loc[mouse_data.index[-1],'CycleDate']
	total_days = (last_day-first_day).days+1
    
	fig = plt.figure(num=None, figsize=(0.15*total_days, 3), dpi=resolution)
	ax = fig.add_subplot(111)      
	for index, period in enumerate(time):
		select_color = colors[index]
		data_slice = mouse_data[mouse_data['Time']==period]
		ax.plot(data_slice['CycleDate'],data_slice['CycleNumeric'],marker='o', color = select_color, linewidth=2, ls='-', markersize = 6)
		# mark the days with 'No data' as white in the graph
		fake_data = data_slice[data_slice['CycleStage']=='No data']
		ax.plot(fake_data['CycleDate'],fake_data['CycleNumeric'],marker='o', color = select_color, mfc='white', markeredgecolor = select_color, linewidth=2, linestyle='None', markersize = 6)    
	# adjust the appearence of the plot
	plt.xticks(rotation=30,fontsize = 7)
	plt.xlim([first_day-datetime.timedelta(days=1),last_day+datetime.timedelta(days=1)])
	ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
	plt.ylim([0,5])
	plt.yticks(range(1,5),labels, fontsize = 10)
	plt.title(str(mouse_id),fontsize = 10)	
	plt.grid(color='grey', linestyle='--', linewidth=1, alpha=0.5)
	plt.tight_layout()
	# save plot to .png at local
	if saveOutPutFile == True:
		fileName = str(animalID) + '.png'
		plt.savefig(fileName,dpi=resolution,facecolor='w', edgecolor='w')
	plt.show()
    
def plotAllofThem(fileDir, saveOutPutFile = False, resolution = 80, time = [] , colors=[]):
	data=pd.read_excel(fileDir)
	mice_list = data['Mouse_id'].unique().tolist()
	for mouse in mice_list:
		plotCycles(fileDir = fileDir, animalID = mouse, saveOutPutFile = saveOutPutFile, resolution = resolution, time = time , colors=colors)    

def analysis(fileDir, saveOutPutFile = False):
	data=pd.read_excel(fileDir)
	labels = ['E', 'M', 'D', 'P','FEW']
	data = data.loc[data['CycleStage'].isin(labels)]
	if 'Time' not in data.columns:
		data.loc[:,'Time'] = 1; # if not exist, assign all data to group 1
	# Print some basic information
	mice_list = data['Mouse_id'].unique().tolist()
	print('There are ' + str(len(mice_list)) + ' mice in the data:')
	print(mice_list)
	time_list = data['Time'].unique().tolist()
	print('There are ' + str(len(time_list)) + ' different time periods in the data:')
	print(time_list)
	
	percentage_table = data[['Mouse_id', 'Time','CycleStage']].groupby(['Mouse_id', 'Time','CycleStage']).size().to_frame('days').reset_index().copy()
	sum_tabel = data[['Mouse_id', 'Time']].groupby(['Mouse_id', 'Time']).size().to_frame('totalDays').reset_index().copy()
	percentage_table = percentage_table.merge(sum_tabel, on = ['Mouse_id','Time'], how='inner')
	percentage_table['Percentage'] = percentage_table.apply(lambda row: row.days/row.totalDays, axis=1)
	percentage_table = percentage_table[['Mouse_id','Time','CycleStage','Percentage','days','totalDays']]
	percentage_table.set_index(['Mouse_id','Time','CycleStage'],inplace=True)
	if saveOutPutFile == True:
		percentage_table.to_excel('output.xlsx')
	return percentage_table