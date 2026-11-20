from lib import *
import numpy as np

rng = np.random.default_rng(7)
DOSE = np.array([2, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9, 10], float)
C0 = np.round(1.05 * DOSE + 1.6 + rng.normal(0, 1.1, 12), 1)
W, B = np.polyfit(DOSE, C0, 1)
MSE = float(np.mean((C0 - (W * DOSE + B)) ** 2))

def fig_sets():
    f = Fig(800, 600, "Trois ensembles emboîtés : intelligence artificielle, apprentissage automatique, apprentissage profond")
    f.rect(10, 20, 780, 560, "#F2F4F8", GRID, 3, 24)
    f.rect(120, 150, 640, 410, PALE, BLUE, 3, 24)
    f.rect(300, 300, 430, 235, WHITE, BLUE, 5, 24)
    f.lab(40, 44, "Intelligence artificielle", 700, cls="axw ax-b")
    f.lab(40, 86, "faire exécuter par une machine une tâche qui demande du raisonnement", 700)
    f.lab(150, 172, "Apprentissage automatique", 580, cls="axw ax-b")
    f.lab(150, 214, "la règle est apprise à partir d’exemples", 580)
    f.lab(328, 322, "Apprentissage profond", 380, cls="axw ax-b")
    f.lab(328, 364, "réseaux de neurones à nombreuses couches : images, texte, séquences", 380)
    return f

def fig_two_ways():
    f = Fig(1500, 470, "Deux façons de programmer : règles écrites, ou règles apprises")
    for j, (y, a, b, c, col) in enumerate([(30, "Données", "Règles écrites<br>par un expert", "Réponses", GREY), (270, "Données", "Réponses<br>connues", "Règle apprise<br>(le modèle)", BLUE)]):
        f.box(260, y, 300, 76, a, WHITE, col, "axw ax-b")
        f.box(260, y + 96, 300, 86, b, WHITE, col, "axw ax-b", lines=2)
        f.box(720, y + 30, 330, 120, "Programme classique" if j == 0 else "Apprentissage", PALE if j else "#F2F4F8", col, "axw ax-b")
        f.box(1210, y + 40, 290, 100, c, PALE if j else WHITE, col, "axw ax-b", lines=c.count("<br>") + 1)
        f.arrow(566, y + 38, 712, y + 70, INK); f.arrow(566, y + 140, 712, y + 110, INK); f.arrow(1056, y + 90, 1202, y + 90, INK)
    f.lab(0, 96, "Hier", 220, cls="axh", color=GREY)
    f.lab(0, 336, "Ici", 220, cls="axh")
    return f

def fig_scatter(line=False, resid=False, extrap=False):
    f = Fig(800, 600, "Concentration résiduelle de tacrolimus en fonction de la dose, 12 patients fictifs")
    xr = (0, 20) if extrap else (0, 12)
    yr = (0, 24) if extrap else (0, 16)
    f.axes(130, 70, 760, 500, xr, yr, range(0, xr[1] + 1, 5 if extrap else 2), range(0, yr[1] + 1, 6 if extrap else 4), "Dose (mg/jour)", "Concentration résiduelle (ng/mL)")
    if extrap:
        f.rect(f.X(10.6), 70, f.X(20) - f.X(10.6), 430, PINK, None)
        f.curve([10.6, 20], [W * 10.6 + B, W * 20 + B], RED, 5, "12 10")
        f.lab(f.X(10.6) + 16, 96, "aucun patient ici", 260, cls="axh", color=RED)
    if line:
        f.curve([1, 10.6], [W * 1 + B, W * 10.6 + B], BLUE, 5)
    if resid:
        for a, b in zip(DOSE, C0):
            f.line(f.X(a), f.Y(b), f.X(a), f.Y(W * a + B), RED, 5)
    f.dots(DOSE, C0, INK, 10)
    if line and not extrap and not resid:
        f.lab(f.X(7.4), f.Y(W * 9 + B) - 74, "le modèle", 200, cls="axh")
    if resid:
        f.lab(f.X(0.6), 84, "en rouge : l’erreur", 320, cls="axh", color=RED)
    return f

