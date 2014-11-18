"""
Author: Shanen Cross
11-18-2014
Purpose: Averaging columns in every x rows in h5 data files produced by Connor's SpectraLogger

h5 elements appear to have 46 decimal places. HDFView and the print command
truncate these though (the print command more so).
print truncates to 10 decimals, and HDFView to 14.
Trailing zeroes are excluded for both.

"""

import h5py
import numpy as np
import pdb #debugger

def convert_dBm_to_linear(dBm_power):
	#To convert decibel milliwatt units to linear milliwatts
	#conversion formula from wiki page for dBm unit
	mW_power = np.power(10,dBm_power/10.0)
	return mW_power
	
def find_rows_per_freq(dataset):
	#This is meant to find out how many rows there are per frequency,
	#assuming that each frequency (except potentially the last) has
	#the same number of rows.
	
	#Unfinished, not implemented yet.
	
	loop = True
	
	rows = 0
	i=0
	freq=dataset[1,0]
	#while(loop):
	#	if (dataset[i,1])
	
def generate_averaged_array(dataset, decibelPower=True):

	#Modify if the number of rows for each frequency is something else.
	rows_per_freq = 6
	
	#Handles possibility that number of rows may not be divisible by the row per freq number
	#since the last frequency may have less rows
	if (dataset.shape[0] % rows_per_freq == 0):
		final_array = np.zeros([dataset.shape[0]/rows_per_freq,dataset.shape[1]])
	else:
		final_array = np.zeros([dataset.shape[0]/rows_per_freq+1,dataset.shape[1]])
	
	#iterate through every set of rows for each frequency
	i=0
	while (i < dataset.shape[0]):
		#pdb.set_trace()
		#print "i:", i
		
		#average times together for current time
		average_time = np.mean(dataset[i:i+rows_per_freq,0])
		
		powers = dataset[i:i+rows_per_freq,4:]
		
		#convert decibel power to linear power if necessary
		if (decibelPower==True):
			powers = convert_dBm_to_linear(powers)
			
		#average rows together for current freq
		average_power_array = np.mean(powers, axis=0)
		
		#print "Average time:\n", average_time
		#print "Average Powers:\n", average_power_array, "\n"
		
		#give corresponding element of our final array the average time
		final_array[i/rows_per_freq,0] = average_time
		
		# Can assume these are identical in the final array, so we don't have to average them
		final_array[i/rows_per_freq,1:4] = dataset[i,1:4] 
		
		#put averaged powers values in final array
		final_array[i/rows_per_freq,4:] = average_power_array

		#print "Final array:\n", final_array, "\n"
		#Final array has linear powers in milliwatts
		
		#Move onto the next set of rows for the next frequency
		i += rows_per_freq
	
	print final_array
	print len(final_array)	
	print len(final_array[0])
	return final_array

#way more efficient (no while loop)
#but currently doesn't handle case where last frequency
#has fewer rows than previous frequencies
def alt_generate_averaged_array(dataset, decibelPower=True):
	#Modify if the number of rows for each frequency is something else.
	rows_per_freq = 6
	
	old_array = np.array(dataset)
	
	#Columns 4 and onward are powers
	#This converts dBm powers to linear milliwatts if necessary
	if (decibelPower==True):
		old_array[:,4:] = convert_dBm_to_linear(old_array[:,4:])
	
	#The last frequency may have fewer rows. So we check
	#to see of this is the case by taking the remainder of
	#the number of rows divided by the rows per freq of the
	#preceding frequencies
	remainder = dataset.shape[0] % rows_per_freq
	if (remainder == 0):
		#If there is no remainder, take the average of the columns for every rows_per_freq rows
		final_array = np.mean(old_array.reshape(-1,rows_per_freq,dataset.shape[1]), axis=1)
	else:
		#If there is a remainder, separate the rows for the last frequency into a separate array
		#from the preceding frequencies
		most_of_old_array = old_array[:(-1*remainder)]
		end_of_old_array = old_array[(-1*remainder):]
		
		#Average the columns for every rows_per_freq rows in the first section.
		most_of_final_array = np.mean(most_of_old_array.reshape(-1,rows_per_freq,dataset.shape[1]), axis=1)
		#Average the columns for the final set of rows
		end_of_final_array = np.mean(end_of_old_array, axis=0)
		
		#final_array = np.zeros([dataset.shape[0]/rows_per_freq + 1,dataset.shape[1]])
		#final_array[:-1] = most_of_final_array
		#final_array[-1] = end_of_final_array
		
		#Combine the two arrays of averages/
		#The average array for the final set of rows will be a 1D array,
		#so we must put it in [] to make into a 2D array for concatenation
		final_array = np.concatenate((most_of_final_array, [end_of_final_array]))
	
	print final_array
	print len(final_array)
	print len(final_array[0])
	return final_array

#Code for testing function

#reading in dataset from file
filepath = 'data/'
#filename = 'Datalog - 2014 10 22, Wed, 16-51-56.h5'
filename = 'Datalog - 2014 10 22, Wed, 16-56-08.h5'
datafile = h5py.File(filepath+filename, "r")	
our_dataset = datafile["Spectrum_Data"]

#resulting_array = generate_averaged_array(our_dataset)
resulting_array = alt_generate_averaged_array(our_dataset)