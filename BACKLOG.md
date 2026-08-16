# Simon Vergély — backlog

Audit dans `AUDIT.md`. **Gate PO à la fin de chaque sprint.**

---

## La thèse

Il explose avec un style précis — **49 700 abonnés** — et il a des clients qui
impressionnent : **Ircam, Devialet, Snapchat**. Son site ne montre ni l'un ni
l'autre, et sa vidéo de présentation est cassée.

**Le site doit faire trois choses, dans cet ordre :**

1. **Montrer** le travail qui décolle, dès la première seconde
2. **Prouver** avec les logos, avant qu'on ait le temps de douter
3. **Qualifier** — transformer les messages privés en demandes qui portent un
   budget, un format et une date, pour qu'il arrête de négocier en DM

*Le site d'un motion designer a une particularité : le produit est le média.
Une page qui ne bouge pas est une contre-démonstration.*

---

## Sprint 0 — La direction · GATE PO AVANT TOUTE LIGNE

### S0.1 — Quelle marque porte le site
`[SIC] FILM` ou `Simon Vergely` ? La seconde a 49 700 abonnés et un nom qu'on
retient. La première a un logo d'avion en papier et une accroche de plaquette.

**Ma position** : le site s'appelle **Simon Vergély**, et [SIC] Film devient le
nom du studio pour les films de commande. On ne perd rien, on hiérarchise.
**Acceptation** : une seule marque en tête de page, l'autre en sous-titre ou nulle part.

### S0.2 — La grammaire visuelle
Son univers est le **grotesque coloré** : visages distordus, aplats saturés,
contours épais. C'est sa signature et personne d'autre ne l'a.

**La grammaire du site sort de son travail, pas d'une métaphore plaquée :**
- **l'aplat de couleur franche** porte les sections — chaque page a sa couleur, comme chaque animation
- **le contour épais** porte les cadres et les boutons
- **la déformation** porte les survols : au passage, un élément se tord légèrement
- **la boucle** porte la preuve : le bandeau de logos tourne sans fin, comme un GIF

**Acceptation** : rien de la grammaire d'Arsène, du Rio, de la boucherie, de
Donna Maria ni de l'EARL.

### S0.3 — La structure
Trois pages, pas plus. Un motion designer se juge en trente secondes.
**Accueil** (le travail + la preuve + l'appel) · **Le travail** (les films par
catégorie) · **Travailler ensemble** (formats, délais, comment ça se passe).

---

## Sprint 1 — Ce qui fait entrer

### S1.1 — Le showreel en ouverture — BLOQUANT
Son site actuel affiche « cette vidéo n'est pas disponible » à cet endroit exact.
**Acceptation** : la vidéo se lance, ou à défaut une animation en boucle tient la
place. Jamais un rectangle vide.

**Il faut le fichier.** Tant qu'on ne l'a pas, l'ouverture est portée par ses
images, pas par un lecteur mort.

### S1.2 — LE BANDEAU DE LOGOS QUI DÉFILE ✱ demandé par le PO
Les dix logos passent en boucle, en continu, haut de page.

- défilement **automatique et sans fin**, sans bouton, sans saccade
- **doublé dans le code** pour que la boucle soit invisible
- il **s'arrête au survol** : on doit pouvoir lire un logo qui intrigue
- **`prefers-reduced-motion` respecté** : il se fige en grille pour qui a désactivé
  les animations
- aucune variation de luminosité plein cadre — c'est une translation, pas un clignotement

**Acceptation** : les dix logos lisibles, la boucle sans rupture visible, et le
bandeau ne pousse jamais la page de côté.

⚠️ **Les fichiers de logos** sont sur son portfolio. À récupérer proprement, et
à faire confirmer qu'il a le droit de les afficher.

### S1.3 — L'accroche
Elle doit dire ce qu'il fait et pour qui, en une ligne. Sa bio le dit déjà mieux
que nous : **« Surreal animations & distorted worlds »**. À traduire sans l'affadir.

### S1.4 — La preuve chiffrée
**49 700 abonnés** est un chiffre qui se montre. Il est vérifiable, il est à lui,
et il vaut tous les adjectifs. À dater au relevé.

---

## Sprint 2 — Ce qui fait rester

### S2.1 — Le travail, montré et non raconté
Les quatre familles existent déjà : films de commande, projets personnels, gifs
animés, Mass Snaps. À reprendre — mais **en montrant d'abord le travail Instagram**,
celui qui décolle, pas seulement l'ancien travail éditorial.

### S2.2 — Une pièce détaillée
Un projet raconté de bout en bout : la commande, le parti pris, le résultat.
C'est ce qui fait passer d'« il dessine bien » à « il sait résoudre un problème ».
**Acceptation** : un client nommé, une contrainte nommée, un résultat montré.

### S2.3 — Le parcours, court
Autodidacte, arts appliqués, hip hop jazz new-yorkais des années 90, cinéma
d'auteur. Trois phrases, pas une page. **Le lecteur doit vouloir le travail avant
qu'on lui dise qui le fait.**

---

## Sprint 3 — Ce qui fait écrire

### S3.1 — La demande qualifiée
Le formulaire actuel demande nom, e-mail, message. C'est ce qui produit des
messages privés interminables.

Le nouveau demande **le format** (teaser, bande-annonce, publicité, logo animé),
**la date de livraison** et **l'ordre de budget**. Trois champs de plus, et une
conversation qui commence au bon endroit.

**Sans serveur si possible** : il a un mobile, **07 69 05 13 49**, donc le SMS et
WhatsApp sont ouverts — contrairement à tous les autres chantiers où le numéro
était un fixe.

### S3.2 — Les formats et les délais
Ce qui manque le plus pour vendre : combien de temps prend un logo animé, une
bande-annonce, une publicité. **Un ordre de grandeur suffit, mais il faut qu'il
existe.** À obtenir de lui.

### S3.3 — Le nom de domaine
`simonvergely.fr` est libre au 16/08/2026. À déposer **à son nom**, avec une
adresse e-mail derrière — ce qui remplacerait `sicfilmstudio@gmail.com`.

---

## Interdits sur ce chantier

- Aucun client, aucun chiffre, aucun tarif inventé. Les dix logos sont les siens,
  les 49 700 abonnés sont datés.
- Aucune image floue en pleine largeur. **Leçon d'Arsène** : une vignette
  ré-agrandie sur toute la largeur d'un écran est pire que pas d'image.
- Aucune dépendance à un CDN. Polices embarquées.
- Tout ce qui a une date se calcule. **Leçon d'Arsène** aussi.
- Rien de la grammaire des cinq autres sites.
