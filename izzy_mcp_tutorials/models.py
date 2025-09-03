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
    travellerId: str = Field(default="", description="")
    visaRequired: bool = Field(default=False, description="Whether or not the traveler needs a travel visa")

class FlightDatabase(BaseModel):
    records : dict[str, list[FlightAvailability]] = Field(..., description="A map of availability dates to FlightAvailabilityRecords")

    def add_flight_availability(self, departure_date: str, availability: FlightAvailability):

        if departure_date not in self.records:
            self.records[departure_date] = []

        self.records[departure_date].append(availability)
        return self.records[departure_date]

    def get_availability(self, departure_date: str)->  list[FlightAvailability]:
        if departure_date not in self.records:
            return []
        return self.records[departure_date]

    def get_available_dates(self):
        available_dates = list(self.records.keys())
        return available_dates


class TravellerInformation(BaseModel):
    """Schema for collecting traveller information"""
    passport_id: str = Field(description="What is the passport number for the traveller")
    traveller_has_passport: bool = Field(description="Do you have a passport?")
    number_of_passengers: int = Field(description="How many passengers are on the flight")
    total_weight_of_luggage: float = Field(description="What is the total weight of luggage in kilograms")
