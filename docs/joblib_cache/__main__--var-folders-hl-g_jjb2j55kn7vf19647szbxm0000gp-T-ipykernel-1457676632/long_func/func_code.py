# first line: 1
@memory.cache(verbose=True)
def long_func(a: str, b: int):
    time.sleep(2)
    return a * b * 2
