
from src.backend.database.database_activity import ActivityDB


def search_database(ac_name: str) -> list[tuple[str]]:
    """
    Function to enable searching of modules using a search bar.

    @param: ac_name, query to search
    @return: a list of tuples of (activity ids, activity type) that represent
    the search results.
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


def filter_by_difficulty(results: list[tuple[str]], upper_limit: int,
                         lower_limit: int) -> list[tuple[str]]:
    pass


def filter_by_tag(results: list[tuple[str]], tag: str) -> list[tuple[str]]:
    pass
