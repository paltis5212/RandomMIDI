import random
from Enums import WeightsData, ScalePitch, LimitData
from InfoMgr import InfoMgr


class WeightsObject():
    def __init__(self, data: dict):
        self.keyList = list(data.keys())
        self.valueList = list(data.values())
        # str 轉 float
        temp = []
        for value in self.valueList:
            temp.append(float(value))
        self.valueList = temp

    def getRandKey(self):
        """ 獲得一個隨機值 """
        return random.choices(population=self.keyList, weights=self.valueList)[0]


class NoteObject():
    pitch: int
    duration: float
    volume: int
    scale: int
    scaleRaise: int

    def scaleAddFluctuation(self, fluctuation: int):
        """ 音階和起伏得到新音符 -> {"scale": scale, "scaleRaise": scaleRaise, "pitch": pitch}
        :param fluctuation: 起伏
        """
        # 預設值
        scale = self.scale
        scaleRaise = self.scaleRaise

        scale += fluctuation
        # 重複升降音高
        while scale < 1 or scale > 7:
            # 降音高
            if scale < 1:
                scale += 7
                scaleRaise -= 1
            # 升音高
            if scale > 7:
                scale -= 7
                scaleRaise += 1
        return {"scale": scale, "scaleRaise": scaleRaise}


