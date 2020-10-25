def contains(collection, predicate):
    for item in collection:
        if predicate(item):
            return True
    return False


def flatten(collection):
    flattened = [item for sublist in collection for item in sublist]
    return flattened
