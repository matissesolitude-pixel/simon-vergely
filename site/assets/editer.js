/* =====================================================================
   LE MODE « MODIFIER » — on désigne l'endroit sur le site lui-même.

   LE PROBLÈME. Une interface d'édition classique donne une liste de
   rubriques. Il faut deviner laquelle correspond à l'endroit qu'on veut
   changer. Simon connaît son site par ce qu'il voit, pas par nos noms.

   CE QUE ÇA FAIT. Sur le vrai site, en ajoutant ?editer à l'adresse :
   chaque zone modifiable s'encadre, se nomme, et un clic ouvre le bon
   formulaire, déjà au bon endroit. On part de la page, pas du menu.

   CE QUE ÇA NE FAIT PAS, ET POURQUOI. On ne dépose pas une image au
   pixel près n'importe où. Les emplacements sont ceux du site : une
   grille de films en paysage, une grille de mondes en portrait, un
   bandeau de logos. C'est ce qui garantit qu'il reste net quoi qu'on y
   mette. Un site où l'on pose les images librement finit de travers, et
   c'est le client qui en porte le résultat.

   Le script ne se charge QUE si ?editer est dans l'adresse : un visiteur
   normal ne télécharge rien et ne voit rien.
   ===================================================================== */

(function () {
  if (location.search.indexOf('editer') === -1) return;

  var ADMIN = '/admin/#/collections/';
  var FICHIER = {                 /* rubrique -> fichier, pour le lien direct */
    travaux: 'travaux', publications: 'reels', clients: 'clients',
    coordonnees: 'contact', histoire: 'histoire', instagram: 'instagram'
  };

  var css = document.createElement('style');
  css.textContent = [
    '.zed{position:absolute;border:2.5px dashed #E8481F;border-radius:2px;',
    '  background:rgba(232,72,31,.07);z-index:9998;pointer-events:none;',
    '  transition:background .15s}',
    '.zed--on{background:rgba(232,72,31,.16)}',
    '.zeb{position:absolute;z-index:9999;background:#E8481F;color:#fff;',
    '  border:0;cursor:pointer;font:700 12px/1.2 -apple-system,Helvetica,sans-serif;',
    '  letter-spacing:.02em;padding:.5rem .8rem;display:flex;gap:.5rem;',
    '  align-items:center;box-shadow:0 2px 10px rgba(0,0,0,.28);text-align:left}',
    '.zeb:hover,.zeb:focus-visible{background:#141310}',
    '.zeb i{font-style:normal;font-weight:400;opacity:.85}',
    '.zeb b{font-weight:800}',
    '.zbar{position:fixed;left:0;right:0;bottom:0;z-index:10000;background:#141310;',
    '  color:#F2F0EB;padding:.7rem 1.1rem;display:flex;gap:1rem;align-items:center;',
    '  flex-wrap:wrap;font:400 13px/1.4 -apple-system,Helvetica,sans-serif}',
    '.zbar b{font-weight:700}',
    '.zbar a,.zbar button{color:#141310;background:#F2F0EB;border:0;cursor:pointer;',
    '  text-decoration:none;font:700 12px/1 -apple-system,sans-serif;padding:.55rem .8rem}',
    '.zbar .fin{margin-left:auto;background:transparent;color:#F2F0EB;',
    '  border:1.5px solid #56514a}',
    'body{padding-bottom:3.4rem}',
    '@media print{.zed,.zeb,.zbar{display:none}}'
  ].join('');
  document.head.appendChild(css);

  var zones = [].slice.call(document.querySelectorAll('[data-zone]'));
  var pieces = [];

  zones.forEach(function (el) {
    var cadre = document.createElement('div');
    cadre.className = 'zed';

    var bouton = document.createElement('button');
    bouton.className = 'zeb';
    bouton.type = 'button';
    bouton.innerHTML = '<b>' + el.dataset.zoneNom + '</b><i>· ' +
                       el.dataset.zoneQuoi + ' — modifier ↗</i>';

    /* Le clic ouvre la rubrique correspondante, dans un autre onglet :
       on garde la page sous les yeux pendant qu'on modifie. */
    bouton.addEventListener('click', function () {
      var c = el.dataset.zone;
      window.open(ADMIN + c + '/entries/' + (FICHIER[c] || c), '_blank', 'noopener');
    });
    bouton.addEventListener('mouseenter', function () { cadre.classList.add('zed--on'); });
    bouton.addEventListener('mouseleave', function () { cadre.classList.remove('zed--on'); });

    document.body.appendChild(cadre);
    document.body.appendChild(bouton);
    pieces.push({ el: el, cadre: cadre, bouton: bouton });
  });

  /* Les cadres suivent la page : elle bouge au défilement, au
     redimensionnement, et quand les images finissent de charger. */
  function placer() {
    pieces.forEach(function (p) {
      var r = p.el.getBoundingClientRect();
      var y = r.top + window.scrollY, x = r.left + window.scrollX;
      p.cadre.style.cssText += ';top:' + y + 'px;left:' + x + 'px;' +
        'width:' + r.width + 'px;height:' + r.height + 'px';
      /* L'étiquette se pose en haut de la zone, ou juste en dessous si la
         zone touche le bord supérieur de la page. */
      p.bouton.style.top = (y < 46 ? y + 6 : y - 34) + 'px';
      p.bouton.style.left = x + 'px';
    });
  }
  placer();
  addEventListener('scroll', placer, { passive: true });
  addEventListener('resize', placer);
  addEventListener('load', placer);
  setTimeout(placer, 600);
  setTimeout(placer, 1800);

  var barre = document.createElement('div');
  barre.className = 'zbar';
  barre.innerHTML =
    '<b>Mode modification</b>' +
    '<span>Cliquez sur un encadré pour changer ce qu’il contient. ' +
    zones.length + ' endroits modifiables sur cette page.</span>' +
    '<a href="/admin/">Toutes les rubriques</a>' +
    '<button class="fin" type="button">Quitter</button>';
  barre.querySelector('.fin').addEventListener('click', function () {
    location.href = location.pathname;
  });
  document.body.appendChild(barre);
})();
