#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMON VERGÉLY — le générateur.   python3 construire.py

Deux langues, deux sorties, depuis les mêmes données :
  · site/index.html      le site en français
  · site/en/index.html   le même en anglais
  · site/simon.html      version AUTOPORTÉE (polices et images incrustées),
                         publiable en artifact, lisible depuis un téléphone.
                         Non construite en CI : elle ne sert qu'à la relecture.

CE QUI EST GRAVÉ ICI
  1. Le produit est le média. Chez un motion designer, une page qui ne bouge
     pas est une contre-démonstration — d'où le bandeau qui tourne.
  2. Rien d'inventé : les dix logos sont les siens, le nombre d'abonnés est
     relevé et daté, l'accroche « too perfect is suspicious » est de lui.
  3. Le site se tait pour que son travail crie : fond neutre, couleur réservée
     à ses images.
  4. Zéro CDN, polices embarquées.
  5. `prefers-reduced-motion` respecté : le bandeau se fige en grille.
"""
import json, html, base64, pathlib, os

ICI = pathlib.Path(__file__).parent
SRC, OUT = ICI / "donnees", ICI / "site"


def lire(n):
    return json.load(open(SRC / n, encoding="utf-8"))


CL, TR, PU, HI = lire("clients.json"), lire("travaux.json"), \
                 lire("publications.json"), lire("histoire.json")
IN = lire("interface.json")
IG = lire("instagram.json")
CO = lire("contact.json")

# LE NOMBRE D'ABONNÉS N'EST ÉCRIT QU'À UN SEUL ENDROIT : donnees/instagram.json.
# abonnes.py le réécrit depuis l'API, l'action GitHub relance ce générateur.
# Ici on ne fait que le lire et le mettre en forme — jamais le saisir.
ABO = int(IG["abonnes"])
ABO_TXT = f"{ABO:,}".replace(",", "\u202f")   # 49 700, espace fine insécable


def releve(lg):
    """La date du relevé, dite dans la langue de la page. Un chiffre sans date
    n'est pas une preuve."""
    a, m, j = IG["releve"].split("-")
    mois_fr = ["janvier","février","mars","avril","mai","juin","juillet","août",
               "septembre","octobre","novembre","décembre"]
    mois_en = ["January","February","March","April","May","June","July","August",
               "September","October","November","December"]
    i = int(m) - 1
    return (f"{int(j)} {mois_fr[i]} {a}" if lg == "fr"
            else f"{int(j)} {mois_en[i]} {a}")
E = html.escape

PAGES = ["index.html", "travail.html", "ensemble.html"]
CLES_NAV = ["nav_accueil", "nav_travail", "nav_ensemble"]


def t(cle, lg):
    """Le texte d'habillage, dans la langue demandée."""
    return IN[cle][lg]


def d(obj, cle, lg):
    """Un champ de données. L'anglais vit dans « cle_en » à côté du français ;
    s'il manque, on retombe sur le français plutôt que d'afficher un trou."""
    return obj[cle] if lg == "fr" else obj.get(cle + "_en") or obj[cle]


def b64(chemin, mime):
    f = OUT / chemin
    return f"data:{mime};base64," + base64.b64encode(f.read_bytes()).decode() if f.exists() else ""


# Les pages anglaises vivent dans site/en/ : leurs images remontent d'un cran.
RACINE = ""


def img(nom, ap):
    if not ap:
        return f"{RACINE}assets/img/{nom}"
    return b64(f"assets/img/{nom}", "image/png" if nom.endswith(".png") else "image/jpeg")


def police(nom):
    f = OUT / "assets" / "fonts" / nom
    return base64.b64encode(f.read_bytes()).decode() if f.exists() else ""


