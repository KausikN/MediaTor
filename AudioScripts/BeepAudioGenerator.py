'''
Summary
This script is used for generating audio of various frequencies and mixing them

Goals
 - Piano Key Mapping
 - Audio File to bs code
 - Real time playing to bs code
'''
import winsound
import time

def GenerateFreq(freq, duration): 
    winsound.Beep(freq, duration)

def PlaySound(sound):
    winsound.PlaySound(sound)
    
# File Parser Code
def ParseBeepSequenceFile(filepath):
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
            freq = line.split(' ')[0].strip()
            dur = line.split(' ')[1].strip()
            if CurSubSeqName == None:
                MainSeq.append(['M', freq, dur])
            else:
                SubSeqs[CurSubSeqName].append(['M', freq, dur])
    return MainSeq, SubSeqs

def GetFullMainSeq(MainSeq, SubSeqs):
    SubSeqsFull = {}
    FullMainSeq = []

    for s in MainSeq:
        if s[0] == 'M':
            FullMainSeq.append([s[1], s[2]])
        elif s[0] == 'S':
            if s[1] not in SubSeqsFull.keys():
                SubSeqsFull[s[1]] = []
                SubSeqsFull[s[1]] = GetFullMainSeq(SubSeqs[s[1]], SubSeqs)
            FullMainSeq.extend(SubSeqsFull[s[1]])
        elif s[0] == 'D':
            FullMainSeq.append([s[1], s[2]])
    return FullMainSeq

def PlayBeepSequence(Seq):
    print("Started Audio Sequence")
    for s in Seq:
        if s[1] != '':
            print("Playing", s[0], "Hz for", s[1], "ms")
            winsound.Beep(int(s[0]), int(s[1]))
            #GenerateFreq(int(s[0]), int(s[1]))
        else:
            print("Delaying for", float(s[0]), "ms")
            time.sleep(float(s[0])/1000)
    print("Ended Audio Sequence")

def LoopBeepSequence(Seq):
    while True:
        PlayBeepSequence(Seq)

def PianoKeyFreqMap():
    KeysFreq = {}
    Keys = ['C6', 'C6#', 'D6', 'D6#', 'E6', 'F6', 'F6#', 'G6', 'G6#', 'A6', 'A6#', 'B6', 
    'C7', 'C7#', 'D7', 'D7#', 'E7', 'F7', 'F7#', 'G7', 'G7#', 'A7', 'A7#', 'B7', 'C8']
    KeyNos = range(64, 88 + 1, 1)
    for key, keyno in zip(Keys, KeyNos):
        KeysFreq[key] = [GetKeyFreq(keyno)]
    return Keys, KeysFreq
    
def GetKeyFreq(KeyNo):
    return 2 ** ((KeyNo - 49) / 12) * 440

def PlayPianoSounds():
    duration = 1000
    Keys, KeyFreqs = PianoKeyFreqMap()
    for key in Keys:
        for freq in KeyFreqs[key]:
            print(key, freq)
            if freq >= 37 and freq <= 32767:
                GenerateFreq(int(round(freq)), duration)



# Driver Code
# filepath = 'AudioScripts/DeathNote.bs'
# MainSeq, SubSeqs = ParseBeepSequenceFile(filepath)
# print(MainSeq)
# print(SubSeqs)
# Seq = GetFullMainSeq(MainSeq, SubSeqs)
# print("Audio Seq:")
# print(Seq)
# LoopBeepSequence(Seq)
