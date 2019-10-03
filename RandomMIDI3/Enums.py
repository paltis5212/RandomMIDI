from enum import Enum


class ScalePitch(Enum):
    C = 60
    D = 62
    E = 64
    F = 65
    G = 67
    A = 69
    B = 71
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
