# Rubrique des jauges de lecture — barème figé

> But : noter chaque billet sur deux axes **orthogonaux**, de façon **uniforme**
> (même barème pour tous) et **comparative** (les billets notés les uns par
> rapport aux autres, jamais dans le vide). À chaque nouveau billet, re-noter
> TOUT le corpus en un seul passage pour recalibrer l'étalon.
>
> Échelle : 3 crans, rendus `●○○` / `●●○` / `●●●`.

## Axe 1 — Prérequis (bagage externe supposé acquis)

Mesure le **savoir préalable** dont le lecteur a besoin, PAS la difficulté de lecture.
On peut avoir des prérequis élevés sans aucune technicité (ex. le cloud : zéro code,
mais il faut savoir ce que c'est).

| Cran | Règle | Test décisif |
|---|---|---|
| `●○○` Aucun | Tout terme spécialisé est défini dans le texte ; aucun savoir préalable requis. | Un lecteur sans bagage finit le billet sans ouvrir un autre onglet. |
| `●●○` Notions utiles | S'appuie sur 1 domaine que le lecteur gagne à connaître, mais que le texte explique au passage. | Compréhensible sans le bagage, plus confortable avec. |
| `●●●` Domaine supposé | Présume un domaine acquis et ne le réexplique pas entièrement. | Sans ce bagage, au moins un passage-clé reste opaque. |

## Axe 2 — Technicité (bagage technique : code, maths, formalisme)

Distinct du précédent. Mesure si suivre l'argument exige de **manipuler** du
technique (code, formule, jargon dev non traduit).

| Cran | Règle | Test décisif |
|---|---|---|
| `●○○` Non technique | Zéro code, zéro formule, zéro jargon dev non traduit ; tout passe par des images. | Un non-dev ne bute sur aucun symbole. |
| `●●○` Semi-technique | Mentionne des concepts techniques sans exiger de les manipuler. | On peut sauter 2-3 détails techniques sans perdre le fil. |
| `●●●` Technique | Exige de lire du code / des maths / un formalisme pour suivre l'argument. | Sauter le technique = perdre l'argument. |

## Procédure de notation (uniformité)

1. **Toujours comparatif** : noter les N billets ENSEMBLE, en un seul passage.
   Un billet n'a pas de note absolue — il a une note relative au corpus.
2. **Prompt gelé** : le juge reçoit cette rubrique verbatim + le texte des N billets.
   Pas d'évaluation « à l'œil » ad hoc.
3. **Ancrage** : si deux billets diffèrent sur un axe, le tableau doit pouvoir
   l'expliquer par une phrase concrète du texte (pas un ressenti).
4. **Recalibrage** : à chaque ajout de billet, re-noter tout le corpus.

## Rendu en frontmatter

Deux champs par billet :

```yaml
prerequis: 2      # 1..3  (Aucun / Notions utiles / Domaine supposé)
technicite: 1     # 1..3  (Non technique / Semi-technique / Technique)
```
