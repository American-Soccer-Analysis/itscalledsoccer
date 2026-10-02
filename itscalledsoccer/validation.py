"""Pydantic models used to validate API query parameters."""

from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationError,
    field_validator,
    model_validator,
)

StringOrStrings = str | list[str] | None


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
    def validate_string_or_strings(cls, value: Any) -> StringOrStrings:
        if value is None or isinstance(value, str):
            return value
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            return value
        raise ValueError("must be a string or list of strings")

    @model_validator(mode="after")
    def validate_id_name_pairs(self) -> "QueryParameters":
        for ids_field, names_field, label in (
            ("ids", "names", "IDs or names"),
            ("player_ids", "player_names", "player IDs or names"),
            ("team_ids", "team_names", "team IDs or names"),
        ):
            if getattr(self, ids_field) and getattr(self, names_field):
                raise ValueError(f"Please specify only {label}, not both.")
        return self


class SeasonParameters(BaseModel):
    """Validates season values supported by the API."""

    model_config = ConfigDict(strict=True)

    season_name: StringOrStrings = None

    @field_validator("season_name", mode="before")
    @classmethod
    def validate_season_type(cls, value: Any) -> StringOrStrings:
        if value is None or isinstance(value, str):
            seasons = [] if value is None else [value]
        elif isinstance(value, list) and all(isinstance(item, str) for item in value):
            seasons = value
        else:
            raise ValueError("Season must be a valid year.")

        for season in seasons:
            try:
                year = int(season)
            except ValueError as exc:
                raise ValueError(
                    f"Season must be a valid year. Received: {season}"
                ) from exc
            if year < 2013:
                raise ValueError(
                    f"Data is only available from 2013 onward. Requested season: {year}"
                )
        return value


def validation_error_message(error: ValidationError) -> str:
    """Return a concise, stable message for the client's public exceptions."""

    return "; ".join(
        str(item["msg"]).removeprefix("Value error, ") for item in error.errors()
    )
