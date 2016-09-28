import music21 as m21

# A0 is 21 and C8 is 108
HOLD_NOTE = 20
SILENCE = 19

"""separateVoices may put the same note in two different voices...
(This is probably not a problem: these Bach chorals don't appear to have rests)

when getElementsByOffset is called in a situation like:
1   2   3   4
XXX XXX
YYY YYY
    ZZZ
WWW WWW

Note W will be added to both the Tenor and the Bass part...
"""

def separateVoices(song):
    timeSig = song.recurse().getElementsByClass('TimeSignature')[0]
    tempo = song.recurse().getElementsByClass('MetronomeMark')[0]

    sepVoices = m21.stream.Score()

    parts = []
    for voice in ['Soprano','Alto','Tenor','Bass']:
        part = m21.stream.Part()
        part.partName = voice
        part.append(timeSig)
        part.append(tempo)
        #part.append(m21.clef.TrebleClef() #just for readability
        parts.append(part)

    sepVoices.append(parts)

    # takes Chord, returns list of component Notes
    def chord2notes(chord):
        return [m21.note.Note(pitch, duration=chord.duration) for pitch in chord.pitches]

    # Replace chords with notes
    def removeChords(stream):
        import copy
        newStream = copy.deepcopy(stream)
        for noteOrChord in newStream.flat.notes:
            if noteOrChord.isChord:
                offset = noteOrChord.offset
                newStream.remove(noteOrChord, recurse=True)   

                for note in chord2notes(noteOrChord):
                    newStream.insert(offset,note)
        return newStream

    #Remove all chords
    chordless = removeChords(song)

    # At each note, identify and separate the voices
    for note in chordless.flat.notes:
#     for note in chordless.flat.getElementsByOffset(0,11, classList=['Note']):
        simulNotes = list(chordless.flat.getElementsByOffset(note.offset, mustBeginInSpan=False, classList=['Note']))
        simulNotes.sort(key=lambda x: x.pitch, reverse=True)
        

        for part, newnote in zip(parts, simulNotes):                
            if newnote.id not in [n.id for n in part.flat.notes] and note==newnote:
                part.insert(newnote.offset,newnote)
                
    return sepVoices


# Converts note or chord to a midi pitch (int)
def pitch(note):
    try:
        #... Should probably change this part
        return note.pitches[0].midi # If it's a chord, get top note
    except AttributeError:
        return note.pitch.midi # if it's not a chord


# music21.Stream -> [int...]
# Converts a 'voice' (with no chords) to series of pitches
def makePitchArray(voice):
    # Divisions are in quarter notes... we may want to change this
    array = []
    current_note = 0
    for time in range(0, int(voice.duration.quarterLength)):
        # Figure out current note
        notes = voice.flat.getElementsByOffset(time, mustBeginInSpan=False, classList=['Note'])
        if len(notes) == 0:
            array.append(SILENCE)
        else:
            note = notes[0]
            if note.offset > time-1:
                # The note started in the past quarternote
                array.append(note.pitch.midi)
            else:
                array.append(HOLD_NOTE)
    return array

# Converts pitch number to a tuple with "one hot encoding"
LOWEST_PITCH=SILENCE
HIGHEST_PITCH=108 # C8
def pitchToTuple(pitch):
    list = [0] * (HIGHEST_PITCH-LOWEST_PITCH)
    list[pitch-LOWEST_PITCH] = 1
    return tuple(list)

def tupleToPitch(tuple):
    index = max(enumerate(tuple), key=lambda x: x[1])[0]
    return LOWEST_PITCH + index

def pitchToStream(pitch_array):
    stream = m21.stream.Stream()
    for pitch in pitch_array:
        if pitch == HOLD_NOTE:
            stream[-1].quarterLength += 1
        elif pitch != SILENCE:
            stream.append(m21.note.Note(pitch))
    return stream

import glob
from tqdm import tqdm
def loadUnprocessedSongs(num_files=None):
    print('Listing files')
    files = glob.glob('data/bach-chorales/*.mid')
    print('Loading files')
    num_files = num_files if num_files else len(files)+1 
    songs = [m21.converter.parse(file) for file in tqdm(files[:num_files])]
    print('Calculating minimum song length')
    min_length = int(min([song.duration.quarterLength for song in tqdm(songs)]))
    print('Separating voices')
    voices_by_song = [separateVoices(song) for song in tqdm(songs)]
    print('Getting soprano part (input data)')
    soprano_pitches = [makePitchArray(voices[0])[:min_length] for voices in voices_by_song]
    print('Getting bass part (output labels)')
    bass_tuples = [ list(map(pitchToTuple, makePitchArray(voices[3])))[:min_length] for voices in voices_by_song]
    
    return (soprano_pitches, bass_tuples, min_length)