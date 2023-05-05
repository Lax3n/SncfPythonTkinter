"""
ce code sert a crée une liste avec la BDD
"""
def MiseenForme(name:str):
    res:list[str]=[]
    fichier=open(name,"r",encoding="UTF-8").read() #j'ouvre et je lis le fichier
    l=fichier.split("\n") #je sépare tout
    for each_element in l: 
        nomgare,idgare=each_element.split("|") #pour chaque gare n au rang n+1 il y aura sont id
        res.append(nomgare)
        res.append(idgare)
    return res
    
def horaireForme(horaire:str):
    return "\n".join(horaire) #besoin d'expliquer?