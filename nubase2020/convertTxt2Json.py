#!/usr/bin/env python3

# Use the proper idiom in the main module ...
# NOTE: See https://docs.python.org/3.11/library/multiprocessing.html#the-spawn-and-forkserver-start-methods
if __name__ == "__main__":
    # Import standard modules ...
    import json
    import os
    import string

    # Import my modules ...
    try:
        import pyguymer3
    except:
        raise Exception("\"pyguymer3\" is not installed; you need to have the Python module from https://github.com/Guymer/PyGuymer3 located somewhere in your $PYTHONPATH") from None

    # **************************************************************************

    # Check if the dataset is missing ...
    if not os.path.exists("nubase_4.mas20.txt"):
        print("Downloading \"nubase_4.mas20.txt\" ...")

        # Start session ...
        with pyguymer3.start_session() as sess:
            # Download dataset ...
            # NOTE: See https://www.anl.gov/phy/atomic-mass-data-resources
            pyguymer3.download_file(sess, "https://www.anl.gov/sites/www/files/2022-11/nubase_4.mas20.txt", "nubase_4.mas20.txt")

    # **************************************************************************

    # Check if the raw nuclides database is missing ...
    if not os.path.exists("rawNucs.json"):
        print("Making \"rawNucs.json\" ...")

        # Initialise raw nuclides database ...
        rawNucs = {}

        # Open dataset ...
        with open("nubase_4.mas20.txt", "rt", encoding = "utf-8") as fObj:
            # Loop over lines in dataset ...
            for line in fObj:
                # Skip this line if it does not appear to be data ...
                if not line[0:3].isdigit():
                    print("INFO: Skipping line as it does not appear to be data.")
                    continue

                # Parse line ...
                #       1: 3   AAA           a3       Mass Number (AAA)
                #       5: 8   ZZZi          a4       Atomic Number (ZZZ); i=0 (gs); i=1,2 (isomers); i=3,4 (levels); i=5 (resonance); i=8,9 (IAS)
                #                                     i=3,4,5,6 can also indicate isomers (when more than two isomers are presented in a nuclide)
                #     12: 16   A El          a5       A Element
                #     17: 17   s             a1       s=m,n (isomers); s=p,q (levels); s=r (reonance); s=i,j (IAS);
                #                                     s=p,q,r,x can also indicate isomers (when more than two isomers are presented in a nuclide)
                #     19: 31   Mass #     f13.6       Mass Excess in keV (# from systematics)
                #     32: 42   dMass #    f11.6       Mass Excess uncertainty in keV (# from systematics)
                #     43: 54   Exc #      f12.6       Isomer Excitation Energy in keV (# from systematics)
                #     55: 65   dE #       f11.6       Isomer Excitation Energy uncertainty in keV (# from systematics)
                #     66: 67   Orig          a2       Origin of Excitation Energy
                #     68: 68   Isom.Unc      a1       Isom.Unc = *  (gs and isomer ordering is uncertain)
                #     69: 69   Isom.Inv      a1       Isom.Inv = &  (the ordering of gs and isomer is reversed compared to ENSDF)
                #     70: 78   T #         f9.4       Half-life (# from systematics); stbl=stable; p-unst=particle unstable
                #     79: 80   unit T        a2       Half-life unit
                #     82: 88   dT            a7       Half-life uncertainty
                #     89:102   Jpi */#/T=    a14      Spin and Parity (* directly measured; # from systematics; T=isospin)
                #    103:104   Ensdf year    a2       Ensdf update year
                #    115:118   Discovery     a4       Year of Discovery
                #    120:209   BR            a90      Decay Modes and their Intensities and Uncertanties in %; IS = Isotopic Abundance in %
                rawNuc = {}
                rawNuc["A"]          = line[  0:  3].strip()
                rawNuc["Z"]          = line[  4:  7].strip()
                rawNuc["i"]          = line[  7:  8].strip()
                rawNuc["A El"]       = line[ 11: 16].strip()
                rawNuc["s"]          = line[ 16: 17].strip()
                rawNuc["Mass"]       = line[ 18: 31].strip()
                rawNuc["dMass"]      = line[ 31: 42].strip()
                rawNuc["Exc"]        = line[ 42: 54].strip()
                rawNuc["dExc"]       = line[ 54: 65].strip()
                rawNuc["Orig"]       = line[ 65: 67].strip()
                rawNuc["Isom.Unc"]   = line[ 67: 68].strip()
                rawNuc["Isom.Inv"]   = line[ 68: 69].strip()
                rawNuc["T"]          = line[ 69: 78].strip()
                rawNuc["unit T"]     = line[ 78: 80].strip()
                rawNuc["dT"]         = line[ 81: 88].strip()
                rawNuc["Jpi */#/T="] = line[ 88:102].strip()
                rawNuc["ENSDF year"] = line[102:104].strip()
                rawNuc["Discovery"]  = line[114:118].strip()
                rawNuc["Br"]         = line[119:   ].strip().split(";")

                # Figure out the key and check that there isn't a key clash ...
                key = f'{int(rawNuc["Z"]):03d}-{int(rawNuc["A"]):03d}-{int(rawNuc["i"]):03d}'
                if key in rawNucs:
                    raise Exception(f"there is a key clash: \"{key}\"") from None

                # Populate raw nuclides database ...
                rawNucs[key] = rawNuc

        # Save raw nuclides database ...
        with open("rawNucs.json", "wt", encoding = "utf-8") as fObj:
            json.dump(
                rawNucs,
                fObj,
                ensure_ascii = False,
                      indent = 4,
                   sort_keys = True,
            )

    # **************************************************************************

    # Check if the simple database is missing ...
    if not os.path.exists("simple.json"):
        print("Making \"simple.json\" ...")

        # Initialise simple database ...
        simple = {
            "chemicalElements" : {},
            "physicalNuclides" : {},
        }

        # Load raw nuclides database ...
        with open("rawNucs.json", "rt", encoding = "utf-8") as fObj:
            rawNucs = json.load(fObj)

        # Loop over raw nuclides ...
        for rawKey, rawNuc in rawNucs.items():
            # Skip the lonely single neutron ...
            if rawKey == "000-001-000":
                continue

            # Skip "levels"/"resonance"/"IAS" raw nuclides ...
            if rawNuc["s"] in ["p", "q",]:
                continue
            if rawNuc["s"] in ["r",]:
                continue
            if rawNuc["s"] in ["i", "j",]:
                continue

            # Skip raw nuclides without a mass ...
            if rawNuc["Mass"] == "":
                continue

            # Perform some basic checks ...
            if int(rawNuc["A"]) != int(rawNuc["A El"].strip(string.ascii_letters)):
                raise Exception(f'there is an inconsistency: \"{rawNuc["A"]}\" -vs- \"{rawNuc["A El"]}\"') from None

            # Deduce key and make chemical element database entry ...
            eleKey = rawNuc["A El"].strip(string.digits)
            if eleKey not in simple["chemicalElements"]:
                simple["chemicalElements"][eleKey] = {}

            # Deduce key and check that there isn't a key clash ...
            nucKey = rawNuc["A El"]
            if rawNuc["s"] in ["m", "n", "x",]:
                nucKey = f'{int(rawNuc["A"])}m{int(rawNuc["i"]):d}{eleKey}'
            if nucKey in simple["chemicalElements"][eleKey]:
                raise Exception(f"there is a key clash: \"{nucKey}\"") from None
            if nucKey in simple["physicalNuclides"]:
                raise Exception(f"there is a key clash: \"{nucKey}\"") from None

            print(f"Processing \"{eleKey}\" (\"{nucKey}\") ...")

            # Populate chemical element ...
            abun = None                                                         # [%]
            for part in rawNuc["Br"]:
                if not part.startswith("IS"):
                    continue
                abun = float(part.split("=")[1].strip().split()[0])             # [%]
            if abun is not None:
                if abun <= 0.0:
                    raise Exception(f"there is a confusing abundance: \"{abun:f}\"") from None
                simple["chemicalElements"][eleKey][nucKey] = abun               # [%]

            # Populate physical nuclide ...
            if rawNuc["Mass"].endswith("#"):
                rawNuc["Mass"] = f'{rawNuc["Mass"].removesuffix("#")}.0'
            simple["physicalNuclides"][nucKey] = float(rawNuc["Mass"])          # [keV]

        # Save raw nuclides database ...
        with open("simple.json", "wt", encoding = "utf-8") as fObj:
            json.dump(
                simple,
                fObj,
                ensure_ascii = False,
                      indent = 4,
                   sort_keys = True,
            )
