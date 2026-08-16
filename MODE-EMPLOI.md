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

## 1. Le dépôt — FAIT

`github.com/matissesolitude-pixel/simon-vergely`, **en public**.

> **Pourquoi public.** Sur un dépôt privé, l'offre gratuite de Netlify
> n'autorise **qu'un seul contributeur** : tout commit venant d'ailleurs est
> refusé avec « Unrecognized Git contributor ». Ça aurait bloqué les
> publications de Simon, qui arrivent signées de son nom.
> Le dépôt ne contient aucun secret : le jeton Instagram vit dans les
> secrets GitHub, celui de DecapBridge chez DecapBridge. Les visuels étaient
> déjà publics sur le site.
> L'alternative payante était Netlify Pro, ~19 $/mois.

## 2. Netlify construit le site — FAIT

`resilient-cuchufli-a778a1.netlify.app`, relié au dépôt, construit par
`python3 construire.py` à chaque poussée.

## 3. DecapBridge ouvre la porte — FAIT

Netlify Identity a été déprécié en février 2025 et Git Gateway l'est aussi :
sans remplaçant, Decap obligerait Simon à créer un compte GitHub.

Site DecapBridge `48464eb0-e724-4d4a-a775-255871bde32e`, jeton GitHub
« DecapBridge - site Simon Vergely » (portée : ce seul dépôt, Contents et
Pull requests en écriture, sans expiration).

> **Le bloc `backend` de `site/admin/config.yml` est celui que DecapBridge
> fournit, mot pour mot.** L'authentification est en **PKCE** :
> `auth_type`, `base_url`, `auth_endpoint`, `auth_token_endpoint`. Ce ne sont
> pas les clés d'un git-gateway classique, et Decap doit être en 3.8.3
> minimum. Ne pas réécrire ce bloc de mémoire.

**RESTE À FAIRE : inviter Simon par mail** depuis DecapBridge, onglet
« Manage collaborators ».

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
