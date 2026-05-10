print("Generation Identifier")

myYear = int(input("Which Year were you born? "))
if myYear >= 1883 and myYear <= 1900:
    print("Lost Generation")
elif myYear >= 1901 and myYear <= 1927:
    print("Greatest Generation")
elif myYear >= 1928 and myYear <= 1945:
    print("Silent Generation")
elif myYear >= 1946 and myYear <= 1964:
    print("Baby Boomer")
elif myYear >= 1965 and myYear <= 1980:
    print("Generation X")
elif myYear >= 1981 and myYear <= 1996:
    print("Millennials")
elif myYear >= 1997 and myYear <= 2012:
    print("Generation Z")
elif myYear >= 2013 and myYear <= 9999:
    print("Generation Alpha")
else:
    print("Generation Unknown...")