def feuille():
    sy, wk = police("syne.woff2"), police("work-sans.woff2")
    return """
@font-face{font-family:"Syne";src:url(data:font/woff2;base64,__SY__) format("woff2");
  font-weight:400 800;font-style:normal;font-display:swap}
@font-face{font-family:"Work";src:url(data:font/woff2;base64,__WK__) format("woff2");
  font-weight:300 700;font-style:normal;font-display:swap}

/* ============================================================
   SIMON VERGÉLY — animateur 2D. Sprint 1, 16/08/2026.

   LE SITE SE TAIT POUR QUE SON TRAVAIL CRIE.
   Son univers est violemment coloré : orange, rouge, vert saturés,
   contours épais. Si la page l'est aussi, les deux se battent. Le
   fond reste donc neutre, et la couleur n'appartient qu'à ses images.

   LE PRODUIT EST LE MÉDIA. Chez un animateur, une page immobile est
   une contre-démonstration. Le bandeau de clients tourne sans fin —
   c'est la seule chose qui bouge, et elle porte la preuve.
   ============================================================ */
:root{
  --papier:#F2F0EB; --papier-2:#E7E4DC; --encre:#141310; --encre-2:#5A554A;
  --trait:#CFC9BC; --vif:#E8481F;
  --titre:"Syne",Impact,sans-serif; --texte:"Work",-apple-system,Helvetica,sans-serif;
  --marge:clamp(1.15rem,5vw,4.5rem); --large:78rem;
}
*{box-sizing:border-box}
html{font-size:clamp(16.5px,.38vw+15px,18px);scroll-behavior:smooth}
body{margin:0;background:var(--papier);color:var(--encre);font-family:var(--texte);
  font-weight:400;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
h1,h2,h3{margin:0;font-family:var(--titre);font-weight:800;line-height:.94;
  letter-spacing:-.03em;text-wrap:balance;text-transform:uppercase}
h1{font-size:clamp(2.9rem,9vw,7rem)}
h2{font-size:clamp(1.9rem,4.6vw,3.4rem)}
h3{font-size:1.06rem;letter-spacing:-.01em}
p{margin:0 0 1em}
img{max-width:100%;display:block}
a{color:var(--encre)}
:focus-visible{outline:3px solid var(--vif);outline-offset:3px}

.sec{max-width:var(--large);margin-inline:auto;padding:clamp(2.8rem,6vw,5rem) var(--marge)}
.eti{display:block;font-size:.7rem;font-weight:700;letter-spacing:.24em;
  text-transform:uppercase;color:var(--vif);margin-bottom:1rem}
.chapeau{max-width:46ch;color:var(--encre-2);font-size:1.12rem;margin-top:1.3rem}

.b{display:inline-flex;align-items:center;gap:.6rem;text-decoration:none;
  font-family:var(--titre);font-weight:700;font-size:.9rem;letter-spacing:.02em;
  text-transform:uppercase;padding:.95rem 1.6rem;border:2.5px solid var(--encre);
  background:var(--encre);color:var(--papier);transition:.18s}
.b:hover{background:var(--vif);border-color:var(--vif)}
.b--nu{background:transparent;color:var(--encre)}
.b--nu:hover{background:var(--encre);color:var(--papier)}

/* ---------- en-tête ---------- */
.tete{position:sticky;top:0;z-index:50;background:rgba(242,240,235,.94);
  backdrop-filter:blur(8px);border-bottom:2.5px solid var(--encre)}
.tete__in{max-width:var(--large);margin-inline:auto;padding:.65rem var(--marge);
  display:flex;align-items:center;gap:1rem}
.marque{font-family:var(--titre);font-weight:800;font-size:1.12rem;letter-spacing:-.02em;
  text-transform:uppercase;text-decoration:none;color:var(--encre)}
.tete__act{margin-left:auto;display:flex;gap:.5rem;align-items:center}
/* LE COMPTEUR D'ABONNÉS.
   « 49 700 abonnés » en petit texte ne dit rien. Avec le logo et un
   chiffre qui monte à l'affichage, ça devient une preuve qu'on regarde.
   LE NOMBRE VIENT DE donnees/instagram.json, jamais d'ici. Une fois le
   compte relié, abonnes.py le relève quatre fois par jour et le site suit
   tout seul ; en attendant c'est le dernier relevé manuel, affiché avec
   sa date. L'animation ne fait que le compter, elle ne l'invente pas. */
.badge{display:inline-flex;align-items:center;gap:.5rem;text-decoration:none;
  color:var(--encre);border:2.5px solid var(--encre);padding:.42rem .8rem;
  transition:.18s;white-space:nowrap}
.badge:hover{background:var(--vif);border-color:var(--vif);color:#fff}
.badge svg{width:19px;height:19px;flex:0 0 auto}
.badge b{font-family:var(--titre);font-weight:800;font-size:1.02rem;
  letter-spacing:-.02em;font-variant-numeric:tabular-nums}
@media (max-width:560px){.badge{padding:.36rem .6rem}.badge b{font-size:.92rem}}

/* ---------- ouverture ---------- */
.ouv{padding-top:clamp(2.4rem,6vw,4.4rem)}
.ouv h1 em{font-style:normal;color:var(--vif)}
.ouv__act{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:2rem}

/* ============================================================
   LE BANDEAU DE CLIENTS — demandé par le PO.
   Il tourne sans fin : la série est doublée dans le HTML, et
   l'animation translate d'exactement la moitié, donc la boucle
   est invisible. Il s'arrête au survol, parce qu'un logo qui
   intrigue doit pouvoir être lu.
   Ce n'est pas un clignotement mais une translation : aucune
   variation de luminosité plein cadre.
   ============================================================ */
.bandeau{background:var(--encre);border-block:2.5px solid var(--encre);
  padding:1.5rem 0;overflow:hidden}
.bandeau__t{max-width:var(--large);margin:0 auto .9rem;padding-inline:var(--marge);
  font-size:.7rem;font-weight:700;letter-spacing:.24em;text-transform:uppercase;
  color:#8C8578}
.piste{display:flex;width:max-content;animation:defile 42s linear infinite}
.bandeau:hover .piste,.bandeau:focus-within .piste{animation-play-state:paused}
@keyframes defile{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.piste img{height:44px;width:auto;margin-inline:clamp(1.4rem,3.4vw,3.2rem);
  filter:invert(1) brightness(1.6);opacity:.82;flex:0 0 auto}
@media (max-width:600px){.piste img{height:34px}}
@media (prefers-reduced-motion:reduce){
  /* figé en grille : on ne prive personne de la preuve */
  .piste{animation:none;flex-wrap:wrap;width:100%;justify-content:center;gap:1.4rem 0}
  .piste img:nth-child(n+11){display:none}
}

/* ---------- la preuve ---------- */
.chiffres{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));
  gap:1px;background:var(--trait);border:2.5px solid var(--encre)}
.chiffre{background:var(--papier);padding:1.5rem 1.6rem}
.chiffre b{display:block;font-family:var(--titre);font-weight:800;
  font-size:clamp(2.2rem,5vw,3.2rem);line-height:1;letter-spacing:-.03em}
.chiffre span{font-size:.86rem;color:var(--encre-2)}

/* ---------- le travail ---------- */
.grille{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
  gap:1px;background:var(--encre);border:2.5px solid var(--encre)}
.oeuvre{margin:0;position:relative;background:var(--papier);overflow:hidden}
.oeuvre img{width:100%;aspect-ratio:3/4;object-fit:cover;transition:transform .5s ease}
.oeuvre:hover img{transform:scale(1.05) rotate(-.7deg)}
.oeuvre figcaption{position:absolute;left:0;right:0;bottom:0;padding:1.6rem .8rem .6rem;
  font-size:.76rem;font-weight:600;letter-spacing:.04em;color:#fff;
  background:linear-gradient(180deg,transparent,rgba(10,9,7,.78))}

/* ---------- formats ---------- */
.formats{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  gap:1px;background:var(--trait);border:2.5px solid var(--encre);margin-top:2rem}
.format{background:var(--papier);padding:1.4rem 1.5rem 1.6rem}
.format h3{color:var(--vif)}
.format p{margin:.5rem 0 0;font-size:.92rem;color:var(--encre-2)}

/* ---------- le pied ---------- */
.pied{background:var(--encre);color:#CFC9BC;padding:clamp(2.4rem,5vw,3.6rem) 0 1.4rem;
  font-size:.92rem}
.pied__in{max-width:var(--large);margin-inline:auto;padding-inline:var(--marge);
  display:grid;grid-template-columns:repeat(auto-fit,minmax(13rem,1fr));gap:2rem}
.pied h4{font-family:var(--titre);color:#fff;font-size:.8rem;letter-spacing:.18em;
  margin:0 0 .7rem}
.pied a{color:#fff}
.pied__bas{max-width:var(--large);margin:2.2rem auto 0;padding:1.2rem var(--marge) 0;
  border-top:1px solid #3A362E;font-size:.76rem;color:#8C8578;line-height:1.6}

.pouce{position:fixed;left:0;right:0;bottom:0;z-index:60;display:none;gap:.5rem;
  padding:.55rem .7rem calc(.55rem + env(safe-area-inset-bottom));
  background:var(--papier);border-top:2.5px solid var(--encre)}
.pouce .b{flex:1;justify-content:center;font-size:.8rem;padding:.8rem .5rem}
@media (max-width:820px){.pouce{display:flex}body{padding-bottom:4.4rem}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}
  .oeuvre:hover img{transform:none}}
""".replace("__SY__", sy).replace("__WK__", wk)


