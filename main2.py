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


def detection_inclusion(polygones, point, poly, nb_poly):
    """
    renvoie le polygone avec la plus petite aire dans lequel le polynome actuel (celui du point)
    est inclus
    """
    index_poly = -1
    inclus_dans = [] # contient le plus petit polygone dans lequel le polynome actuel (celui du point_de_depart) est inclus
    for poly2 in polygones:
        index_poly += 1
        nb_intersect = 0
        if abs(poly2.area()) > abs(poly.area()): # on teste seulement les polygones avec une aire supérieure à celle de poly
            for segment in poly2.segments(): # on teste chaque segment de poly2
                point1 = Point(list(segment.endpoints[0].coordinates))
                point2 = Point(list(segment.endpoints[1].coordinates))
                x1 = point1.coordinates[0]
                y1 = point1.coordinates[1]
                x2 = point2.coordinates[0]
                y2 = point2.coordinates[1]
                x = point.coordinates[0]
                y = point.coordinates[1]
                if (y1 > y) != (y2 > y) and (x < (x2 - x1)*(y - y1)/(y2-y1) + x1):  # s'il y a une intersection
                    nb_intersect += 1
            if nb_intersect % 2 == 1 and len(inclus_dans) == 0: # si on est inclus dans rien pour le moment
                min_area = abs(poly2.area()) # l'aire minimale
                inclus_dans.append(index_poly)
            elif nb_intersect % 2 == 1 and abs(poly2.area()) < min_area: # si on est deja inclus dans un poly mais qu'on est inclus dans un autre avec une plus petite aire
                min_area = abs(poly2.area())
                inclus_dans[0] = index_poly
    if len(inclus_dans) == 0: # si on est inclus dans aucun polygone
        inclus_dans.append(-1)
    return inclus_dans[0]


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
        point_de_depart = Point(list(poly.points[0].coordinates)) # on prend le tout premier point qui compose poly (c'est arbitraire on aurait pu en prendre un autre)
        nb = detection_inclusion(polygones, point_de_depart, poly, nb_poly)
        table_des_inclusions.append(nb)
    return table_des_inclusions


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
