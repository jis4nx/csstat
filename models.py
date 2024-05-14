from dataclasses import dataclass
from typing import Dict


@dataclass
class Ranks:
    premier_best: str
    premier_current: str
    csgo_best: str
    csgo_last: str


@dataclass
class Weapon:
    most_weapon: Dict[str, str]
    least_weapon: Dict[str, str]


@dataclass
class Stats:
    kd: str
    win_rate: str
    hs_rate: str
    adr: str


@dataclass
class Map:
    highest_win: Dict[str, str]
    least_win: Dict[str, str]


@dataclass
class Player:
    player_rank: Ranks
    player_stats: Stats
    player_map: Map
    player_weapon: Weapon
