# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 22:14:43 2020

@author: julie
"""
import time

pion_rouge="R"  # IA
pion_jaune ="J"
poids = []
poids.append([3,4,5,7,7,7,7,7,7,5,4,3])
poids.append([4,6,8,10,10,10,10,10,10,8,6,4])
poids.append([5,8,11,13,13,13,13,13,13,11,8,5])
poids.append([5,8,11,13,13,13,13,13,13,11,8,5])
poids.append([4,6,8,10,10,10,10,10,10,8,6,4])
poids.append([3,4,5,7,7,7,7,7,7,5,4,3])  

# Teste si s est terminal(fin de jeu)
# C'est à dire dans l'hypothèse où tous les pions ont été utilisés (42) 
# ou si un des deux joueurs a aligné 4 jetons
def Terminal_Test(s):
    jeu_termine = False
    cpt=0
    for i in range(5,-1,-1):
        if(jeu_termine) : break
        for j in range(12):
            if(s[i][j]!='_'):
                cpt+=1
            if(cpt==42):
                jeu_termine=True
                break      # on sort de la double boucle, inutile de continuer
                
    
    if(jeu_termine==False):
        jeu_termine = AGagne_Joueur(s,pion_rouge)
        if(jeu_termine==False):
            jeu_termine=AGagne_Joueur(s,pion_jaune)
    return jeu_termine
    

def AGagne_Joueur(s,pion_joueur):
    joueur_gagne = False
    # Test sur les lignes
    for ligne in range(5,-1,-1):  # parcours des lignes de bas en haut
        cpt=0
        if (joueur_gagne): break
        for colonne in range(12):   
            if(s[ligne][colonne]==pion_joueur):
                cpt+=1
                if(cpt==4):
                    joueur_gagne=True  
                    break    # on sort de la double boucle, inutile de continuer
            else:
                cpt=0
    if(joueur_gagne==False):  # Test sur les colonnes
        for colonne in range(12):
            cpt=0
            if (joueur_gagne): break
            for ligne in range(5,-1,-1):
                if(s[ligne][colonne]==pion_joueur):
                    cpt+=1
                    if(cpt==4):
                        joueur_gagne=True
                        break 
                else:
                    cpt=0
    
    if(joueur_gagne==False): # Test sur les diagonales
        for ligne in range(5,-1,-1):
            if(joueur_gagne==True):
                break
            for colonne in range(12):
                if(s[ligne][colonne]==pion_joueur):
                    cpt=1
                    for i in range(1,4): # diagonale de gauche
                        if(ligne-i<0 or colonne-i<0): # on sort des limites de la grille
                            break
                        if(s[ligne-i][colonne-i]==pion_joueur):
                            cpt+=1
                        else:
                            break
                    if(cpt==4): 
                        joueur_gagne = True
                        break
                    else:
                        cpt=1
                        for j in range(1,4):  # diagonale de droite
                            if(ligne-j<0 or colonne+j>=12): # on sort des limites de la grille
                                break
                            if(s[ligne-j][colonne+j]==pion_joueur):
                                cpt+=1
                            else:
                                break
                        if(cpt==4): 
                            joueur_gagne = True
                            break  
    return joueur_gagne

# Attribue une valeur à l’´etat s (-1,0 ou 1) + valeur de l'heuristique
def Utility(s,pion_jmax):         #dépend de joueur max
    rep=0
    pion_adverse = pion_jaune if pion_jmax==pion_rouge else pion_rouge
    if(AGagne_Joueur(s,pion_jmax)):
        rep=1 + Heuristique(s,pion_jmax,poids) #252  # max de l'heuristique est de 250  modif ici
    elif (AGagne_Joueur(s,pion_adverse)):
        rep=-1 - Heuristique(s,pion_adverse,poids)   #-251  modif ici
    return rep

# Retourne la liste représentant les cases vides <=> les actions possibles
def Actions(s):
    actions=[]
    for colonne in range(12):
        ligne = GraviteLigne(s,colonne)
        if(ligne>-1):
            actions.append([ligne,colonne])
    return actions

# Applique l’action a dans l’´etat s
def Result(s,a):
    ligne=a[0]
    colonne= a[1]
    rep=CopierGrille(s)
    rep[ligne][colonne]=a[2]
    return rep

# Permet de créer une copie temporaire de la grille de jeu afin de ne pas 
# modifier la grille principale en manipulant la copie
def CopierGrille(grille):
    copie = []
    for i in range(len(grille)):
        copie.append(grille[i].copy())
    return copie

def GraviteLigne(s,colonne):
    ligne_case = -1
    if(colonne>=0 and colonne <12):
        for ligne in range(5,-1,-1):
            if(s[ligne][colonne]=='_'):  #case vide
                ligne_case=ligne
                break
    return ligne_case

# Determine si la colonne passée en paramètres possède une case libre dans la grille de jeu
def CaseLibre(s,colonne):
    libre=False
    if(GraviteLigne(s,colonne)>-1):
        libre =True
    return libre

# Affiche la grille de jeu
def AfficherGrille(grille):
    print(' ------------------------------------------------------------')
    for i in range(len(grille)):
        print('| ',end='')
        for j in range(len(grille[0])):
            if(grille[i][j]=='R'):
                print('\033[41m' + grille[i][j], '\033[0m'+ ' | ',end='')
            elif(grille[i][j]== 'J'):
                print('\033[44m' + grille[i][j], '\033[0m'+ ' | ',end='')
            else:
                print(grille[i][j], ' | ',end='')
                
        print('\n|    |    |    |    |    |    |    |    |    |    |    |    |')
        print(' ------------------------------------------------------------')
    print('|  1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9 | 10 | 11 | 12 |')

# Détermine si une grille est vide
def GrilleVide(grille):
    vide=True
    for i in range(12):
        if(grille[5][i]!='_'):
            vide=False
    return vide

####### Fonctions Algorithme Minimax avec élagage Alpha Beta
def Max_Value_alpha(s,player,jmax,alpha,beta,profondeur,poids):
    v=0
    if Terminal_Test(s) or profondeur==0: 
        v=Utility(s,jmax)
    else:
        other_player = pion_jaune if(player==pion_rouge) else pion_rouge
        v=-10000000
        actions= Actions(s)
        for a in actions:
            act=a.copy()
            act.append(other_player)
            v=max(v,Min_Value_alpha(Result(s,act),other_player,jmax,alpha,beta,profondeur-1,poids)+ Heuristique(Result(s,act),jmax,poids))
            alpha=max(alpha,v)
            if(beta<=alpha):
                return v
    return v

def Min_Value_alpha(s,player,jmax,alpha,beta,profondeur,poids):
    v=0
    if Terminal_Test(s) or profondeur==0: 
        v=Utility(s,jmax)
    else:
        other_player = pion_jaune if(player==pion_rouge) else pion_rouge
        v=10000000
        actions= Actions(s)
        for a in actions:
            act=a.copy()
            act.append(other_player)
            v=min(v,Max_Value_alpha(Result(s,act),other_player,jmax,alpha,beta,profondeur-1,poids)- Heuristique(Result(s,act),other_player,poids))  
            beta=min(beta,v)
            if(beta<=alpha):
                return v
    return v

def Alpha_Beta_Search(s,player,jmax,profondeur,poids):
    if Terminal_Test(s):
        return Utility(s,jmax) 
    if GrilleVide(s):
        return [5,5]        # si la grille est vide, alors on place le pion au centre de la grille
    
    indices=[]
    actions = Actions(s)
    if(actions!=[]):
        maxa = -1000
        for a in actions:
            act=a.copy()
            act.append(player)
            alpha=-1000
            beta=1000
            vp = Min_Value_alpha(Result(s,act),player,jmax,alpha,beta,profondeur,poids)
            if(vp>maxa): 
                maxa=vp
                indices=[a[0],a[1]]
        return indices
    else:
        return indices

def MatPoids():
    poids = []
    poids.append([3,4,5,7,7,7,7,7,7,5,4,3])
    poids.append([4,6,8,10,10,10,10,10,10,8,6,4])
    poids.append([5,8,11,13,13,13,13,13,13,11,8,5])
    poids.append([5,8,11,13,13,13,13,13,13,11,8,5])
    poids.append([4,6,8,10,10,10,10,10,10,8,6,4])
    poids.append([3,4,5,7,7,7,7,7,7,5,4,3])  
    return poids

def Heuristique(s,pion_jmax,poids):
    cpt = 0
    for ligne in range(6):
        for colonne in range(12):
            if(s[ligne][colonne]==pion_jmax):
                cpt+= poids[ligne][colonne]
    return cpt


     
def Jeu():
    
    
    s=[['_','_','_','_','_','_','_','_','_','_','_','_'],
       ['_','_','_','_','_','_','_','_','_','_','_','_'],
       ['_','_','_','_','_','_','_','_','_','_','_','_'],
       ['_','_','_','_','_','_','_','_','_','_','_','_'],
       ['_','_','_','_','_','_','_','_','_','_','_','_'],
       ['_','_','_','_','_','_','_','_','_','_','_','_']]
    
    
    poids = MatPoids()
    case=['non vide']
    jmax=pion_rouge  # IA 
    jmin=pion_jaune  # Humain
    profondeur = 4
    AfficherGrille(s)
    player=(input('Qui commence ? : tapez R(IA) ou J = >  ')).upper()
    while(case!=[]):
        if(type(case) is int or Terminal_Test(s)):
            print('Jeu terminé')
            res=Utility(s,jmax)
            print(res)
            if(res>=1):
                print('Le joueur ',jmax,' a gagné !!')
            elif(res<=-1):
                print('Le joueur ',jmin,' a gagné !! ')
            else:
                print('Egalité !! ')
            case=[]
        else :
            if(player!=jmax):
                print('Dans quelle case souhaitez vous placer votre pion ?')
                libre=False
                while(libre==False):
                    colonne=int(input('indice de la colonne (entre 1 et 12) =>   '))-1
                    libre=CaseLibre(s,colonne)

                ligne=GraviteLigne(s,colonne)
                case=[ligne,colonne,jmin]
                if(case!=[]):
                    s=Result(s,case)
                player=jmax
                
            else:
                debut=time.perf_counter()
                #print('ok')
                case=Alpha_Beta_Search(s,jmax,jmax,profondeur,poids)    # minimax avec élagage alpha beta
                #print('ok2')
                fin=time.perf_counter() 
                print(fin-debut,' sc')
                if(case!=[]):
                    action=case.copy()
                    action.append(jmax)
                    s=Result(s,action)
                    
                player=jmin
            AfficherGrille(s)
            print("\nLe joueur a joué en : ",case[1]+1)

    print(Terminal_Test(s))
    AfficherGrille(s)


    
if __name__ == '__main__':
    Jeu()    
    #Essai()
