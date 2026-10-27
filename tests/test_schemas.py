"""Tests for the conversion of raw API values in the schemas."""

from datetime import date, datetime, timezone

import pytest

from judobase import Competition, Contest, CountryShort, Judoka


@pytest.fixture
def competition_data(get_test_data):
    """Raw competition as the API returns it."""
    return get_test_data("get_competition_list.json")["mock_response"][0]


@pytest.fixture
def contest_data(get_test_data):
    """Raw contest as the API returns it."""
    return get_test_data("find_contests.json")["mock_response"]["contests"][0]


@pytest.fixture
def judoka_data(get_test_data):
    """Raw judoka as the API returns it."""
    return get_test_data("get_judoka_info.json")["mock_response"]


class TestCompetition:
    """Test cases for the Competition schema."""

    def test_types(self, competition_data):
        """Ids are ints, days are dates, flags are bools, times are UTC."""
        competition = Competition(**competition_data)

        assert competition.id_competition == 2259
        assert competition.id_country == 32
        assert competition.date_from == date(2021, 12, 11)
        assert competition.date_to == date(2021, 12, 11)
        assert competition.is_teams is False
        assert competition.has_results == 0
        assert competition.updated_at_ts == datetime(2024, 12, 4, 9, 50, 17, tzinfo=timezone.utc)
        assert competition.updated_at == datetime(2024, 12, 4, 9, 50, 17, tzinfo=timezone.utc)

    @pytest.mark.parametrize(
        "raw",
        [
            "2024-07-27",
            "2024/07/27",
            "2024-07-27T00:00:00Z",
            "2024/07/27 10:00:00",
            date(2024, 7, 27),
        ],
    )
    def test_day_formats(self, competition_data, raw):
        """Any of the formats judobase uses becomes a plain day."""
        competition = Competition(**{**competition_data, "date_from": raw})
        assert competition.date_from == date(2024, 7, 27)

    def test_has_results_is_a_count(self, competition_data):
        """has_results is the number of results, not a flag."""
        competition = Competition(**{**competition_data, "has_results": "112"})
        assert competition.has_results == 112

    def test_updated_at_can_be_missing(self, competition_data):
        """A missing updated_at stays None."""
        competition_data.pop("updated_at")
        assert Competition(**competition_data).updated_at is None


class TestContest:
    """Test cases for the Contest schema."""

    def test_types(self, contest_data):
        """Ids are ints, flags are bools, times are UTC."""
        contest = Contest(**contest_data)

        assert contest.id_fight == 785134
        assert contest.id_competition == 2653
        assert contest.id_person_blue == 10231
        assert contest.id_person_white == 14431
        assert contest.id_winner == 14431
        assert contest.id_weight == 6
        assert contest.bye is False
        assert contest.date_start_ts == datetime(2024, 8, 1, 8, 1, 8, tzinfo=timezone.utc)
        assert contest.first_hajime_at_ts == datetime(2024, 8, 1, 8, 1, 54, tzinfo=timezone.utc)
        assert contest.updated_at.tzinfo == timezone.utc

    @pytest.mark.parametrize("raw", ["0", 0, "", None])
    def test_unknown_ids_are_none(self, contest_data, raw):
        """Before the draw and the result judobase sends 0 instead of an id."""
        contest = Contest(
            **{
                **contest_data,
                "id_person_blue": raw,
                "id_person_white": raw,
                "id_winner": raw,
                "id_country_blue": raw,
                "id_weight": raw,
            }
        )
        assert contest.id_person_blue is None
        assert contest.id_person_white is None
        assert contest.id_winner is None
        assert contest.id_country_blue is None
        assert contest.id_weight is None

    @pytest.mark.parametrize("raw", ["0", 0, "1970-01-01 00:00:00", None])
    def test_unknown_times_are_none(self, contest_data, raw):
        """Judobase sends 0 for a time it does not know."""
        contest = Contest(**{**contest_data, "date_start_ts": raw, "first_hajime_at_ts": raw})
        assert contest.date_start_ts is None
        assert contest.first_hajime_at_ts is None

    def test_bye(self, contest_data):
        """Bye is a flag."""
        assert Contest(**{**contest_data, "bye": "1"}).bye is True


class TestJudoka:
    """Test cases for the Judoka schema."""

    def test_types(self, judoka_data):
        """The year of birth and the country are ints, the hidden birth date is None."""
        judoka = Judoka(**judoka_data)

        assert judoka.dob_year == 2001
        assert judoka.id_country == 24
        assert judoka.birth_date is None

    def test_known_birth_date(self, judoka_data):
        """A real birth date is kept, in UTC."""
        judoka = Judoka(**{**judoka_data, "birth_date": "2001-05-04"})
        assert judoka.birth_date == datetime(2001, 5, 4, tzinfo=timezone.utc)

    @pytest.mark.parametrize("raw", ["0", 0, "", None])
    def test_unknown_year_of_birth(self, judoka_data, raw):
        """An unknown year of birth is None."""
        assert Judoka(**{**judoka_data, "dob_year": raw}).dob_year is None


def test_country_id_is_int():
    """Country ids are ints."""
    country = CountryShort(name="Japan", id_country="7", ioc="JPN")
    assert country.id_country == 7
