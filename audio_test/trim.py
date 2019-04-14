# test code for trimming stuff

from pydub import AudioSegment


def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    print(sound[trim_ms:trim_ms+chunk_size].dBFS)
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size
        print(sound[trim_ms:trim_ms+chunk_size].dBFS)

    return trim_ms

def print_db_values(sound, silence_threshold=-50.0, chunk_size=10):
    '''
    sound is a pydub.AudioSegment
    silence_threshold in dB
    chunk_size in ms

    iterate over chunks until you find the first one with sound
    '''
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while trim_ms < len(sound):
        trim_ms += chunk_size
        print(sound[trim_ms:trim_ms+chunk_size].dBFS)

sound = AudioSegment.from_file("test1.wav", format="wav")

print_db_values(sound)

print("leading")
start_trim = detect_leading_silence(sound)
print("reverse")
end_trim = detect_leading_silence(sound.reverse())

duration = len(sound)    
trimmed_sound = sound[start_trim:duration-end_trim]