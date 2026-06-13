# Le déterminisme sous-traité au probabiliste — mesure

**Question.** Une tâche à réponse mécanique (« lister les fonctions d'un module qui
renvoient un type donné ») peut être confiée à un agent LLM de quatre façons.
Laquelle est juste, reproductible, et à quel prix ?

## Protocole

- **Corpus.** Le package `axm-git`, figé au tag `git/v0.4.0` (= PyPI `axm-git==0.4.0`,
  publiquement rejouable via `pip download axm-git==0.4.0`). 30 fichiers, ~3 700 lignes.
- **Tâche.** « Liste toutes les fonctions/méthodes dont le type de retour est
  `ToolResult`, y compris les unions comme `ToolResult | None`. »
- **Vérité-terrain.** Dérivée par AST : **18 fonctions/méthodes** (14 en `-> ToolResult`
  exact + **4 en union** : `ToolResult | None` ×3, `ToolResult | tuple[...]` ×1).
  Vérifiée par 3 méthodes indépendantes (ast_search MCP, deux extracteurs AST distincts)
  — 0 faux positif, 0 faux négatif. **Un grep naïf `-> ToolResult` n'attrape que 14/18.**
- **Modèle.** Claude Haiku 4.5 (`claude-haiku-4-5-20251001`), identique pour tous les bras.
- **Mesure.** Via `axm-harness` (HarnessRun : tokens, appels d'outils, durée). Coût \$
  calculé au tarif public Haiku (1 / 5 / 0,10 \$ par Mtok input/output/cache-read), pas
  le \$ indicatif du SDK (mode abonnement).
- **N = 8 runs par régime** (32 runs au total).

## Les quatre régimes

| Régime | Outils donnés | Consigne |
|---|---|---|
| **A — au jugé** | Read, Grep, Glob | « tu n'as pas d'outil d'analyse, lis le code toi-même » |
| **B — agent + outil libre** | Bash | « lance `axm ast_search`, puis rapporte » (libre de re-vérifier) |
| **C — grep expert** | Bash | « tu as grep/rg/awk, combine-les en expert » (pas d'`ast_search`) |
| **B′ — outil pur** | Bash, `max_turns=2` | « lance `axm ast_search` UNE fois, fais confiance, ne re-vérifie pas » |

## Résultats (moyenne sur N=8)

| Régime | \$/run | σ \$ | appels | exact. /18 | unions /4 | total = 18 ? |
|---|---|---|---|---|---|---|
| **A** au jugé | 0,081 | ±0,013 | 17,9 | (10/10 dist.) | — | **8/8** ✓ |
| **B** agent + outil libre | 0,059 | **±0,052** | 10,8 | — | — | **3/8** (a dit **117** ×1) |
| **C** grep expert | 0,068 | ±0,033 | 15,6 | **13,1/18** (min **5**) | **2,9/4** | 4/8 |
| **B′** outil pur | **0,011** | ±0,001 | **1,0** | **18,0/18** | **4,0/4** | **8/8** ✓ |

## Lecture

1. **B′ (outil pur, appelé sans le re-juger) est parfait et déterministe.** 8 runs sur 8 :
   un appel, 18/18, 4/4 unions, total 18, ~0,011 \$, écart-type quasi nul. C'est la borne idéale.

2. **Dès qu'un agent *raisonne autour* de la tâche, il devient cher, faillible et instable.**
   - **A** relit le code : juste (10/10) mais ~7,4× plus cher que B′, 17,9 appels.
   - **B** appelle l'outil *puis se met à le vérifier* : un run a affirmé **117** hits (au lieu de 18),
     seulement 3 runs sur 8 ont donné le bon total. Le tâtonnement ré-introduit l'aléa.
   - **C** (grep « expert ») rate les unions : **13,1/18** en moyenne, **3 runs effondrés à 5/18**,
     2 runs sans total. « Un bon grep suffit » est réfuté par les données.

3. **Le coût n'est pas l'argument central — l'exactitude et le déterminisme le sont.**
   Le même travail déterministe, fait par un agent qui *réfléchit*, n'est ni reproductible
   ni certifiable. Fait par un outil déterministe qu'on *appelle sans le re-deviner*, il est
   exact à tous les coups. Un résultat déterministe ne vaut que si on lui fait confiance.

## Reproduire

```bash
pip download axm-git==0.4.0          # le corpus exact mesuré
# vérité-terrain : tout symbole dont l'annotation de retour contient ToolResult → 18
# (un grep `-> ToolResult` en trouve 14 ; il rate les 4 unions)
```

Scripts : `run.py` (A, B), `run_bc.py` (B′, C). Métriques brutes : `metrics.json` (32 runs).

## Précisions méthodologiques (pour qui creuse)

Deux nuances que le billet ne détaille pas, et qui toutes deux vont dans le sens
des conclusions (elles ne les contredisent pas) :

- **Le score `found_of_18` compte des *noms*, pas des *définitions* exactes.**
  Plusieurs méthodes `execute` sont homonymes (chaque AXMTool a la sienne). Un
  agent qui liste les 18 noms distincts obtient donc 18/18 même s'il ne distingue
  pas les `execute` entre eux. Sans conséquence pour B′ (ses sorties listent bien
  les 18 lignes), mais c'est une approximation : « 18/18 » signifie « les 18 noms
  apparaissent », pas « les 18 définitions identifiées sans ambiguïté ».

- **Le bras C est en réalité *plus* faux que son score ne le dit.** Sur un run
  (`C_bash_expert` idx 7, le run à 5/18), l'agent a non seulement raté des noms
  mais *inventé des numéros de ligne* : `runner.py:192` et `:407` au lieu des
  vrais `:32` et `:221`. Le scorer ne vérifiant que les noms, cette hallucination
  d'emplacement n'apparaît pas dans les chiffres — mais elle confirme l'argument :
  le shell générique, livré à lui-même, n'a aucune garantie d'exactitude. (C'est
  le seul run sur 32 où des lignes sont fausses ; partout ailleurs les lignes
  citées sont correctes.)
