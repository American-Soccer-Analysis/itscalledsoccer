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


class Games:
    pass