# ============================================================
# LES BLOCS
# ============================================================

def tete(courante, lg, ap):
    def lien(f, cle):
        cur = ' aria-current="page"' if f == courante else ''
        return '<a href="' + f + '"' + cur + '>' + E(t(cle, lg)) + '</a>'
    nav = "".join(lien(f, c) for f, c in zip(PAGES, CLES_NAV))
    # Le bouton de langue mène à la MÊME page dans l'autre langue, jamais à
    # l'accueil : basculer ne doit pas faire perdre sa place au visiteur.
    # Dans la version autoportée il n'y a qu'un fichier : on l'affiche éteint.
    if ap:
        bascule = f'<span class="langue langue--morte">{E(t("langue_autre", lg))}</span>'
    else:
        cible = ("en/" + courante) if lg == "fr" else ("../" + courante)
        bascule = (f'<a class="langue" href="{cible}" hreflang="{"en" if lg=="fr" else "fr"}" '
                   f'title="{E(t("langue_titre", lg))}">{E(t("langue_autre", lg))}</a>')
    return f"""
<header class="tete"><div class="tete__in">
  <a class="marque" href="index.html">Simon Vergély</a>
  <nav class="nav">{nav}</nav>
  <div class="tete__act">
    {bascule}
    <a class="badge" href="https://www.instagram.com/{CO['instagram']}/" target="_blank"
       rel="noopener" title="{E(t('badge_titre', lg))}">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"
           stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <rect x="2.6" y="2.6" width="18.8" height="18.8" rx="5.2"/>
        <circle cx="12" cy="12" r="4.1"/>
        <circle cx="17.5" cy="6.5" r="1.1" fill="currentColor" stroke="none"/></svg>
      <b data-compteur="{ABO}">0</b></a>
    <a class="b" href="ensemble.html">{E(t('tete_projet', lg))}</a>
  </div>
</div></header>"""


