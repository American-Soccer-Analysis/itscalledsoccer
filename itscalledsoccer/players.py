from typing import List


class Player:
    def __init__(
        self,
        player_id: str,
        player_name: str,
        birth_date: str,
        height_ft: int,
        height_in: int,
        weight_lb: int,
        nationality: str,
        primary_broad_position: str,
        primary_general_position: str,
        secondary_broad_position: str = None,
        secondary_general_position: str = None,
        season_name: List[str] = [],
    ) -> None:
        self.player_id = player_id
        self.player_name = player_name
        self.birth_date = birth_date
        self.height_ft = height_ft
        self.height_in = height_in
        self.weight_lb = weight_lb
        self.nationality = nationality
        self.primary_broad_position = primary_broad_position
        self.primary_general_position = primary_general_position
        self.secondary_broad_position = secondary_broad_position
        self.secondary_general_position = secondary_general_position
        self.season_name = season_name


class Players:
    pass
