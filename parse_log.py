import re
from parse_node import *

#à besoin d'un dictionnaire contenant les nodes présent (pour éviter les interférences)
#complète le dictionnaire

def parse_log(fichier):

    dic = set_list_node(fichier)

    fichier_log = fichier + ".log"

    chan= {}
    pattern = r"ch (\d+).*?(uc|bc).*(tx|rx) LL-(\w+)->"

    with open(fichier_log, 'r') as FILE:
        for ligne in FILE:
            if "TSCH-LOG" in ligne and "seq" in ligne:

                matches = re.search(pattern,ligne)

                if matches:

                    channel = matches.group(1)
                    uc = matches.group(2)
                    tx = matches.group(3)
                    id = matches.group(4)
                    
                    if not uc == "uc":
                        continue

                    uid = dic.get(id)
                    if uid is None:
                        continue
                    else:
                        if tx == "tx":
                            dic[id] = [uid[0],uid[1],uid[2]+1]
                        elif tx == "rx":
                            dic[id] = [uid[0],uid[1]+1,uid[2]]
                        else:
                            continue
                        check = chan.get(channel)
                        if check is None:
                            chan[channel] = 1
                        else:
                            chan[channel] = check + 1
    return (dic,chan)