# UNE IMAGE, UN SEUL ENDROIT.
# Cinq des huit « mondes » sont déjà montrés en vidéo dans les reels de
# l'accueil. Les remontrer en image fixe sur la page Travail, c'était la
# répétition. On retire ceux-là de la grille — automatiquement, pour qu'ajouter
# un reel demain suffise à le sortir de la grille sans y penser.
_EN_VIDEO = {r["apercu"] for r in PU["reels"]}
MONDES_FIXES = [x for x in TR["mondes"]["liste"] if x["f"] not in _EN_VIDEO]


def bandeau(ap, lg):
    """LE BANDEAU QUI TOURNE. La série est écrite deux fois et l'animation
    translate exactement de la moitié : la boucle est invisible. Il s'arrête
    au survol, et se fige en grille si les animations sont désactivées."""
    une = "".join(f'<img src="{img(l["f"], ap)}" alt="{E(l["nom"])}" '
                  f'title="{E(l["nom"])}" loading="lazy">' for l in CL["logos"])
    return f"""
<div class="bandeau">
  <p class="bandeau__t">{E(t('bandeau_titre', lg))}</p>
  <div class="piste">{une}{une}</div>
</div>"""


def reels(ap, lg):
    """LES REELS, JOUÉS SUR PLACE.
    Un aller-retour vers Instagram, c'est un visiteur perdu. L'intégration
    officielle joue la vidéo ici même. Dans la maquette publiée en artifact,
    les appels extérieurs sont bloqués : on retombe alors sur l'image."""
    out = []
    for r in PU["reels"]:
        vu = d(r, "vu", lg)
        if ap:
            out.append(
                f'<figure class="reel reel--repli">'
                f'<img src="{img(r["apercu"], ap)}" alt="{E(vu)}" loading="lazy">'
                f'<figcaption>{E(vu)}<br><span>{E(t("reel_repli", lg))}</span>'
                f'</figcaption></figure>')
        else:
            out.append(
                f'<figure class="reel"><iframe src="https://www.instagram.com/reel/'
                f'{E(r["code"])}/embed" loading="lazy" title="{E(vu)}" '
                f'scrolling="no" allowtransparency="true"></iframe></figure>')
    return f'<div class="reels">{"".join(out)}</div>'


def galerie(bloc, ap, lg, format_="16/9", liste=None):
    o = "".join(
        f'<figure class="oeuvre"><img src="{img(x["f"], ap)}" alt="{E(d(x, "vu", lg))}" '
        f'style="aspect-ratio:{format_}" loading="lazy">'
        f'<figcaption>{E(d(x, "vu", lg))}</figcaption></figure>'
        for x in (bloc["liste"] if liste is None else liste))
    return f"""
<span class="eti">{E(d(bloc, 'titre', lg))}</span>
<p class="chapeau" style="margin-top:0">{E(d(bloc, 'chapeau', lg))}</p>
<div class="grille" style="margin-top:2rem">{o}</div>"""


