"""
PYTHON 3.9 minimun requis pour le typage des paramètres dans les fonctions
Bonjour, tout d'abord j'aimerais vous parlez des inputs à mettre dans mon projet, 
en effet comme vous pouvez le savoir il n'y a pas qu'une seule gare à paris (10),
pour plus de praticité pour chaque nom de gare avec des espaces ' ' il faudra les
remplacer par des tirets '-'. Exemple: Paris gare de lyon sera Paris-gare-de-lyon,
Cagnes sur mer sera Cagnes-sur-mer. Enfin il faut mettre le nom exacte contenu
dans la base de donnée 'gares_et_ids.txt', rentré dans la fenetre: Paris, Marseille
ne marche donc pas.

"""

import requests,MiseEnForme,formatageHeure,APIs,tkinter,tkinter.font

if __name__=="__main__": #je demande si le programme exécuter est le bon

    class Train():
        
        def __init__(self):
            self.GaresID= open("gares_et_ids.txt", "r", encoding="UTF-8") #j'ouvre ma "base de données"
            self.API_KEY:str=APIs.APISNCF #je rentre ma clé d'API
            self.toutesLesGares:list[str]= [eachgare.split("|")[0] for eachgare in self.GaresID] #je récupère les gares dans ma "bdd"
            self.largeurGrandeFenetre:int=700 #largeur de la fenêtre (700 pour une meilleur expérience utilisateur)
            self.hauteurGrandeFenetre:int=700 #largeur de la fenêtre (700 pour une meilleur expérience utilisateur)
            self.milieu:tuple[int,int]=(self.hauteurGrandeFenetre//2,self.largeurGrandeFenetre//2)
            self.premierlancement:bool=True
            self.firstWindow()

        
        def getTrain(self,gare_depart:str, gare_arrivee:str, nombreOutput:int):           
            time:str = formatageHeure.timeToFormat() #je récupère l'heure au format de la SNCF (YYYYMMDDTHHMMSS)
            dataBaseGareNomId = MiseEnForme.MiseenForme("gares_et_ids.txt") # chaque gare on un ID unique et spécifique il faut donc le chercher pour faire une requête
            if gare_depart in dataBaseGareNomId:
                idGareDepart = dataBaseGareNomId[dataBaseGareNomId.index(gare_depart)+1]#je cherche le nom de la gare et revoie son id qui est exatement au rang n+1 du nom
            else:
                return ["Erreur", "Problème avec la gare de départ"]
            if gare_arrivee in dataBaseGareNomId:
                idGareArrivee = dataBaseGareNomId[dataBaseGareNomId.index(gare_arrivee)+1] #pareil pour la gare d'arrivee
            else:
                return ["Erreur", "problème avec la gare d'arriver"]
            listeDepart:list[str] = [] 
            memoire = ""
            url = f"https://api.sncf.com/v1/coverage/sncf/journeys?from=stop_area:SNCF:{idGareDepart}&to=stop_area:SNCF:{idGareArrivee}&count={nombreOutput}&datetime={time}&key={self.API_KEY}" #requête effectuer à l'API de la SNCF
            response = requests.get(url) # je récupère la page générer par l'url au dessus
            if response.status_code == 200: #je demande si la page à bien était trouver
                data = response.json() #la variable data marche comme un dictionaire de dictionaire de dictionaire de dictionaire de dictionaire, ou comme un système de dossier
                if "journeys" in data and len(data["journeys"]) > 0: # regarde si la catégorie "journeys" existe et qu'elle n'est pas vide
                    for i in range(nombreOutput): #nombre de résultat que l'utilisateur veut, fonctionalité à ajouté plus tard
                        try: #on cherche les horaires de départ et d'arriver
                            journey = data["journeys"][i] # i sera le nombre output voulu (a voir futur)
                            horaireDepart = journey["departure_date_time"] #je récupère l'horaire de départ
                            horaireArrivee = journey["arrival_date_time"] #je récupère l'horaire d'arrivee'
                        except IndexError:
                            pass
                        try:
                            modeDeTransport: str = journey["sections"][1]["links"][3]["id"].split(":")[1]  #type:ignore # on cherche le mode de transport de notre train voir data.json pour en savoir plus
                            if modeDeTransport == "OUI": # "OUI" n'était pas très parlant alors je le remplace par INOUI
                                modeDeTransport = "INOUI"
                        except IndexError:
                            modeDeTransport = "" #on remarquera que la SNCF n'indique pas toujours le mode de transport dans la requête que j'effectue (les TGV autre que les INOUI ne sont pas indiquer)
                        if formatageHeure.formatToTimeDate(horaireDepart) != memoire: #type:ignore #je vérifie que la date de départ n'est pas la même d'une jour à l'autre
                            dateDepart = formatageHeure.formatToTimeDate(horaireDepart)  # type:ignore #je mets les dates au format normal DD/MM/YYYY
                            listeDepart.append(dateDepart+":") #j'ajoute des : pour faire beau
                            memoire = formatageHeure.formatToTimeDate(horaireDepart)  # type:ignore #j'actualise ma mémoire avec la bonne date
                        heureDepart = formatageHeure.formatToTimeHeure(horaireDepart)  # type:ignore #je mets au bon format les heures (HH:MM)
                        heureArrivee = formatageHeure.formatToTimeHeure(horaireArrivee)  # type:ignore #je mets au bon format les heures (HH:MM)
                        listeDepart.append(f"{heureDepart} >>> {heureArrivee} {modeDeTransport}")  # type:ignore #je concatène tout ce petit monde
                    return listeDepart #et je le return
            return ["Impossible de trouvée des horaires"]
        
        
        def secondWindow(self):
                gareDepart=msg1.get().lower() #je vais chercher vos input et je les mets en minuscule (pour la bdd)
                gareArrivee=msg2.get().lower()
                if gareArrivee=="" and gareDepart=="": #pas avoir à taper des gares à fois (flemmard)
                    gareDepart="nice"
                    gareArrivee="cagnes-sur-mer"
                global fenetreTrain #je crée une nouvelle fenêtre différente de celle d'avant
                fenetreTrain = tkinter.Tk()
                fenetreTrain.title("%s - %s"%(gareDepart.capitalize(),gareArrivee.capitalize())) #je mets un beau titre à cette fenêtre
                fenetreTrain.resizable(height = False, width = False) #fais pour ne pas pouvoir redimensionner la fenêtre
                global listehoraires #pour qu'on puissent réutiliser la liste des horaires sans refaire de requête à l'api
                listehoraires = self.getTrain(gareDepart,gareArrivee, 32) #requête a l'api avec les gares demander
                global canvasFenetreTrain
                canvasFenetreTrain = tkinter.Canvas(fenetreTrain,background="#0084D4",width=self.largeurGrandeFenetre,height=self.hauteurGrandeFenetre) # dans ma fenêtre tk je crée un canvas avec une couleur de font et une hauteur, largeur
                self.insideSecondWindow(listehoraires,0.0) #je lance la fonction qui affiche les horaires en fonction de la scroll bar
                global curseur #création d'un curseur sur la droite de la fenêtre qui est utilisable partout
                curseur=tkinter.Scrollbar(fenetreTrain,orient="vertical",command=self.scrolle_bar) # la fonction scrolle_bar sera appeller à chaque fois qu'on bouge la scroll bar
                curseur.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
                canvasFenetreTrain.pack()
                fenetreTrain.mainloop()       
        
        def insideSecondWindow(self,listehoraire:list[str]=[],scrollposition:float=0.0): # cette fonction à pour but premier de faire descendre/monter les horaires quand on bouge la scroll bar
            realScrollPosition:int=int(scrollposition*1000) # la scroll bar renvoies un float entre 0 et 1 qui indique ça position, je le multiplie par 1000 pour avoir les déplacement en pixiel(environ)
            canvasFenetreTrain.delete('all') #je supprime tout ce qu'il y avait avant (rien si c'est le premier lancement)
            i=0
            padding:int=55 #position entre chaque horaire
            for each in listehoraire: # pour chaque horaire dans listehoraire je crée un rectangle de couleur alterner (pour faire beau) et je crée sont horaire dessus
                if i%2==0:
                    if self.isDate(each):
                        canvasFenetreTrain.create_rectangle(0,padding*i-realScrollPosition,self.largeurGrandeFenetre+padding,padding*i-realScrollPosition+padding,fill="#DAAA00",outline="#DAAA00")
                        canvasFenetreTrain.create_text(10,padding*i-realScrollPosition,anchor="nw",text=each,fill="#003865",font="Avenir 40")
                    else:
                        canvasFenetreTrain.create_rectangle(0,padding*i-realScrollPosition,self.largeurGrandeFenetre+padding,padding*i-realScrollPosition+padding,fill="#003865",outline="#003865")
                        canvasFenetreTrain.create_text(10,padding*i-realScrollPosition,anchor="nw",text=each,fill="#FFFFFF",font="Avenir 40")
                else:
                    if self.isDate(each): # si c'est une date je mets une autre couleur dans le rectangle (toujours pour faire beau)
                        canvasFenetreTrain.create_rectangle(0,padding*i-realScrollPosition,self.largeurGrandeFenetre+padding,padding*i-realScrollPosition+padding,fill="#DAAA00",outline="#DAAA00")
                        canvasFenetreTrain.create_text(10,padding*i-realScrollPosition,anchor="nw",text=each,fill="#003865",font="Avenir 40")
                    else:
                        canvasFenetreTrain.create_text(10,55*i-realScrollPosition,anchor="nw",text=each,fill="#FFFFFF",font="Avenir 40")
                i+=1
            if self.premierlancement:
                self.tictac(True) #je lance la première fois l'horloge avec True en argument pour qu'elle se répète à l'infini
                self.premierlancement=False
            else:
                self.tictac()
 

        
        def firstWindow(self):
            root = tkinter.Tk() #je crée la première fenêtre, je donne un titre, un icone, un fond, une taille
            root.title("SNCF")
            root.iconphoto(False,tkinter.PhotoImage(file="SNCF.png"))
            root.configure(bg="#0084D4")
            root.geometry("300x225")
            root.resizable(height = False, width = False)
            nomGareDepart:str="Gare de départ:"
            nomGareArrivée:str="Gare d'arrivée:"
            global msg1
            global msg2
            msg1=tkinter.StringVar() #je crée des variables qui change quand on mets des inputs dedans
            msg2=tkinter.StringVar()
            textGareDepart = tkinter.Label(root, text=f"{nomGareDepart:<70}",anchor="nw", font='Avenir 12',bg="#003865",fg="snow") #je mets tout en forme
            textGareDepart.pack()
            entreeGareDepart = tkinter.Entry(root, textvariable=msg1, bg="#EED484",font='Avenir 12',fg="#000000")
            entreeGareDepart.pack(padx=37,pady=5)
            textGareArrivee = tkinter.Label(root, text=f"{nomGareArrivée:<70}",anchor="nw", font='Avenir 12',bg="#003865",fg="snow")
            textGareArrivee.pack()
            entreeGareArrivee = tkinter.Entry(root, textvariable=msg2, bg="#EED484",font='Avenir 12',fg="#000000")
            entreeGareArrivee.pack(pady=5,padx=37)
            bouton = tkinter.Button(root,height=10, width="10", text="Recherche",font='Avenir 12',bg="#003865",activebackground="#DAAA00",activeforeground="#000000",fg="#FFFFFF",relief="flat",command=self.secondWindow) #je crée un bouton relier a une fonction quand on clique dessus
            bouton.pack(pady=25)
            root.mainloop()

      
        def scrolle_bar(self,inutile:str=...,scrollposition:str="0.0",*args): #sert a connaitre la position du cuseur (0.0 est la valeur de base), scrollposition changera tout seul quand le curseur bougera, le paramètre *agrs sert à ne pas avoir d'erreur si on clique sur les boutons de la scroll bar
            curseur.set(float(scrollposition),float(scrollposition)) #pour qu'il ne remonte pas toute seul (très chiant)
            self.insideSecondWindow(listehoraire=listehoraires,scrollposition=float(scrollposition)) #je transmet la nouvelle position du curseur a la fonction qui affiche les horaires en fonction de la position du curseur
        
        
        def tictac(self,auto:bool=False): #le but de cette fonction est de mettre a jour l'heure dans la fenêtre des horaires sans qu'il y est a scroll pour actualiser l'heure (auto a la valeur par défaut à False)
            actualtime:str=formatageHeure.formatToTimeHeure(formatageHeure.timeToFormat()) # je récupère l'heure et crée un emplacement sur le canvas pour celle ci
            canvasFenetreTrain.create_rectangle(self.largeurGrandeFenetre-130,self.hauteurGrandeFenetre-60,self.largeurGrandeFenetre,self.hauteurGrandeFenetre,fill="#003865",outline="#DAAA00")
            canvasFenetreTrain.create_text(self.largeurGrandeFenetre,self.hauteurGrandeFenetre,anchor="se",text=actualtime,fill="white",font="Avenir 40")
            if auto:
                canvasFenetreTrain.after(1000,self.tictac,True) #la méthode after marche de la façon suivante -> def after(self, ms, func=None, *args): 
                                                                                                                    # if func is None:
                                                                                                                    #     self.tk.call('after', ms)
                                                                                                                    #     return None
                                                                                                                    # else:
                                                                                                                    #     def callit():
                                                                                                                    #     try:
                                                                                                                    #         func(*args) <-IMPORTANT
                                                                                                                    
                # donc je mets en dans *args True pour qu'elle ce fasse ré-appeller à l'infini (notation self.tictac(True) impossible)                                                                                                 
            
        
        def isDate(self,datehoraire:str)->bool:
            return datehoraire.count("/")==2 
            #-Vraiment besoin d'expliquer?
            #-Oui
            #-Alors datehoraire est un string, j'utilise la methode .count() sur datehoraire qui compte le string qu'on lui met en paramètre, si la méthode .count("/") return 2 alors c'est une date, donc // est une date


    train=Train()