#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import special modules ...
    try:
        import shapely
        import shapely.geometry
    except:
        raise Exception("\"shapely\" is not installed; run \"pip install --user Shapely\"") from None

    # Import my modules ...
    try:
        import pyguymer3
        import pyguymer3.geo
    except:
        raise Exception("\"pyguymer3\" is not installed; run \"pip install --user PyGuymer3\"") from None

    # **************************************************************************

    # Test ...
    a = pyguymer3.now()
    print(a)

    # Test ...
    b = pyguymer3.generate_password().lower()
    print(b)

    # Test ...
    with pyguymer3.start_session() as sess:
        c = sess.headers["User-Agent"]
    print(c)

    # Test ...
    d = "hello world on FOOBAR".replace(
        "FOOBAR",
        pyguymer3.now().isoformat(),
    )
    print(d)

    # Test ...
    e = pyguymer3.geo.buffer(
        shapely.geometry.point.Point(
            [1.0, 1.0]
        ),
        1000.0,
        ramLimit = round(pyguymer3.now().timestamp()),                          # Setting the RAM limit to be a UNIX timestamp is very
                                                                                # silly, but it allows me to test how to access "pyguymer3"
                                                                                # calls as keyword arguments to functions using "ast".
    )
    print(e)

    # Test ...
    f = pyguymer3.geo.buffer(
        shapely.geometry.point.Point(
            [2.0, 2.0]
        ),
        2000.0,
        ramLimit = round(pyguymer3.now().timestamp()),                          # Setting the RAM limit to be a UNIX timestamp is very
                                                                                # silly, but it allows me to test how to access "pyguymer3"
                                                                                # calls as keyword arguments to functions using "ast".
    ).buffer(2.0)
    print(f)
