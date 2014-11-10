import time
#h5py is the database
import h5py
import sys
import numpy as np
import matplotlib.pyplot as plt
import numexpr as ne
#os used to use directories
import os

def plotFreq(fileName):

	#name of h5 file being read
	#fileName = 'data/Datalog - 2014 06 09, Mon, 00-34-40.h5 #used if we want this hard-coded
	#reads file with name fileName
	file = h5py.File(fileName,"r")

	#collects all the start frequencies in the file and puts them in a list
	allStartFreq = file['Spectrum_Data'][:,1]
	#: every row 1st column [:,1] [row,column]
	startFreqList = list(set(allStartFreq))

	#beginning plot with the starting frequency only this is a 
	#reminder from caio's code will be eliminated later
	plt.plot((file['Spectrum_Data'][i,4:len(file['Spectrum_Data'][0,:])]), 'g--')

	# a =  0 #will set a starting point if needed

	#finds how many frequency sweeps have been made in the file
	length = len(file[:,0])
	#searches through the file until all pieces sweeps of the same frequency have been found
	#plots all frequency sweeps of the same start frequency
	while (allStartFreqs[i] == allStartFreqs[i + 1]):
		plt.plot((file['Spectrum_Data'][i,4:len(file['Spectrum_Data'][0,:])]), 'c--')
		i += 1
	
	plt.show()
	
	print((file['Spectrum_Data'][:,2:len(file['Spectrum_Data'][0,:])]))

def concatenate(directory):
	"""this will combine data-logs in a directory this needs to be debugged"""
	"""find what is in the directory,  then find the first spectra of every h5 file
	then make a new h5 file with the parts from the old files
	we have to make a new header probably just take scavenge other files
	plug in directory when method is called
	lets sort by start frequency first, then by Unicode time. Unicode time should be unique in this instance"""
	
	#creates a file named concatenate
	#does not make a new file if a Concatenate.hdf5 exists
	#not sure if h5 or hdf5 is right one to use
	h5py.File('concatenate.h5','w-')
	#used to write to the file
	concat = h5py.File('concatenate.h5','r+')
	#makes a list of the files in directory assume only h5 files in directory
	h5Files = os.listDir(directory)
	#number of h5 files
	numH5Files = len(h5Files)
	#list with current row of each file (used when concatenating 
	j = [0] * numH5Files
	#make a list which holds Unicode time (row 0)
	uniTime = [0] * numH5Files
	#make a list which holds start frequency (row 1)
	startFreq = [0] *numH5Files
	#this is the list of objects used to read the files
	readH5Files = [None] * numH5Files
	#this will tell how many rows exist in files
	length = [0] * numH5Files
	k = 0
	
	dset = concat.create_dataset('Spectrum_Data', (100,), dtype='f64')
	
	while (k < numH5Files):
		#this instantiates the list of objects used to read the files
		readH5Files[k] = h5py.File(h5Files[k])
		uniTime[k] = readH5Files[k]['Spectrum_Data'][0,0]
		
		startFreq[k] = readH5Files[k]['Spectrum_Data'][0,1]
		#this finds the length by finding the number of items in the entire data set / the number of columns
		#I was unable to find a method which returned the number of rows
		length[k] = readH5Files[k].size / readH5Files[k].len()
		k +=1
		
	
	"""concatenate needs two groups inside it
	it needs acquire data (i do not know what this does)
	it also needs Spectrum_Data (this is the main one we are using)
	we also need to add the metadata header
	"""
	#if end is true then we have reached the end of all files being concatenated
	end = False
	while (end == False):
	
		l = 0
		firstFreq = 0
		while (l < numH5Files):
			#this compares the current row number of a file with the total number of rows in the file if j[l] >= length[l]
			#then we know that it has reached the end of the file and must ignore this next point
			if (j[l] < length[l]):
				#if firstFreq == 0 then no original frequency has been chosen and it will save the first start frequency it sees
				#otherwise it will check to see if the new frequency is lower than the old frequency
				if (firstFreq == 0 || firstFreq > startFreq[l]:
					#if either of these are true it saves this as firstFreq
					firstFreq = startFreq[l]
			
		m = 0
		#timeUni is the index which indicates the file with the correct starting frequency (== firstFreq) and earliest Unicode time
		timeUni = 0
		while (m < numH5Files):
			#this compares the current row number of a file with the total number of rows in the file if j[m] >= length[m]
			#then we know that it has reached the end of the file and must ignore this next point
			if (j[m] < length[m]):
				#if this is true then we know that this has the correct starting frequency
				if (firstFreq == uniTime[k]:
					#this checks to see is this file has a earlier Unicode time than the current lowest
					if (readH5Files[timeUni]['Spectrum_Data'][j[timeUni],0]) > uniTime[k]):
						timeUni = m
			m += 1
			
		"""HERE we add the data set of index timeUni to the concatenate file"""
		n = 0
		while (firstFreq == readH5Files[timeUni]['Spectrum_Data'][j[timeUni] + n,1])
			
			#save the n to new file
		j[timeUni] += n
		
		o = 0
		#if end not changed to false then we know that all files have reached the end.
		end = True
		while (o < numH5Files):
			#if the current row < row length of any file the end is turned false
			if (j[o] < length[o]):
				end = False
			o += 1


def avgSamples(specData):
	"""Averages samples that are taken from each frequency.
    All values including saveTime, startFreq, binSize, and runningSumItems are averaged.
    Input: the Spectrum_Data group from the hdf5 file.
    Output: a two dimensional array that is similar in structure to the input, but with one spectrum per frequency change.
    """

def waveformGenerate(avgSpecData):
    """Creates a complete waveform for each sweep
    All values including saveTime, startFreq, binSize, and runningSumItems are averaged.
    Input: the averaged samples from avgSamples().
    Output: a two dimensional array that provides a waveform for each completed sweep"""
