import httpx
from typing import List, Dict

async def fetch_api_data(member_id: int, urls: List[str]) -> List[Dict[str, int]]:
    responses = []
    async with httpx.AsyncClient() as client:
        for url in urls:
            print(f"Requesting data from: {url}{member_id}")  # Debugging output
            try:
                response = await client.get(f"{url}{member_id}")
                response.raise_for_status()
                data = await response.json()
                print(f"Fetched data from {url}: {data}")  # Debugging output
                responses.append(data)
            except httpx.HTTPStatusError as exc:
                print(f"HTTP error while fetching data from {url}: {exc}")
            except json.JSONDecodeError as exc:
                print(f"JSON decode error: {exc}")
    print(f"All collected responses: {responses}")  # Debugging output
    return responses

