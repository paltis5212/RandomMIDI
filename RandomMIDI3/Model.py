from enum import Enum
from mimetypes import init
from typing import Dict, List


class Pitch(Enum):
    C = 0
    SharpC = 1
    D = 2
    SharpD = 3
    E = 4
    F = 5
    SharpF = 6
    G = 7
    SharpG = 8
    A = 9
    SharpA = 10
    B = 11
    Rest = -1
    Step = 12
    Base = 60


class Value(Enum):
    ThirtySecond = 0.125
    DottedThirtySecond = 0.1875
    Sixteenth = 0.25
    DottedSixteenth = 0.375
    Eighth = 0.5
    DottedEighth = 0.75
    Quarter = 1
    DottedQuarter = 1.5
    Half = 2
    DottedHalf = 3
    Whole = 4
    DottedWhole = 6
    DoubleWhole = 8


class ParagraphName(Enum):
    # 可自行隨意添加
    Intro = "Intro"  # 前奏
    Verse = "Verse"  # 主歌
    PreChorus = "PreChorus"  # 導歌：主、副歌的連接段落
    Chorus = "Chorus"  # 副歌
    Bridge = "Bridge"  # 橋樑：重複主、副歌之間插入的過渡段落，曲風常有別於原曲
    Outro = "Outro"  # 尾奏、歌曲結尾


class ChordWeight:
    '''
    和弦權重
    `mainSwing: Dict[int, int]`，和弦主音距離主旋律多遠。
    `swing: Dict[int, int]`，和弦擴散距離和弦主音多遠。
    `count: Dict[int, int]`，和弦音符數。
    `interval: Dict[int, int]`，和弦間隔多久生成。
    '''
    mainSwing: Dict[int, int]
    swing: Dict[int, int]
    count: Dict[int, int]
    interval: Dict[int, int]

    def __init__(self, mainSwing: Dict[int, int], swing: Dict[int, int], count: Dict[int, int], interval: Dict[int, int]) -> None:
        self.mainSwing = mainSwing
        self.swing = swing
        self.count = count
        self.interval = interval


class NoteWeight:
    '''
    音符權重
    `swing: Dict[int, int]`，與前音符的音高差距。
    `pitch: Dict[Pitch, int]`，音高。
    `value: Dict[Value, int]`，音時。
    '''
    swing: Dict[int, int]
    pitch: Dict[Pitch, int]
    value: Dict[Value, int]

    def __init__(self, swing: Dict[int, int], pitch: Dict[Pitch, int], value: Dict[Value, int]) -> None:
        self.swing = swing
        self.pitch = pitch
        self.value = value


class SentenceWeight:
    '''
    句子權重
    `noteCount: Dict[int, int]`，句子音符數量。
    `changeProportion: Dict[float, int]`，當句子 repeat 的時候，要改變多少比例的音符。
    `noteWeight: NoteWeight`，使用哪種音符權重。
    `chordWeight: ChordWeight`，使用哪種和弦權重。
    '''
    noteCount: Dict[int, int]
    changeProportion: Dict[float, int]
    noteWeight: NoteWeight
    chordWeight: ChordWeight

    def __init__(self, noteCount: Dict[int, int], changeProportion: Dict[float, int],  noteWeight: NoteWeight, chordWeight: ChordWeight) -> None:
        self.noteCount = noteCount
        self.changeProportion = changeProportion
        self.noteWeight = noteWeight
        self.chordWeight = chordWeight


