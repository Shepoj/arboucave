# élément avec la plus grand clé
def argmax[T](d: dict[int, T]):
    m = list(d.keys())[0]
    for key in d:
        if key > m:
            m = key
    return d[m]