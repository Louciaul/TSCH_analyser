from traitement import *
from parse_node import *
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


# trace tous les graphes et les place dans le dossier Graph
def main():
    distance = analyze_dist()
    star = traitement_packet("star")
    line = traitement_packet("line")
    scaling = traitement_packet("scaling")

    graph_dist(distance)
    graph_scaling(unique_scaling())
    graph_line_vs_star(star,line)

    graph_position("all_data/star/star_369053","star")
    graph_position("all_data/line/line_369057","line")

    channel_repartition(line)

    message_over_nodes(scaling)
    lost_nodes(scaling)


# trace le graph distance
def graph_dist(distance):
    x = []
    y = []  # moyenne
    for element in distance:
        x.append(element[0])
        y.append(element[1])

    plt.scatter(x, y)

    plt.ylim(0, 1.1)

    plt.title("PDR moyen en fonction de la distance en m")

    plt.xlabel("distance")
    plt.ylabel("PDR")

    plt.savefig("Graph/distance.png")
    plt.close()

def channel_repartition(tab):
    fusion_chan = fusion_channel(tab)
    nb_messages = sum(fusion_chan.values())
    plt.pie(fusion_chan.values(), labels=fusion_chan.keys(), autopct="%1.1f%%")
    plt.title("Répartition dans les canaux de " + str(nb_messages) + " messages")
    plt.savefig("Graph/channel_repartition.png") 
    plt.close()


def message_over_nodes(tab):
    tab_exp = []
    nb_messages = []
    for i in range(len(tab)):
        if i > 0 and tab[i][0] == tab[i - 1][0]:
            continue
        tab_exp.append(tab[i][0])
        if i + 1 < len(tab) and tab[i][0] == tab[i + 1][0]:
            nb_messages.append(
                (sum(tab[i][4].values()) + sum(tab[i + 1][4].values())) / 2
            )
        else:
            nb_messages.append(sum(tab[i][4].values()))

    plt.scatter(tab_exp, nb_messages, marker="x")
    plt.title("Nombre de messages sur le nombre de noeuds")
    plt.xlabel("Nombre de noeuds")
    plt.ylabel("Nombre de messages")
    plt.grid(True)
    plt.savefig("Graph/messages_over_nodes.png")    
    plt.close()


def lost_nodes(tab):
    # print(tab)
    total = []
    reals = []
    for i in range(len(tab)):
        if i > 0 and tab[i][0] == tab[i - 1][0]:
            continue
        total.append(tab[i][0])
        if i + 1 < len(tab) and tab[i][0] == tab[i + 1][0]:
            reals.append((tab[i][1] + tab[i + 1][1]) / 2)
        else:
            reals.append(tab[i][1])

    plt.scatter(
        total,
        total,
        marker="x",
    )
    plt.scatter(total, reals, marker="x")
    plt.title("Nombre de noeuds perdus comparé au nombre de noeuds")
    plt.legend(["Avant panne", "Après panne"])
    plt.xlabel("Nombre de noeuds")
    plt.ylabel("Nombre de noeuds")
    plt.grid(True)
    plt.savefig("Graph/lost_nodes.png")
    plt.close()


def graph_scaling(scaling):
    x = []
    y = []  # moyenne
    z = []  # median

    for element in scaling:
        x.append(element[0])
        y.append(element[1])
        z.append(element[2])

    plt.scatter(x, y, label="moyenne", color="blue")
    plt.scatter(x, z, label="mediane", color="red")

    plt.ylim(0, 1.1)

    plt.title("PDR moyen et median en fonction du nombre de nodes")

    plt.xlabel("nombre de nodes")
    plt.ylabel("PDR")

    legend_labels = ["Médiane", "Moyenne"]
    legend_colors = ["red", "blue"]
    custom_legend = [
        plt.Line2D([], [], color=color, marker="o", linestyle="None")
        for color in legend_colors
    ]
    plt.legend(custom_legend, legend_labels)

    plt.savefig("Graph/scaling.png")

    plt.close()

#show data of graph line and star
def graph_line_vs_star(star,line):
    
    star = unique_line_or_star(star)
    line = unique_line_or_star(line)

    print("Star value: Mean PDR, Median PDR")
    print(star)
    print("Line value: Mean PDR, Median PDR")
    print(line)

def graph_position(fichier,name):
    pos = list_position(fichier)

    x = []
    y = []
    z = []

    #we don't want coordinator
    start = True
    for element in pos:
        if start:
            start = False
        else:
            x.append(element[0])
            y.append(element[1])
            z.append(element[2])

    # Créer une nouvelle figure 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Afficher les points dans l'espace 3D
    ax.scatter(x, y, z, c='r', marker='o')
    ax.scatter(pos[0][0], pos[0][1], pos[0][2], c='b', marker='o')

    # Ajouter des étiquettes aux axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    legend_labels = ['Sender', 'Coordinator']
    legend_colors = ['red', 'blue']
    custom_legend = [plt.Line2D([], [], color=color, marker='o', linestyle='None') for color in legend_colors]
    plt.legend(custom_legend, legend_labels)

    # Enregistrer la figure au format PNG
    fig.savefig("Graph/Position" + name + ".png")

    # Afficher la figure
    plt.close()


main()
