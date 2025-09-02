from izzy_mcp_tutorials import FlightsDataAccessObject


def main():
    dao = FlightsDataAccessObject()
    dao.populate_records()

    print(dao.get_available_dates())
    print(dao.get_passport_ids())


if __name__ == "__main__":
    main()


#  uv run -m tests.check_database