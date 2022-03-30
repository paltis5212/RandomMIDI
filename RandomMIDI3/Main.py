import random
from webbrowser import get
from Model import *


do_count = 50


def get_target(w: Dict[any, int]):
    total = sum(list(w.values()))
    rand = random.randint(1, total)
    s = 0
    for k in w:
        s += w[k]
        if s >= rand:
            return k


def get_first_sentence(w: SentenceWeight):
    chordInterval = get_target(w.chordWeight.interval)
    noteCount = get_target(w.noteCount)
    for i in range(noteCount):
        pass


def get_note(w: SentenceWeight, is_chord: bool):
    note = Note(
        pitch=get_target(w.noteWeight.pitch).value + Pitch.Base.value,
        value=get_target(w.noteWeight.value)
    )
    if is_chord:
        note.chord = get_chord(w.chordWeight, note.pitch)


def get_chord(w: ChordWeight, pitch: int):
    main_swing = get_target(w.mainSwing)
    main_pitch = pitch - main_swing
    count = get_target(w.count)
    do_index = 0
    chord = ChordNote()
    chord.notes_pitch = []
    while not swing or swing <= main_swing:
        do_index += 1
        assert do_index <= do_count, "無法計算，ChordWeight 的 count 和 swing 權重可能有衝突！"
        swing = get_target(w.swing)
        note_pitch = swing * get_sign() + main_pitch
        if note_pitch not in chord.notes_pitch:
            count -= 1
            chord.notes_pitch.append(note_pitch)
        if count == 0:
            break

    get_target(w.swing) <= count
    chord = ChordNote()


def get_sign():
    return random.choice([1, -1])


refer_paragraph = {}

for name, w in refer_paragraph_weight.items():
    paragraph = Paragraph()
    sentences = []
    # for i in range(get_target(w.sentenceCount)):
