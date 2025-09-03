from izzy_mcp_tutorials import FlightsDataAccessObject


def main():
    dao = FlightsDataAccessObject()
    dao.populate_records()

    print(dao.get_available_dates())
    print(dao.get_passport_ids())
    print(dao.search_flights("2025-09-03", "LAX", "MCO"))

    is_international_flight = dao.is_international_flight("LAX", "YUL")
    print("is_international_flight", is_international_flight)
if __name__ == "__main__":
    main()


#  uv run -m tests.check_database