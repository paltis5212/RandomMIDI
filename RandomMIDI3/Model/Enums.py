from enum import Enum


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
