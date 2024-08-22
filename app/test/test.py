import httpx
import pytest
from unittest.mock import patch, AsyncMock
from app.api_client import fetch_api_data
from app.coalesce import DataCoalescer

@pytest.fixture
def mock_responses_fixture():
    return [
        {"oop_max": 10000, "remaining_oop_max": 9000, "copay": 1000},
        {"oop_max": 20000, "remaining_oop_max": 8000, "copay": 5000},
        {"oop_max": 15000, "remaining_oop_max": 7000, "copay": 3000},
    ]

@pytest.mark.asyncio
@pytest.mark.parametrize("strategy, expected", [
    ("average", {"oop_max": 15000, "remaining_oop_max": 8000, "copay": 3000}),
    ("min", {"oop_max": 10000, "remaining_oop_max": 7000, "copay": 1000}),
    ("max", {"oop_max": 20000, "remaining_oop_max": 9000, "copay": 5000}),
    ("median", {"oop_max": 15000, "remaining_oop_max": 8000, "copay": 3000}),
])
@patch("httpx.AsyncClient.get")
async def test_coalesce_strategies(mock_get, strategy, expected, mock_responses_fixture):
    mock_responses = mock_responses_fixture.copy()

    async def mock_return_value(*args, **kwargs):
        if mock_responses:
            mock_resp = AsyncMock()
            mock_resp.status_code = 200
            mock_resp.json = AsyncMock(return_value=mock_responses.pop(0))
            return mock_resp
        return None

    mock_get.side_effect = mock_return_value

    urls = ["https://api1.com?member_id=", "https://api2.com?member_id=", "https://api3.com?member_id="]
    api_responses = await fetch_api_data(1, urls)

    # Initialize DataCoalescer with the current strategy
    coalescer = DataCoalescer(strategy_name=strategy)
    data = coalescer.coalesce_data(api_responses)

    # Debugging output to inspect values
    print(f"Strategy: {strategy}")
    print(f"Actual data returned by the API: {data}")
    print(f"Expected data: {expected}")

    # Compare the actual and expected results
    assert data == expected, f"Expected {expected}, but got {data}"

