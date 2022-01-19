import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw

afilt =[1.0000,   -1.7027,    1.4164,   -0.5560,    0.0889]
bfilt =[0.0154,    0.0616,   0.0925,    0.0616,    0.0154]



pre_recorded = '3.wav'
rate_pre_recorded, pre_recorded = wavfile.read(pre_recorded);
pre_recorded = np.array(pre_recorded, dtype='float')
signal_length = len(pre_recorded)

pre_recorded2 = '2.wav'
rate_pre_recorded2, pre_recorded2 = wavfile.read(pre_recorded2);
pre_recorded2 = np.array(pre_recorded2, dtype='float')
signal_length2 = len(pre_recorded2)

pre_recorded3 = '1.wav'
rate_pre_recorded3, pre_recorded3 = wavfile.read(pre_recorded3);
pre_recorded3 = np.array(pre_recorded3, dtype='float')
signal_length3 = len(pre_recorded3)


pre_recorded = signal.lfilter(bfilt, afilt, pre_recorded)
pre_recorded2 = signal.lfilter(bfilt, afilt, pre_recorded)
pre_recorded3 = signal.lfilter(bfilt, afilt, pre_recorded)

p1file = 'p1.wav'
_ , p1 = wavfile.read('p1.wav');
p1 = np.array(p1, dtype='float')


p2file = 'p2.wav'
_ , p2 = wavfile.read(p2file);
p2 = np.array(p2, dtype='float')


p3file = 'p3.wav'
_ , p3 = wavfile.read(p3file);
p3 = np.array(p3, dtype='float')



_ , p1_2 = wavfile.read('1_2.wav');
p1_2 = np.array(p1_2, dtype='float')



_ , p2_3 = wavfile.read('2_3.wav');
p2_3 = np.array(p2_3, dtype='float')

p1 = signal.lfilter(bfilt, afilt, p1)
p2 = signal.lfilter(bfilt, afilt, p2)
p3 = signal.lfilter(bfilt, afilt, p3)

p1_2 = signal.lfilter(bfilt, afilt, p1_2)
p2_3 = signal.lfilter(bfilt, afilt, p2_3)

max_p = np.max(np.concatenate((np.abs(p1),np.abs(p2), np.abs(p3)), axis=0))

p1 = p1/max_p
p2 = p2/max_p
p3 = p3/max_p

len_p1 = len(p1)
len_p2 = len(p2)
len_p3 = len(p3)

half_len_p1 = int(len(p1)/2) + 1
half_len_p2 = int(len(p2)/2) + 1
half_len_p3 = int(len(p3)/2) + 1

max_pd = np.max(np.concatenate((np.abs(p1_2),np.abs(p2_3)), axis=0))

p1_2 = p1_2/max_pd
p2_3 = p2_3/max_pd

len_p1_2 = len(p2_3)
len_p2_3 = len(p2_3)


half_len_p1_2 = int(len_p1_2/2) + 1
half_len_p2_3 = int(len_p2_3/2) + 1






import pyaudio, wave, struct, math
from myfunctions import normalize, dft, where, cross_correlation_using_fft

#normalized1 = normalize(pre_recorded)
#normalized1[np.abs(normalized1) < 0.1] = 0
#sfft1 = dft(normalized1 , signal_length)

WIDTH       = 2         		# Number of bytes per sample
CHANNELS    = 1         		# mono
RATE        = rate_pre_recorded     	# Sampling rate (frames/second)
DURATION    = 100        			# duration of processing (seconds)

max_length = np.max([signal_length,signal_length2,signal_length3])

BLOCKLEN = int(max_length/2)
# Number of blocks to run for
num_blocks = int(RATE / BLOCKLEN * DURATION)



p = pyaudio.PyAudio()
stream = p.open(format = pyaudio.paInt16,  
                channels = 1, 
                rate = RATE,
                input = True, 
                output = False)

K = DURATION * RATE     # K : Number of samples to process

#print('* Start')


last_taken_samples = BLOCKLEN * [0]   # list of zeros
last_taken_samples1 = np.array(last_taken_samples, dtype='float')
last_taken_samples2 = np.array(last_taken_samples, dtype='float')
last_taken_samples3 = np.array(last_taken_samples, dtype='float')
last_taken_samples5 = np.array(last_taken_samples, dtype='float')
last_taken_samples4 = np.array(3 * BLOCKLEN * [0], dtype='float')


num_blocks = int(RATE / BLOCKLEN * DURATION)
idx = int(BLOCKLEN/2) #+ 1
half_idx = int(idx/2)


pre_recorded = normalize(pre_recorded)
pre_recorded2 = normalize(pre_recorded2)
pre_recorded3 = normalize(pre_recorded3)


#sfft = dft(pre_recorded , BLOCKLEN)

ORDER = 4   # filter is fourth order
states = np.zeros(ORDER)
states.reshape(ORDER)


