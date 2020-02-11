'''
Summary
This script is used for generating audio of various frequencies in piano code and mixing them

Goals
 - Piano Key Mapping
 - Audio File to bs code
 - Real time playing to piseq code
'''
import time
from scipy.io import wavfile
import numpy as np
import pygame
import os
import pickle
from tqdm import tqdm


def speedx(snd_array, factor):
    """ Speeds up / slows down a sound, by some factor. """
    indices = np.round(np.arange(0, len(snd_array), factor))
    indices = indices[indices < len(snd_array)].astype(int)
    return snd_array[indices]


def stretch(snd_array, factor, window_size, h):
    """ Stretches/shortens a sound, by some factor. """
    phase = np.zeros(window_size)
    hanning_window = np.hanning(window_size)
    result = np.zeros(int(len(snd_array) / factor + window_size))

    for i in np.arange(0, len(snd_array) - (window_size + h), h*factor):
        i = int(i)
        # Two potentially overlapping subarrays
        a1 = snd_array[i: i + window_size]
        a2 = snd_array[i + h: i + window_size + h]

        # The spectra of these arrays
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)

        # Rephase all frequencies
        phase = (phase + np.angle(s2/s1)) % 2*np.pi

        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        i2 = int(i/factor)
        result[i2: i2 + window_size] += hanning_window*a2_rephased.real

    # normalize (16bit)
    result = ((2**(16-4)) * result/result.max())

    return result.astype('int16')


def pitchshift(snd_array, n, window_size=2**13, h=2**11):
    """ Changes the pitch of a sound by ``n`` semitones. """
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)

# File Parser Code
def ParsePianoSequenceFile(filepath):
    MainSeq = []
    SubSeqs = {}

    beepfile = open(filepath, 'r')
    CurSubSeqName = None
    for line in beepfile.readlines():
        line = line.strip()
        if line.startswith('//'):
            continue
        elif '{' in line:
            CurSubSeqName = line[:(line.index('{'))].strip()
            SubSeqs[CurSubSeqName] = []
        elif '}' in line:
            CurSubSeqName = None
        elif '.' in line:
            if CurSubSeqName == None:
                MainSeq.append(['S', line[(line.index('.')+1):].strip(), ''])
            else:
                SubSeqs[CurSubSeqName].append(['S', line[(line.index('.')+1):].strip(), ''])
        elif '-' in line:
            if CurSubSeqName == None:
                MainSeq.append(['D', line[(line.index('-')+1):].strip(), ''])
            else:
                SubSeqs[CurSubSeqName].append(['D', line[(line.index('-')+1):].strip(), ''])
        else:
            splitline = line.split(' ')
            freq = splitline[0].strip()
            dur = splitline[1].strip()
            asynccheck = str(False)
            if len(splitline) > 2:
                asynccheck = str(splitline[2].strip() == 'a')
            if CurSubSeqName == None:
                MainSeq.append(['M', freq, dur, asynccheck])
            else:
                SubSeqs[CurSubSeqName].append(['M', freq, dur, asynccheck])
    return MainSeq, SubSeqs

def GetFullMainSeq(MainSeq, SubSeqs):
    SubSeqsFull = {}
    FullMainSeq = []

    for s in MainSeq:
        if s[0] == 'M':
            FullMainSeq.append([s[1], s[2], s[3]])
        elif s[0] == 'S':
            if s[1] not in SubSeqsFull.keys():
                SubSeqsFull[s[1]] = []
                SubSeqsFull[s[1]] = GetFullMainSeq(SubSeqs[s[1]], SubSeqs)
            FullMainSeq.extend(SubSeqsFull[s[1]])
        elif s[0] == 'D':
            FullMainSeq.append([s[1], s[2], s[3]])
    return FullMainSeq

def PlayPianoSequence(Seq, KeySoundDict, fade_ms=50):
    print("Started Audio Sequence")
    for s in Seq:
        if s[1] != '':
            print("Playing key", s[0], " for", s[1], "ms async:", s[2])
            if s[2] == 'False':
                KeySoundDict[s[0]].play(fade_ms=fade_ms)
                time.sleep(float(s[1])/1000)
            else:
                KeySoundDict[s[0]].play(fade_ms=fade_ms)
        else:
            print("Delaying for", float(s[0]), "ms")
            time.sleep(float(s[0])/1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
    print("Ended Audio Sequence")

def LoopPianoSequence(Seq, KeySoundDict):
    while True:
        PlayPianoSequence(Seq, KeySoundDict)

def CreatePianoSounds(RefSound_file_path, KeyConfig_file_path, TransposedSounds_file_path='', SaveSounds=False):
    # Get Reference Audio File
    fps, sound = wavfile.read(RefSound_file_path)

    # Create Key Sounds from reference file
    tones = range(-25, 25)
    print('Started Creating Key Sounds')
    transposed_sounds = []
    for tone in tqdm(tones):
        transposed_sounds.append(pitchshift(sound, tone))
    print('Finished Creating Key Sounds')

    # Save Sounds
    if SaveSounds:
        pickle.dump(transposed_sounds, open(TransposedSounds_file_path, 'wb'))

    # Init Pygame
    pygame.mixer.init(fps, -16, 1, 2048)
    screen = pygame.display.set_mode((150, 150))

    # Init Key Configs
    keys = open(KeyConfig_file_path, 'r+').read().split('\n')
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)
    keysound_dict = dict(zip(keys, sounds))
    return keysound_dict

def LoadKeySounds(TransposedSounds_file_path, KeyConfig_file_path):
    # Init Key Configs
    keys = open(KeyConfig_file_path, 'r+').read().split('\n')
    sounds = map(pygame.sndarray.make_sound, pickle.load(open(TransposedSounds_file_path, 'rb')))
    return keys, sounds

# Driver Code
# Paths
mainpath = 'E:\Github Codes and Projects\Projects\MediaTor-Project\PianoAudioGenerator'
TransposedSounds_file_path = os.path.join(mainpath, 'GeneratedSounds.p')
RefSound_file_path = os.path.join(mainpath, 'bowl.wav')
KeyConfig_file_path = os.path.join(mainpath, 'KeyConfig.kc')

# Controls
GenSounds = False
SaveSounds = True

# Create / Load Piano Sounds
# If Available load precreated sounds
KeySoundDict = None
if not GenSounds and os.path.exists(TransposedSounds_file_path):
    # Load Generated Sounds
    keys, sounds = LoadKeySounds(TransposedSounds_file_path, KeyConfig_file_path)
    # Get Reference Audio File
    fps, sound = wavfile.read(RefSound_file_path)
    # Init Pygame
    pygame.mixer.init(fps, -16, 1, 2048)
    screen = pygame.display.set_mode((150, 150))
    KeySoundDict = dict(zip(keys, sounds))
else:
    # Generate Sounds
    KeySoundDict = CreatePianoSounds(RefSound_file_path, KeyConfig_file_path, TransposedSounds_file_path=TransposedSounds_file_path, SaveSounds=SaveSounds)

        

# Get Piano Sequence
seqPath = os.path.join(mainpath, 'DeathNote.piseq')
MainSeq, SubSeqs = ParsePianoSequenceFile(seqPath)
print(MainSeq)
print(SubSeqs)
Seq = GetFullMainSeq(MainSeq, SubSeqs)
print("Audio Seq:")
print(Seq)



# Play Piano Sequence
LoopPianoSequence(Seq, KeySoundDict)
