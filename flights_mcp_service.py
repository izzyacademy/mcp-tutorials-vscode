import asyncio

from mcp import ServerSession
from mcp.server import FastMCP
from mcp.server.fastmcp import Context

from izzy_mcp_tutorials import FlightsDataAccessObject, AirportCode, PassportOwner
from izzy_mcp_tutorials.models import TravellerInformation, FlightAvailability

# Create the Flights MCP server
mcp = FastMCP("Flights MCP Service")

@mcp.tool(description="Retrieve all available passport ids")
async def get_available_passport_ids()->list[str]:
    """
    Retrieve all available passport identifiers in the database.

    Returns:
        list[str]: A list of passport ids for travellers in the database.
    """
    dao = FlightsDataAccessObject()
    return dao.get_passport_ids()

@mcp.tool(description="Retrieve details for the owner of a specific passport id")
async def get_passport_owner(passport_id: str) -> PassportOwner:
    """
    Retrieves the profile data for the specified passport id.

    Args:
        passport_id (str): The passport identifier.

    Returns:
        PassportOwner: The profile of the passport owner matching the identifier
    """
    dao = FlightsDataAccessObject()
    return dao.get_passport_owner(passport_id=passport_id)

@mcp.tool(description="Retrieve all dates for which flight availability data exists")
async def get_available_dates()->list[str]:
    """
    Retrieve all dates for which flight availability data exists.

    Returns:
        list[str]: A list of date strings in YYYY-MM-DD format.
    """
    dao = FlightsDataAccessObject()
    return dao.get_available_dates()

@mcp.tool(description="Search for available flights between two airports on a given date")
async def flight_search(search_date: str,
                  source_airport: AirportCode,
                  destination_airport: AirportCode,
                  ctx: Context[ServerSession, None]) ->  list[FlightAvailability]:
    """
    Search for available flights between two airports on a given date.

    Args:
        search_date (str): The departure date in YYYY-MM-DD format.
        source_airport (AirportCode): The IATA code of the source airport.
        destination_airport (AirportCode): The IATA code of the destination airport.
        ctx (Context[ServerSession, None]): The MCP or server session context
            passed into the function for request handling.

    Returns:
        list[FlightAvailability]: A list of matching flight availabilities
    """

    dao = FlightsDataAccessObject()
    search_results: list[FlightAvailability] = []
    query_results = dao.search_flights(search_date=search_date, source_airport=source_airport, destination_airport=destination_airport)

    is_international_flight = dao.is_international_flight(source_airport, destination_airport)

    if is_international_flight:
        elicitation_result = await ctx.elicit(message="Please enter your passport id", schema=TravellerInformation)

        if elicitation_result.action == "accept" and elicitation_result.data:
            if elicitation_result.data.traveller_has_passport:
                passport_id = elicitation_result.data.passport_id
                is_destination_citizen = dao.is_destination_citizen(passport_id=passport_id, airport_code=destination_airport)
                for query_result in query_results:
                    query_result.travellerId = passport_id
                    query_result.visaRequired = is_destination_citizen is not True
                    search_results.append(query_result)
            else:
                return query_results
        else:
            return query_results

    else:
        return query_results
    return search_results


@mcp.resource("passport://passport-owner/{passport_id}")
async def get_passport_owner(passport_id: str):
    """Returns details about the passport owner"""
    dao = FlightsDataAccessObject()
    return dao.get_passport_owner(passport_id=passport_id)

@mcp.resource("airport://airport-country/{airport_code}")
async def get_airport_country(airport_code: AirportCode):
    """Returns the country code for the airport"""
    return FlightsDataAccessObject.airport_country(airport=airport_code)

# Add a prompt
@mcp.prompt()
async def get_passenger(passport_id: str) -> str:
    """Generate a passenger retrieval prompt"""
    return f"Retrieve details about passport id {passport_id}"


async def main():
    await mcp.run_streamable_http_async()

if __name__ == "__main__":
    asyncio.run(main())