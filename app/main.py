import logging
from fastapi import FastAPI, Query
from app.config import config
from app.api_client import fetch_api_data
from app.coalesce import DataCoalescer

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

@app.get("/coalesce")
async def coalesce_api(member_id: int, strategy: str = Query(None)):
    # Log the incoming request details
    logging.info(f"Received GET /coalesce?member_id={member_id}&strategy={strategy or 'default'}")

    # Initialize the DataCoalescer with the specified or default strategy
    data_coalescer = DataCoalescer(strategy or config.COALESCE_STRATEGY)

    # Fetch data using API URLs from the configuration
    api_responses = await fetch_api_data(member_id, urls=config.API_URLS)

    if not api_responses:
        logging.error("Failed to fetch data from all APIs")
        return {"error": "Failed to fetch data from all APIs"}

    # Coalesce the data using the specified strategy
    coalesced_result = data_coalescer.coalesce_data(api_responses)

    # Log the coalesced result
    logging.info(f"Coalesced result: {coalesced_result}")

    return coalesced_result

