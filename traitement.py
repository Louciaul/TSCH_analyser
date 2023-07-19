from parse_log import *
import os
from statistics import *


# renvoie un tableau de tuple
#  avec pour chaque entrée (nbr nodes départ(sender), nbr nodes défaillant,moy PDR,med PDR,data_ch {})

#group ne peut prendre que les valeurs star,line,scaling
def traitement_packet(group):
    chemin_du_dossier = "all_data/" + group

    tab_result = []

    liste_fichier = os.listdir(chemin_du_dossier + "/")
    liste_fichier.sort()

    for nom_fichier in liste_fichier:
        if not nom_fichier.endswith(".log"):
            continue

        # un dictionnaire des messages par nodes, un dictionnaire des channels
        result_log = parse_log(
            chemin_du_dossier + "/" + os.path.splitext(nom_fichier)[0]
        )

        tab_result_PDR = []  # tab contenant tous les PDR d'une expérience

        for data in result_log[0].values():
            if(data[2] == 0):
                continue
            taux_reussite = float(data[1]) / float(data[2])  # PDR d'un node
            if(taux_reussite < 0.05):
                continue
            if(taux_reussite > 1):
                continue
            tab_result_PDR.append(taux_reussite)

        starter = len(result_log[0])
        survivor = len(tab_result_PDR)
        if len(tab_result_PDR) == 0:
            continue
        tab_result.append(
            (starter,survivor,round(mean(tab_result_PDR),2), round(median(tab_result_PDR),2), result_log[1])
        )
    return tab_result


def fusion_channel(tab):
    fusion_chan = {}

    for line in tab:
        dict = line[4]
        for element in dict:
            if fusion_chan.get(element) is None:
                fusion_chan[element] = dict[element]
            else:
                fusion_chan[element] += dict[element]
    return fusion_chan


#fonction qui analyse le RDP en fonction de la distance
#traite seulement le dossier distance
#renvoie un tableau de tuple (distance_au_coord,PDR)
def analyze_dist():
    chemin_du_dossier = "all_data/distance"

    tab_result = [] #un tableau de tuple (distance,RDP)

    liste_fichier = os.listdir(chemin_du_dossier + "/")
    liste_fichier.sort()

    for nom_fichier in liste_fichier:
        if not nom_fichier.endswith(".log"):
            continue
        # un dictionnaire des messages par nodes, un dictionnaire des channels
        result_log = parse_log(
            chemin_du_dossier + "/" + os.path.splitext(nom_fichier)[0]
        )

        for data in result_log[0].values():
            if(data[2] == 0):
                continue
            taux_reussite = float(data[1]) / float(data[2])  # PDR d'un node
            if(taux_reussite < 0.70):
                continue
            if(taux_reussite > 1):
                continue
            tab_result.append(
                (data[0],taux_reussite)
            )


    dic = {}

    for element in tab_result:
        if dic.get(element[0]) is None:
            dic[element[0]] = [1,element[1]]
        else:
            valeur = dic.get(element[0])
            #On moyenne nous même/concatène [nbr_element,somme des valeurs]
            dic[element[0]] = [valeur[0]+1,valeur[1]+element[1]]

    tab_result_dist = []

    for element in dic:
        valeur = dic.get(element)
        tab_result_dist.append((element,round(valeur[1]/valeur[0],2)))


    return tab_result_dist

#moyenne les résultats des expériences de scaling
#on aggrège les lignes qui ont le même nombre de nodes
#renvoie un tableau de tuple (nbr nodes,moyenne PDR, median PDR)
def unique_scaling():
    result = traitement_packet("scaling")

    dic = {}

    for element in result:
        #je veux faire un peu de tri
        if (element[0] < 2 or element[0] > 5):
            if dic.get(element[0]) is None:
                dic[element[0]] = [1,element[2],element[3]]
            else:
                valeur = dic.get(element[0])
                dic[element[0]] = [valeur[0] + 1,valeur[1] + element[3],valeur[2] + element[3]]
    
    tab_result = []

    for element in dic:
        valeur = dic.get(element)
        tab_result.append((element,round(valeur[1]/valeur[0],2),round(valeur[2]/valeur[0],2)))

    return tab_result

#pareil on veut tout aggréger (only line or star data)
#return tuple (mean PDR, median PDR)
def unique_line_or_star(result):

    sum_mean = 0
    sum_median = 0

    for element in result:
        sum_mean = sum_mean + element[2]
        sum_median = sum_median + element[3]
    
    return (round(sum_mean/len(result),2),round(sum_median/len(result),2))