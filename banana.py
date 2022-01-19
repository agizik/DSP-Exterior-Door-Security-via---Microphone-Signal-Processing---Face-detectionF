import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt
from myfunctions import normalize, where

import pyaudio, wave, struct, math
#print(2**(6/12))
afilt =[1.0000,   -1.7027,    1.4164,   -0.5560,    0.0889]
bfilt =[0.0154,    0.0616,   0.0925,    0.0616,    0.0154]

pre_recorded1 = 'b1.wav'
rate_pre_recorded, pre_recorded1 = wavfile.read(pre_recorded1);
pre_recorded1 = np.array(pre_recorded1, dtype='float')
signal_length1 = len(pre_recorded1)

pre_recorded2 = 'b2.wav'
rate_pre_recorded, pre_recorded2 = wavfile.read(pre_recorded2);
pre_recorded2 = np.array(pre_recorded2, dtype='float')
signal_length2 = len(pre_recorded2)

pre_recorded3 = 'b3.wav'
rate_pre_recorded, pre_recorded3 = wavfile.read(pre_recorded3);
pre_recorded3 = np.array(pre_recorded3, dtype='float')
signal_length3 = len(pre_recorded3)

pre_recorded4 = 'b4.wav'
rate_pre_recorded, pre_recorded4 = wavfile.read(pre_recorded4);
pre_recorded4 = np.array(pre_recorded4, dtype='float')
signal_length4 = len(pre_recorded4)

pre_recorded5 = 'b5.wav'
rate_pre_recorded, pre_recorded5 = wavfile.read(pre_recorded5);
pre_recorded5 = np.array(pre_recorded5, dtype='float')
signal_length5 = len(pre_recorded5)

pre_recorded6 = 'b6.wav'
rate_pre_recorded, pre_recorded6 = wavfile.read(pre_recorded6);
pre_recorded6 = np.array(pre_recorded6, dtype='float')
signal_length6 = len(pre_recorded6)


pre_recorded1 = signal.lfilter(bfilt, afilt, pre_recorded1)
pre_recorded2 = signal.lfilter(bfilt, afilt, pre_recorded2)
pre_recorded3 = signal.lfilter(bfilt, afilt, pre_recorded3)
pre_recorded4 = signal.lfilter(bfilt, afilt, pre_recorded4)
pre_recorded5 = signal.lfilter(bfilt, afilt, pre_recorded5)
pre_recorded6 = signal.lfilter(bfilt, afilt, pre_recorded6)





pre_recorded1 = normalize(pre_recorded1)
pre_recorded2 = normalize(pre_recorded2)
pre_recorded3 = normalize(pre_recorded3)
pre_recorded4 = normalize(pre_recorded4)
pre_recorded5 = normalize(pre_recorded5)
pre_recorded6 = normalize(pre_recorded6)



max_len = np.max([signal_length1,signal_length2,signal_length3,signal_length4,signal_length5,signal_length6])


WIDTH       = 2         		# Number of bytes per sample
CHANNELS    = 1         		# mono
RATE        = rate_pre_recorded     	# Sampling rate (frames/second)
DURATION    = 100        			# duration of processing (seconds)

BLOCKLEN = int(max_len/2)
num_blocks = int(RATE / BLOCKLEN * DURATION)
idx = int(BLOCKLEN/2)

p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,  
                channels = 1, 
                rate = RATE,
                input = True, 
                output = False)


last_taken_samples = BLOCKLEN * [0]   # list of zeros
last_taken_samples1 = np.array(last_taken_samples, dtype='float')
last_taken_samples2 = np.array(last_taken_samples, dtype='float')
last_taken_samples3 = np.array(last_taken_samples, dtype='float')


ORDER = 4   # filter is fourth order
states = np.zeros(ORDER)

#print('listening now')
#print('Block Duration in sec:' ,BLOCKLEN/6000 )

