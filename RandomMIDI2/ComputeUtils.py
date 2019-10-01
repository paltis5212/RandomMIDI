import random
from ObjectModel import *
from Enums import *


class ComputeUtils():
    def setLimitNotePitch(self, minPitch: int, maxPitch: int):
        """ 設定上下限的音階
        :param min: 下限
        :param max: 上限
        """
        self.minPitch = minPitch
        self.maxPitch = maxPitch

    def _noteStrToPitch(self, noteStr: str):
        """ 純文字音符變成 pitch
        :param noteStr: 純文字音符，例如 7'
        """
        up: int = noteStr.count("'")
        down: int = noteStr.count(",")
        note: int = noteStr[: 1]
        return NoteNum[NoteNum.order[note]].value + (up - down) * NoteNum.lifting.value

    def _scaleAndRaiseToPitch(self, scale: int, scaleRaise: int):
        """ 音符和升降音高轉成 pitch
        :param scale: 音符
        :param scaleRaise: 音高多高
        """
        return NoteNum[NoteNum.order[scale]].value + scaleRaise * NoteNum.lifting.value

    def _scaleAddFluctuation(self, scale: int, scaleRaise: int, fluctuation: int):
        """ 音階和起伏得到新音符 -> {"scale": scale, "scaleRaise": scaleRaise}
        :param scale: 音階
        :param scaleRaise: 音高
        :param fluctuation: 起伏
        """
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

    def _isInLimit(self, pitch: int):
        """ 是否在使用者設定的音階上下限
        :param pitch: 音階
        """
        return self.minPitch <= pitch <= self.maxPitch

    def createNewNoteFromPass(self, music: dict, sentence: Sentence, index: int, scaleFluctuationWeight: Weights, scaleWeight: Weights, tempoWeight: Weights, strengthWeight: Weights):
        """ 依照舊的音符，生成一個新音符
        :param music: 全部音樂
        :param sentence: 本句句子
        :param index: 要改變的音符在句子的編號
        :param scaleFluctuationWeight: 起伏權重
        :param scaleWeight: 音階權重
        """
        # 找到上一個音符
        passNote = self._getPassNote(music, sentence, index)
        # 處理音階、音高
        createStep0 = self._createStep0(
            passNote, scaleFluctuationWeight, scaleWeight)
        result = createStep0["result"]
        fluctuationKeyDict = createStep0["fluctuationKeyDict"]
        scaleKeyDict = createStep0["scaleKeyDict"]
        fluctuationList = createStep0["fluctuationList"]
        if result is not None:
            result["scale"] = self._createStep1(
                fluctuationKeyDict, scaleKeyDict)
            # 用音階找第一個出現這個音階的，以取得正確音高
            for value in fluctuationList:
                if value["scale"] == result["scale"]:
                    result["scaleRaise"] = value["scaleRaise"]
                    break
        # 處理節奏、音量
        tempo = tempoWeight.getRandKey()
        volume = strengthWeight.getRandKey()
        # 填入值
        newNote: Note = Note()
        newNote.scale = result["scale"]
        newNote.scaleRaise = result["scaleRaise"]
        newNote.duration = tempo
        newNote.pitch = self._scaleAndRaiseToPitch(
            newNote.scale, newNote.scaleRaise)
        newNote.volume = volume
        return newNote

    def _createStep0(self, passNote: Note, scaleFluctuationWeight: Weights, scaleWeight: Weights):
        """ 狀況零 -> {"result": result, "fluctuationKeyDict": fluctuationKeyDict, "scaleKeyDict": scaleKeyDict}
        :param passNote: 上一個音符
        :param scaleFluctuationWeight: 起伏權重
        :param scaleWeight: 音階權重
        """
        result: dict = None
        fluctuationList: list = []
        fluctuationKeyDict: dict = {}
        scaleKeyDict: dict = {}
        index: int = 0
        while index < 50:
            newScaleAndRaise = self._scaleAddFluctuation(
                passNote.scale, scaleFluctuationWeight.getRandKey())
            newScale0 = newScaleAndRaise["scale"]
            newRaise = newScaleAndRaise["scaleRaise"]
            newPitch = self._scaleAndRaiseToPitch(
                newScale0, newRaise)
            # 不在限制內沒有未來
            if not self._isInLimit(newPitch):
                continue
            newScale1 = scaleWeight.getRandKey()
            # 同時出現就是結果了
            if newScale0 == newScale1:
                result = {"scale": newScale0, "scaleRaise": newRaise}
                break
            # 紀錄 key 出現次數
            if newScale0 not in fluctuationKeyDict:
                fluctuationKeyDict[newScale0] = 0
            fluctuationKeyDict[newScale0] += 1
            if newScale1 not in scaleKeyDict:
                scaleKeyDict[newScale1] = 0
            scaleKeyDict[newScale1] += 1
            # 紀錄一下波動後的結果
            fluctuationList.append(
                {"scale": newScale0, "scaleRaise": newRaise})
            index += 1
        return {"result": result, "fluctuationKeyDict": fluctuationKeyDict, "scaleKeyDict": scaleKeyDict, "fluctuationList": fluctuationList}

    def _createStep1(self, fluctuationKeyDict: dict, scaleKeyDict: dict):
        fluctuationMaxNum = max(list(fluctuationKeyDict.values()))
        scaleMaxNum = max(list(scaleKeyDict.values()))
        fluctuationMaxList = []
        for key in fluctuationKeyDict:
            # 同樣的 key 出現最多次
            if fluctuationKeyDict[key] == fluctuationMaxNum and scaleKeyDict[key] == scaleMaxNum:
                return key
            # 記錄身為最多的 key
            elif fluctuationKeyDict[key] == fluctuationMaxNum:
                fluctuationMaxList.append(key)
        return random.choice(fluctuationMaxList)

    def _getPassNote(self, music: dict, sentence: Sentence, index: int):
        """ 獲得上一個音符
        :param music: 全部音樂
        :param sentence: 本句句子
        :param index: 本音符在句子的編號
        """
        passNote: Note
        if index-1 < 0:
            if sentence.pos-1 < 0:
                print(
                    "ERROR ComputeUtils._getPassNote: This note is first note, not have pass note.")
            else:
                passSentence = music[sentence.pos-1]
                passNote = passSentence.notes[passSentence.wordCount-1]
        else:
            passNote = sentence.notes[index-1]
        return passNote