def fig_bowl():
    f = Fig(800, 600, "Erreur moyenne en fonction de la pente w : une cuvette dont le fond est la meilleure pente")
    ws = np.linspace(0.2, 2.0, 60)
    es = [float(np.mean((C0 - (w * DOSE + B)) ** 2)) for w in ws]
    f.axes(130, 70, 760, 500, (0.2, 2.0), (0, 30), [0.5, 1.0, 1.5, 2.0], [0, 10, 20, 30], "Pente w", "Erreur moyenne", fmt=lambda v: str(v).replace(".", ","))
    f.curve(ws, es, BLUE, 5)
    path = [0.42, 0.62, 0.78, 0.9, 0.98, float(W)]
    for a, b in zip(path[:-1], path[1:]):
        ea, eb = float(np.mean((C0 - (a * DOSE + B)) ** 2)), float(np.mean((C0 - (b * DOSE + B)) ** 2))
        f.arrow(f.X(a), f.Y(ea) - 16, f.X(b), f.Y(eb) - 16, RED, 4, 14)
    f.circle(f.X(W), f.Y(MSE), 13, RED)
    f.lab(f.X(0.45) + 20, f.Y(27), "on descend pas à pas", 340, cls="axh", color=RED)
    f.lab(f.X(W) - 40, f.Y(MSE) - 120, "meilleure pente", 300, cls="axh")
    return f

