#! -*- coding:utf-8 -*-
from DetailProcess import WeightsObject, ComputeUtils, ExcelMgr, MidiMgr
import random


class Main():
    def __init__(self):
        # 整首歌
        self.music = {}
        # 讀取 excel 內容
        self.allTable = ExcelMgr().getAllTable("rules.xlsx")
        # 需要轉換的資料
        self.maxScale = ComputeUtils().noteStrToNum(
            self.allTable["limit"]["scale"]["max"])
        self.minScale = ComputeUtils().noteStrToNum(
            self.allTable["limit"]["scale"]["min"])
        # 權重變成 WeightsObject
        self.allWeights = {}
        for weights in self.allTable["weights"]:
            self.allWeights[weights] = WeightsObject(
                self.allTable["weights"][weights])
        self.passSentences = 0
        # 句數
        for sentencesNum in range(int(self.allTable["limit"]["number_of_sentences"]["value"])):
            if self.isCopyRepeat(sentencesNum):
                continue
            # 分句存
            self.music[sentencesNum] = []
            # 決定一句的字數、字尾數(字尾數不能超過字數)
            wordCount: int = int(self.allWeights["word_count"].getRandKey())
            endWordCount: int = int(
                self.allWeights["end_word_count"].getRandKey())
            while(int(endWordCount) > int(wordCount)):
                endWordCount = int(
                    self.allWeights["end_word_count"].getRandKey())
            # 生成分為句前、句尾的音符
            for nowWordNum in range(wordCount):
                if nowWordNum <= wordCount - endWordCount:
                    self.getNewNote(sentencesNum, "tempo")
                else:
                    self.getNewNote(sentencesNum, "end_tempo")
            # 每句結尾加休止符
            self.music[sentencesNum].append("0")
            print("\r", sentencesNum + 1, "/",
                  self.allTable["limit"]["number_of_sentences"]["value"], end="")
        # 存成 midi
        MidiMgr(self.music, self.allTable["limit"]["speed"]
                ["bpm"],  self.allTable["limit"]["program"]["value"])

    # 是不是在音階限制內
    def isInLimit(self, noteNum: int):
        return self.minScale <= noteNum <= self.maxScale

    # 生成第一個音符
    # tempoType: str = 使用的節奏
    def firstNote(self, tempoType: str):
        # down =
        noteStr = self.allWeights["scale"].getRandKey() + self.getAPitch()
        note = ComputeUtils().noteStrToNum(noteStr)
        while(not self.isInLimit(note)):
            noteStr = self.allWeights["scale"].getRandKey() + self.getAPitch()
            note = ComputeUtils().noteStrToNum(noteStr)
        tempo = self.allWeights[tempoType].getRandKey()
        return noteStr + tempo

    # 根據限制給一個隨機音高
    def getAPitch(self):
        # 需要的數值
        maxStr: str = self.allTable["limit"]["scale"]["max"]
        minStr: str = self.allTable["limit"]["scale"]["min"]
        down = maxStr.count(",") + minStr.count(",")
        up = maxStr.count("'") + minStr.count("'")
        # 取得參賽資格
        upOrDown = []
        if down > 0:
            upOrDown.append(0)
        if up > 0:
            upOrDown.append(1)
        # 參賽
        if len(upOrDown) > 0:
            upOrDown = random.choice(upOrDown)
            if upOrDown == 0:
                return "," * random.randint(0, down)
            elif upOrDown == 1:
                return "'" * random.randint(0, up)
        # 都不能參賽
        else:
            return ""

    # 配出音階新配方，利用過去音符、音階波動權重、音階權重
    def CompareScale(self, passNoteStr):
        passScale = ComputeUtils().getScaleAndTempo(passNoteStr)["scale"]
        # 取得合理波動換算後的音符
        scaleFluctuation: list = self.allWeights["scale_fluctuation"].getRandListKey(
        )
        scaleFluctuationNote: list = []
        for index in range(len(scaleFluctuation)):
            value = scaleFluctuation[index]
            value = int(value) * random.choice([-1, 1])
            # 不在範圍內的音符重做
            while not self.isInLimit(ComputeUtils().noteStrToNum(ComputeUtils().stepToScale(passScale, int(value)))):
                value = self.allWeights["scale_fluctuation"].getRandKey()
                value = int(value) * random.choice([-1, 1])
            scaleFluctuationNote.append(
                ComputeUtils().stepToScale(passScale, int(value)))
        # 音階權重取得值
        scaleWeights = self.allWeights["scale"].getRandListKey()
        # 兩相比較
        result = ComputeUtils().weightsCompare(
            [noteStr[: 1] for noteStr in scaleFluctuationNote], scaleWeights)
        # 真正結果
        for noteStr in scaleFluctuationNote:
            if noteStr[: 1] == result:
                return noteStr

    def getNewNote(self, sentencesNum: int, tempoType: str):
        # 全曲第一個音
        if len(self.music[0]) == 0:
            self.music[sentencesNum].append(self.firstNote(tempoType))
        else:
            note = ""
            # 最後一個非休止符，則用來取得新 note
            if len(self.music[sentencesNum]) > 0:
                note = self.CompareScale(self.music[sentencesNum][-1])
            elif sentencesNum not in self.music or len(self.music[sentencesNum]) == 0:
                note = self.CompareScale(self.music[sentencesNum - 1][-2])
            note += self.allWeights[tempoType].getRandKey()
            self.music[sentencesNum].append(note)

    def isCopyRepeat(self, sentencesNum: int):
        """ 是否複製前面句子 """
        # 未到複製句子解禁時
        if self.passSentences > 0:
            self.passSentences -= 1
            return False
        # 複製了
        repeatNum = int(self.allWeights["repeat"].getRandKey())
        if repeatNum > len(self.music):
            repeatNum = len(self.music)
        for index in range(repeatNum):
            self.music[sentencesNum +
                       index] = self.music[sentencesNum + index - repeatNum].copy()
            self.music[sentencesNum +
                       index] = self.changeSomeInSentences(self.music[sentencesNum + index])
        self.passSentences = repeatNum
        return repeatNum > 0

    def changeSomeInSentences(self, sentences: list):
        """ 對於完全直接複製的句子，抽出幾個音改掉 """
        changeIndex = []
        # 選一些要替換的音符
        for i in range(int(self.allWeights["repeat_change"].getRandKey())):
            changeIndex.append(random.randint(0, len(sentences)))
        # 音符替換掉
        for index in range(len(sentences)):
            if index in changeIndex:
                sentences[index] = self.firstNote(
                    random.choice(["tempo",  "end_tempo"]))
        return sentences


a = Main()
print("\n", a.music)
