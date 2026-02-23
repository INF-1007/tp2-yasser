"""
TP2 – Exercice 1 : Analyse des modules de la station spatiale ORBIT-X

Objectif :
Analyser les modules de la station afin d'extraire des statistiques utiles
pour la planification de la maintenance.

Un module est représenté par :
    nom_module : (cout_maintenance, temps_intervention, criticite)

Exemple :
modules = {
    'Laboratoire': (120, 15, 8),
    'Habitat': (200, 10, 9),
    'Observatoire': (150, 20, 6)
}
"""


def analyser_modules(modules):

    """
    Analyse les modules de la station.

    Args:
        modules (dict): {nom_module: (cout, temps, criticite)}

    Returns:
        dict contenant :
            - 'module_plus_critique' : str ou None
            - 'cout_moyen' : float
            - 'temps_moyen' : float
    """

    stats = {
        'module_plus_critique': None,
        'cout_moyen': 0,
        'temps_moyen': 0 }
    
    if len(modules)==0:
        return stats
  

    meilleur_ratio=-1
    meilleur_module=None
    for nom_module,(cout,temps,criticite) in modules.items():
        if temps==0:
            continue
        ratio=criticite/temps
        if ratio > meilleur_ratio:
         meilleur_ratio=ratio
         meilleur_module=nom_module
    return(meilleur_module)

modules = {
    'Laboratoire': (120,15,8),
    'Habitat': (200,10,9),
    'Observatoire': (150,20,6)
}

print(analyser_modules(modules))


somme_couts=sum(v[0] for v in modules.values())
cout_moyen = somme_couts/len(modules)

somme_temps=sum(v[1] for v  in modules.values())
temps_moyen=somme_temps/len(modules)

print(cout_moyen,temps_moyen)



def regrouper_modules_par_type(modules, types):
    """
    Regroupe les modules par type.

    Args:
        modules (dict): dictionnaire des modules
        types (dict): {nom_module: type}

    Returns:
        dict: {type: [liste des modules]}
    """

    modules_par_type = {}


    for nom_module in modules:
        if nom_module not in types or types[nom_module] is None:
            continue
        t=types[nom_module]
        if t not in modules_par_type:
         modules_par_type[t]=[]
        modules_par_type[t].append(nom_module)

    return modules_par_type


def calculer_cout_total(modules, interventions):
    """
    Calcule le coût total de maintenance prévu.

    Args:
        modules (dict): {nom_module: (cout, temps, criticite)}
        interventions (dict): {nom_module: nombre_interventions}

    Returns:
        float: coût total
    """

    cout_total = 0.0
    for nom_module in interventions:
       if nom_module not in modules or modules[nom_module] is None:
          continue
       nombre_interventions=interventions[nom_module]
       cout_total+=modules[nom_module][0]* nombre_interventions

    return cout_total

# -------------------------------------------------------------------
# TESTS main
# -------------------------------------------------------------------


if __name__ == "__main__":
    modules_test = {
        'Laboratoire': (120, 15, 8),
        'Habitat': (200, 10, 9),
        'Observatoire': (150, 20, 6)
    }

    types_test = {
        'Laboratoire': 'science',
        'Habitat': 'vie',
        'Observatoire': 'science'
    }

    interventions_test = {
        'Laboratoire': 2,
        'Habitat': 1
    }

    print(analyser_modules(modules_test))
    print(regrouper_modules_par_type(modules_test, types_test))
    print(calculer_cout_total(modules_test, interventions_test))
