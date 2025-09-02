from typing import Literal

from pydantic import Field, BaseModel

CountryCode = Literal['US', 'MX', 'CA']

AirportCode = Literal["MCO", "MIA", "LAX", "ATL", "YYZ", "YVR", "YUL", "CUN", "MEX"]

class PassportOwner(BaseModel):
    fullName: str = Field(..., description="Full name of Passport Owner")
    passportId: str = Field(..., description="Passport identifier")
    countryCitizenship: CountryCode = Field(..., description="Country of Citizenship")

class FlightAvailability(BaseModel):
    id: str = Field(..., description="A unique identifier for the availability")
    sourceAirport: AirportCode = Field(..., description="Departure IATA airport code")
    destinationAirport: AirportCode = Field(..., description="Destination IATA airport code")
    departureDate: str = Field(..., description="Departure date in YYYY-MM-DD format")
    sourceAirportCountry: CountryCode = Field(..., description="The IATA country code of the departure airport")
    destinationAirportCountry: CountryCode = Field(..., description="The IATA country code of the arrival airport")

class FlightDatabase(BaseModel):
    records : dict[str, list[FlightAvailability]] = Field(..., description="A map of availability dates to FlightAvailabilityRecords")

    def add_flight_availability(self, departure_date: str, availability: FlightAvailability):

        if departure_date not in self.records:
            self.records[departure_date] = []

        self.records[departure_date].append(availability)
        return self.records[departure_date]

    def get_availability(self, departure_date: str)->  list[FlightAvailability] | None:
        if departure_date not in self.records:
            return None
        return self.records[departure_date]

    def get_available_dates(self):
        available_dates = list(self.records.keys())
        return available_dates