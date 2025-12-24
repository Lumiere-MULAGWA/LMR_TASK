def creer_profil(nom, **details):

    print(f"Profil de {nom}:")
    for cle, valeur in details.items():
        print(f"- {cle}: {valeur}")

creer_profil("Lmr", ville="Lubumbashi", job="Data Scientist", passion="Football")


