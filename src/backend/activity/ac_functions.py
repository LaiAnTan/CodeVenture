
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

    # result in the form (id, type)

    return results


def filter_by_difficulty(results: list[tuple[str]], upper_limit: int,
                         lower_limit: int) -> list[tuple[str]]:
    """
    Function to enable filtering of results by difficulty.
    """
    adb = ActivityDB()

    filtered = []

    if isinstance(upper_limit, int) is False or isinstance(lower_limit, int)\
            is False:
        return filtered

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


def sort_results(results: list[tuple[str]], mode: str, option: str):
    """
    Function to sort results based on certain criteria.
    """

    adb = ActivityDB()

    match mode.lower():

        case "difficulty":
            weights = [adb.fetch_attr("difficulty", result[0]) for result in
                       results]
        case "name":
            weights = [adb.fetch_attr("title", result[0]) for result in
                       results]

    if option == "asc":
        s = [x for _, x in sorted(zip(weights, results))]
    elif option == "desc":
        s = [x for _, x in sorted(zip(weights, results), reverse=True)]

    return s
