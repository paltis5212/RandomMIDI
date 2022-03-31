from typing import Dict
import Model.Enums as Enums


class Chord:
    '''
    和弦權重
    `distance: Dict[int, int]`，和弦主音距離主旋律多遠。
    `swing: Dict[int, int]`，和弦擴散距離和弦主音多遠。
    `count: Dict[int, int]`，和弦音符數。
    `interval: Dict[int, int]`，和弦間隔多久生成。
    '''
    distance: Dict[int, int]
    swing: Dict[int, int]
    count: Dict[int, int]
    interval: Dict[int, int]

    def __init__(self, distance: Dict[int, int], swing: Dict[int, int], count: Dict[int, int], interval: Dict[int, int]) -> None:
        self.distance = distance
        self.swing = swing
        self.count = count
        self.interval = interval


class Note:
    '''
    音符權重
    `swing: Dict[int, int]`，與前音符的音高差距。
    `pitch: Dict[Pitch, int]`，音高。
    `value: Dict[Value, int]`，音時。
    '''
    swing: Dict[int, int]
    pitch: Dict[Enums.Pitch, int]
    value: Dict[Enums.Value, int]

    def __init__(self, swing: Dict[int, int], pitch: Dict[Enums.Pitch, int], value: Dict[Enums.Value, int]) -> None:
        self.swing = swing
        self.pitch = pitch
        self.value = value


class Sentence:
    '''
    句子權重
    `noteCount: Dict[int, int]`，句子音符數量。
    `changeProportion: Dict[float, int]`，當句子 repeat 的時候，要改變多少比例的音符。
    `noteWeight: NoteWeight`，使用哪種音符權重。
    `chordWeight: ChordWeight`，使用哪種和弦權重。
    '''
    noteCount: Dict[int, int]
    changeProportion: Dict[float, int]
    noteWeight: Note
    chordWeight: Chord

    def __init__(self, noteCount: Dict[int, int], changeProportion: Dict[float, int],  noteWeight: Note, chordWeight: Chord) -> None:
        self.noteCount = noteCount
        self.changeProportion = changeProportion
        self.noteWeight = noteWeight
        self.chordWeight = chordWeight


class Paragraph:
    '''
    段落權重
    `allSwing: Dict[bool, int]`，是否整段變調。主旋律變調，和弦重生成。
    `sentenceCount: Dict[int, int]`，句子數量。
    `sentenceWeight: SentenceWeight`，使用哪種句子權重。
    '''
    allSwing: Dict[bool, int]
    sentenceCount: Dict[int, int]
    sentenceWeight: Sentence

    def __init__(self, allSwing: Dict[bool, int], sentenceCount: Dict[int, int], sentenceWeight: Sentence) -> None:
        self.allSwing = allSwing
        self.sentenceCount = sentenceCount
        self.sentenceWeight = sentenceWeight




