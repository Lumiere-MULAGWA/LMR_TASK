def logger_fonction(func):
    def wrapper(*args, **kwargs):
        print(f"Appel de {func.__name__} avec {args} et {kwargs}")
        return func(*args, **kwargs)
    return wrapper

@logger_fonction
def commander_pizza(taille, *garnitures, **options):
    print(f"Pizza {taille} avec {garnitures}. Livraison : {options.get('livraison')}")

commander_pizza("Large", "Champignons", "Olives", livraison=True, paiement="Carte")

