#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fichier principal pour la detection des inclusions.
ce fichier est utilise pour les tests automatiques.
attention donc lors des modifications.
"""
import sys
from tycat import read_instance
from collections import defaultdict

from math import cos, sin, pi
from itertools import islice, cycle

from geo.point import Point
from geo.tycat import tycat
from geo.segment import Segment
from geo.polygon import Polygon
from geo.quadrant import Quadrant


def detection_inclusion(polygones, point, nb_poly):
    """
    renvoie tous les polygones dans lequel le polynome actuel (celui du segment)
    est inclus
    """
    index_poly = -1
    inclus_dans = [] # contient les polynomes dans lequel le polynome actuel (celui du segment) est inclus
    t = [-1 for _ in range(len(polygones))] # contient le nombre d'intersections de chaque polynome avec le segment en question
    for poly in polygones:
        index_poly += 1
        for segment in poly.segments():
            point1 = Point(list(segment.endpoints[0].coordinates))
            point2 = Point(list(segment.endpoints[1].coordinates))
            x1 = point1.coordinates[0]
            y1 = point1.coordinates[1]
            x2 = point2.coordinates[0]
            y2 = point2.coordinates[1]
            x = point.coordinates[0]
            y = point.coordinates[1]
            if (y1 > y) != (y2 > y) and (x < (x2 - x1)*(y - y1)/(y2-y1) + x1):  # s'il y a une intersection
                t[index_poly] += 1
    for j in range(len(t)):
        if t[j] % 2 == 0 and j != nb_poly: #le point est dedans et on verifie que chaque poly n'est pas inclus dans lui même
            inclus_dans.append(j)
    if len(inclus_dans) == 0:  # la liste est vide => c'est inclus dans rien
        inclus_dans.append(-1)
    return inclus_dans


def trouver_petit_polygone(tableau, indice, table, tableau_final):
    """
    fonction complexe à expliquer
    mais elle participe au tri
    (je l'ai testé sur des exemples et elle devrait fonctionner :/ )
    """
    if len(tableau) == 2:
        for i in tableau:
            if table[i][0] != -1:
                petit_polygone = i
                tableau_final[indice] = petit_polygone
    else:
        for j in tableau:
            if len(table[j]) == len(tableau) - 1:
                petit_polygone = j
                tableau_final[indice] = petit_polygone


def tri_inclusion(table):
    """
    un polygone peut etre inclus dans plusieurs
    polygone à la fois. Donc on trie pour garder
    le plus petit polynome dans lequel il est inclus
    """
    tableau_final = [-1 for _ in range(len(table))]
    for i in range(len(table)):
        if len(table[i]) > 1:
            possibilites = table[i] # tableau de longueur > 1 avec tous les polgones où on est inclus
            trouver_petit_polygone(possibilites, i, table, tableau_final)
        else:
            petit_polygone = table[i][0]
            tableau_final[i] = petit_polygone
    return tableau_final


def trouve_inclusions(polygones):
    """
    renvoie le vecteur des inclusions
    la ieme case contient l'indice du polygone
    contenant le ieme polygone (-1 si aucun).
    (voir le sujet pour plus d'info)
    """
    nb_poly = -1 # numéro du polygone dont on s'occupe
    table_des_inclusions = [] # table contenant toutes les inclusions
    for poly in polygones:
        nb_poly += 1
        point_de_depart = Point(list(poly.points[0].coordinates)) # ou sinon: Point(list(poly.points[0].coordinates)) ou poly.points[0]
        tab = detection_inclusion(polygones, point_de_depart, nb_poly)
        table_des_inclusions.append(tab)
    table_triee = tri_inclusion(table_des_inclusions)
    return table_triee


def main():
    """
    charge chaque fichier .poly donne
    trouve les inclusions
    affiche l'arbre en format texte
    """
    for fichier in sys.argv[1:]:
        polygones = read_instance(fichier)
        inclusions = trouve_inclusions(polygones)
        print(inclusions)

if __name__ == "__main__":
    main()
