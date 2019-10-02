from enum import Enum


class ScalePitch(Enum):
    C = 72
    D = 74
    E = 76
    F = 79
    G = 81
    A = 84
    B = 86
    step = 12
    scaleName = ["C", "D", "E", "F", "G", "A", "B"]


class LimitData(Enum):
    limit = "limit"
    speed = "speed"
    scale = "scale"
    sentenceCount = "sentenceCount"
    program = "program"


class WeightsData(Enum):
    weights = "weights"
    scale = "scale"
    tempo = "tempo"
    scaleFluctuation = "scaleFluctuation"
    wordCount = "wordCount"
    endTempo = "endTempo"
    endWordCount = "endWordCount"
    repeatCount = "repeatCount"
    repeatChange = "repeatChange"
    strength = "strength"
