"""
TP2 – Exercice 3 : Gestion des ressources vitales (Station ORBIT-X)

Objectif :
Gérer un inventaire de ressources (oxygène, eau, énergie, etc.) pour éviter
les ruptures et planifier un réapprovisionnement.

Structure des données
---------------------
1) Ressources (inventaire) :
    ressources = { 'oxygene': 120, 'eau': 300, 'energie': 500 }

2) Besoin / consommation (pour 1 cycle) :
    besoin = { 'oxygene': 5, 'eau': 12 }

3) Consommations par activité (menu_activites) :
    consommations = {
        'EVA': {'oxygene': 8, 'energie': 15},
        'Hydroponie': {'eau': 20, 'energie': 10}
    }



⚠️ Rappels / Contraintes importantes :
- Si une ressource est absente de l'inventaire des ressources, sa quantité est considérée comme 0.
- Vous devez éviter les KeyError en utilisant dict.get().
- Ne modifiez pas directement les dictionnaires si la fonction demande une copie.
"""

COUTS_UNITAIRES = {
    'oxygene': 2.5,
    'eau': 0.5,
    'energie': 1.2,
    'nourriture': 3.0
}
"""
    Vérifie si les ressources disponibles suffisent pour couvrir un besoin.

    Args:
        ressources (dict): stock actuel {ressource: quantité}
        besoin (dict): ressources nécessaires {ressource: quantité}

    Returns:
        tuple: (peut_faire: bool, manquantes: list)
            - peut_faire = True si toutes les ressources sont suffisantes
            - manquantes = liste des ressources insuffisantes (noms)
    """

def verifier_ressources(ressources, besoin):
    peut_faire = True
    manquantes = []

    for nom, quantite_dem in besoin.items():
        stock_actuel = ressources.get(nom, 0)
        if stock_actuel < quantite_dem:
            peut_faire = False
            manquantes.append(nom)
    return peut_faire, manquantes

def mettre_a_jour_ressources(ressources, besoin, cycles=1):
    """
    Met à jour les ressources après avoir exécuté un certain nombre de cycles.

    Exemple :
- si besoin = {'oxygene': 5} et cycles=3, on consomme 15 d'oxygène.

    Args:
        ressources (dict): stock actuel
        besoin (dict): consommation par cycle
        cycles (int): nombre de cycles

    Returns:
        dict: nouveau dictionnaire de ressources (copie)
    """
    nouvelles = ressources.copy()
    consommes=0
    for nom, quantite_dem in besoin.items():
        consommes=quantite_dem*cycles
        nouvelles[nom]=nouvelles.get(nom,0)- consommes
    return nouvelles




def generer_alertes_ressources(ressources, seuil=50):
    """
    Identifie les ressources dont le stock est inférieur au seuil.

    Pour chaque ressource en alerte, on suggère une quantité standard
      à commander
    pour revenir à un niveau cible.

    Règle de suggestion :
    - Niveau cible = 200 unités


    Args:
        ressources (dict)
        seuil (int)

    Returns:
        dict: {ressource: (stock_actuel, a_commander)}
    """
    alertes = {}
    niveau_cible = 200
    a_commander=0
    for nom, stock_actuel in ressources.items():
        if stock_actuel<seuil:
         a_commander=niveau_cible-stock_actuel
        alertes[nom]=(stock_actuel,a_commander)
    return alertes


def calculer_cycles_possibles(ressources, consommations):
    """
    Calcule, pour chaque activité, combien de cycles peuvent être réalisés
    avec les ressources actuelles.

    ⚠️ Si une activité nécessite une ressource avec conso 0, vous pouvez l'ignorer
       pour éviter une division par zéro (comme dans l'exercice 1).

    Args:
        ressources (dict)
        consommations (dict): {activite: {ressource: conso_par_cycle}}

    Returns:
        dict: {activite: nb_cycles_possibles}
    """
    possibles = {}

    for activite, ressources_conso in consommations.items():
        min_cycles = float("inf")

        for ressource, conso in ressources_conso.items():
             if conso > 0:
              cycles = ressources.get(ressource, 0) / conso
              min_cycles = min(min_cycles, cycles)
       
        possibles[activite] = min_cycles

    return possibles


def optimiser_reapprovisionnement(ressources, besoins_prevus, budget):
    """
    Objectif :
Déterminer une liste d'achats {ressource: quantite_a_acheter}
pour couvrir des besoins prévus, sans dépasser le budget.

Paramètres :
- ressources : stock actuel
- besoins_prevus : besoins totaux à couvrir (déjà agrégés)
    ex: {'oxygene': 300, 'eau': 500}
- budget : budget disponible (float)

Étapes attendues (guidage) :
1) Calculer le manque pour chaque ressource 
2) Acheter en respectant le budget, selon les coûts unitaires.
   Stratégie simple attendue :
   - acheter dans l'ordre des manques décroissants
   - acheter autant que possible sans dépasser le budget

⚠️ On attend une solution SIMPLE, pas une optimisation mathématique parfaite.

Returns:
    dict: {ressource: quantite_a_acheter}
    """
    
    achats = {}

    manques = {}
    for nom, besoin in besoins_prevus.items():
        if nom not in ressources:
            continue

        info = ressources[nom]
        if isinstance(info, dict):
            stock = info.get("stock", 0)
            cout = info.get("cout", 0)
        else:  
            stock = info[0]
            cout = info[1]

        manque = besoin - stock
        if manque > 0:
            manques[nom] = manque


    priorites = sorted(manques.items(), key=lambda x: x[1], reverse=True)



    for nom, manque in priorites:
        info = ressources[nom]

        if isinstance(info, dict):
            cout = info.get("cout", 0)
        else:
            cout = info[1]

        if cout <= 0:
            continue
        if budget <= 0:
            break

        qte_max = int(budget // cout)       
        qte_achetee = min(manque, qte_max)  

        if qte_achetee > 0:
            achats[nom] = qte_achetee
            budget -= qte_achetee * cout




    return achats


if __name__ == "__main__":
  ressources_test = {'oxygene': 120, 'eau': 300, 'energie': 500}
  besoin_cycle = {'oxygene': 5, 'eau': 12}

print("Vérif :", verifier_ressources(ressources_test, besoin_cycle))
print("Après 3 cycles :", mettre_a_jour_ressources(ressources_test, besoin_cycle, cycles=3))
print("Alertes :", generer_alertes_ressources({'oxygene': 40, 'eau': 120}, seuil=50))

consommations_test = {
        'EVA': {'oxygene': 8, 'energie': 15},
        'Hydroponie': {'eau': 20, 'energie': 10}
    }
print("Cycles possibles :", calculer_cycles_possibles(ressources_test, consommations_test))

besoins_prevus = {'oxygene': 300, 'eau': 500, 'energie': 650}
print("Achats :", optimiser_reapprovisionnement(ressources_test, besoins_prevus, budget=200))