def pied(lg):
    return f"""
<footer class="pied"><div class="pied__in">
  <div><h4>{E(t('pied_1_h', lg))}</h4><p>{E(t('pied_1_p_1', lg))}<br>
    {E(t('pied_1_p_2', lg))}</p></div>
  <div><h4>{E(t('pied_2_h', lg))}</h4>
    <p><a href="mailto:{CO['mail']}">{CO["mail"]}</a></p>
    <p><a href="tel:{CO['tel']}">{CO["tel_affiche"]}</a></p></div>
  <div><h4>{E(t('pied_3_h', lg))}</h4>
    <p><a href="https://www.instagram.com/{CO['instagram']}/" target="_blank"
       rel="noopener">@{CO["instagram"]}</a> · {ABO_TXT} {E(t('pied_abonnes', lg))}</p></div>
</div>
<div class="pied__bas">{E(t('pied_bas', lg))}</div></footer>"""


JS = """
/* LE COMPTEUR D'ABONNÉS.
   Il monte de zéro jusqu'au chiffre relevé, une seule fois, à l'apparition.
   C'EST UNE ANIMATION, PAS UN RELEVÉ EN DIRECT : le nombre vient des données,
   daté du 16/08/2026. Pour qu'il soit vraiment vivant il faut un jeton de
   l'API Instagram — voir le README.
   Respecte prefers-reduced-motion : le chiffre s'affiche d'emblée. */
(function(){
  var doux = matchMedia('(prefers-reduced-motion: reduce)').matches;
  function fmt(n){ return n.toLocaleString('fr-FR').replace(/\\u202f|,/g,' '); }
  document.querySelectorAll('[data-compteur]').forEach(function(e){
    var cible = +e.dataset.compteur;
    if (doux) { e.textContent = fmt(cible); return; }
    var t0 = null, duree = 1400;
    function pas(t){
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / duree, 1);
      e.textContent = fmt(Math.round(cible * (1 - Math.pow(1 - p, 3))));
      if (p < 1) requestAnimationFrame(pas);
    }
    var io = new IntersectionObserver(function(en){
      if (en[0].isIntersecting) { io.disconnect(); requestAnimationFrame(pas); }
    });
    io.observe(e);
  });
})();
"""


def pouce(lg):
    return (f'<div class="pouce"><a class="b b--nu" href="travail.html">'
            f'{E(t("pouce_1", lg))}</a>'
            f'<a class="b" href="ensemble.html">{E(t("pouce_2", lg))}</a></div>')


def mailto(lg):
    from urllib.parse import quote
    return (f"mailto:{CO['mail']}?subject=" + quote(t("mail_sujet", lg))
            + "&body=" + quote(t("mail_corps", lg)))


def smsto(lg):
    from urllib.parse import quote
    return f"sms:{CO['tel']}?&body=" + quote(t("sms_corps", lg))


# ============================================================
# LES TROIS PAGES
# ============================================================