class ParagraphWeight:
    '''
    段落權重
    `allSwing: Dict[bool, int]`，是否整段變調。主旋律變調，和弦重生成。
    `sentenceCount: Dict[int, int]`，句子數量。
    `sentenceRepeatCount: Dict[int, int]`，句子重複幾句。
    `sentenceWeight: SentenceWeight`，使用哪種句子權重。
    '''
    allSwing: Dict[bool, int]
    sentenceCount: Dict[int, int]
    sentenceRepeatCount: Dict[int, int]
    sentenceWeight: SentenceWeight

    def __init__(self, allSwing: Dict[bool, int], sentenceCount: Dict[int, int], sentenceRepeatCount: Dict[int, int], sentenceWeight: SentenceWeight) -> None:
        self.allSwing = allSwing
        self.sentenceCount = sentenceCount
        self.sentenceRepeatCount = sentenceRepeatCount
        self.sentenceWeight = sentenceWeight


class ChordNote:
    '''
    和弦音符
    `notes_pitch: List[int]`，和弦用到的音高。
    '''
    notes_pitch: List[int] = []


class Note:
    '''
    音符
    `pitch: int`，音高，`-1` 為休止符。
    `value: Value`，音時。
    `chord: ChordNote`，和弦音符。
    '''
    pitch: int
    value: Value
    chord: ChordNote


class Sentence:
    '''
    句子
    `notes: List[Note]`，句子包含的音符。
    '''
    notes: List[Note] = []


class Paragraph:
    '''
    段落
    `sentences: List[Sentence]`，段落包含的句子。
    '''
    sentences: List[Sentence] = []


class Transposition:
    '''
    移調
    `swing: int`，移調音高。
    `referParagraph: Paragraph`，參考段落。
    `paragraph: Paragraph`，實際的段落，如果 swing == 0，paragraph == referParagraph。
    '''
    swing: int
    referParagraph: Paragraph
    paragraph: Paragraph

refer_paragraph_weight: Dict[ParagraphName, ParagraphWeight] = {}
refer_paragraph_weight[ParagraphName.Chorus] = ParagraphWeight(
    allSwing={
        True: 1,
        False: 1
    },
    sentenceCount={
        4: 2,
        6: 1,
        8: 1,
    },
    sentenceRepeatCount={
        0: 4,
        1: 1,
        2: 1,
        4: 1,
        6: 1,
    },
    sentenceWeight=SentenceWeight(
        noteCount={
            5: 1,
            6: 1,
            7: 1,
            8: 1,
        },
        changeProportion={
            0: 1,
            0.3: 2,
            0.5: 1
        },
        noteWeight=NoteWeight(
            swing={
                0: 1,
                1: 1,
                2: 1,
                3: 2,
                4: 3,
                5: 2,
                6: 2,
                7: 2
            },
            pitch={
                Pitch.C: 2,
                Pitch.SharpC: 1,
                Pitch.D: 2,
                Pitch.SharpD: 1,
                Pitch.E: 2,
                Pitch.F: 2,
                Pitch.SharpF: 1,
                Pitch.G: 2,
                Pitch.SharpG: 1,
                Pitch.A: 2,
                Pitch.SharpA: 1,
                Pitch.B: 2,
            },
            value={
                Value.ThirtySecond: 1,
                Value.DottedThirtySecond: 1,
                Value.Sixteenth: 2,
                Value.DottedSixteenth: 1,
                Value.Eighth: 3,
                Value.DottedEighth: 1,
                Value.Quarter: 5,
                Value.DottedQuarter: 1,
                Value.Half: 2,
                Value.DottedHalf: 1,
                Value.Whole: 1,
                Value.DottedWhole: 1,
                Value.DoubleWhole: 1,
            }
        ),
        chordWeight=ChordWeight(
            mainSwing={
                0: 1,
                1: 1,
                2: 1,
                3: 2,
                4: 2,
                5: 3,
                6: 3,
                7: 3,
                8: 3,
                9: 3,
            },
            swing={
                1: 3,
                2: 3,
                3: 3,
                4: 1,
                5: 1
            },
            count={
                1: 3,
                2: 1,
                3: 3,
                4: 1,
                5: 1
            },
            interval={
                0: 1,
                1: 1,
                2: 1,
                3: 2,
                4: 3,
                5: 1,
                6: 1,
                7: 1,
            }
        )
    )
)