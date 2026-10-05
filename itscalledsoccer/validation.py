"""Pydantic models used to validate API query parameters."""

from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationInfo,
    field_validator,
    model_validator,
)

from itscalledsoccer.errors import (
    ConflictingParametersError,
    InvalidLeagueError,
    InvalidParameterFormatError,
    InvalidSeasonError,
)

StringOrStrings = str | list[str] | None
VALID_LEAGUES = ("nwsl", "mls", "uslc", "usl1", "usls", "nasl", "mlsnp")


class QueryParameters(BaseModel):
    """Common query parameters accepted by the ASA API."""

    model_config = ConfigDict(extra="allow", strict=True)

    leagues: StringOrStrings = None
    ids: StringOrStrings = None
    names: StringOrStrings = None
    game_ids: StringOrStrings = None
    team_ids: StringOrStrings = None
    team_names: StringOrStrings = None
    player_ids: StringOrStrings = None
    player_names: StringOrStrings = None
    season_name: StringOrStrings = None

    @field_validator(
        "leagues",
        "ids",
        "names",
        "game_ids",
        "team_ids",
        "team_names",
        "player_ids",
        "player_names",
        "season_name",
        mode="before",
    )
    @classmethod
    def validate_string_or_strings(
        cls, value: Any, info: ValidationInfo
    ) -> StringOrStrings:
        if value is None or isinstance(value, str):
            values = [value] if value is not None else []
        elif isinstance(value, list) and all(isinstance(item, str) for item in value):
            values = value
        else:
            field_labels = {
                "ids": "IDs",
                "game_ids": "IDs",
                "team_ids": "IDs",
                "player_ids": "IDs",
                "names": "Names",
                "team_names": "Names",
                "player_names": "Names",
                "leagues": "Leagues",
                "season_name": "Season",
            }
            label = field_labels.get(info.field_name or "", "Parameter")
            value_description = (
                "list of names"
                if info.field_name in {"names", "team_names", "player_names"}
                else "list of strings"
            )
            raise InvalidParameterFormatError(
                f"{label} must be passed as a string or {value_description}."
            )

        if info.field_name == "leagues":
            valid_leagues = (info.context or {}).get("valid_leagues", VALID_LEAGUES)
            for league in values:
                if (isinstance(value, list) or league) and league not in valid_leagues:
                    if isinstance(value, list):
                        message = (
                            f"{league} is not a valid league. "
                            f"Must be one of: {list(valid_leagues)}"
                        )
                    else:
                        message = (
                            f"{league} is not valid. "
                            f"Must be one of: {list(valid_leagues)}"
                        )
                    raise InvalidLeagueError(message)
        return value

    @model_validator(mode="after")
    def validate_id_name_pairs(self) -> "QueryParameters":
        for ids_field, names_field, label in (
            ("ids", "names", "IDs or names"),
            ("player_ids", "player_names", "player IDs or names"),
            ("team_ids", "team_names", "team IDs or names"),
        ):
            if getattr(self, ids_field) and getattr(self, names_field):
                raise ConflictingParametersError(
                    f"Please specify only {label}, not both."
                )
        return self


class SeasonParameters(BaseModel):
    """Validates season years and names supported by the API."""

    model_config = ConfigDict(strict=True)

    season_name: StringOrStrings = None

    @field_validator("season_name", mode="before")
    @classmethod
    def validate_season_type(cls, value: Any) -> StringOrStrings:
        if value is None:
            return None
        if isinstance(value, int) and not isinstance(value, bool):
            seasons = [str(value)]
            normalized_value: StringOrStrings = seasons[0]
        elif isinstance(value, str):
            seasons = [value]
            normalized_value = value
        elif isinstance(value, list) and all(
            isinstance(item, str)
            or (isinstance(item, int) and not isinstance(item, bool))
            for item in value
        ):
            seasons = [str(item) for item in value]
            normalized_value = seasons
        else:
            raise InvalidParameterFormatError(
                "Season must be a string, integer, or list of strings or integers."
            )

        for season in seasons:
            try:
                year = int(season)
            except ValueError:
                if len(season) >= 7 and season[:4].isdigit() and season[4] == "-":
                    year = int(season[:4])
                else:
                    continue
            if year < 2013:
                raise InvalidSeasonError(
                    f"Data is only available from 2013 onward. Requested season: {year}"
                )
        return normalized_value