def page_accueil(ap, lg):
    """L'ACCUEIL PORTE LES MONDES DÉFORMÉS, EN ENTIER.

    Deux règles tenues ici, et elles vont ensemble :
      · UNE IMAGE, UN SEUL ENDROIT — rien n'est montré deux fois sur le site.
      · UN CORPS DE TRAVAIL, UNE SEULE SECTION — les mondes ne se coupent pas
        en deux. Les cinq qui ont une vidéo et les trois qui n'en ont pas se
        suivent dans la même section : d'abord ce qui bouge, puis le reste.
    Les huit films sont sur la page Travail, et nulle part ailleurs."""
    fixes = "".join(
        f'<figure class="oeuvre"><img src="{img(x["f"], ap)}" alt="{E(d(x, "vu", lg))}" '
        f'style="aspect-ratio:3/4" loading="lazy">'
        f'<figcaption>{E(d(x, "vu", lg))}</figcaption></figure>' for x in MONDES_FIXES)
    return f"""
<section class="sec ouv">
  <span class="eti">{E(t('acc_eti', lg))}</span>
  <h1>{E(t('acc_h1_1', lg))}<br><em>{E(t('acc_h1_2', lg))}</em></h1>
  <p class="chapeau">{E(d(HI, 'promesse', lg))}</p>
  <div class="ouv__act">
    <a class="b" href="travail.html">{E(t('acc_b1', lg))}</a>
    <a class="b b--nu" href="ensemble.html">{E(t('acc_b2', lg))}</a>
  </div>
</section>

{bandeau(ap, lg)}

<section class="sec">
  <div class="chiffres">
    <div class="chiffre"><b>{ABO_TXT}</b><span>{E(t('chiffre_1', lg))} {E(releve(lg))}</span></div>
    <div class="chiffre"><b>10</b><span>{E(t('chiffre_2', lg))}</span></div>
    <div class="chiffre"><b>4</b><span>{E(t('chiffre_3', lg))}</span></div>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <span class="eti">{E(d(TR['mondes'], 'titre', lg))}</span>
  <h2>{E(t('acc_reels_h2_1', lg))}<br>{E(t('acc_reels_h2_2', lg))}</h2>
  <p class="chapeau">{E(d(TR['mondes'], 'chapeau', lg))}</p>
  {reels(ap, lg)}
  <div class="grille grille--haute" style="margin-top:1.4rem">{fixes}</div>
</section>

<section class="fond-2"><div class="sec">
  <span class="eti">{E(t('acc_films_eti', lg))}</span>
  <h2>{E(t('acc_films_h2', lg))}</h2>
  <p class="chapeau">{E(d(TR['films'], 'chapeau', lg))}</p>
  <p class="chapeau" style="margin-top:.9rem">{E(t('acc_films_note', lg))}</p>
  <p style="margin-top:1.6rem"><a class="b" href="travail.html">{E(t('acc_films_b', lg))}</a></p>
</div></section>
"""


def page_travail(ap, lg):
    """LA PAGE TRAVAIL PORTE LES FILMS, ET RIEN QUE LES FILMS.
    Les mondes déformés sont entiers sur l'accueil ; on ne les recoupe pas ici,
    on y renvoie."""
    return f"""
<section class="sec ouv">
  <span class="eti">{E(t('tra_eti', lg))}</span>
  <h1>{E(t('tra_h1_1', lg))}<br><em>{E(t('tra_h1_2', lg))}</em></h1>
  <p class="chapeau">{E(t('tra_chapeau', lg))}</p>
</section>

{bandeau(ap, lg)}

<section class="sec">{galerie(TR['films'], ap, lg, '16/9')}</section>

<section class="fond-2"><div class="sec">
  <span class="eti">{E(d(TR['mondes'], 'titre', lg))}</span>
  <p class="chapeau" style="margin-top:0">{E(d(TR['mondes'], 'chapeau', lg))}</p>
  <p class="chapeau" style="margin-top:.9rem">{E(t('tra_mondes_note_1', lg))}
    <a href="index.html">{E(t('tra_mondes_note_2', lg))}</a>.</p>
</div></section>

<section class="sec">
  <div class="ouv__act"><a class="b" href="ensemble.html">{E(t('tra_b1', lg))}</a>
  <a class="b b--nu" href="https://www.instagram.com/{CO['instagram']}/" target="_blank"
     rel="noopener">{E(t('tra_b2', lg))}</a></div>
</section>
"""


