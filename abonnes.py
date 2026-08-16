#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LE NOMBRE D'ABONNÉS, RELEVÉ POUR DE VRAI.   python3 abonnes.py

Interroge l'API Instagram et réécrit donnees/instagram.json. Le générateur
lit ce fichier : le chiffre du site suit donc le compte, sans intervention.

DEUX VARIABLES D'ENVIRONNEMENT, ET RIEN D'AUTRE
  IG_TOKEN     le jeton d'accès longue durée
  IG_USER_ID   l'identifiant du compte professionnel Instagram

POURQUOI UN JETON — Instagram ne donne le nombre d'abonnés qu'au
propriétaire d'un compte professionnel. Il n'existe aucune source publique
stable : les services qui prétendent le contraire lisent la page en douce et
cassent à chaque changement de Meta. On ne bâtit pas là-dessus.

CE SCRIPT NE CASSE JAMAIS LE SITE. Sans jeton, ou si Meta répond de travers,
il sort en laissant le fichier intact et le site garde le dernier bon chiffre.
Un compteur figé est un défaut ; un site cassé en est un autre.
"""
import json, os, sys, pathlib, datetime
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

ICI = pathlib.Path(__file__).parent
CIBLE = ICI / "donnees" / "instagram.json"
API = "https://graph.facebook.com/v21.0"


def sortir(motif, code=0):
    """On sort en silence (code 0) quand le jeton manque : ce n'est pas une
    panne, c'est un site pas encore relié. Le code 1 est réservé aux vraies
    erreurs, pour que l'action GitHub les signale."""
    print(f"  abonnes : {motif}")
    sys.exit(code)


def main():
    jeton, uid = os.environ.get("IG_TOKEN"), os.environ.get("IG_USER_ID")
    if not jeton or not uid:
        sortir("pas de jeton (IG_TOKEN / IG_USER_ID) — fichier laissé tel quel")

    url = f"{API}/{uid}?fields=followers_count,username&access_token={jeton}"
    try:
        with urlopen(url, timeout=20) as r:
            rep = json.load(r)
    except HTTPError as e:
        corps = e.read().decode("utf-8", "replace")[:400]
        sortir(f"Meta a répondu {e.code} — {corps}", 1)
    except (URLError, ValueError) as e:
        sortir(f"appel impossible ({e}) — fichier laissé tel quel", 1)

    n = rep.get("followers_count")
    if not isinstance(n, int) or n <= 0:
        sortir(f"réponse inattendue : {rep}", 1)

    d = json.load(open(CIBLE, encoding="utf-8"))
    avant = d.get("abonnes")
    d["abonnes"] = n
    d["compte"] = rep.get("username", d.get("compte", ""))
    d["releve"] = datetime.date.today().isoformat()
    d["source"] = "api"
    json.dump(d, open(CIBLE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    ecart = "" if avant is None else f"  ({n - avant:+d})"
    print(f"  abonnes : {avant} -> {n}{ecart}  le {d['releve']}")


if __name__ == "__main__":
    main()
