from random import choice
import os

from starlette.applications import Starlette
from starlette.responses import FileResponse, Response
import uvicorn
from midi2voice.midi2xml import midi2xml

from Voice import renderize_voice, compose

app = Starlette(debug=False)

# Needed to avoid cross-domain issues
response_header = {
    'Access-Control-Allow-Origin': '*',
}

cors_preflight_header = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
}

@app.route('/voice', methods=['GET', 'POST', 'OPTIONS'])
async def voice(request):
    if request.method == 'OPTIONS':
        return Response(headers=cors_preflight_header)

    if request.method == 'GET':
        params = request.query_params
    elif request.method == 'POST':
        params = await request.json()

    lyrics = params.get('lyrics', ['oo '])
    notes = params.get('notes', [0])
    octave = params.get("octave", 6)
    dur = params.get('dur', [1])
    tempo = params.get('tempo', 120)
    lang = params.get('lang', 'es')
    scale = params.get('scale', [0, 2, 4, 5, 7, 9, 11])
    root_note = params.get('root', 0)  # C is the root note
    notes = list(map(lambda x: x + root_note, notes))

    filename = 'output.wav'

    renderize_voice(filename, lyrics, notes, dur, tempo, scale, lang)
    return FileResponse(filename, headers=response_header)


@app.route('/midi', methods=['GET', 'POST', 'OPTIONS'])
async def midi(request):
    if request.method == 'OPTIONS':
        return Response(headers=cors_preflight_header)

    if request.method == 'GET':
        params = request.query_params
    elif request.method == 'POST':
        params = await request.json()

    lyrics = params.get('lyrics', 'oo ')
    notes = params.get('notes', [0])
    octave = params.get("octave", 6)
    dur = params.get('dur', [1])
    tempo = params.get('tempo', 120)
    lang = params.get('lang', 'es')
    scale = params.get('scale', [0, 2, 4, 5, 7, 9, 11])
    root_note = params.get('root', 0)  # C is the root note
    notes = list(map(lambda x: x + root_note, notes))

    filename = 'voice.mid'
    compose(notes, dur, scale, filename)
    return FileResponse(filename, headers=response_header)


@app.route('/sheet', methods=['GET', 'POST', 'OPTIONS'])
async def sheet(request):
    if request.method == 'OPTIONS':
        return Response(headers=cors_preflight_header)

    if request.method == 'GET':
        params = request.query_params
    elif request.method == 'POST':
        params = await request.json()

    lyrics = params.get('lyrics', 'oo ')
    notes = params.get('notes', [0])
    octave = params.get("octave", 6)
    dur = params.get('dur', [1])
    tempo = params.get('tempo', 120)
    lang = params.get('lang', 'es')
    scale = params.get('scale', [0, 2, 4, 5, 7, 9, 11])
    root_note = params.get('root', 0)  # C is the root note
    notes = list(map(lambda x: x + root_note, notes))

    MIDI_PATH = "voice.mid"
    filename = "voice.xml"
    compose(notes, dur, scale, MIDI_PATH)
    midi2xml(lyrics, MIDI_PATH, filename, tempo)

    return FileResponse(filename, headers=response_header)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
