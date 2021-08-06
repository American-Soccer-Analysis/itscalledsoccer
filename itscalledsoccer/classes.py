from typing import List


class Game:
    def __init__(
        self,
        game_id: str,
        date_time_utc: str,
        home_score: int,
        away_score: int,
        home_team_id: str,
        away_team_id: str,
        referee_id: str,
        stadium_id: str,
        home_manager_id: str,
        away_manager_id: str,
        expanded_minutes: int,
        season_name: str,
        matchday: int,
        attendance: int,
        knockout_game: bool,
        last_updated_utc: str,
    ) -> None:
        self.game_id = game_id
        self.date_time_utc = date_time_utc
        self.home_score = home_score
        self.away_score = away_score
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.referee_id = referee_id
        self.stadium_id = stadium_id
        self.home_manager_id = home_manager_id
        self.away_manager_id = away_manager_id
        self.expanded_minutes = expanded_minutes
        self.season_name = season_name
        self.matchday = matchday
        self.attendance = attendance
        self.knockout_game = knockout_game
        self.last_updated_utc = last_updated_utc


class Manager:
    def __init__(self, manager_id: str, manager_name: str, nationality: str) -> None:
        self.manager_id = manager_id
        self.manager_name = manager_name
        self.nationality = nationality


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


class Referee:
    def __init__(self, referee_id: str, referee_name: str, nationality: str) -> None:
        self.referee_id = referee_id
        self.referee_name = referee_name
        self.nationality = nationality


class Stadium:
    def __init__(
        self,
        stadium_id: str,
        stadium_name: str,
        capacity: int = None,
        year_built: int = None,
        roof: bool = None,
        turf: bool = None,
        street: str = None,
        city: str = None,
        province: str = None,
        country: str = None,
        postal_code: str = None,
        latitude: float = None,
        longitude: float = None,
        field_x: int = None,
        field_y: int = None,
    ) -> None:
        self.stadium_id = stadium_id
        self.stadium_name = stadium_name
        self.capacity = capacity
        self.year_built = year_built
        self.roof = roof
        self.turf = turf
        self.street = street
        self.city = city
        self.province = province
        self.country = country
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude
        self.field_x = field_x
        self.field_y = field_y


class Team:
    def __init__(
        self, team_id: str, team_name: str, team_short_name: str, team_abbreviation: str
    ) -> None:
        self.team_id = team_id
        self.team_name = team_name
        self.team_short_name = team_short_name
        self.team_abbreviation = team_abbreviation
