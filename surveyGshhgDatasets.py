#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.12/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import json
    import os
    import pathlib

    # Import special modules ...
    try:
        import cartopy
        cartopy.config.update(
            {
                "cache_dir" : pathlib.PosixPath("~/.local/share/cartopy").expanduser(),
            }
        )
    except:
        raise Exception("\"cartopy\" is not installed; run \"pip install --user Cartopy\"") from None
    try:
        import shapely
        import shapely.geometry
    except:
        raise Exception("\"shapely\" is not installed; run \"pip install --user Shapely\"") from None

    # **************************************************************************

    # Make output folder if it is missing ...
    if not os.path.exists("surveyGshhgDatasets"):
        os.makedirs("surveyGshhgDatasets")

    # Loop over GSHHG resolutions ...
    for gshhgRes in [
        "c",                            # crude
        "l",                            # low
        "i",                            # intermediate
        "h",                            # high
        "f",                            # full
    ]:
        print(f"Surveying \"{gshhgRes}\" ...")

        # Loop over GSHHG levels ...
        for gshhgLevel in [
            1,
            2,
            3,
            4,
            5,
            6,
        ]:
            # Skip known missing datasets ...
            if gshhgLevel == 4 and gshhgRes == "c":
                continue

            print(f"  Surveying \"{gshhgRes}\" at \"{gshhgLevel}\" ...")

            # Initialize database ...
            db = {}

            # Loop over records in the GSHHG Shapefile for this level and
            # resolution ...
            for record in cartopy.io.shapereader.Reader(
                cartopy.io.shapereader.gshhs(
                    level = gshhgLevel,
                    scale = gshhgRes,
                )
            ).records():
                # Check record ...
                assert isinstance(record.attributes, dict), repr(type(record.attributes))
                assert isinstance(record.bounds, tuple), repr(type(record.bounds))
                assert isinstance(record.geometry, shapely.geometry.polygon.Polygon), repr(type(record.geometry))
                assert record.geometry.geom_type == "Polygon"
                assert not record.geometry.has_m
                assert not record.geometry.has_z
                assert not record.geometry.is_empty
                assert len(record.geometry.interiors) == 0, "a Polygon has a hole"

                # Check that it is self-consistent ...
                assert record.attributes["level"] == gshhgLevel
                assert record.bounds == record.geometry.bounds
                assert record.geometry.is_valid == record.geometry.exterior.is_valid
                assert record.geometry.minimum_clearance == record.geometry.exterior.minimum_clearance

                # Check that it is not a duplicate ...
                assert record.attributes["id"] not in db, "a record is already in the database"

                # Populate database ...
                db[record.attributes["id"]] = {
                    "attributes" : record.attributes,
                      "geometry" : {
                                     "area" : record.geometry.area,
                                   "bounds" : record.geometry.bounds,
                                 "centroid" : (record.geometry.centroid.x, record.geometry.centroid.y),
                                 "exterior" : {
                            "is_closed" : record.geometry.exterior.is_closed,
                              "is_ring" : record.geometry.exterior.is_ring,
                            "is_simple" : record.geometry.exterior.is_simple,
                               "length" : record.geometry.exterior.length,
                        },
                                 "is_valid" : record.geometry.is_valid,
                        "minimum_clearance" : record.geometry.minimum_clearance,
                    }
                }
                del db[record.attributes["id"]]["attributes"]["level"]
                del db[record.attributes["id"]]["attributes"]["id"]

            # Save database ...
            with open(f"surveyGshhgDatasets/gshhgRes={gshhgRes}_gshhgLevel={gshhgLevel}.json", "wt", encoding = "utf-8") as fObj:
                json.dump(
                    db,
                    fObj,
                    ensure_ascii = False,
                          indent = 4,
                       sort_keys = True,
                )
