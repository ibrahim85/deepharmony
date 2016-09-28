# Preprocessing of midi files + file loading
import pickle
from tqdm import tqdm

from util import *

'''
# Example use:
preprocessAllData()

soprano_data = loadData('Soprano')
alto_data = loadData('Alto')
tenor_data = loadData('Tenor')
bass_data = loadData('Bass')

min_song_length = findMinLength(soprano_data)

'''

# Loads the pickle file of the voice_string (e.g. Alto)
def loadData(voice_string):
    filename = 'data/preprocessed/{:}-voices.p'.format(voice_string)
    try:
        file = open(filename, 'rb')
    except FileNotFoundError:
        print("File {:} doesn't exist... loading empty dataset for {:} part".format(filename, voice_string))
        return []
    else:
        return pickle.load(file)

# Finds the shortest song, given voice data (e.g. output from loadData)
def findMinLength(voice_data):
    min_length = 1000000
    for voice in voice_data:
        min_length = min(len(voice), min_length)
    return min_length

# Can safely be called when we've got pregenerated data.
def preprocessAllData(batch_size = 10, total_songs = 5000):
    # batch_size = Number of songs to process before saving
    
    
    # Preprocesses a single batch of songs
    # Returns a tuple that can be fed into preprocessData's initial_data argument
    def preprocessData(start_song, number_of_songs, initial_data=([],[],[],[])):
        data = initial_data # Data is in the form of data[part#][song#][quarter_note#] = pitch
        # Soprano data is in data[0] etc...
        part_names = ['Soprano', 'Alto', 'Tenor', 'Bass']

        print('Preprocessing songs starting with {:}'.format(start_song))
        for song_number in tqdm(range(start_song,number_of_songs+start_song)):
            filename = 'data/bach-chorales/bach-{:}.mid'.format(song_number)
            song = m21.converter.parse(filename)
            voices = separateVoices(song)
            for part in range(4): # For each part:
                data[part].append(makePitchArray(voices[part]))
        
        filename = 'data/preprocessed/{:}-voices.p'
        for part in range(4):
            with open(filename.format(part_names[part]), 'wb') as file:
                pickle.dump(data[part], file)
        return (soprano_data, alto_data, tenor_data, bass_data)

    
    print('Loading in previous data')
    soprano_data = loadData('Soprano')
    alto_data = loadData('Alto')
    tenor_data = loadData('Tenor')
    bass_data = loadData('Bass')
    start_number = 1+min(len(soprano_data), len(alto_data), len(tenor_data), len(bass_data))
    data = (soprano_data[:start_number],
            alto_data[:start_number],
            tenor_data[:start_number],
            bass_data[:start_number])
    
    while start_number <= total_songs:
        min(batch_size, total_songs-start_number)
        data = preprocessData(start_number, min(batch_size, total_songs-start_number), initial_data=data)
        start_number = 1+len(data[0])

