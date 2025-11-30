from datetime import UTC, datetime, timedelta

import pytest

from repositories.auctions_repository import AuctionsRepository
from tests.factories.auction_factory import AuctionFactory


@pytest.fixture(scope="function")
def repository(clean_db, container) -> AuctionsRepository:
    return container.auctions_repository()


class TestAuctionsRepository:
    @pytest.mark.parametrize(
        "_from,size",
        [
            (0, 10),
            (1, 5),
        ],
    )
    async def test_get_newest(self, repository: AuctionsRepository, _from: int, size: int):
        # Create auctions with different end dates
        now = datetime.now(UTC)
        AuctionFactory.create(name="Auction 1", end_datetime=now + timedelta(days=1))
        AuctionFactory.create(name="Auction 2", end_datetime=now + timedelta(days=2))
        AuctionFactory.create(name="Auction 3", end_datetime=now + timedelta(days=3))

        actual = await repository.get_newest(_from, size)

        assert len(actual) <= size
        if _from == 0:
            assert len(actual) == min(3, size)

        # Verify ordering (newest end_datetime first)
        if len(actual) > 1:
            for i in range(len(actual) - 1):
                assert actual[i].end_datetime <= actual[i + 1].end_datetime

    async def test_get_newest_with_filters(self, repository: AuctionsRepository):
        # Create auctions with different countries and statuses
        AuctionFactory.create(name="US Auction", country="US")
        AuctionFactory.create(name="DE Auction", country="DE")
        AuctionFactory.create(name="UK Auction", country="UK")

        # Test country filter
        filters = {"country": "US"}
        actual = await repository.get_newest(_from=0, size=10, **filters)

        assert len(actual) == 1
        assert actual[0].country == "US"
        assert actual[0].name == "US Auction"

    async def test_get_newest_count(self, repository: AuctionsRepository):
        AuctionFactory.create(name="Auction 1")
        AuctionFactory.create(name="Auction 2")
        AuctionFactory.create(name="Auction 3")

        actual = await repository.get_newest_count()

        assert actual == 3

    async def test_get_newest_empty_result(self, repository: AuctionsRepository):
        actual = await repository.get_newest(_from=0, size=10)

        assert len(actual) == 0