for n in range(0, num_blocks):


	cond1 = 0
	cond2 = 0
	cond3 = 0
	cond4 = 0
	cond5 = 0
	cond6 = 0

	result1 = 0
	result2 = 0
	result3 = 0
	result4 = 0
	result5 = 0
	result6 = 0


	max_corr = 0
	mean_corr = 0

	input_bytes = stream.read(BLOCKLEN)   # BLOCKLEN = number of frames read
	input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)

	#input_tuple[np.abs(input_tuple) < 10] = 0.0

	[last_taken_samples1, states] = signal.lfilter(bfilt, afilt, input_tuple, zi = states)

	last_taken_samples1 = np.array(last_taken_samples1, dtype='float')

	last_taken_samples1 = normalize(last_taken_samples1)

	

	last_taken_samples4 = np.concatenate((last_taken_samples3,last_taken_samples2, last_taken_samples1), axis=0) #one dimensional array


	cr1 = signal.correlate(last_taken_samples4, pre_recorded1, 'full');
	cr2 = signal.correlate(last_taken_samples4, pre_recorded2, 'full');
	cr3 = signal.correlate(last_taken_samples4, pre_recorded3, 'full');
	cr4 = signal.correlate(last_taken_samples4, pre_recorded4, 'full');
	cr5 = signal.correlate(last_taken_samples4, pre_recorded5, 'full');
	cr6 = signal.correlate(last_taken_samples4, pre_recorded6, 'full');

	b1 = np.argmax(np.abs(cr1));
	b2 = np.argmax(np.abs(cr2));
	b3 = np.argmax(np.abs(cr3));
	b4 = np.argmax(np.abs(cr4));
	b5 = np.argmax(np.abs(cr5));
	b6 = np.argmax(np.abs(cr6));


	if b1 > BLOCKLEN and b1 <  BLOCKLEN*3:

		cond1 = 1;
		arr1 = last_taken_samples4[b1 - BLOCKLEN: b1 + BLOCKLEN]
		r1 = np.correlate(arr1, pre_recorded1, 'full');
		result1 = np.max(np.abs(r1))


	if b2 > BLOCKLEN and b2 <  BLOCKLEN*3:
		cond2 = 1;
		arr2 = last_taken_samples4[b2 - BLOCKLEN: b2 + BLOCKLEN]
		r2 = np.correlate(arr2, pre_recorded2, 'full');
		result2 = np.max(np.abs(r2))

	if b3 > BLOCKLEN and b3 <  BLOCKLEN*3:
		cond3 = 1;
		arr3 = last_taken_samples4[b3 - BLOCKLEN: b3 + BLOCKLEN]
		r3 = np.correlate(arr3, pre_recorded3, 'full');
		result3 = np.max(np.abs(r3))

	if b4 > BLOCKLEN and b4 <  BLOCKLEN*3:
		cond4 = 1;
		arr4 = last_taken_samples4[b4 - BLOCKLEN: b4 + BLOCKLEN]
		r4 = np.correlate(arr4, pre_recorded4, 'full');
		result4 = np.max(np.abs(r4))

	if b5 > BLOCKLEN and b5 <  BLOCKLEN*3:
		cond5 = 1;
		arr5 = last_taken_samples4[b5 - BLOCKLEN: b5 + BLOCKLEN]
		r5 = np.correlate(arr5, pre_recorded5, 'full');
		result5 = np.max(np.abs(r5))

	if b6 > BLOCKLEN and b6 <  BLOCKLEN*3:
		cond6 = 1;
		arr6 = last_taken_samples4[b6 - BLOCKLEN: b6 + BLOCKLEN]
		r6 = np.correlate(arr6, pre_recorded6, 'full');
		result6 = np.max(np.abs(r6))

	total = cond1*result1 + cond2*result2 + cond3*result3 + cond4*result4 + cond5*result5 + cond6*result6
	tot_div = cond1 + cond2 + cond3 + cond4 + cond5 + cond6

	max_corr = np.max([cond1*result1 , cond2*result2 , cond3*result3 , cond4*result4 , cond5*result5 , cond6*result6])

	
	if max_corr > 20:
		mean_corr = total/tot_div
		if mean_corr > 40:
			print("Security: Correct password banana is detected!")
			print("Face is detected, framed and saved with the date!")
			print("Welcome Home!")
			break

	last_taken_samples3 = last_taken_samples2
	last_taken_samples2 = last_taken_samples1


stream.stop_stream()
stream.close()
p.terminate()


