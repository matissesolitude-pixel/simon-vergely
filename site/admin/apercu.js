/* =====================================================================
   LE VOLET D'APERÇU DE L'INTERFACE D'ÉDITION

   LE PROBLÈME QUE ÇA RÈGLE. Une interface d'édition nue montre des champs
   et rien d'autre : Simon dépose une image sans savoir sur quelle page elle
   atterrit, dans quel format, ni à côté de quoi. Il tape dans le vide.

   CE QUE FAIT CE FICHIER. À droite de chaque formulaire, il affiche
     1. UN BANDEAU DE LOCALISATION — « Page d'accueil › Les mondes
        déformés », avec un lien pour aller voir la vraie page ;
     2. LE RENDU RÉEL — la même feuille de style que le site, donc les
        mêmes polices, les mêmes cadres, les mêmes proportions.

   Ce qu'il voit à droite, c'est ce qui sortira. C'est tout l'objet.
   ===================================================================== */

(function () {
  var SITE = 'https://resilient-cuchufli-a778a1.netlify.app';

  /* La feuille du site, écrite par construire.py à chaque construction :
     l'aperçu ne peut pas dériver du site, il lit la même source. */
  CMS.registerPreviewStyle('/assets/apercu.css');

  /* Un peu d'habillage propre à l'aperçu, lui seul. */
  CMS.registerPreviewStyle(
    'body{padding:0;background:var(--papier)}' +
    '.ou{position:sticky;top:0;z-index:9;background:#141310;color:#F2F0EB;' +
    '  padding:.7rem 1.1rem;font:600 12px/1.45 -apple-system,Helvetica,sans-serif;' +
    '  letter-spacing:.02em;display:flex;gap:.7rem;align-items:baseline;flex-wrap:wrap}' +
    '.ou b{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:#E8481F}' +
    '.ou a{color:#F2F0EB;margin-left:auto}' +
    '.ou i{font-style:normal;opacity:.62;font-weight:400}' +
    '.vide{padding:2.4rem 1.4rem;color:#5A554A;font:400 14px/1.6 -apple-system,sans-serif}' +
    '.zone{padding:1.6rem 1.4rem 2.2rem}',
    { raw: true }
  );

  /* -------------------------------------------------------------------
     Outils. Decap fournit `h` (createElement) sur window.
     On construit le HTML en chaîne puis on l'injecte : ça permet de
     réutiliser les classes du site telles quelles, sans les retranscrire. */

  function ech(v) {
    return String(v == null ? '' : v)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* Une image peut être un nom nu (données d'origine) ou un chemin complet
     (déposé par l'interface). Même règle que dans construire.py. */
  function src(v) {
    if (!v) return '';
    v = String(v);
    if (v.indexOf('blob:') === 0 || v.indexOf('data:') === 0) return v;
    return '/assets/img/' + v.split('/').pop();
  }

  function liste(v) {
    if (!v) return [];
    return v.toJS ? v.toJS() : v;
  }

  function bandeau(page, section, note) {
    var lien = page === 'Page Travail' ? '/travail.html'
             : page === 'Travailler ensemble' ? '/ensemble.html'
             : page === 'Toutes les pages' ? '/index.html' : '/index.html';
    return '<div class="ou"><b>' + ech(page) + '</b><span>' + ech(section) + '</span>' +
      (note ? '<i>' + ech(note) + '</i>' : '') +
      '<a href="' + SITE + lien + '" target="_blank" rel="noopener">Voir la vraie page ↗</a></div>';
  }

  function vide(msg) {
    return '<p class="vide">' + ech(msg) + '</p>';
  }

  function rendu(html) {
    return h('div', { dangerouslySetInnerHTML: { __html: html } });
  }

  function figures(items, ratio) {
    if (!items.length) return vide('Rien pour le moment. Ajoutez une entrée à gauche.');
    return '<div class="grille" style="margin-top:0">' + items.map(function (x) {
      var s = src(x.f);
      return '<figure class="oeuvre">' +
        (s ? '<img src="' + ech(s) + '" style="aspect-ratio:' + ratio + '" alt="">'
           : '<div style="aspect-ratio:' + ratio + ';background:#E7E4DC"></div>') +
        '<figcaption>' + ech(x.vu || '(légende à écrire)') + '</figcaption></figure>';
    }).join('') + '</div>';
  }

  /* -------------------------------------------------------------------
     MES TRAVAUX — deux registres, deux emplacements différents.
     C'est la rubrique où l'on se perd le plus : on montre donc les deux
     destinations côte à côte, dans l'ordre du site. */

  CMS.registerPreviewTemplate('travaux', createClass({
    render: function () {
      var d = this.props.entry.getIn(['data']);
      var f = d.get('films'), m = d.get('mondes');
      var fl = liste(f && f.get('liste')), ml = liste(m && m.get('liste'));

      /* Les mondes qui ont un reel s'affichent en vidéo sur l'accueil :
         ils ne doivent pas apparaître deux fois. On le dit ici aussi. */
      return rendu(
        bandeau('Page Travail', 'Les films', 'les huit visuels, en paysage') +
        '<div class="zone"><span class="eti">' + ech(f && f.get('titre') || '') + '</span>' +
        '<p class="chapeau" style="margin-top:0">' + ech(f && f.get('chapeau') || '') + '</p>' +
        '<div style="margin-top:1.4rem">' + figures(fl, '16/9') + '</div></div>' +

        bandeau('Page d’accueil', 'Les mondes déformés',
                'sous les vidéos, en portrait') +
        '<div class="zone"><span class="eti">' + ech(m && m.get('titre') || '') + '</span>' +
        '<p class="chapeau" style="margin-top:0">' + ech(m && m.get('chapeau') || '') + '</p>' +
        '<div style="margin-top:1.4rem">' + figures(ml, '3/4') + '</div>' +
        '<p class="chapeau" style="font-size:.92rem">Ceux qui ont un reel dans ' +
        '« Mes reels » s’affichent en vidéo plus haut sur la page, et ' +
        'disparaissent d’eux-mêmes de cette grille.</p></div>'
      );
    }
  }));

  /* -------------------------------------------------------------------
     MES REELS — la première chose qu'on voit bouger sur l'accueil. */

  CMS.registerPreviewTemplate('publications', createClass({
    render: function () {
      var r = liste(this.props.entry.getIn(['data', 'reels']));
      var corps = r.length
        ? '<div class="reels">' + r.map(function (x) {
            var s = src(x.apercu);
            return '<figure class="reel reel--repli">' +
              (s ? '<img src="' + ech(s) + '" alt="">'
                 : '<div style="aspect-ratio:3/4;background:#E7E4DC"></div>') +
              '<figcaption>' + ech(x.vu || '(légende à écrire)') +
              '<br><span>code : ' + ech(x.code || '—') + '</span></figcaption></figure>';
          }).join('') + '</div>'
        : vide('Aucun reel. Ajoutez-en un à gauche avec son code Instagram.');

      return rendu(
        bandeau('Page d’accueil', 'Les vidéos, en haut de la section',
                'elles défilent de gauche à droite') +
        '<div class="zone">' + corps +
        '<p class="chapeau" style="font-size:.92rem">Ici on voit l’image de ' +
        'secours. Sur le site, c’est la vraie vidéo Instagram qui joue à cet ' +
        'endroit, sans quitter la page.</p></div>'
      );
    }
  }));

  /* -------------------------------------------------------------------
     MES CLIENTS — le bandeau noir, sur les trois pages. */

  CMS.registerPreviewTemplate('clients', createClass({
    render: function () {
      var l = liste(this.props.entry.getIn(['data', 'logos']));
      var une = l.map(function (x) {
        var s = src(x.f);
        return s ? '<img src="' + ech(s) + '" alt="' + ech(x.nom || '') + '">' : '';
      }).join('');
      return rendu(
        bandeau('Toutes les pages', 'Le bandeau qui défile',
                'les premiers de la liste passent en premier') +
        (l.length
          ? '<div class="bandeau"><p class="bandeau__t">Ils lui ont confié un film</p>' +
            '<div class="piste">' + une + une + '</div></div>'
          : vide('Aucun logo.')) +
        '<div class="zone"><p class="chapeau" style="font-size:.92rem">Les logos ' +
        'sont affichés en blanc sur fond noir. Un logo sombre sur fond ' +
        'transparent deviendra invisible : prenez la version claire.</p></div>'
      );
    }
  }));

  /* -------------------------------------------------------------------
     MES COORDONNÉES — en pied de page partout, et sur les boutons. */

  CMS.registerPreviewTemplate('coordonnees', createClass({
    render: function () {
      var d = this.props.entry.getIn(['data']);
      var mail = d.get('mail') || '', tel = d.get('tel') || '';
      var aff = d.get('tel_affiche') || '', ig = d.get('instagram') || '';
      var alerte = /^\+[0-9]{8,15}$/.test(tel) ? ''
        : '<p class="chapeau" style="color:#E8481F;font-weight:600">Le téléphone ' +
          'doit commencer par + et l’indicatif, sans espace — sinon les ' +
          'boutons Appeler et SMS ne marcheront pas. Exemple : +33769051349</p>';
      return rendu(
        bandeau('Toutes les pages', 'Le pied de page, et les boutons de contact') +
        '<footer class="pied"><div class="pied__in">' +
        '<div><h4>Simon Vergély</h4><p>Animateur 2D et motion designer.<br>' +
        'Teasers, bandes-annonces, publicités, logos animés.</p></div>' +
        '<div><h4>Écrire</h4><p>' + ech(mail) + '</p><p>' + ech(aff) + '</p></div>' +
        '<div><h4>Suivre</h4><p>@' + ech(ig) + '</p></div></div></footer>' +
        '<div class="zone"><div class="ouv__act" style="margin-top:0">' +
        '<span class="b">Écrire un mail</span>' +
        '<span class="b b--nu">Envoyer un SMS</span>' +
        '<span class="b b--nu">Appeler</span></div>' + alerte + '</div>'
      );
    }
  }));

  /* -------------------------------------------------------------------
     MON HISTOIRE — la page Travailler ensemble, de haut en bas. */

  CMS.registerPreviewTemplate('histoire', createClass({
    render: function () {
      var d = this.props.entry.getIn(['data']);
      var ch = liste(d.get('chapitres')), fo = liste(d.get('formats')),
          co = liste(d.get('comment'));
      return rendu(
        bandeau('Travailler ensemble', 'Toute la page') +
        '<div class="zone"><p class="chapeau" style="margin-top:0">' +
        ech(d.get('promesse') || '') + '</p>' +

        '<div class="formats">' + fo.map(function (f) {
          return '<div class="format"><h3>' + ech(f.nom || '') + '</h3>' +
            '<p>' + ech(f.quoi || '') + '</p>' +
            '<p class="format__q">' + ech(f.pour || '') + '</p></div>';
        }).join('') + '</div>' +

        '<h2 style="margin-top:2.4rem">' + ech(d.get('comment_titre') || '') + '</h2>' +
        '<p class="chapeau">' + ech(d.get('comment_chapeau') || '') + '</p>' +
        '<ol class="etapes">' + co.map(function (e) {
          return '<li><b>' + ech(e.n || '') + '</b><div><h3>' + ech(e.t || '') +
            '</h3><p>' + ech(e.d || '') + '</p></div></li>';
        }).join('') + '</ol>' +

        '<div class="chapitres" style="margin-top:2.4rem">' + ch.map(function (c) {
          var tx = liste(c.texte).map(function (p) { return '<p>' + ech(p) + '</p>'; }).join('');
          return '<article class="chap"><h3>' + ech(c.titre || '') + '</h3>' + tx +
            '<blockquote>«&nbsp;' + ech(c.citation || '') + '&nbsp;»</blockquote></article>';
        }).join('') + '</div></div>'
      );
    }
  }));

  /* -------------------------------------------------------------------
     NOMBRE D'ABONNÉS — le badge de l'en-tête, et le premier chiffre. */

  CMS.registerPreviewTemplate('instagram', createClass({
    render: function () {
      var d = this.props.entry.getIn(['data']);
      var n = Number(d.get('abonnes') || 0);
      var txt = n ? n.toLocaleString('fr-FR').replace(/ |,/g, ' ') : '—';
      var dt = String(d.get('releve') || '').slice(0, 10);
      return rendu(
        bandeau('Toutes les pages', 'Le badge en haut à droite, et le premier chiffre') +
        '<div class="zone"><div class="tete__act" style="justify-content:flex-start">' +
        '<span class="badge"><b>' + ech(txt) + '</b></span></div>' +
        '<div class="chiffres" style="margin-top:1.6rem">' +
        '<div class="chiffre"><b>' + ech(txt) + '</b>' +
        '<span>abonnés sur Instagram, au ' + ech(dt) + '</span></div></div>' +
        '<p class="chapeau" style="font-size:.92rem">Une fois le compte relié, ' +
        'ce chiffre se met à jour tout seul quatre fois par jour et cette ' +
        'rubrique devient inutile.</p></div>'
      );
    }
  }));
})();
