'''
Summary
This script is used for Audio Utils Functions
'''
import wave as w
import os
import struct

# Create WAV Files
def CreateWAVFile(filepath, nchannels, sampwidth, framerate, nframes, comptype, compname):
    #open(filepath, 'w+')
    fw = OpenWAV(filepath, 'w')
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    params = (nchannels, sampwidth, framerate, nframes, comptype, compname)
    fw.setparams(params)

# Open WAV Files
def OpenWAV(filepath, mode):
    if not os.path.exists(filepath):
        open(filepath, 'w+')
    if mode in ['r', 'rb', 'Read', 'read']:
        return w.open(filepath, 'rb')
    if mode in ['w', 'wb', 'Write', 'write']:
        return w.open(filepath, 'wb')

def WriteBytesToWAV(filepath, data, datasize, nchannels=2, sampwidth=3, framerate=48000, comptype='NONE', compname='not compressed'):
    if not os.path.exists(filepath):
        CreateWAVFile(filepath, nchannels, sampwidth, framerate, datasize, comptype, compname)
        fw = OpenWAV(filepath, 'w')
        for sample in data:
            fw.writeframes(struct.pack('h', int( sample * 32767.0 )))
        #fw.writeframes(data)
        fw.close()
    else:
        fr = OpenWAV(filepath, 'r')
        fw = OpenWAV(filepath, 'w')
        fw.setnframes(fr.getnframes() + datasize)
        fw.writeframes(data)
        fr.close()
        fw.close()

def save_wav(file_name, audio):
    # Open up a wav file
    wav_file=w.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    sample_rate = 48000
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the 
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        print("Sample:", type(sample), sample)
        wav_file.writeframes(sample)

    wav_file.close()

    return

# Driver Code
path = 'E:/Github Codes and Projects/Projects/MediaTor-Project/MediaFiles/TestAudio.wav'
fr = OpenWAV(path, 'r')
data = fr.readframes(100)
print(fr.getparams())
save_path = 'E:/Github Codes and Projects/Projects/MediaTor-Project/MediaFiles/TestAudio2.wav'
WriteBytesToWAV(save_path, data, 100)
# save_wav(save_path, data)
fr.close()
