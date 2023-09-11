def cellule(tête, queue=None):
   """
   Construit une liste chaînée en rajoutant l'élément tête au
   *début* de la liste chaînée queue. La liste queue n'est pas
   modifiée par cette opération.

   Renvoie une cellule immuable.
   """

   return (tête, queue)

def cellule_variable(tête, queue):
   """
   Construit une liste ddchaînée en rajoutant l'élément tête au
   *début* de la liste chaînée queue. La liste queue n'est pas
   modifiée par cette opération.

   Renvoie une cellule variable.
   """

   return [tête, queue]

def change_tête(cellule, nouvelle_valeur):
   """
   Modifie la valeur de tête de la liste
   """
   
   cellule[0] = nouvelle_valeur

def change_queue(cellule, nouvelle_cellule):
   """
   Modifie la valeur de la queue de la liste: la cellule
   pointera sur une nouvelle cellule.
   """
   
   cellule[1] = nouvelle_cellule

def tête(liste):
   """
   Renvoie le premier élément de la liste chaînée passée en 
   paramètre.
   """

   return liste[0]

def queue(liste):
   """
   Renvoie la liste chaînée liste privée de son premier élément 
   (la liste passée en paramètre n'est cependant pas modifiée
   par cette opération).

   Déclenche une erreur si appelé sur une liste vide.
   """

   return liste[1]

def liste_vide():
   """
   Renvoie une liste chaînée vide.
   """

   return None

def est_vide(liste):
   """
   Teste si une liste chaînée est vide ou non.
   """

   return liste is None

def longueur(liste):
   """
   Retourne la longueur de la liste chaînée passée en paramètre.
   """

   if liste is None:
      return 0
   else:
      return 1 + longueur(queue(liste))

def concaténer(l1, l2):
   """
   Renvoie une nouvelle liste chaînée qui sera la concaténation
   de l1 et de l2.

   Les listes l1 et l2 ne sont pas modifiées par cette appel.
   """

   if est_vide(l1):
      return l2
   else:
      return cellule(tête(l1), concaténer(queue(l1), l2))
   
   
def affiche_liste_rec(liste):
   if not liste:
      return ""
   else:
      val = tête(liste)
      queue_list = affiche_liste_rec(queue(liste))
      return f"{val} {queue_list}"

def liste_chaînée(liste_python):
    if not liste_python:  # Si la liste est vide
        return liste_vide()  # Retourner une liste chaînée vide
    # Sinon on crée une cellule avec l'élément actuel et le reste de la liste
    return cellule(liste_python[0], liste_chaînée(liste_python[1:]))