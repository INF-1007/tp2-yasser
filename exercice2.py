"""
TP2 – Exercice 2 : Priorisation des interventions (Station ORBIT-X)

Objectif :
Les interventions techniques arrivent en continu. Il faut :
- Calculer une priorité pour chaque intervention
- Trier les interventions par priorité décroissante (SANS sorted)
- Estimer le temps total de traitement
- Identifier les interventions urgentes

Structure d'une intervention (dict) :
{
  'id': 1,
  'urgence': 20,     # int (plus grand = plus urgent)
  'duree': 3,        # int (unités abstraites)
  'critique': True   # bool (True = intervention critique)
}

⚠️ Champs manquants :
- Utiliser 0 par défaut pour urgence et duree
- Utiliser False par défaut pour critique
"""



def calculer_priorite(intervention):
    """
    Calcule la priorité d'une intervention.

    Formule :
        score de priorité = (urgence × 2) + (duree × 1) + (critique × 10)

    Rappels :
    - Le booléen critique vaut 1 si True, 0 sinon
    - Champs manquants → valeur 0 (ou False pour critique)

    Args:
        intervention (dict)

    Returns:
        int: score de priorité
    """
    score = 0
    "urgence"==intervention.get("urgence", 0)
    "duree" ==intervention.get("duree", 0)
    "critique" == intervention.get("critique", False)
    critique=int(intervention["critique"])
    score=intervention["urgence"]*2+ critique *10 + intervention["duree"]




    return score


# -------------------------------------------------------------------
# 2) Tri des interventions
# -------------------------------------------------------------------

def trier_interventions(liste_interventions):
    """
    Trie les interventions par priorité décroissante (plus grand score en premier).

    Contraintes :
    - Interdit d'utiliser sorted() ou .sort()
    - Le tri doit être STABLE :
        si deux interventions ont la même priorité, conserver leur ordre d'origine.

    Suggestion :
    - Implémenter un tri à bulles ou un tri par insertion.

    Args:
        liste_interventions (list): liste de dicts

    Returns:
        list: nouvelle liste triée (idéalement, ne pas modifier l'original)
    """

    interventions = liste_interventions[:]
def trier_interventions(liste_interventions):

    interventions = liste_interventions[:]
 
    n = len(interventions)
    for i in range(n - 1):
        echange = False
        for j in range(0, n - 1 - i):
            score_j = calculer_priorite(interventions[j])
            score_next = calculer_priorite(interventions[j + 1])
            if score_j < score_next:
                interventions[j], interventions[j + 1] = interventions[j + 1], interventions[j]
                echange = True

        if not echange:
            break

    return interventions
    





def estimer_temps_interventions(liste_triee):
    """
    Estime le temps total et moyen pour traiter les interventions.

    Hypothèse :
    - Chaque unité de 'duree' correspond à 4 minutes.

    Args:
        liste_triee (list)

    Returns:
        dict: {
            'temps_total': int,
            'temps_moyen': float
        }
    """
    temps_stats = {
        'temps_total': 0,
        'temps_moyen': 0
    }
def trier_interventions(liste_triee):
    result = 0
    temps_stats = {}

    for single_interv in liste_triee:
     result += single_interv.get("duree", 0) * 4

    temps_stats["temps_total"] = result

    if len(liste_triee) == 0:
     temps_stats["temps_moyen"] = 0
    else:
     temps_stats["temps_moyen"] = result / len(liste_triee)
    return temps_stats


def identifier_interventions_urgentes(liste, seuil=30):
    """
    Identifie les interventions dont l'urgence dépasse un seuil.

    Règle :
    - Une intervention est urgente si intervention['urgence'] > seuil
    - Si 'urgence' est manquant, considérer 0.

    Args:
        liste (list): liste d'interventions
        seuil (int)

    Returns:
        list: liste des identifiants 'id' urgents
    """
    urgentes = []
    for elem in liste:
     if elem["urgence"]>seuil:
        urgentes.append((list(elem.items()))[0])
     if (list(elem.keys()))[0] not in elem:
      continue
    return urgentes
# -------------------------------------------------------------------
# TESTS main
# -------------------------------------------------------------------


if __name__ == "__main__":
   interventions_test = [
         {'id': 1, 'urgence': 10, 'duree': 3, 'critique': False},
        {'id': 2, 'urgence': 25, 'duree': 2, 'critique': True},
      {'id': 3, 'urgence': 5,  'duree': 5, 'critique': False},
         {'id': 4, 'urgence': 35, 'duree': 1, 'critique': False},
       {'id': 5, 'urgence': 15, 'duree': 4, 'critique': True},
   ]

print("Priorités :")
for itv in interventions_test:
       print(itv['id'], calculer_priorite(itv))

tri = trier_interventions(interventions_test)
print("\nTri (ids) :", [x.get('id') for x in tri])

temps = estimer_temps_interventions(tri)
print("\nTemps :", temps)

urg = identifier_interventions_urgentes(interventions_test, seuil=30)
print("\nUrgentes :", urg)

