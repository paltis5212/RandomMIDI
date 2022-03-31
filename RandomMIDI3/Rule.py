from typing import Dict
import Model.Weights as Weights
import Model.Enums as Enums

refer_paragraph_weight: Dict[Enums.ParagraphName, Weights.Paragraph] = {}
refer_paragraph_weight[Enums.ParagraphName.Chorus] = Weights.Paragraph(
    allSwing={
        True: 1,
        False: 1
    },
    sentenceCount={
        4: 2,
        6: 1,
        8: 1,
    },
    sentenceWeight=Weights.Sentence(
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
        noteWeight=Weights.Note(
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
                Enums.Pitch.C: 2,
                Enums.Pitch.SharpC: 1,
                Enums.Pitch.D: 2,
                Enums.Pitch.SharpD: 1,
                Enums.Pitch.E: 2,
                Enums.Pitch.F: 2,
                Enums.Pitch.SharpF: 1,
                Enums.Pitch.G: 2,
                Enums.Pitch.SharpG: 1,
                Enums.Pitch.A: 2,
                Enums.Pitch.SharpA: 1,
                Enums.Pitch.B: 2,
            },
            value={
                Enums.Value.ThirtySecond: 1,
                Enums.Value.DottedThirtySecond: 1,
                Enums.Value.Sixteenth: 4,
                Enums.Value.DottedSixteenth: 1,
                Enums.Value.Eighth: 5,
                Enums.Value.DottedEighth: 1,
                Enums.Value.Quarter: 8,
                Enums.Value.DottedQuarter: 1,
                Enums.Value.Half: 4,
                Enums.Value.DottedHalf: 1,
                Enums.Value.Whole: 1,
                Enums.Value.DottedWhole: 1,
                Enums.Value.DoubleWhole: 1,
            }
        ),
        chordWeight=Weights.Chord(
            distance={
                0: 1,
                2: 1,
                4: 1,
                6: 3,
                8: 2,
                10: 3,
                12: 3,
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