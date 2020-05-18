#! -*- coding:utf-8 -*-
import random
import Objects


class CreateTrack():
    def __init__(self):
        self.track = Objects.Track()
        self.track.track = 0
        self.track.track_name = 'new'
        self.track.tempo = 180
        self.track.program = 0
        self.last_repeat_at = 0

    def get_weight_result(self, weights):
        total = sum(weights.values())
        rad = random.randint(0, total)
        weight_up = 0
        for k, v in weights.items():
            weight_up += v
            if rad <= weight_up:
                return k

    def is_repeat(self):
        return random.randint(0, 100) < 50

    def get_repeat_sentence(self, sentence):
        pass

    def get_sentence(self):
        pass

    def run(self):
        sentences = list()
        for index in range(50):
            is_repeat = index == 0 and False or self.is_repeat()
            sentence = is_repeat and self.get_repeat_sentence(sentences[index - 1].copy()) or self.get_sentence()
            sentences.append(sentence)
        self.track.sentences = sentences
