import random
from typing import Dict, List
from typing_extensions import Self
import Model.Enums as Enums
import Model.Weights as Weights


def get_target(w: Dict[any, int]):
    total = sum(list(w.values()))
    rand = random.randint(1, total)
    s = 0
    for k in w:
        s += w[k]
        if s >= rand:
            return k


class ChordNote:
    '''
    和弦音符
    `notes_pitch: List[int]`，和弦用到的音高。
    '''
    notes_pitch: List[int] = []

    def create(self, w: Weights.Chord, pitch: int) -> Self:
        try:
            # 第一個和後面的音符
            self.notes_pitch.append(self._add_note(pitch, w.distance))
            for _ in range(get_target(w.count) - 1):
                self.notes_pitch.append(self._add_note(pitch, w.swing))
        except AssertionError:
            pass
        return self

    def _add_note(self, pitch: int, ww: Dict[int, int]):
        pitch -= get_target(ww)
        assert pitch >= 0
        self.notes_pitch.append(pitch)
        return pitch


class Note:
    '''
    音符
    `pitch: int`，音高，`-1` 為休止符。
    `value: Value`，音時。
    `chord: ChordNote`，和弦音符。
    '''
    pitch: int = None
    value: Enums.Value = None
    chord: ChordNote = None

    def create(self, w: Weights.Sentence, is_chord: bool) -> Self:
        '''創建音符'''
        self.pitch = get_target(
            w.noteWeight.pitch).value + Enums.Pitch.Base.value
        self.value = get_target(w.noteWeight.value)
        if is_chord:
            self.chord = ChordNote().create(w.chordWeight, self.pitch)
        return self

    def create_by_pre(self, w: Weights.Sentence, is_chord: bool, pre_note: Self) -> Self:
        '''依照上個音符，創建新音符。'''
        # 新的音高權重
        pitch_weight = {}
        pre_pitch = pre_note.pitch
        for k, v in w.noteWeight.swing.items():
            # 正負都做
            for kk in [k, -k]:
                p = pre_pitch + kk
                pitch_weight[p] = v + \
                    w.noteWeight.pitch[Enums.Pitch[Enums.Pitch(p % 12).name]]

        self.pitch = get_target(pitch_weight)
        self.value = get_target(w.noteWeight.value)
        if is_chord:
            self.chord = ChordNote().create(w.chordWeight, self.pitch)
        return self

    def create_rest(self, w: Dict[Enums.Value, int]) -> Self:
        '''創建休止符'''
        self.pitch = -1
        self.value = get_target(w)
        return self


class Sentence:
    '''
    句子
    `notes: List[Note]`，句子包含的音符。
    '''
    notes: List[Note] = []

    def create(self, w: Weights.Sentence) -> Self:
        noteCount = get_target(w.noteCount)
        # 第一個音符
        self.notes.append(Note().create(w, random.choice([True, False])))
        noteCount -= 1
        # 其他音符
        chord_interval = get_target(w.chordWeight.interval)
        for _ in range(noteCount):
            # 和弦間距
            is_chord = False
            chord_interval -= 1
            if chord_interval == 0:
                chord_interval = get_target(w.chordWeight.interval)
                is_chord = True

            self.notes.append(Note().create_by_pre(
                w, is_chord, self.notes[-1]))
        # 加休止符
        self.notes.append(Note().create_rest(w.noteWeight.value))
        return self


class Paragraph:
    '''
    段落
    `sentences: List[Sentence]`，段落包含的句子。
    '''
    sentences: List[Sentence] = []

    def create(self, w: Weights.Paragraph) -> Self:
        sentence_count = get_target(w.sentenceCount)
        for _ in range(sentence_count):
            self.sentences.append(Sentence().create(w.sentenceWeight))
        return self


# TODO 要不塞到 Paragraph ？
class Transposition:
    '''
    移調
    `swing: int`，移調音高。
    `_referParagraph: Paragraph`，參考段落。
    `paragraph: Paragraph`，實際的段落，如果 swing == 0，paragraph == referParagraph。
    '''
    swing: int
    _referParagraph: Paragraph
    paragraph: Paragraph

    def __init__(self, referParagraph: Paragraph) -> None:
        self._referParagraph = referParagraph

    def get_refer_paragraph(self):
        return self._referParagraph
