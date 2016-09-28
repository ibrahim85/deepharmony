# Preprocessing of midi files + file loading

import music21 as m21
from util import *
import pickle


'''
MIDI -> (~time consuming)
m21.score.Score -> (very time consuming)
voices, length
->
data (soprano_pitches), labels (bass_tuples)
Somehow get min_length
'''

# Loads a song and saves it as a pickle file
def preprocessSong(song_number):
    filename = 'data/bach-chorales/bach-{:}.mid'.format(song_number)
    song = m21.converter.parse(filename)
    voices = separateVoices(song)
    for voice in voices:
        saveVoice(voice, song_number)

# Saves the pitch array of a voice generated by separateVoices
def saveVoice(voice, song_number):
    voice_file = 'data/preprocessed/song-{:}-voice-{:}.p'.format(song_number, voice.partName)
    with open(voice_file, 'wb') as file:
        pickle.dump(makePitchArray(voice), file)

# Gets the already saved pitch array of a voice for a song
def loadVoice(song_number, voice_string):
    voice_file = 'data/preprocessed/song-{:}-voice-{:}.p'.format(song_number, voice_string)
    with open(voice_file, 'rb') as file:
        pitch_array = pickle.load(file)
        return pitch_array

# Gets the pitch array of all the voices for a given song
def loadVoices(song_number):
    voice_strings = ['Soprano','Alto','Tenor','Bass']
    return [load_voice(song_number, voice_string) for voice_string in voice_strings]

# Probably pretty slow
def calculateMinLength():
    total_songs = 1000 # Should be 5000...
    minimum_length = 100000
    for i in range(1, total_songs+1):
        # Not song.duration.quarterLength
        minimum_length = min(len(loadVoice(n, 'Bass'), minimum_length))
    return minimum_length

# Returns (data, labels)
def loadSongData(song_number, length):
    data = loadVoice(song_number, 'Soprano')[:length]
    labels = [pitchToTuple(pitch) for pitch in loadVoice(song_number, 'Bass')[:length]]
    return (data, labels)
    

#preprocessMidi(1)
#print('preprocessed')
#loadVoices(1)

#preprocessSong(1)
#loadVoice(1, 'Soprano')