def page_ensemble(ap, lg):
    ch = "".join(
        f'<article class="chap"><h3>{E(d(c, "titre", lg))}</h3>'
        + "".join(f"<p>{E(x)}</p>" for x in d(c, "texte", lg))
        + f'<blockquote>«&nbsp;{E(d(c, "citation", lg))}&nbsp;»</blockquote></article>'
        for c in HI["chapitres"])
    fo = "".join(
        f'<div class="format"><h3>{E(d(f, "nom", lg))}</h3><p>{E(d(f, "quoi", lg))}</p>'
        f'<p class="format__q">{E(d(f, "pour", lg))}</p></div>' for f in HI["formats"])
    co = "".join(
        f'<li><b>{E(e["n"])}</b><div><h3>{E(d(e, "t", lg))}</h3>'
        f'<p>{E(d(e, "d", lg))}</p></div></li>' for e in HI["comment"])
    ml, sm = mailto(lg), smsto(lg)
    return f"""
<section class="sec ouv">
  <span class="eti">{E(t('ens_eti', lg))}</span>
  <h1>{E(t('ens_h1_1', lg))}<br><em>{E(t('ens_h1_2', lg))}</em></h1>
  <p class="chapeau">{E(t('ens_chapeau', lg))}</p>
  <div class="ouv__act">
    <a class="b" href="{ml}">{E(t('ens_b_mail', lg))}</a>
    <a class="b b--nu" href="{sm}">{E(t('ens_b_sms', lg))}</a>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="formats">{fo}</div>
</section>

<section class="fond-2"><div class="sec">
  <span class="eti">{E(t('ens_comment_eti', lg))}</span>
  <h2>{E(d(HI, 'comment_titre', lg))}</h2>
  <p class="chapeau">{E(d(HI, 'comment_chapeau', lg))}</p>
  <ol class="etapes">{co}</ol>
</div></section>

<section class="sec">
  <span class="eti">{E(t('ens_qui_eti', lg))}</span>
  <h2>{E(t('ens_qui_h2_1', lg))}<br><em>{E(t('ens_qui_h2_2', lg))}</em></h2>
  <div class="chapitres">{ch}</div>
</section>

{bandeau(ap, lg)}

<section class="sec">
  <h2>{E(t('ens_fin_h2', lg))}</h2>
  <p class="chapeau">{CO["mail"]} · {CO["tel_affiche"]} · @{CO["instagram"]}</p>
  <div class="ouv__act">
    <a class="b" href="{ml}">{E(t('ens_b_mail', lg))}</a>
    <a class="b b--nu" href="tel:{CO['tel']}">{E(t('ens_b_tel', lg))}</a>
  </div>
</section>
"""


EN_PLUS = """
/* ---------- la navigation ---------- */
.nav{display:none;gap:1.8rem;margin-left:2rem}
.nav a{font-family:var(--titre);font-weight:700;font-size:1rem;letter-spacing:-.01em;
  text-transform:uppercase;text-decoration:none;color:var(--encre-2);white-space:nowrap}
.nav a:hover,.nav a[aria-current]{color:var(--vif)}
@media (min-width:860px){.nav{display:flex}}

/* ============================================================
   LES REELS, JOUÉS SUR PLACE.
   Un aller-retour vers Instagram, c'est un visiteur perdu.
   ============================================================ */
/* Une rangée qui défile, pas une grille. En grille, cinq reels sur quatre
   colonnes laissent un orphelin seul sur la deuxième ligne — et l'intégration
   Instagram refuse de descendre sous 326 px, donc on ne peut pas les serrer.
   Le défilement horizontal reste DANS le cadre : la page, elle, ne bouge pas. */
.reels{display:flex;gap:1.1rem;margin-top:2rem;overflow-x:auto;
  scroll-snap-type:x proximity;padding-bottom:.9rem;
  scrollbar-color:var(--encre) var(--papier-2)}
.reel{flex:0 0 clamp(288px,80vw,336px);scroll-snap-align:start;
  margin:0;position:relative;background:var(--papier-2);
  border:2.5px solid var(--encre);overflow:hidden}
.reel iframe{width:100%;height:640px;border:0;display:block;background:#fff}
@media (max-width:640px){.reel iframe{height:560px}}
.reel--repli img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block}
.reel--repli figcaption{padding:.7rem .8rem .9rem;font-size:.82rem;font-weight:600}
.reel--repli figcaption span{font-weight:400;color:var(--encre-2);font-size:.76rem}

/* ---------- le récit ---------- */
.chapitres{display:grid;grid-template-columns:repeat(auto-fit,minmax(19rem,1fr));
  gap:1px;background:var(--trait);border:2.5px solid var(--encre);margin-top:2.2rem}
.chap{background:var(--papier);padding:1.7rem 1.8rem 1.9rem;margin:0}
.chap h3{color:var(--vif);margin-bottom:.7rem}
.chap p{font-size:.98rem;color:var(--encre-2);margin:0 0 .8rem}
.chap blockquote{margin:1rem 0 0;padding-left:1rem;border-left:3px solid var(--vif);
  font-family:var(--titre);font-weight:700;font-size:1.06rem;line-height:1.3;
  color:var(--encre);text-transform:none;letter-spacing:-.01em}

/* ---------- les étapes ---------- */
.etapes{list-style:none;margin:2.2rem 0 0;padding:0;display:grid;
  grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1px;
  background:var(--trait);border:2.5px solid var(--encre)}
.etapes li{background:var(--papier);padding:1.5rem 1.6rem;display:flex;gap:1rem;
  align-items:flex-start}
.etapes b{font-family:var(--titre);font-weight:800;font-size:2rem;line-height:.9;
  color:var(--vif);flex:0 0 auto}
.etapes h3{margin:0 0 .3rem}
.etapes p{margin:0;font-size:.92rem;color:var(--encre-2)}

/* ---------- la bascule de langue ---------- */
/* Deux lettres, dans l'en-tête, à côté du badge : visible sur téléphone où la
   navigation, elle, est repliée. Elle mène à la MÊME page dans l'autre langue. */
.langue{font-family:var(--titre);font-weight:800;font-size:.78rem;
  letter-spacing:.1em;color:var(--encre);text-decoration:none;
  padding:.42rem .58rem;border:2px solid var(--encre);line-height:1;
  transition:background .15s,color .15s}
.langue:hover,.langue:focus-visible{background:var(--encre);color:var(--papier)}
.langue--morte{opacity:.32;border-style:dashed}

.format__q{margin-top:.6rem!important;font-size:.84rem!important;
  color:var(--vif)!important;font-weight:600}
.grille--haute{grid-template-columns:repeat(auto-fit,minmax(min(240px,100%),1fr))}
"""


