'''
Summary
Piano App using Python

-> Bowl.wav - reference audio
-> Configuration / Mapping for the piano keys to keyboard
'''

# Imports
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

def GenerateKeySoundDict(sound_file_path, KeyConfig_file_path, TransposedSounds_file_path, SaveSounds=True):
    # Get Reference Audio File
    fps, sound = wavfile.read(sound_file_path)

    # Create Key Sounds from reference file
    tones = range(-25, 25)
    print('Started Creating Key Sounds')
    transposed_sounds = []
    for tone in tqdm(tones):
        transposed_sounds.append(pitchshift(sound, tone))
    print('Finished Creating Key Sounds')

    if SaveSounds:
        pickle.dump(transposed_sounds, open(TransposedSounds_file_path, 'wb'))

    # Init Key Configs
    keys = open(KeyConfig_file_path, 'r+').read().split('\n')
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)
    
    return keys, sounds, fps

def LoadKeySounds(TransposedSounds_file_path, KeyConfig_file_path):
    # Init Key Configs
    keys = open(KeyConfig_file_path, 'r+').read().split('\n')
    sounds = map(pygame.sndarray.make_sound, pickle.load(open(TransposedSounds_file_path, 'rb')))
    return keys, sounds

def main():
    # Paths
    mainpath = 'E:\Github Codes and Projects\Projects\MediaTor-Project\Piano'
    TransposedSounds_file_path = os.path.join(mainpath, 'GeneratedSounds.p')
    sound_file_path = os.path.join(mainpath, 'bowl.wav')
    KeyConfig_file_path = os.path.join(mainpath, 'KeyConfig.kc')

    # Controls
    GenSounds = False
    SaveSounds = True

    # Create / Load Piano Sounds
    # If Available load precreated sounds
    keysound_dict, is_playing, fps = None, None, 24
    if not GenSounds and os.path.exists(TransposedSounds_file_path):
        # Load Generated Sounds
        keys, sounds = LoadKeySounds(TransposedSounds_file_path, KeyConfig_file_path)
        # Get Reference Audio File
        fps, sound = wavfile.read(sound_file_path)
        # Init Pygame
        pygame.mixer.init(fps, -16, 1, 2048)
        screen = pygame.display.set_mode((150, 150))
        # Create KeySoundDict
        keysound_dict = dict(zip(keys, sounds))
    else:
        # Generate KeySounds
        keys, sounds, fps = GenerateKeySoundDict(sound_file_path, KeyConfig_file_path, TransposedSounds_file_path, SaveSounds=SaveSounds)
        # Init Pygame
        pygame.mixer.init(fps, -16, 1, 2048)
        screen = pygame.display.set_mode((150, 150))
        # Create KeySoundDict
        keysound_dict = dict(zip(keys, sounds))
    
    is_playing = {k: False for k in keysound_dict.keys()}

    while True:
        event = pygame.event.wait()

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN:
            if (key in keysound_dict.keys()) and (not is_playing[key]):
                keysound_dict[key].play(fade_ms=50)
                is_playing[key] = True

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise KeyboardInterrupt

        elif event.type == pygame.KEYUP and key in keysound_dict.keys():
            # Stops with 50ms fadeout
            keysound_dict[key].fadeout(500)
            is_playing[key] = False


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('App Closed')
