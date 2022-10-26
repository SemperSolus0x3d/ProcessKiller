from dataclasses import dataclass

@dataclass
class Config:
    predicates = []
    ignores = []
    interval = 1
