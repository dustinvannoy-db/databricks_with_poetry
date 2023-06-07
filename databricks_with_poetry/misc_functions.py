def id_lookup(name):
    lookups = {
        "person1": 111,
        "person2": 222,
        "person3": 333
    }
    return lookups.get(name,0)