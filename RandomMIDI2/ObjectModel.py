import random


class Weights():
    def __init__(self, data: dict):
        self.keyList = list(data.keys())
        self.valueList = list(data.values())

    def getRandKey(self):
        """ 獲得一個隨機值 """
        return random.choices(population=self.keyList, weights=self.valueList)[0]


class Note():
    track: int
    channel: int
    pitch: int
    duration: float
    volume: int
    scale: int
    scaleRaise: int


class Sentence():
    startWordCount: int
    endWordCount: int
    wordCount: int
    pos: int
    repeatFrom: int
    notes: list

    def __init__(self, repeatFrom=None, wordWeights: Weights = None, endWeights: Weights = None):
        isInit = False
        # 指定重複句子
        if repeatFrom is not None:
            self.notes = repeatFrom.notes
            self.repeatFrom = repeatFrom.pos
        # 新語句生成字數規則
        elif wordWeights is not None and endWeights is not None:
            while self.wordCount < self.endWordCount or not isInit:
                isInit = True
                self.wordCount = int(wordWeights.getRandKey())
                self.endCount = int(endWeights.getRandKey())
            self.startWordCount = self.wordCount - self.endWordCount
        else:
            print("ERROR Sentence.__init__")


class LimitData():
    speed: dict
    scale: dict
    sentenceCount: dict
    program: dict
    title = ["speed", "scale", "sentenceCount", "program"]


class WeightsData():
    scale: dict
    tempo: dict
    scaleFluctuation: dict
    wordCount: dict
    endTempo: dict
    endWordCount: dict
    repeatCount: dict
    repeatChange: dict
    strength: dict
    title = ["scale", "tempo", "scaleFluctuation", "wordCount", "endTempo",
             "endWordCount", "repeatCount", "repeatChange", "strength"]