#print('listening now')
#print('Block Duration in sec:' ,BLOCKLEN/6000 )
log = []
log_val = []
print('I am listening, call my name when you are ready!')
for n in range(0, num_blocks):

    cond1 = 0;
    cond2 = 0;
    cond3 = 0;

    input_bytes = stream.read(BLOCKLEN)   # BLOCKLEN = number of frames read
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)

    # filter
    [input_tuple, states] = signal.lfilter(bfilt, afilt, input_tuple, zi = states)


    last_taken_samples1 = np.array(input_tuple, dtype='float')




    #last_taken_samples1[np.abs(last_taken_samples1) < 10] = 0.001
    
    last_taken_samples1 = normalize(last_taken_samples1)

    last_taken_samples4 = np.concatenate((last_taken_samples5,last_taken_samples3,last_taken_samples2, last_taken_samples1), axis=0) #one dimensional array

    r55 = signal.correlate(last_taken_samples4[half_idx:], p1, 'full');
    b5 = np.argmax(np.abs(r55));
    a = r55[b5]
    b5 = b5+half_idx;

    

    if b5 <  BLOCKLEN*2 + half_idx:

        p1_score = np.max(signal.correlate(last_taken_samples4[b5 - half_len_p1 : b5 + half_len_p1], p1, 'full'))             
        #print('part 1 score:',p1_score)

        p12_score = np.max(signal.correlate(last_taken_samples4[b5 - half_len_p1 : b5 + half_len_p1_2 + half_len_p1], p1_2, 'full'))             
        #print('part 1_2 score:',p12_score)

        p2_loc = b5 + half_len_p1
        r66 = signal.correlate(last_taken_samples4[p2_loc:(2*BLOCKLEN  + idx)], p2, 'full');
        b6 = np.argmax(np.abs(r66));
        b = r66[b6]
        #print(b)
        b6 = p2_loc + b6;

        if b6 <  3*BLOCKLEN:

            p2_score = np.max(signal.correlate(last_taken_samples4[b6 - half_len_p2 : b6 + half_len_p2], p2, 'full'))             
            #print('part 2 score:',p2_score)

            p23_score = np.max(signal.correlate(last_taken_samples4[b6 - half_len_p2 : b6 + half_len_p2_3 + half_len_p2], p2_3, 'full'))             
            #print('part 2_3 score:',p23_score)

            p3_loc = b6 + 200
            r77 = signal.correlate(last_taken_samples4[p3_loc:], p3, 'full');
            b7 = np.argmax(np.abs(r77));
            c = r77[b7]        
            b7 = p3_loc + b7;

            if 4*BLOCKLEN - half_len_p3 >  b7:

                p3_score = np.max(signal.correlate(last_taken_samples4[b7 - half_len_p3 : b7 + half_len_p3], p3, 'full'))             
                #print('--------------case1-----------------------part 3 score:',p3_score)
   



                if p23_score > p12_score:
                    arr2 = last_taken_samples4[b6 - idx: b6 + idx]
                    r61 = np.correlate(arr2, pre_recorded, 'full');
                    r62 = np.correlate(arr2, pre_recorded2, 'full');
                    r63 = np.correlate(arr2, pre_recorded3, 'full');
                    #print('--------------case1----part2-------------ikinci-taraf-better----')
                else:
                    arr2 = last_taken_samples4[b5 - half_len_p1 : b5 + BLOCKLEN + half_len_p1]
                    r61 = np.correlate(arr2, pre_recorded, 'full');
                    r62 = np.correlate(arr2, pre_recorded2, 'full');
                    r63 = np.correlate(arr2, pre_recorded3, 'full');

                    #print('--------------case1----part1-------------------')


                r6 = np.concatenate((r61,r62, r63), axis=0) #one dimensional array

                a = np.max(r61)
                b = np.max(r62)
                c = np.max(r63)


                arr = [a, b, c]
                if(np.mean(arr)>45 and np.min(arr) > 35):
                    print("Security: Hey There!")
                    print("Security: What is the password?")
                    break

        
        

            else:

                #print('-----case2---do-not--print--but--save---the---log-------')
                if p23_score > p12_score:
                    arr2 = last_taken_samples4[b6 - idx: b6 + idx]
                    r61 = np.correlate(arr2, pre_recorded, 'full');
                    r62 = np.correlate(arr2, pre_recorded2, 'full');
                    r63 = np.correlate(arr2, pre_recorded3, 'full');
                    log.append(p23_score)
                    log_val.append(n)

                else:
                    arr2 = last_taken_samples4[b5 - half_len_p1 : b5 + BLOCKLEN + half_len_p1]
                    r61 = np.correlate(arr2, pre_recorded, 'full');
                    r62 = np.correlate(arr2, pre_recorded2, 'full');
                    r63 = np.correlate(arr2, pre_recorded3, 'full');
                    log.append(p12_score)
                    log_val.append(n)
                

                r6 = np.concatenate((r61,r62, r63), axis=0) #one dimensional array


            a = np.max(r61)
            b = np.max(r62)
            c = np.max(r63)
            d = np.max(np.correlate(last_taken_samples4, pre_recorded, 'full'));

            a1 = np.min(r61)
            b1 = np.min(r62)
            c1 = np.min(r63)

            arr = [a, b, c]
            #if(np.mean(arr)>45 and np.min(arr) > 45):
                #print('total score---------------->',a,b,c,d)
                #print('total score---------------->',a1,b1,c1)
                #print('little---->',p1_score,p2_score,p12_score,p23_score)

    last_taken_samples5 = last_taken_samples3
    last_taken_samples3 = last_taken_samples2
    last_taken_samples2 = last_taken_samples1


stream.stop_stream()
stream.close()
p.terminate()

