import json
import os
import re
from math import *

# renvoie un dictionnaire
# "uid":[distance,nbr_message_reçus,nbr_messages_envoyés]


def set_list_node(fichier):
    # lit un fichier json et donne une liste avec
    # les uid des noeuds utilisés. le premier étant toujours le coordinateur

    uid_coord = search_coordinator(fichier)
    fichier_json = fichier + ".json"

    with open(fichier_json, "r") as FILE:
        data = json.load(FILE)

    dic = {}
    #coordonnées du coordinateur
    for item in data["items"]:
        node_id = item["uid"]
        if node_id == uid_coord:
            x_cor = float(item["x"])
            y_cor = float(item["y"])
            z_cor = float(item["z"])

    for item in data["items"]:
        node_id = item["uid"]
        if node_id == uid_coord:
            continue

        distance = calcul_distance(
            x_cor, y_cor, z_cor, float(item["x"]), float(item["y"]), float(item["z"])
        )

        to_add = [round(distance, 2), 0, 0]

        dic[node_id] = to_add

    return dic

#renvoie la distance entre 2 nodes
def calcul_distance(x_cor, y_cor, z_cor, x_snd, y_snd, z_snd):
    d = sqrt((x_cor - x_snd) ** 2 + (y_cor - y_snd) ** 2 + (z_cor - z_snd) ** 2)
    return d


#renvoie l'uid du coordinateur pour l'exclure
def search_coordinator(fichier):

    fichier_data = fichier + ".data"

    with open(fichier_data, "r") as FILE:
        data = json.load(FILE)

    num_coordinator = -1

    firmwareassociation = data["firmwareassociations"]
    for firmwares in firmwareassociation:
        if firmwares["firmwarename"].find("coordinator") != -1:
            coordinator = firmwares["nodes"][0][3:6]
            if not coordinator[-2].isdigit():
                # print(coordinator[0:1])
                num_coordinator = coordinator[0:1]
            elif not coordinator[-1].isdigit():
                # print(coordinator[0:2])
                num_coordinator = coordinator[0:2]
            else:
                # print(coordinator)
                num_coordinator = coordinator

    FILE.close()

    pattern = r"m3-(\d+)."

    fichier_json = fichier + ".json"
    with open(fichier_json) as FILE:
        data = json.load(FILE)
        for item in data["items"]:
            matches = re.search(pattern, item["network_address"])
            if matches.group(1) == num_coordinator:
                
                return item["uid"]
        return None


def list_position(fichier):
    # lit un fichier json et renvoie la liste des coordonnées

    uid_coord = search_coordinator(fichier)
    fichier_json = fichier + ".json"

    with open(fichier_json, "r") as FILE:
        data = json.load(FILE)

    pos = []
    #coordonnées du coordinateur
    for item in data["items"]:
        node_id = item["uid"]
        if node_id == uid_coord:
            x_cor = float(item["x"])
            y_cor = float(item["y"])
            z_cor = float(item["z"])

    #en première position
    pos.append((x_cor,y_cor,z_cor))

    for item in data["items"]:
        node_id = item["uid"]
        if node_id != uid_coord:
            x_cor = float(item["x"])
            y_cor = float(item["y"])
            z_cor = float(item["z"])
            pos.append((x_cor,y_cor,z_cor))

    return pos