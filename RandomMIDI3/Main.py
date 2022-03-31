import random
from typing import Dict, List
import Model.Enums as Enums
import Model.Objects as Objects
import Model.Weights as Weights
from Rule import *


# TODO 變調

# TODO 異步
refer_paragraph = {}

for k, w in refer_paragraph_weight.items():
    refer_paragraph[k] = Objects.Paragraph().create(w)

print(refer_paragraph)