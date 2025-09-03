from .models import FlightDatabase, CountryCode, AirportCode, FlightAvailability, PassportOwner
from datetime import date, timedelta

class FlightsDataAccessObject:
    """
        Data Access Object (DAO) for managing flight and passenger data.

        This class provides an abstraction layer over the `FlightDatabase` model,
        enabling the management of available flights, passport owners, and airport
        country mappings. It supports operations such as retrieving flight
        availability, searching for flights, and managing passport information.

    Attributes:
        database (FlightDatabase): The in-memory flight database instance.
        source_airports (list[AirportCode]): List of available source airports.
        passport_numbers (dict[str, PassportOwner]): Mapping of passport IDs to
            their corresponding owner profiles.
    """
    def __init__(self):
        """
        Initializes the FlightsDataAccessObject with an empty flight database,
        a list of source airports, and a set of predefined passport owners.
        """
        self.database: FlightDatabase = FlightDatabase(records={})
        self.source_airports: list[AirportCode] = ["MCO", "MIA", "LAX", "ATL", "YYZ", "YVR", "YUL", "CUN", "MEX"]
        self.passport_numbers: dict[str, PassportOwner] = {
            "12345": PassportOwner(fullName="Jane Doe", passportId="12345", countryCitizenship="US"),
            "98765": PassportOwner(fullName="Jose Garcia", passportId="98765", countryCitizenship="MX"),
            "77889": PassportOwner(fullName="John Smith", passportId="77889", countryCitizenship="CA"),
            "54321": PassportOwner(fullName="Samantha Garcia", passportId="54321", countryCitizenship="MX"),
            "43210": PassportOwner(fullName="Samantha Smith", passportId="43210", countryCitizenship="US")
        }

        self.populate_records()

    def is_international_flight(self, source_airport: AirportCode, destination_airport: AirportCode)-> bool:

        if source_airport not in self.source_airports:
            return False
        if destination_airport not in self.source_airports:
            return False

        source_country = FlightsDataAccessObject.airport_country(source_airport)
        destination_country = FlightsDataAccessObject.airport_country(destination_airport)
        
        return source_country is not destination_country

    def is_destination_citizen(self, passport_id: str, airport_code: AirportCode) -> bool:
        destination_country = FlightsDataAccessObject.airport_country(airport_code)
        owner = self.get_passport_owner(passport_id=passport_id)
        return destination_country == owner.countryCitizenship

    def get_passport_ids(self):
        """
        Retrieve all passport IDs available in the system.

        Returns:
            list[str]: A list of passport ID strings.
        """
        return list(self.passport_numbers.keys())

    def get_passport_owner(self, passport_id: str):
        """
        Retrieve the profile details of a passport owner.

        Args:
            passport_id (str): The passport ID to look up.

        Returns:
            PassportOwner | None: The corresponding passport owner profile if
            found, otherwise None.
        """
        if passport_id not in self.passport_numbers:
            return None
        return self.passport_numbers[passport_id]

    @staticmethod
    def airport_country(airport: AirportCode):
        """
        Determine the country code for a given airport.

        Args:
            airport (AirportCode): The IATA airport code.

        Returns:
            CountryCode: The corresponding country code for the airport.
        """

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

    def search_flights(self, search_date: str, source_airport: AirportCode, destination_airport: AirportCode):
        """
        Search for available flights on a given date between two airports.

        Args:
            search_date (str): The departure date in YYYY-MM-DD format.
            source_airport (AirportCode): The departure airport code.
            destination_airport (AirportCode): The arrival airport code.

        Returns:
            list[FlightAvailability] | None: A list of matching flight
            availabilities if found, otherwise None.
        """
        initial_results = self.get_availability(search_date=search_date)
        if len(initial_results) < 1:
            return []

        search_results: list[FlightAvailability] = []
        for flight_item in initial_results:
            if flight_item.sourceAirport == source_airport and flight_item.destinationAirport == destination_airport:
                search_results.append(flight_item)
        if len(search_results) > 0:
            return search_results
        return []

    def get_availability(self, search_date: str):
        """
        Retrieve all flight availabilities for a given date.

        Args:
            search_date (str): The departure date in YYYY-MM-DD format.

        Returns:
            list[FlightAvailability] A list of available flights for the given date.
        """
        return self.database.get_availability(departure_date=search_date)

    def get_available_dates(self):
        """
        Retrieve all dates for which flight availability data exists.

        Returns:
            list[str]: A list of date strings in YYYY-MM-DD format.
        """
        return self.database.get_available_dates()

    def populate_records(self):
        """
        Populate the flight database with sample flight availabilities.

        Generates flight availability records for today and the next three days,
        covering all combinations of source and destination airports.

        Returns:
            FlightDatabase: The updated flight database with populated records.
        """
        # Start from today
        today = date.today()

        availability_id:int = 1000
        number_of_days_from_today = 8

        # Loop through today and the next {number_of_days_from_today} days
        for i in range(number_of_days_from_today):
            next_date = today + timedelta(days=i)
            current_date = next_date.strftime("%Y-%m-%d")

            # Loop through all source and destination combinations
            for source in self.source_airports:
                for destination in self.source_airports:
                    if source != destination:  # avoid source == destination
                        source_country:CountryCode = FlightsDataAccessObject.airport_country(source)
                        destination_country:CountryCode = FlightsDataAccessObject.airport_country(destination)
                        visa_required:bool = source_country is not destination_country

                        record_id_1 = str(availability_id)
                        record_id_2 = str(availability_id + 1)
                        record_id_3 = str(availability_id + 2)
                        record_id_4 = str(availability_id + 3)
                        record_id_5 = str(availability_id + 4)
                        
                        availability_1 = FlightAvailability(id=record_id_1, sourceAirport=source, destinationAirport=destination, departureDate=current_date, sourceAirportCountry=source_country, destinationAirportCountry=destination_country, airline="Air Canada", visaRequired=visa_required)
                        availability_2 = FlightAvailability(id=record_id_2, sourceAirport=source, destinationAirport=destination, departureDate=current_date, sourceAirportCountry=source_country, destinationAirportCountry=destination_country, airline="Air Mexico", visaRequired=visa_required)
                        availability_3 = FlightAvailability(id=record_id_3, sourceAirport=source, destinationAirport=destination, departureDate=current_date, sourceAirportCountry=source_country, destinationAirportCountry=destination_country, airline="Alaska Air", visaRequired=visa_required)
                        availability_4 = FlightAvailability(id=record_id_4, sourceAirport=source, destinationAirport=destination, departureDate=current_date, sourceAirportCountry=source_country, destinationAirportCountry=destination_country, airline="Delta Airlines", visaRequired=visa_required)
                        availability_5 = FlightAvailability(id=record_id_5, sourceAirport=source, destinationAirport=destination, departureDate=current_date, sourceAirportCountry=source_country, destinationAirportCountry=destination_country, airline="United Airlines", visaRequired=visa_required)
                        
                        self.database.add_flight_availability(departure_date=current_date, availability=availability_1)
                        self.database.add_flight_availability(departure_date=current_date, availability=availability_2)
                        self.database.add_flight_availability(departure_date=current_date, availability=availability_3)
                        self.database.add_flight_availability(departure_date=current_date, availability=availability_4)
                        self.database.add_flight_availability(departure_date=current_date, availability=availability_5)

                availability_id = availability_id + 100

        return self.database