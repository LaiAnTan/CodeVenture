
from src.backend.database.database_activity import ActivityDB


def search_database(ac_name: str) -> list[str]:
    """
    Function to enable searching of modules using a search bar.

    @param: ac_name, query to search
    @return: a list of activity ids that represent the search results.
    """

    # get raw data
    adb = ActivityDB()
    raw_data = adb.getIDTypeTitle()

    results = []

    # remove spaces
    tokenstr = "".join(ac_name.split(" ")).lower()

    # data is a tuple in the form (id, type, title)
    for data in raw_data:

        matchstr = "".join(data[2].split(" ")).lower()
        if tokenstr in matchstr:
            results.append(data[:-1])

    return results
