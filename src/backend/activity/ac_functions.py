
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
    """
    Function to enable filtering of results by difficulty.
    """
    adb = ActivityDB()

    filtered = []

    for result in results:
        diff = adb.fetch_attr("difficulty", result[0])
        if diff <= upper_limit and diff >= lower_limit:
            filtered.append(result)

    return filtered


def filter_by_tags(results: list[tuple[str]], tag_names: list[str],
                   tag_state: list[int]) -> list[tuple[str]]:
    """
    Function to enable filtering of results by tags.
    """
    adb = ActivityDB()

    filter_by = [tag for i, tag in enumerate(tag_names) if tag_state[i] == 1]

    filtered = []

    for result in results:
        tags = adb.fetch_attr("tags", result[0]).split(",")
        for tag in tags:
            if tag in filter_by:
                filtered.append(result)
                break

    return filtered
