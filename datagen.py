import random
import uuid
import hashlib

names = [
    "Mick",
    "Ian",
    "Charlie",
    "John",
    "Ronnie",
    "Eric",
    "Keith",
    "Paul",
    "Neil",
    "Ringo",
    "Roger",
    "Bruce",
    "Brian",
    "Pete",
    "Phil",
    "Stuart",
    "Ron",
    "George",
    "Bono",
    "Dave",
    "Chris",
    "Bob",
]

lastnames = [
    "Dickinson",
    "Harris",
    "Cocker",
    "Lennon",
    "Watts",
    "Hendrix",
    "Cohen",
    "Allison",
    "Lester",
    "Gahan",
    "Wood",
    "Plant",
    "Grohl",
    "Jones",
    "Bowie",
    "Davies",
    "Gallagher",
    "Jagger",
    "Joplin",
    "Weller",
    "Starr",
    "Bono",
    "Page",
    "Waters",
    "Daltrey",
    "Harrison",
    "Richards",
    "Young",
    "Gilmour",
    "Stewart",
    "Dylan",
    "Cassidy",
    "Clapton",
    "Morrison",
    "Collins",
    "Townshend",
    "Cobain",
    "McCartney",
]
email = [
    "@gmail.com",
    "@yahoo.com",
    "@hotmail.com",
    "@outlook.com",
    "@aol.com",
    "@mail.com",
    "@icloud.com",
    "@msn.com",
    "@live.com",
    "@comcast.net",
]


workers = {
    "name": lambda: random.choice(names),
    "lastname": lambda: random.choice(lastnames),
    "uuid": lambda: uuid.uuid4().hex,
    "passhash": lambda: hashlib.sha256(uuid.uuid4().hex.encode()).hexdigest(),
    "choice": lambda *args: random.choice(args),
    "login": lambda: type(
        "",
        (),
        {
            "n": random.choice(names).lower(),
            "ln": random.choice(lastnames).lower(),
            "res": lambda s: s.n + s.ln,
        },
    )().res(),
    "randint": lambda a, b: random.randint(int(a), int(b)),
    # For meta
    "list": lambda d, x: [v for k, v in d.items()] * int(x),
    "duplicate": lambda d, a: [d for _ in range(int(a))],
}

structure = {
    "_meta": ["duplicate 10"],
    "name": "!name",
    "lastname": "!lastname",
    "uuid": "!uuid",
    "passhash": "!passhash",
    "gender": "!choice male female",
    "login": "!login",
    "data": {
        "_meta": ["list 10"],
        "randint": "!randint 1000 9999",
    },
}


def done(structure):
    if isinstance(structure, list):
        return [done(s) for s in structure]
    elif isinstance(structure, dict):
        return {k: done(v) for k, v in structure.items()}
    elif isinstance(structure, str):
        if structure.startswith("!"):
            f, *args = structure[1:].split(" ")
            func = workers.get(f)
            return func(*args)
        else:
            return structure
    return structure


def generate(structure):
    if isinstance(structure, dict):
        for m in structure.pop("_meta", []):
            f, *args = m.split(" ")
            func = workers.get(f)
            structure = func(structure, *args)
        if isinstance(structure, dict):
            for k, v in structure.items():
                structure[k] = generate(v)
            return {**structure}
        else:
            return generate(structure)
    elif isinstance(structure, list):
        return [generate(s) for s in structure]
    return structure


if __name__ == "__main__":

    """
    ...
        {
            'name': 'Paul',
            'lastname': 'Richards',
            'uuid': '73a0464e45a24197993b152dbf18dec0',
            'passhash': '5f3b1a80e2cac655add751a0e670e029953674f5f8d30f1374ab8d1da82d5206',
            'gender': 'male',
            'login': 'georgedickinson',
            'data': [3112, 4205, 2581, 5753, 1108, 4081, 9403, 6025, 4386, 5445]
        }
    ]
    """
    print(done(generate(structure)))
