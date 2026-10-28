from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest

from judobase import Competition, Contest, JudoBase, RankingEntry
from judobase.schemas import WeightEnum


class TestJudobase:
    """Test cases for the Judobase class."""

    @patch("judobase.base.CompetitionAPI.get_competition_list")
    @pytest.mark.asyncio
    async def test_all_competition(self, mock_get_competition_list):
        """Test all_competition response."""
        async with JudoBase() as client:
            await client.all_competition()
            mock_get_competition_list.assert_called_once_with()

    @patch("judobase.base.CompetitionAPI.get_competition_list", new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_competitions_in_range(self, mock_get_competition_list, get_test_data):
        """Test competitions_in_range response."""
        test_data = get_test_data("competitions_in_range.json")
        mock_get_competition_list.return_value = [
            Competition(**comp) for comp in test_data["mock_response"]
        ]

        async with JudoBase() as client:
            comps = await client.competitions_in_range(
                datetime(2023, 5, 1, tzinfo=timezone.utc),
                datetime(2023, 8, 1, tzinfo=timezone.utc),
            )
            mock_get_competition_list.assert_called_once_with()
            assert comps == [Competition(**comp) for comp in test_data["expected"]]

            comps_by_day = await client.competitions_in_range(date(2023, 5, 1), date(2023, 8, 1))
            assert comps_by_day == comps

    @pytest.mark.asyncio
    async def test_timeout(self):
        """The request timeout can be set."""
        async with JudoBase() as client:
            assert client._timeout.total == 10
        async with JudoBase(timeout=30) as client:
            assert client._timeout.total == 30

    @patch("judobase.base.ContestAPI.find_contests", new_callable=AsyncMock)
    @patch("judobase.base.CompetitionAPI.get_competition_list", new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_all_contests(self, mock_get_competition_list, mock_find_contests, get_test_data):
        """Test all_contests response."""
        test_data = get_test_data("competitions_in_range.json")
        mock_get_competition_list.return_value = [
            Competition(**comp) for comp in test_data["mock_response"]
        ]
        async with JudoBase() as client:
            await client.all_contests()
            mock_get_competition_list.assert_called_once_with()
            assert mock_find_contests.call_count == len(test_data["mock_response"])

    @patch("judobase.base.ContestAPI.find_contests", new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_contests_by_competition_id(self, mock_find_contests, get_test_data):
        """Test contests_by_competition_id response."""
        test_data = get_test_data("contests_by_competition_id.json")
        mock_find_contests.return_value = [Contest(**cont) for cont in test_data["mock_response"]]
        async with JudoBase() as client:
            await client.contests_by_competition_id(competition_id=2869)
            mock_find_contests.assert_called_once_with(competition_id="2869", weight_id="")

            mock_find_contests.reset_mock()
            await client.contests_by_competition_id(competition_id=2869, include_events=True)
            assert mock_find_contests.call_count == len(test_data["mock_response"]) + 1

    @patch("judobase.base.CompetitionAPI.get_competition_info")
    @pytest.mark.asyncio
    async def test_competition_by_id(self, mock_competition_by_id):
        """Test competition_by_id response."""
        async with JudoBase() as client:
            await client.competition_by_id(123)
            mock_competition_by_id.assert_called_once_with("123")

    @patch("judobase.base.JudokaAPI.get_judoka_info")
    @pytest.mark.asyncio
    async def test_judoka_by_id(self, mock_get_judoka_info):
        """Test judoka_by_id response."""
        async with JudoBase() as client:
            await client.judoka_by_id(123)
            mock_get_judoka_info.assert_called_once_with("123")

    @patch("judobase.base.CountryAPI.get_country_info")
    @pytest.mark.asyncio
    async def test_country_by_id(self, mock_get_country_info):
        """Test country_by_id response."""
        async with JudoBase() as client:
            await client.country_by_id(123)
            mock_get_country_info.assert_called_once_with("123")

    @patch("judobase.base.CountryAPI.get_country_list")
    @pytest.mark.asyncio
    async def test_all_countries(self, mock_get_country_list):
        """Test all_countries response."""
        async with JudoBase() as client:
            await client.all_countries()
            mock_get_country_list.assert_called_once_with()

    @patch("judobase.base.RatingAPI.get_current_rating")
    @pytest.mark.asyncio
    async def test_current_rating_by_id(self, mock_get_current_rating):
        """Test current_rating_by_id response."""
        async with JudoBase() as client:
            await client.current_rating_by_id(123)
            mock_get_current_rating.assert_called_once_with("123")

    @patch("judobase.base.RatingAPI.get_rating_history")
    @pytest.mark.asyncio
    async def test_rating_history_by_id(self, mock_get_rating_history):
        """Test rating_history_by_id response."""
        async with JudoBase() as client:
            await client.rating_history_by_id(123)
            mock_get_rating_history.assert_called_once_with("123")

    @patch("judobase.base.RatingAPI.get_ranking_list", new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_world_ranking_list(self, mock_get_ranking_list, get_test_data):
        """Test world_ranking_list keeps the senior weights only."""
        test_data = get_test_data("get_ranking_list.json")
        mock_get_ranking_list.return_value = [RankingEntry(**r) for r in test_data["expected"]]

        async with JudoBase() as client:
            result = await client.world_ranking_list()
            mock_get_ranking_list.assert_called_once_with()
            assert [entry.id_person for entry in result] == [13208, 87228]

    @patch("judobase.base.RatingAPI.get_ranking_list", new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_world_ranking_list_of_one_weight(self, mock_get_ranking_list):
        """Test world_ranking_list asks judobase for one weight."""
        async with JudoBase() as client:
            await client.world_ranking_list(WeightEnum.M66)
            mock_get_ranking_list.assert_called_once_with(weight_id="2")