def page(fichier, titre, desc, corps, ap, lg):
    css = feuille() + EN_PLUS
    if ap:
        return (f"<title>{E(titre)}</title>\n<style>{css}</style>\n{corps}\n"
                f"<script>{JS}</script>\n")
    # hreflang : dit à Google que les deux versions sont la même page, et
    # laquelle servir selon la langue du visiteur.
    autre = ("en/" + fichier) if lg == "fr" else ("../" + fichier)
    alt = (f'<link rel="alternate" hreflang="{"en" if lg == "fr" else "fr"}" href="{autre}">'
           f'<link rel="alternate" hreflang="x-default" '
           f'href="{"" if lg == "fr" else "../"}{fichier}">')
    return (f'<!doctype html><html lang="{lg}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(titre)}</title><meta name="description" content="{E(desc)}">'
            f'<meta name="theme-color" content="#F2F0EB">{alt}'
            f'<style>{css}</style></head><body>{corps}'
            f'<script>{JS}</script></body></html>')


def construire(lg, dossier):
    """Une langue, un dossier. Le français à la racine (site/), l'anglais dans
    site/en/ — donc ses images remontent d'un cran, d'où RACINE."""
    global RACINE
    RACINE = "" if lg == "fr" else "../"
    dossier.mkdir(parents=True, exist_ok=True)
    marque = t("meta_titre_acc", lg)
    desc = t("meta_desc", lg)
    plan = [("index.html",    marque,                                  page_accueil),
            ("travail.html",  t("meta_titre_tra", lg) + " — " + marque, page_travail),
            ("ensemble.html", t("meta_titre_ens", lg) + " — " + marque, page_ensemble)]
    for f, titre, fn in plan:
        corps = (tete(f, lg, False) + "<main>" + fn(False, lg) + "</main>"
                 + pied(lg) + pouce(lg))
        (dossier / f).write_text(page(f, titre, desc, corps, False, lg), encoding="utf-8")
        ko = (dossier / f).stat().st_size // 1024
        print(f"  {lg}  {f:16} {ko:4} Ko")


def autoporte(lg, nom):
    """Les trois pages à la suite, polices et images incrustées : un seul
    fichier, publiable en artifact et lisible depuis un téléphone."""
    un = (tete("index.html", lg, True) + "<main>" + page_accueil(True, lg)
          + page_travail(True, lg) + page_ensemble(True, lg) + "</main>" + pied(lg))
    (OUT / nom).write_text(
        page(nom, t("meta_titre_acc", lg), t("meta_desc", lg), un, True, lg),
        encoding="utf-8")
    print(f"  {lg}  {nom:16} {(OUT / nom).stat().st_size // 1024:4} Ko  (autoporté)")


if __name__ == "__main__":
    construire("fr", OUT)
    construire("en", OUT / "en")
    RACINE = ""
    # Les versions autoportées pèsent 4,6 Mo chacune et ne servent qu'à la
    # relecture depuis un téléphone. Inutile de les embarquer dans la mise en
    # ligne : Netlify pose CI=true, on les saute là-bas.
    if os.environ.get("CI"):
        print("  (CI : versions autoportées non construites)")
    else:
        autoporte("fr", "simon.html")
        autoporte("en", "simon-en.html")
    print(f"\n  {len(CL['logos'])} logos · {len(PU['reels'])} reels · "
          f"{len(TR['films']['liste'])} films · "
          f"{len(MONDES_FIXES)} mondes en image · 2 langues")
