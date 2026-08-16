# Le site de Simon — mode d'emploi

Deux lecteurs, deux parties. La première est pour Simon : elle ne parle
que de son navigateur. La seconde est pour toi : elle branche la machine.

---

# Pour Simon

## Modifier votre site

Allez sur **`votre-site.com/admin`**, connectez-vous avec votre adresse mail.
Vous verrez six rubriques :

| Rubrique | Ce que vous y changez |
|---|---|
| **Mes coordonnées** | Adresse mail, téléphone, compte Instagram |
| **Mes travaux** | Les huit films, les mondes déformés, leurs légendes |
| **Mes reels** | Les vidéos qui jouent sur la page d'accueil |
| **Mes clients** | Les logos qui défilent en bandeau |
| **Mon histoire** | La page « Travailler ensemble » |
| **Nombre d'abonnés** | Le compteur, tant qu'il n'est pas automatique |

Vous modifiez, vous cliquez sur **Enregistrer**, puis sur **Publier**.
Le site se refait tout seul en une minute environ.

**Chaque texte a une version française et une version anglaise**, côte à côte
dans le même formulaire. Si vous laissez l'anglais vide, le site affiche le
français à la place — il ne reste jamais un trou.

## Ajouter un reel

1. Ouvrez la publication sur Instagram, appuyez sur **Partager → Copier le lien**.
2. Dans le lien `instagram.com/reel/DbIySQNChyT/`, le code est **`DbIySQNChyT`**.
3. Dans **Mes reels**, ajoutez une ligne, collez le code, écrivez ce qu'on voit.

Si un monde déformé a un reel, il s'affiche en vidéo et disparaît
automatiquement de la grille d'images : il n'est jamais montré deux fois.

## Ce que vous ne pouvez pas changer

Les couleurs, les polices, la mise en page. Ce n'est pas un oubli : c'est ce
qui garantit que le site reste net quoi qu'il arrive. Pour ça, passez par
Matisse.

---

# Pour Matisse — brancher la machine

Rien de ce qui suit ne demande d'écrire du code. Tout se fait dans un
navigateur, et l'ordre compte.

## 1. Le dépôt

Le projet est un dépôt Git. Il faut le pousser sur GitHub, en **privé** :
les visuels de Simon y sont, et le site n'est pas encore public.

## 2. Netlify construit le site

Dans Netlify : **Add new site → Import an existing project**, choisir le
dépôt. `netlify.toml` donne déjà la commande (`python3 construire.py`) et le
dossier (`site`) — il n'y a rien à saisir.

> **Le site actuellement en ligne a été déposé à la main.** Tant qu'il l'est,
> les publications de Simon n'apparaîtront nulle part. C'est cette étape qui
> relie l'interface au site réel, et elle n'est pas optionnelle.

## 3. DecapBridge ouvre la porte

Netlify Identity a été déprécié en février 2025 et Git Gateway l'est aussi :
sans remplaçant, Decap obligerait Simon à créer un compte GitHub.

Sur [decapbridge.com](https://decapbridge.com) : créer un site, récupérer son
identifiant, puis dans `site/admin/config.yml` remplacer

- `__DEPOT__` par `<compte>/<dépôt>`
- `__SITE_DECAPBRIDGE__` par l'identifiant

Enfin, inviter Simon par mail depuis DecapBridge.

**Tant que ces deux valeurs sont en gabarit, `/admin` refuse de démarrer et
affiche la marche à suivre.** Elle ne montre pas un écran de connexion qui
échouerait sans rien expliquer.

Gratuit jusqu'à 3 sites et 10 collaborateurs. Au-delà : 9 $/mois, ou 199 $
une fois avec le droit de l'héberger soi-même — c'est la brique de connexion
d'une future interface maison, sans avoir à l'écrire.

## 4. Le compteur d'abonnés, pour de vrai

Aujourd'hui le nombre vient de `donnees/instagram.json`, relevé à la main et
affiché avec sa date. L'animation le compte, elle ne l'invente pas.

Pour qu'il suive le compte tout seul, **trois choses, toutes chez Simon** :

1. son compte Instagram en **compte professionnel** — gratuit, réversible,
   son profil ne change pas ;
2. ce compte **relié à une page Facebook**, même vide ;
3. un **jeton d'accès longue durée**.

Puis, dans les secrets du dépôt GitHub (`Settings → Secrets → Actions`) :

| Secret | Valeur |
|---|---|
| `IG_TOKEN` | le jeton longue durée |
| `IG_USER_ID` | l'identifiant du compte professionnel |

L'action `.github/workflows/abonnes.yml` tourne alors quatre fois par jour :
elle relève le nombre, reconstruit le site et publie **seulement si le
chiffre a bougé**. Si Simon passe à 50 000, le site le dit dans les six heures.

**Sans jeton, rien ne casse** : le script sort en silence et le dernier bon
chiffre reste affiché.

> **Il n'existe aucune version sans jeton qui tienne dans la durée.**
> Instagram ne donne le nombre d'abonnés qu'au propriétaire d'un compte
> professionnel. Les services qui prétendent le contraire lisent la page en
> douce et cassent à chaque changement de Meta.

## 5. Reste à faire

- Le **showreel** : le fichier est chez Simon, il n'est pas dans le site.
- **Quel film va avec quel client** : les légendes décrivent ce qu'on voit,
  aucune n'attribue un film à une marque. C'est la première chose à lui
  faire remplir.
- Les **fichiers sources** des visuels : ce sont des captures d'écran, nettes
  en petit et moyen format seulement.
- La **date dans le pied de page** dit « maquette » : à retirer le jour de la
  mise en ligne pour de vrai.
- Le chapeau des mondes déformés cite « 49 700 abonnés » **en toutes lettres
  dans la phrase** : ce texte-là ne suit pas le compteur. À reformuler si
  l'écart devient visible.

---

## Comment ça marche, en une ligne

`donnees/*.json` → `python3 construire.py` → `site/`

Six fichiers de données, un générateur, deux langues en sortie. Aucun CDN,
aucune dépendance : les polices et le style sont dans la page. La seule
exception est `/admin`, qui charge Decap — et elle n'est pas indexée.
