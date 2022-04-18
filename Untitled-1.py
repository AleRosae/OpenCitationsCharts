lista = [("ciao", "bo"), ("phil", "daff"), ("homer", "marge"), ("bart", "homer"), ("homer", "meggie")]
citing = [el for el in lista if "homer" == el[0]]
print(citing)
cited = [el for el in citing if "marge" == el[1]]
print(cited)