class SentenceObject():
    startWordCount: int
    endWordCount: int
    wordCount: int
    pos: int
    notes: list

    def __init__(self, pos: int):
        self.pos = pos

    def setNew(self):
        self._setWordCount()
        self.notes = []
        noteIndex = 0
        for i in range(self.startWordCount):
            self.notes.append(self._createNote(
                noteIndex, InfoMgr.weights[WeightsData.tempo.value]))
            noteIndex += 1
        for i in range(self.endWordCount):
            self.notes.append(self._createNote(
                noteIndex, InfoMgr.weights[WeightsData.endTempo.value]))
            noteIndex += 1

    def _setWordCount(self):
        """ 設定字數，句尾數超過重取 """
        self.wordCount = int(
            InfoMgr.weights[WeightsData.wordCount.value].getRandKey())
        self.endWordCount = int(
            InfoMgr.weights[WeightsData.endWordCount.value].getRandKey())
        index = 0
        while self.wordCount < self.endWordCount and index < 50:
            self.endWordCount = int(
                InfoMgr.weights[WeightsData.endWordCount.value].getRandKey())
            index += 1
        self.startWordCount = self.wordCount-self.endWordCount

    def _getPassNote(self, index: int):
        """ 獲得上一個音符
        :param index: 本音符在句子的編號
        """
        passNote: NoteObject
        if index - 1 < 0:
            if self.pos - 1 < 0:
                return None
            else:
                passSentence = InfoMgr.music[self.pos - 1]
                passNote = passSentence.notes[passSentence.wordCount - 1]
        else:
            passNote = self.notes[index - 1]
        return passNote

    def _createNote(self, noteIndex: int, tempoWeight: WeightsObject):
        """ 製造一個新 note，音階、節奏、輕重一應俱全
        :param noteIndex: 本句第幾顆 note
        :param tempoWeight: 使用的節奏權重
        """
        newNote = NoteObject()
        passNote = self._getPassNote(noteIndex)
        scaleResult: dict
        if passNote is not None:
            scaleResult = self._twoWeightsToScale(passNote)
        else:
            scaleResult = self._getNewScale()
        newNote.scale = int(scaleResult["scale"])
        newNote.scaleRaise = int(scaleResult["scaleRaise"])
        newNote.pitch = int(scaleResult["pitch"])
        newNote.duration = float(tempoWeight.getRandKey())
        newNote.volume = int(
            InfoMgr.weights[WeightsData.strength.value].getRandKey())
        return newNote

    def _twoWeightsToScale(self, passNote: NoteObject):
        """ 用兩個權重依照 passNote 獲得新音階 -> {"scale": scale, "scaleRaise": scaleRaise, "pitch": pitch}
        :param passNote: 上一個音符
        """
        index = 0
        fluctuationResultList: list = []
        fluctuationKeyDict: dict = {}
        scaleKeyDict: dict = {}
        # 階段一: 取得兩個權重同時出現的結果
        while index < 50:
            fluctuation = int(InfoMgr.weights[WeightsData.scaleFluctuation.value].getRandKey(
            )) * random.choice([1, -1])
            fluctuationResult = passNote.scaleAddFluctuation(fluctuation)
            fluctuationResultScale = fluctuationResult["scale"]
            fluctuationResult["pitch"] = self._scaleAndRaiseToPitch(
                scale=fluctuationResultScale, scaleRaise=fluctuationResult["scaleRaise"])
            # 不在限制內沒有未來
            if not self._isInLimit(fluctuationResult["pitch"]):
                continue
            scaleResult = InfoMgr.weights[WeightsData.scale.value].getRandKey()
            # 取得相同的音，即達成目的
            if str(fluctuationResultScale) == str(scaleResult):
                return fluctuationResult
            # 紀錄 key 出現次數
            if fluctuationResultScale not in fluctuationKeyDict:
                fluctuationKeyDict[fluctuationResultScale] = 0
            fluctuationKeyDict[fluctuationResultScale] += 1
            if scaleResult not in scaleKeyDict:
                scaleKeyDict[scaleResult] = 0
            scaleKeyDict[scaleResult] += 1
            # 紀錄波動結果
            fluctuationResultList.append(fluctuationResult)
            index += 1

        # 階段二: 在多個權重一、二結果中，同樣為第一名出現次數的；否則，權重一出現最多次的
        # 出現最多次的 key
        fluctuationMax = max(list(fluctuationKeyDict.values()))
        scaleMax = max(list(scaleKeyDict.values()))
        # 同樣出現最多次的 key
        fluctuationMaxList = []
        # 目標音階
        targetScale: int = -1
        for key in fluctuationKeyDict:
            # 同樣的 key 出現最多次
            if fluctuationKeyDict[key] == fluctuationMax and scaleKeyDict[key] == scaleMax:
                targetScale = key
            # 記錄身為最多的 key
            elif fluctuationKeyDict[key] == fluctuationMax:
                fluctuationMaxList.append(key)
        # 前面沒有出現才做
        if targetScale == -1:
            targetScale = random.choice(fluctuationMaxList)

        # 階段三: 使用剛剛獲得的 scale，看看哪個 fluctuationResult 最快吻合
        for data in fluctuationResultList:
            if data["scale"] == targetScale:
                return data

    def _isInLimit(self, pitch: int):
        """ pitch 在上下限制範圍之中嗎?
        :param pitch: 檢查的 pitch
        """
        return InfoMgr.minPitch <= pitch <= InfoMgr.maxPitch

    def _getNewScale(self):
        """ 沒有依據的取得範圍限制內的值 -> {"scale": scale, "scaleRaise": scaleRaise, "pitch": pitch} """
        scale: int
        scaleRaise: int
        pitch: int = -1
        while not self._isInLimit(pitch):
            # 隨機一個音階 -> 從 min 和 max 中拿到最多最少的音高 -> 但是還要過濾一下有沒有在限制範圍內
            scale = InfoMgr.weights[WeightsData.scale.value].getRandKey()
            minStr = InfoMgr.limit[LimitData.scale.value]["min"]
            maxStr = InfoMgr.limit[LimitData.scale.value]["max"]
            minRaise = minStr.count("'") - minStr.count(",")
            maxRaise = maxStr.count("'") - maxStr.count(",")
            scaleRaise = random.randint(minRaise, maxRaise)
            pitch = self._scaleAndRaiseToPitch(scale, scaleRaise)
        return {"scale": scale, "scaleRaise": scaleRaise, "pitch": pitch}

    def _scaleAndRaiseToPitch(self, scale: int, scaleRaise: int):
        """ 音符和升降音高轉成 pitch
        :param scale: 音符
        :param scaleRaise: 音高多高
        """
        return ScalePitch[ScalePitch.scaleName.value[int(scale) - 1]].value + scaleRaise * ScalePitch.step.value

    def repeatFrom(self, sentenceObject):
        """ 複製句子基本訊息，並改隨機音符
        :param sentenceObject: 被複製的句子
        """
        self.startWordCount = sentenceObject.startWordCount
        self.endWordCount = sentenceObject.endWordCount
        self.wordCount = sentenceObject.wordCount
        self.notes = sentenceObject.notes
        # 要改多少音符
        cahageCount: int = int(
            InfoMgr.weights[WeightsData.repeatChange.value].getRandKey())
        while cahageCount > self.wordCount:
            cahageCount: int = int(
                InfoMgr.weights[WeightsData.repeatChange.value].getRandKey())
        # 改掉隨機的音符
        changeIndexList: list = []
        index = 0
        while index < cahageCount:
            rand = random.randint(0, self.wordCount - 1)
            if rand not in changeIndexList:
                # 看看在句首句尾?給一個好 tempoWeight
                tempoWeight: WeightsObject
                if rand < self.startWordCount:
                    tempoWeight = InfoMgr.weights[WeightsData.tempo.value]
                else:
                    tempoWeight = InfoMgr.weights[WeightsData.endTempo.value]
                # 生成新音符取代
                self.notes[rand] = self._createNote(rand, tempoWeight)
                changeIndexList.append(rand)
                index += 1
