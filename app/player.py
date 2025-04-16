from dataclasses import dataclass, asdict


@dataclass
class Player:
    name: str
    score: int
    card_num: int
