import numpy as np
import scipy
import matplotlib.pyplot as plt
import pydub
import os

from scipy.io import wavfile


# Fixing random state for reproducibility
np.random.seed(19680801)

dt = 0.01
t = np.arange(0, 30, dt)
white_noise_1 = np.random.randn(len(t))                 # white noise 1

np.random.seed(19680802)
white_noise_2 = np.random.randn(len(t))                 # white noise 2

# Two signals with a coherent part at 10Hz and a random part
sine_wave_1 = np.sin(2 * np.pi * 10 * t + 5)			 # sine wave 1
sine_wave_2 = np.sin(2 * np.pi * 10 * t)				 # sine wave 2

#correlate signals
from scipy import signal
corrw = signal.correlate(white_noise_1, white_noise_2, mode='full')
corrs = signal.correlate(sine_wave_1, sine_wave_2, mode='full')
xcorr = np.arange(corrw.size)


#======DELAY=================================================

from pydub import AudioSegment

audio_in_file = "beat16.wav"
audio_out_file = "beat16_3.wav"

# create 3 sec of silence audio segment
three_sec_segment = AudioSegment.silent(duration=3000)  #duration in milliseconds

#read wav file to an audio segment
music_file_1 = AudioSegment.from_wav(audio_in_file)	 # music file 1

#Add above two audio segments    
music_file_2 = three_sec_segment + music_file_1					 # music file 2

#save modified audio
music_file_2.export(audio_out_file, format="wav")



#======WAV=================================================

# Load the data and calculate the time of each sample
samplerate1, song1 = wavfile.read('beat16.wav')
times1 = np.arange(len(song1))/float(48000)					#samplerate 48000, 16-bit
samplerate2, song2 = wavfile.read('beat16_3.wav')
times2 = np.arange(len(song2))/float(48000)					#samplerate 48000, 16-bit

# Plot Audio File
plt.figure(figsize=(30, 4))
plt.fill_between(times1, song1[:,0], song1[:,1], color='k') 
plt.xlim(times1[0], times1[-1])
plt.xlabel('time (s)')
plt.ylabel('amplitude')
#plt.show()

#Correlate Music
corrm = signal.correlate(song1, song2, mode='full')
xcorr2 = np.arange(corrm.size)
#======PLOT=================================================

# plot white noise correlation for 3 seconds
fig, axs = plt.subplots(2, 1)
axs[0].plot(t, white_noise_1, t, white_noise_2)
axs[0].set_xlim(0, 3)
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('White Noise 1 and 2')
axs[0].grid(True)

axs[1].plot(corrw)
axs[1].set_xlabel('Correlation Iteration')
axs[1].set_ylabel('Correlation')
axs[1].set_title('Correlation Between White Noise Signals')


fig.tight_layout()
#plt.show()

# plot sin wave correlation for 8 seconds, same frequency
fig, axs = plt.subplots(2, 1)
axs[0].plot(t, sine_wave_1, t, sine_wave_2)
axs[0].set_xlim(0, 3)
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Sine Wave 1 and 2')
axs[0].grid(True)

axs[1].plot(corrs)
axs[1].set_xlabel('Correlation Iteration')
axs[1].set_ylabel('Correlation')
axs[1].set_title('Correlation Between Sine Waves With Frequency 10Hz')

fig.tight_layout()
#plt.show()

# plot music delay correlation for 8 seconds
fig, axs = plt.subplots(2, 1)
axs[0].plot(times1, song1[:,0], times1, song1[:,1], times2, song2[:,0], times2, song2[:,1])
axs[0].set_xlim(0, 8)
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Song1 and Song2')
axs[0].grid(True)

axs[1].plot(corrm)
axs[1].set_xlabel('Correlation Iteration')
axs[1].set_ylabel('Correlation')
axs[1].set_title('Correlation Between Music Files With Delay 3 Sec')

fig.tight_layout()
plt.show()

