def test(name):
    print(f"Function test {name}")


def baz(name):
    print(f"Function baz {name}")


def aggr(name, cb):
    cb(name)


aggr('Serega', cb=test)
aggr('Serega', cb=baz)