def build():
    S = Session(1, "fr", "Partie I · Fondamentaux", "Apprendre à partir de données", "Ce que veut dire « apprentissage automatique », sur un exemple de suivi thérapeutique.")
    w, b, mse = f"{W:.2f}".replace(".", ","), f"{B:.1f}".replace(".", ","), f"{MSE:.1f}".replace(".", ",")
    S.sec("Ouverture : la situation de départ, les objectifs et le plan.")
    S.cover("Bonjour à toutes et à tous. Cette séance ouvre le cours d’intelligence artificielle pour les sciences pharmaceutiques. Le cours compte dix séances. Les quatre premières, en français, s’adressent à tout le monde : aucune connaissance en programmation n’est nécessaire. Les six suivantes, en anglais, vont plus loin et s’adressent aux étudiants de master recherche, aux doctorants et aux chercheurs. Aujourd’hui, une seule question : que veut dire « apprendre » pour une machine ?")
    S.sit("Prévoir la prochaine mesure", "Un patient greffé du rein prend du <b>tacrolimus</b>. À chaque visite, on mesure sa concentration résiduelle dans le sang. Trop basse, le greffon est menacé de rejet. Trop haute, le médicament devient toxique pour le rein.<br><br>Vous disposez du dossier de 40 patients : doses, dates, mesures.",
          "Comment une machine peut-elle apprendre à prévoir la prochaine concentration ?",
          "Partons d’une situation concrète. Un patient greffé du rein prend du tacrolimus, un immunosuppresseur à marge thérapeutique étroite. Trop peu, et le greffon risque le rejet. Trop, et le médicament abîme le rein. On mesure donc régulièrement la concentration résiduelle. Imaginez que vous disposiez du dossier de quarante patients. La question du jour : comment une machine pourrait-elle apprendre, à partir de ces dossiers, à prévoir la prochaine mesure ? C’est le même jeu de données fictif que dans le cours de programmation.")
    S.obj(["Distinguer intelligence artificielle, apprentissage automatique et apprentissage profond.",
           "Nommer les trois ingrédients d’un apprentissage : données, modèle, fonction de coût.",
           "Expliquer comment un modèle simple se règle pour réduire son erreur.",
           "Reconnaître le type d’apprentissage adapté à une question pharmaceutique."],
          "Voici ce que vous saurez faire à la fin. D’abord, distinguer trois termes que l’on confond souvent : intelligence artificielle, apprentissage automatique, apprentissage profond. Ensuite, nommer les trois ingrédients de tout apprentissage. Puis expliquer, sur un exemple très simple, comment un modèle se règle tout seul. Enfin, reconnaître quel type d’apprentissage convient à une question donnée.")
    S.plan([("Trois mots à ne pas confondre", "IA, apprentissage automatique, apprentissage profond"),
            ("Un premier modèle : une droite", "De la dose à la concentration, sur 12 patients"),
            ("Comment le modèle se règle", "L’erreur, et la façon de la réduire"),
            ("Quatre façons d’apprendre", "Et ce qu’un modèle n’apprend pas")],
           "La séance a quatre parties. Nous commencerons par le vocabulaire. Nous construirons ensuite le modèle le plus simple possible : une droite. Nous verrons comment cette droite se règle pour coller aux données. Et nous finirons par les grandes familles d’apprentissage, avec leurs limites.")
    S.sec("Le vocabulaire : trois ensembles emboîtés, et la différence entre une règle écrite et une règle apprise.")
    S.pts("Trois mots emboîtés", "L’apprentissage profond est une partie de l’apprentissage automatique, lui-même une partie de l’IA.",
          ["<b>IA</b> : le but. Faire exécuter une tâche qui demande du raisonnement.", "<b>Apprentissage automatique</b> : un moyen. La règle vient des exemples.", "<b>Apprentissage profond</b> : une famille de modèles, les réseaux de neurones."],
          "Trois mots, trois ensembles emboîtés. L’intelligence artificielle, c’est le but : faire exécuter par une machine une tâche qui demande du raisonnement. Un logiciel d’interactions médicamenteuses fondé sur des règles écrites à la main, c’est déjà de l’IA. L’apprentissage automatique est un moyen d’y arriver : au lieu d’écrire la règle, on la fait apprendre à partir d’exemples. L’apprentissage profond, enfin, est une famille particulière de modèles, les réseaux de neurones à nombreuses couches. Ce sont eux qui ont rendu possibles les assistants conversationnels et l’analyse d’images.",
          fig=fig_sets())
    S.wide("Règle écrite ou règle apprise ?", "Dans les deux cas, on part des données. Ce qui change : qui écrit la règle.", fig_two_ways(),
           "Voici la différence essentielle. Dans un programme classique, un expert écrit les règles : si la clairance est inférieure à tel seuil, réduire la dose. La machine applique. Dans l’apprentissage automatique, on fournit des données et les réponses connues, par exemple les concentrations réellement mesurées. C’est l’algorithme qui cherche la règle. Cette règle apprise, on l’appelle le modèle. Conséquence importante : un modèle ne vaut jamais mieux que les exemples qu’on lui a montrés.",
           band="Un modèle, c’est une règle trouvée par le calcul à partir d’exemples.")
    S.sec("Un premier modèle : une droite entre la dose et la concentration, et la mesure de son erreur.")
    S.pts("Douze patients, deux colonnes", "Chaque point est un patient : sa dose, et la concentration mesurée.",
          ["La concentration monte avec la dose : il y a une <b>tendance</b>.", "À dose égale, les patients diffèrent : il y a de la <b>variabilité</b>.", "Peut-on résumer la tendance par une règle simple ?"],
          "Commençons petit. Douze patients, et deux colonnes : la dose quotidienne, et la concentration résiduelle mesurée. Chaque point du graphique est un patient. Que voit-on ? D’abord une tendance : plus la dose est élevée, plus la concentration l’est aussi. Ensuite de la variabilité : à cinq milligrammes par jour, deux patients n’ont pas la même concentration. C’est normal, ils n’éliminent pas le médicament à la même vitesse. La question : peut-on résumer la tendance par une règle simple ?",
          fig=fig_scatter(), widget="fitline")
    S.eq("Le modèle le plus simple : une droite", "Deux nombres suffisent à la décrire.", r"\hat{y} = w\,x + b",
         [(r"x", "La <b>dose</b>, en mg/jour : ce que l’on connaît. On l’appelle l’entrée, ou la variable explicative."),
          (r"\hat{y}", "La <b>concentration prédite</b>, en ng/mL. L’accent circonflexe signifie « estimé par le modèle »."),
          (r"w", "La <b>pente</b> : de combien la prédiction monte quand la dose augmente de 1 mg/jour."),
          (r"b", "L’<b>ordonnée à l’origine</b> : la valeur prédite pour une dose nulle. Un simple décalage.")],
         "Le modèle le plus simple est une droite. Lisons la formule, symbole par symbole. x, c’est la dose : ce que l’on connaît. y chapeau, c’est la concentration prédite ; le chapeau signifie toujours « estimé par le modèle », par opposition à y, la valeur réellement mesurée. w est la pente : de combien la prédiction augmente pour un milligramme de plus. Et b est un décalage. w et b sont les deux paramètres du modèle. Ce sont les deux boutons que l’on va régler.",
         band="Apprendre, ici, c’est choisir les deux paramètres w et b.")
    S.eq("Mesurer l’erreur du modèle", "On compare chaque prédiction à la valeur mesurée.", r"E(w,b) = \frac{1}{n}\sum_{i=1}^{n}\left(y_i - \hat{y}_i\right)^2",
         [(r"y_i - \hat{y}_i", "L’<b>écart</b> entre la mesure et la prédiction pour le patient numéro i : les segments rouges."),
          (r"(\cdot)^2", "On élève au carré : un écart de −2 compte autant qu’un écart de +2, et les gros écarts pèsent lourd."),
          (r"\frac{1}{n}\sum_{i=1}^{n}", "On fait la <b>moyenne</b> sur les n patients (ici n = 12).")],
         f"Pour régler les boutons, il faut une mesure de qualité. Pour chaque patient, on calcule l’écart entre la concentration mesurée et la concentration prédite : ce sont les segments rouges. On élève chaque écart au carré, pour que les erreurs positives et négatives ne se compensent pas, et pour pénaliser davantage les grosses erreurs. Puis on fait la moyenne. Ce nombre s’appelle l’erreur quadratique moyenne. C’est notre fonction de coût : plus elle est petite, mieux la droite colle aux points. Ici, la meilleure droite donne une erreur de {mse}.",
         fig=fig_scatter(line=True, resid=True), band="Ce nombre s’appelle la fonction de coût.")
    S.sec("Comment le modèle se règle : descendre la pente de l’erreur, pas à pas.")
    S.pts("Apprendre, c’est descendre", "On trace l’erreur pour chaque valeur possible de la pente.",
          ["La courbe a la forme d’une cuvette.", "On part d’une pente au hasard.", "On regarde de quel côté l’erreur diminue, et on fait un petit pas.", f"On recommence. Au fond : w = {w}."],
          f"Comment trouver les bonnes valeurs ? Traçons l’erreur pour toutes les pentes possibles. On obtient une cuvette. L’algorithme part d’une pente choisie au hasard, à gauche. Il regarde de quel côté l’erreur diminue, et fait un petit pas dans cette direction. Puis il recommence. Pas après pas, il descend au fond de la cuvette. Cette méthode s’appelle la descente de gradient. Ici, elle s’arrête à une pente de {w} : chaque milligramme supplémentaire ajoute environ un nanogramme par millilitre. Retenez l’image : c’est exactement ainsi que s’entraînent les plus grands modèles, avec des milliards de boutons au lieu de deux.",
          fig=fig_bowl(), band="Cette méthode s’appelle la descente de gradient.", widget="descent")
    S.cols("Les trois ingrédients d’un apprentissage", "Vous les retrouverez dans tous les modèles du cours, du plus simple au plus grand.",
           [("1. Des données", "Des exemples, avec ce que l’on veut prédire. Ici : 12 patients, leur dose, leur concentration."),
            ("2. Un modèle", "Une famille de règles possibles, avec des paramètres à régler. Ici : toutes les droites, avec w et b."),
            ("3. Une fonction de coût", "Un nombre qui dit si la règle est bonne. Ici : l’erreur quadratique moyenne.")],
           "Résumons. Tout apprentissage repose sur trois ingrédients. Des données : des exemples, avec ce que l’on veut prédire. Un modèle : une famille de règles possibles, dotée de paramètres réglables. Et une fonction de coût, qui dit par un nombre si la règle est bonne. On ajoute un quatrième élément, l’algorithme d’optimisation, qui règle les paramètres pour faire baisser le coût. Devant n’importe quel système d’IA, posez ces trois questions : quelles données ? quel modèle ? quel coût ?",
           band="Un algorithme d’optimisation règle les paramètres pour faire baisser le coût.")
    S.sec("Les quatre familles d’apprentissage, un exercice de classement, et les limites.")
    S.tbl("Quatre façons d’apprendre", "Ce qui change : la nature de l’information fournie au modèle.", ["Famille", "Ce que l’on fournit", "Exemple pharmaceutique"],
          [["Supervisé", "Des exemples avec la bonne réponse", "Prédire la concentration à partir de la dose et du poids"],
           ["Non supervisé", "Des exemples seuls, sans réponse", "Regrouper des patients qui se ressemblent"],
           ["Auto-supervisé", "Des exemples dont on cache une partie", "Deviner un mot masqué dans une notice : c’est ainsi qu’apprennent les modèles de langage"],
           ["Par renforcement", "Des essais et une récompense", "Ajuster une dose pas à pas, en simulation"]],
          "Il existe quatre grandes familles. En apprentissage supervisé, chaque exemple vient avec la bonne réponse : c’est notre droite. En non supervisé, il n’y a pas de réponse ; on cherche une structure, par exemple des groupes de patients. En auto-supervisé, on cache une partie des données et le modèle doit la deviner : c’est ainsi que sont entraînés les modèles de langage. Enfin, par renforcement, le modèle essaie des actions et reçoit une récompense. En santé, cela se fait en simulation, jamais directement sur des patients.",
          widths=[20, 34, 46])
    S.ex("Quelle famille pour quelle question ?", ["Un laboratoire dispose de 5 000 molécules dont la toxicité hépatique a été testée. Il veut prédire celle de nouvelles molécules.",
          "Une pharmacie hospitalière veut repérer des profils de prescription inhabituels, sans savoir à l’avance lesquels.",
          "Un modèle lit des millions de résumés d’articles en devinant les mots cachés.",
          "Pour chacune : quelle famille ? Quelles sont les données, et que cherche-t-on à prédire ?"],
         dict(time="5 minutes", mat="Une feuille", out="Trois lignes : famille, données, cible"),
         "À vous. Voici trois situations. Un laboratoire possède cinq mille molécules dont la toxicité hépatique est connue, et veut prédire celle de nouvelles molécules. Une pharmacie hospitalière veut repérer des prescriptions inhabituelles, sans savoir lesquelles à l’avance. Un modèle lit des millions de résumés d’articles en devinant des mots cachés. Pour chacune, donnez la famille d’apprentissage, les données, et ce que l’on cherche à prédire. Prenez cinq minutes.")
    S.sol("Quelle famille pour quelle question ?", ["<b>Toxicité des molécules</b> : supervisé. Données : la structure. Cible : toxique ou non.", "<b>Prescriptions inhabituelles</b> : non supervisé. Aucune réponse connue ; on cherche ce qui s’écarte des autres.", "<b>Mots cachés</b> : auto-supervisé. La réponse est dans le texte lui-même."],
          "La correction. La toxicité : c’est du supervisé, puisque la réponse est connue pour cinq mille molécules. L’entrée est la structure de la molécule, la cible est « toxique » ou « non toxique ». Les prescriptions inhabituelles : c’est du non supervisé, personne n’a étiqueté les prescriptions. Les mots cachés : c’est de l’auto-supervisé. Personne n’a eu besoin d’annoter les textes, la réponse est dans le texte lui-même. C’est ce qui permet d’utiliser d’immenses quantités de données.",
          band="Le bon réflexe : chercher d’abord si la bonne réponse est disponible.")
    S.pts("Ce qu’un modèle n’apprend pas", "Trois limites à garder en tête dès maintenant.",
          ["<b>Hors des données, il extrapole.</b> Aucun patient au-delà de 10 mg/jour : la droite continue, sans preuve.", "<b>Une association n’est pas une cause.</b> La dose a souvent été choisie à cause de la concentration précédente.", "<b>Il reproduit ses données</b>, erreurs et biais compris."],
          "Terminons par trois limites. La première : hors des données, le modèle extrapole. Aucun de nos patients ne reçoit plus de dix milligrammes par jour. La droite continue pourtant, en pointillés, sans la moindre preuve. La deuxième : une association n’est pas une cause. Dans la vraie vie, le médecin adapte la dose à la concentration précédente ; le lien entre les deux colonnes va dans les deux sens. La troisième : le modèle reproduit ses données, erreurs et biais compris. Nous y reviendrons dans le cours sur l’IA responsable.",
          fig=fig_scatter(line=True, extrap=True))
    S.quiz([("Un logiciel applique 200 règles d’interactions écrites par des pharmaciens. C’est :", ["De l’apprentissage profond", "De l’IA, sans apprentissage", "De l’apprentissage supervisé"], 1, "Les règles sont écrites à la main : il y a raisonnement automatisé, donc IA, mais rien n’est appris à partir d’exemples."),
            ("Dans ŷ = w·x + b, que règle l’apprentissage ?", ["x et ŷ", "w et b", "Seulement x"], 1, "x est une donnée et ŷ le résultat. Les paramètres réglables sont w et b."),
            ("La fonction de coût sert à :", ["Mesurer l’écart entre prédictions et mesures", "Compter les patients", "Choisir la dose"], 0, "C’est le nombre que l’algorithme cherche à réduire.")],
           "Trois questions pour vérifier. Prenez un instant pour chacune avant de regarder la réponse. Première question : un logiciel qui applique des règles écrites à la main, c’est de l’IA, mais sans apprentissage. Deuxième question : l’apprentissage règle les paramètres, w et b. Troisième question : la fonction de coût mesure l’écart entre les prédictions et les mesures.")
    S.take(["L’apprentissage automatique remplace une règle écrite par une règle apprise à partir d’exemples.", "Trois ingrédients : des données, un modèle, une fonction de coût.", "Apprendre, c’est régler des paramètres pour réduire le coût, pas à pas.", "Un modèle ne vaut que dans le domaine couvert par ses données."],
           "Quatre idées à retenir. Un : l’apprentissage automatique remplace une règle écrite par une règle apprise à partir d’exemples. Deux : il faut toujours trois ingrédients, des données, un modèle et une fonction de coût. Trois : apprendre, c’est régler des paramètres pour faire baisser le coût, pas à pas. Quatre : un modèle ne vaut que dans le domaine couvert par ses données.")
    S.refs(["G. James, D. Witten, T. Hastie, R. Tibshirani, <i>An Introduction to Statistical Learning</i>, 2ᵉ éd., Springer, 2021 (chapitres 1 à 3 ; libre accès sur statlearning.com).",
            "C. M. Bishop, H. Bishop, <i>Deep Learning: Foundations and Concepts</i>, Springer, 2024 (chapitre 1).",
            "Jeu de données du cours : 40 patients fictifs, fichiers <i>suivi_tacrolimus.csv</i> et <i>patients.csv</i> (cours de programmation, axe 2)."],
           "Pour aller plus loin, deux ouvrages. Le premier, An Introduction to Statistical Learning, est en libre accès et se lit sans prérequis avancés. Le second est plus complet. Les données de l’exemple sont celles du cours de programmation.")
    S.end("Séance 2 · Prédire : régression, classification et arbres", "C’est la fin de cette première séance. La prochaine fois, nous ajouterons des variables, nous prédirons une catégorie plutôt qu’un nombre, et nous verrons les arbres de décision, très utilisés sur les données cliniques. À bientôt.")
    return S
