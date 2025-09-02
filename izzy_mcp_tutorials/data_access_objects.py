from .models import FlightDatabase, CountryCode, AirportCode, FlightAvailability, PassportOwner
from datetime import date, timedelta

class FlightsDataAccessObject:

    def __init__(self):
        self.database: FlightDatabase = FlightDatabase(records={})
        self.source_airports: list[AirportCode] = ["MCO", "MIA", "LAX", "ATL", "YYZ", "YVR", "YUL", "CUN", "MEX"]
        self.passport_numbers: dict[str, PassportOwner] = {
            "12345": PassportOwner(fullName="Jane Doe", passportId="12345", countryCitizenship="US"),
            "98765": PassportOwner(fullName="Jose Garcia", passportId="98765", countryCitizenship="MX"),
            "77889": PassportOwner(fullName="John Smith", passportId="77889", countryCitizenship="CA"),
            "54321": PassportOwner(fullName="Samantha Garcia", passportId="54321", countryCitizenship="MX"),
            "43210": PassportOwner(fullName="Samantha Smith", passportId="43210", countryCitizenship="US")
        }

    def get_passport_ids(self):
        return list(self.passport_numbers.keys())

    def get_passport_owner(self, passport_id: str):
        if passport_id not in self.passport_numbers:
            return None
        return self.passport_numbers[passport_id]

    @staticmethod
    def airport_country(airport: AirportCode):

        airport_countries: dict[AirportCode, CountryCode] = {
            "MCO": "US",  # Orlando International Airport
            "MIA": "US",  # Miami International Airport
            "LAX": "US",  # Los Angeles International Airport
            "ATL": "US",  # Hartsfield–Jackson Atlanta International Airport
            "YYZ": "CA",  # Toronto Pearson International Airport
            "YVR": "CA",  # Vancouver International Airport
            "YUL": "CA",  # Montréal–Trudeau International Airport
            "CUN": "MX",  # Cancún International Airport
            "MEX": "MX",  # Mexico City International Airport
        }

        return airport_countries[airport]

    def get_availability(self, search_date: str):
        return self.database.get_availability(departure_date=search_date)

    def get_available_dates(self):
        return self.database.get_available_dates()

    def populate_records(self):
        # Start from today
        today = date.today()

        availability_id:int = 1
        number_of_days_from_today = 3

        # Loop through today and the next n days
        for i in range(number_of_days_from_today):
            next_date = today + timedelta(days=i)
            current_date = next_date.strftime("%Y-%m-%d")

            # Loop through all source and destination combinations
            for source in self.source_airports:
                for destination in self.source_airports:
                    if source != destination:  # avoid source == destination
                        source_country = FlightsDataAccessObject.airport_country(source)
                        destination_country = FlightsDataAccessObject.airport_country(destination)

                        record_id = str(availability_id)
                        availability = FlightAvailability(id=record_id, sourceAirport=source, destinationAirport=destination, departureDate=current_date, sourceAirportCountry=source_country, destinationAirportCountry=destination_country)
                        self.database.add_flight_availability(departure_date=current_date, availability=availability)
        return self.database