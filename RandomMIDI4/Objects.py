#! -*- coding:utf-8 -*-

# Track > Sentence > Note


class Note:
    pitch: int
    duration: float
    volume: int


class Sentence:
    notes: list  # list(Note(), ...)
    pause_duration: float


class Track:
    track: str
    track_name: str
    tempo: int  # bpm
    program: int  # 樂器
    sentences: list  # list(Sentence(), ...)
