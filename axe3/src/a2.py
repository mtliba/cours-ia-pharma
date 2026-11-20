from lib import *
import numpy as np

rng = np.random.default_rng(11)
# 30 visites fictives : dose et surexposition (oui / non)
D = np.round(np.clip(rng.normal(6, 2.3, 30), 1.5, 11.5), 1)
PTRUE = 1 / (1 + np.exp(-(0.95 * (D - 7.2))))
Y = (rng.random(30) < PTRUE).astype(float)

def logit_fit(x, y, it=40):
    X = np.c_[x, np.ones_like(x)]; w = np.zeros(2)
    for _ in range(it):
        p = 1 / (1 + np.exp(-X @ w)); Wd = p * (1 - p) + 1e-9
        w += np.linalg.solve(X.T @ (X * Wd[:, None]), X.T @ (y - p))
    return w
WL, BL = logit_fit(D, Y)
P8 = 1 / (1 + np.exp(-(WL * 8 + BL)))
D50 = -BL / WL

def fig_sigmoid(data=True):
    f = Fig(800, 600, "Probabilité de surexposition en fonction de la dose : courbe en S entre 0 et 1")
    f.axes(130, 70, 760, 500, (0, 12), (0, 1), [0, 2, 4, 6, 8, 10, 12], [0.0, 0.25, 0.5, 0.75, 1.0], "Dose (mg/jour)", "Probabilité de surexposition", fmt=lambda v: (f"{int(v * 100)} %" if isinstance(v, float) else str(v)))
    xs = np.linspace(0, 12, 80)
    f.line(130, f.Y(0.5), 760, f.Y(0.5), RED, 3, "10 9")
    f.curve(xs, 1 / (1 + np.exp(-(WL * xs + BL))), BLUE, 5)
    if data:
        f.dots(D[Y == 0], np.zeros(int((Y == 0).sum())) + 0.0, INK, 9, 0.75)
        f.dots(D[Y == 1], np.ones(int((Y == 1).sum())), RED, 9, 0.75)
        f.lab(140, f.Y(1) + 14, "surexposition observée", 330, cls="axh", color=RED)
        f.lab(f.X(5.7), f.Y(0) - 64, "pas de surexposition", 320, cls="axh", color=INK)
    f.lab(140, f.Y(0.5) - 40, "seuil de décision", 260, color=RED)
    return f

def fig_tree():
    f = Fig(800, 600, "Arbre de décision à deux questions : dose supérieure à 6 mg par jour, puis expression du CYP3A5")
    f.line(400, 110, 170, 250, INK, 4); f.line(400, 110, 630, 250, INK, 4)
    f.line(630, 340, 500, 450, INK, 4); f.line(630, 340, 720, 450, INK, 4)
    f.box(230, 20, 340, 90, "Dose &gt; 6 mg/jour ?", WHITE, INK, "axw ax-b")
    f.box(460, 250, 340, 90, "CYP3A5 expresseur ?", WHITE, INK, "axw ax-b")
    f.box(40, 250, 260, 130, "<b>Risque 5 %</b><br>120 visites", PALE, BLUE, "axw", lines=2)
    f.box(390, 450, 200, 130, "<b>Risque 10 %</b><br>30 visites", PALE, BLUE, "axw", lines=2)
    f.box(610, 450, 190, 130, "<b>Risque 46 %</b><br>50 visites", PINK, RED, "axw", lines=2)
    f.lab(190, 150, "non", 90, "center", cls="axh"); f.lab(520, 150, "oui", 90, "center", cls="axh")
    f.lab(470, 370, "oui", 80, "center", cls="axh"); f.lab(690, 370, "non", 80, "center", cls="axh")
    return f

def fig_boundary():
    r = np.random.default_rng(5)
    dose = np.round(r.uniform(2, 11, 44), 1); poids = np.round(r.uniform(48, 98, 44))
    over = ((dose > 6) & (poids < 75)) ^ (r.random(44) < 0.05)
    f = Fig(800, 600, "Deux variables, dose et poids : frontière droite du modèle linéaire et frontière en escalier de l’arbre")
    f.axes(130, 70, 760, 500, (0, 12), (40, 100), [0, 3, 6, 9, 12], [40, 60, 80, 100], "Dose (mg/jour)", "Poids (kg)")
    f.rect(f.X(6), f.Y(75), f.X(12) - f.X(6), f.Y(40) - f.Y(75), PINK, None, op=0.7)
    f.poly([(f.X(6), f.Y(40)), (f.X(6), f.Y(75)), (f.X(12), f.Y(75))], RED, 5, dash="12 10")
    X = np.c_[(dose - 6) / 3, (poids - 70) / 15, np.ones(44)]; w = np.zeros(3)
    for _ in range(60):
        p = 1 / (1 + np.exp(-X @ w)); Wd = p * (1 - p) + 1e-6
        w += np.linalg.solve(X.T @ (X * Wd[:, None]) + 0.3 * np.eye(3), X.T @ (over - p) - 0.3 * w)
    yb = lambda d: 70 + 15 * (-(w[0] * (d - 6) / 3 + w[2]) / w[1])
    d0, d1 = 2.0, 12.0
    pts = [(d, yb(d)) for d in np.linspace(d0, d1, 60) if 40 <= yb(d) <= 100]
    f.curve([a for a, b in pts], [b for a, b in pts], BLUE, 5)
    f.dots(dose[~over], poids[~over], INK, 8); f.dots(dose[over], poids[over], RED, 8)
    f.lab(f.X(7.6), f.Y(47), "zone de l’arbre", 240, cls="axh", color=RED, bg=True)
    f.lab(f.X(0.3), f.Y(47), "frontière linéaire", 290, cls="axh", bg=True)
    return f

def fig_ensemble():
    f = Fig(800, 560, "Quatre petits arbres dont les prédictions sont combinées en une seule")
    preds = ["41 %", "52 %", "44 %", "47 %"]
    for i in range(4):
        x = 30 + i * 195; c = [BLUE, BLUE, BLUE, BLUE][i]
        for (a, b, cc, d) in [(x + 80, 50, x + 35, 130), (x + 80, 50, x + 125, 130), (x + 35, 130, x + 10, 210), (x + 35, 130, x + 60, 210), (x + 125, 130, x + 100, 210), (x + 125, 130, x + 150, 210)]:
            f.line(a, b, cc, d, c, 4)
        for (a, b) in [(x + 80, 50), (x + 35, 130), (x + 125, 130)]: f.circle(a, b, 13, WHITE, c, 4)
        for j, (a, b) in enumerate([(x + 10, 210), (x + 60, 210), (x + 100, 210), (x + 150, 210)]): f.circle(a, b, 11, RED if (i + j) % 4 == 1 else c, WHITE, 3)
        f.lab(x, 240, preds[i], 160, "center", cls="axw ax-b")
        f.arrow(x + 80, 290, 400 + (x + 80 - 400) * 0.25, 392, INK, 4)
    f.box(240, 400, 320, 110, "<b>Moyenne : 46 %</b><br>prédiction finale", PALE, BLUE, "axw", lines=2)
    return f

def build():
    S = Session(2, "fr", "Partie I · Fondamentaux", "Prédire : régression, classification et arbres", "Les modèles les plus utilisés sur des données cliniques en tableau.")
    p8 = f"{P8 * 100:.0f}"; d50 = f"{D50:.1f}".replace(".", ",")
    S.sec("Ouverture : deux questions pour un même patient.")
    S.cover("Bonjour. À la dernière séance, nous avons vu qu’apprendre, c’est régler les paramètres d’un modèle pour réduire une erreur. Notre modèle était une droite, avec une seule variable. Aujourd’hui, nous passons aux modèles réellement utilisés sur des données cliniques : la régression à plusieurs variables, la régression logistique, et les arbres de décision.")
    S.sit("Un nombre, ou une catégorie ?", "Le patient de la première séance revient en consultation. L’équipe se pose deux questions.<br><br><b>Première question :</b> quelle sera sa concentration résiduelle à la prochaine visite ?<br><br><b>Deuxième question :</b> sera-t-il en surexposition, c’est-à-dire au-dessus de 15 ng/mL ?",
          "Prédire un nombre et prédire « oui ou non » : est-ce le même problème ?",
          "Reprenons notre patient greffé. L’équipe se pose deux questions. La première : quelle sera sa concentration à la prochaine visite ? La réponse est un nombre. La seconde : sera-t-il en surexposition, au-dessus de quinze nanogrammes par millilitre ? La réponse est oui ou non. Est-ce le même problème ? Pas tout à fait. Les données sont les mêmes, mais ce que l’on prédit change, et avec lui le modèle et la façon de mesurer l’erreur. Le seuil de quinze est ici illustratif.")
    S.obj(["Distinguer une régression d’une classification.", "Lire un modèle linéaire à plusieurs variables.", "Expliquer pourquoi une classification produit une probabilité.", "Lire un arbre de décision, et dire pourquoi on en combine plusieurs."],
          "À la fin de la séance, vous saurez distinguer une régression d’une classification. Vous saurez lire un modèle linéaire à plusieurs variables. Vous saurez expliquer pourquoi un modèle de classification annonce une probabilité plutôt qu’un oui ou un non. Et vous saurez lire un arbre de décision, et dire pourquoi, en pratique, on en combine des centaines.")
    S.plan([("Le vocabulaire d’un tableau de données", "Exemples, variables, cible"), ("Prédire un nombre", "La régression linéaire à plusieurs variables"), ("Prédire une catégorie", "La régression logistique et la probabilité"), ("Les arbres, et les forêts", "Des questions successives, puis un vote")],
           "Quatre parties. D’abord le vocabulaire, pour parler la même langue que les data scientists. Ensuite la régression, pour prédire un nombre. Puis la classification, pour prédire une catégorie. Enfin les arbres de décision et leurs combinaisons, qui sont aujourd’hui les modèles les plus performants sur des données en tableau.")
    S.sec("Le vocabulaire : exemples, variables et cible ; régression ou classification.")
    S.tbl("Le vocabulaire d’un tableau de données", "Une ligne par exemple, une colonne par variable. La dernière colonne est la cible.", ["Patient", "Dose (mg/jour)", "Poids (kg)", "CYP3A5", "Concentration (ng/mL)"],
          [["P01", "4", "62", "non expresseur", "7,8"], ["P02", "8", "81", "expresseur", "6,1"], ["P03", "6", "70", "non expresseur", "11,4"], ["P04", "9", "58", "non expresseur", "16,9"]],
          "Fixons le vocabulaire. Chaque ligne du tableau est un exemple, on dit aussi une observation : ici, une visite d’un patient. Chaque colonne est une variable. Les colonnes que l’on connaît avant de prédire s’appellent les variables explicatives ; en anglais, les features. Ici : la dose, le poids, et le statut du CYP3A5, une enzyme qui élimine le tacrolimus. La colonne que l’on veut prédire s’appelle la cible ; en anglais, le label ou la target. Regardez le patient P02 : une forte dose, mais une concentration basse. Il exprime le CYP3A5 et élimine vite le médicament. Ces valeurs sont inventées.",
          widths=[13, 19, 16, 24, 28], hl=1, band="Variables explicatives : ce que l’on connaît. Cible : ce que l’on veut prédire.")
    S.cols("Deux types de prédiction", "C’est la nature de la cible qui décide.",
           [("Régression", "La cible est un <b>nombre</b>.<br><br>Concentration à la prochaine visite, clairance, exposition totale (AUC).<br><br>L’erreur se mesure dans l’unité de la cible : « je me trompe de 2 ng/mL en moyenne »."),
            ("Classification", "La cible est une <b>catégorie</b>.<br><br>Surexposition ou non, molécule toxique ou non, patient répondeur ou non.<br><br>L’erreur se compte : combien de cas bien classés, combien de fausses alertes.")],
           "Deux types de prédiction. Si la cible est un nombre, c’est une régression. Attention, le mot a ici un sens large : toute prédiction d’un nombre, quel que soit le modèle. L’erreur se lit dans l’unité de la cible : je me trompe en moyenne de deux nanogrammes par millilitre. Si la cible est une catégorie, c’est une classification. L’erreur se compte alors en cas bien ou mal classés. Notre première question était une régression, la seconde une classification.")
    S.sec("Prédire un nombre : la régression linéaire à plusieurs variables.")
    S.eq("Plusieurs variables, une seule formule", "On ajoute un terme par variable.", r"\hat{y} = w_1 x_1 + w_2 x_2 + \dots + w_p x_p + b",
         [(r"x_1,\dots,x_p", "Les <b>p variables explicatives</b> du patient : dose, poids, âge, délai depuis la greffe…"),
          (r"w_j", "Le <b>poids</b> de la variable numéro j : de combien la prédiction change quand cette variable augmente d’une unité, les autres restant fixes."),
          (r"b", "Le <b>biais</b> : la valeur de départ, quand toutes les variables valent zéro."),
          (r"\hat{y}", "La <b>prédiction</b> : une somme pondérée des variables.")],
         "Avec plusieurs variables, la droite devient une somme pondérée. Chaque variable x est multipliée par son poids w, et l’on additionne. Le poids se lit ainsi : de combien la prédiction change quand cette variable augmente d’une unité, toutes les autres restant fixes. Par exemple, un poids de moins zéro virgule zéro cinq pour le poids corporel voudrait dire : dix kilos de plus, un demi-nanogramme de moins. C’est la grande qualité de ce modèle : il se lit. Sa limite : il suppose que les effets s’additionnent simplement.",
         band="Un modèle linéaire se lit : c’est sa force. Il suppose des effets qui s’additionnent : c’est sa limite.")
    S.sec("Prédire une catégorie : la régression logistique et la probabilité.")
    S.pts("De la droite à la probabilité", "Chaque point est une visite : en haut, surexposition observée ; en bas, non.",
          ["Une droite donnerait des valeurs inférieures à 0 ou supérieures à 1 : absurde pour une probabilité.", "On la replie en une courbe en S, toujours comprise entre 0 et 1.", f"À 8 mg/jour, le modèle annonce un risque de {p8} %."],
          f"Passons à la classification. En haut, les visites avec surexposition ; en bas, les visites sans. On ne veut pas seulement un oui ou un non : on veut une probabilité. Une droite ne convient pas, elle sortirait de l’intervalle zéro, un. On la replie donc en une courbe en S. À faible dose, le risque est proche de zéro ; à forte dose, proche de un. Ici, à huit milligrammes par jour, le modèle annonce un risque d’environ {p8} pour cent. La décision vient ensuite, en fixant un seuil. Ce modèle s’appelle la régression logistique.",
          fig=fig_sigmoid(), widget="logistic")
    S.eq("La régression logistique", "Un score linéaire, transformé en probabilité.", [r"z = w\,x + b", r"p = \sigma(z) = \frac{1}{1+e^{-z}}"],
         [(r"z", "Le <b>score</b> : la même somme pondérée que précédemment. Il peut être négatif ou très grand."),
          (r"\sigma", "La fonction <b>sigmoïde</b> : elle transforme n’importe quel score en un nombre entre 0 et 1."),
          (r"p", "La <b>probabilité prédite</b> de surexposition. Un score de 0 donne exactement p = 0,5."),
          (r"e", "La constante exponentielle, environ 2,718.")],
         f"Voici la formule, en deux lignes. Première ligne : on calcule un score z, exactement comme avant. Deuxième ligne : on passe ce score dans la fonction sigmoïde, notée sigma. Si z est très négatif, l’exponentielle au dénominateur est énorme, et p est proche de zéro. Si z est très positif, elle est proche de zéro, et p vaut presque un. Si z vaut zéro, p vaut un demi. Ici, le risque atteint cinquante pour cent vers {d50} milligrammes par jour. Retenez cette sigmoïde : nous la retrouverons dans les réseaux de neurones.",
         band="Le modèle donne une probabilité. La décision, elle, dépend du seuil que l’on choisit.")
    S.sec("Les arbres de décision, puis les forêts et le boosting.")
    S.pts("Un arbre de décision", "Une suite de questions simples, apprises à partir des données.",
          ["On pose une question sur une variable ; selon la réponse, on descend à gauche ou à droite.", "Au bout de chaque branche, une <b>feuille</b> : la prédiction pour les patients qui y arrivent.", "L’algorithme choisit lui-même les questions et les seuils qui séparent le mieux les cas."],
          "Autre famille de modèles : l’arbre de décision. Il ressemble à un raisonnement clinique. Première question : la dose dépasse-t-elle six milligrammes par jour ? Si non, on arrive à une feuille : parmi les cent vingt visites concernées, cinq pour cent de surexpositions. Si oui, deuxième question : le patient exprime-t-il le CYP3A5 ? S’il l’exprime, il élimine vite, le risque est de dix pour cent. Sinon, quarante-six pour cent. Le point essentiel : ni les questions ni les seuils ne sont écrits par un expert. L’algorithme les choisit pour séparer au mieux les cas. Ces chiffres sont inventés.",
          fig=fig_tree())
    S.pts("Deux façons de tracer une frontière", "Deux variables : la dose et le poids. En rouge, les surexpositions.",
          ["Le modèle linéaire trace une <b>frontière droite</b>.", "L’arbre découpe le plan en <b>rectangles</b> : il capte une interaction (forte dose <i>et</i> petit poids).", "Aucun des deux n’est parfait : quelques points restent du mauvais côté."],
          "Comparons les deux familles. Chaque point est une visite, placée selon la dose et le poids ; en rouge, les surexpositions. Le modèle linéaire sépare les deux groupes par une frontière droite. L’arbre, lui, pose des questions une variable à la fois : il découpe le plan en rectangles. Ici, il capte une interaction : le risque est élevé quand la dose est forte et le poids faible, les deux à la fois. Un modèle linéaire simple ne peut pas représenter cela. Remarquez aussi que quelques points restent du mauvais côté : aucun modèle n’est parfait, et c’est normal.",
          fig=fig_boundary())
    S.pts("Un arbre hésite, une forêt décide", "On entraîne beaucoup d’arbres, puis on combine leurs réponses.",
          ["Un arbre seul est <b>instable</b> : quelques patients en plus, et les questions changent.", "<b>Forêt aléatoire</b> : des centaines d’arbres, entraînés chacun sur un échantillon différent, puis moyennés.", "<b>Boosting</b> : des arbres construits l’un après l’autre, chacun corrigeant les erreurs des précédents."],
          "Un arbre seul a un défaut : il est instable. Ajoutez quelques patients, et il peut choisir d’autres questions. La solution : en entraîner beaucoup, et combiner leurs réponses. Deux méthodes. La forêt aléatoire entraîne des centaines d’arbres, chacun sur un échantillon un peu différent des données, puis fait la moyenne. Le boosting construit les arbres l’un après l’autre : chaque nouvel arbre se concentre sur les erreurs des précédents. Les outils les plus connus s’appellent XGBoost et LightGBM. Sur des données en tableau, ce sont très souvent les modèles les plus performants.",
          fig=fig_ensemble(), band="Sur des données en tableau, le boosting est souvent le premier modèle à essayer.")
    S.nums("Un exemple réel, à Limoges", "Estimer l’exposition au tacrolimus avec un modèle de boosting (Woillard et al., 2021).",
           [("2 ou 3", "prises de sang suffisent au modèle pour estimer l’exposition totale (AUC), au lieu d’un profil complet"), ("4 997", "AUC de patients traités deux fois par jour ont servi à construire et tester le modèle (1 452 pour la prise unique)"), ("&lt; 10 %", "d’erreur relative sur les données de test, avec un biais inférieur à 5 %")],
           "Voici un exemple réel, publié en 2021 par l’équipe de pharmacologie de Limoges. L’objectif : estimer l’exposition totale au tacrolimus, l’aire sous la courbe, à partir de deux ou trois prises de sang seulement. Le modèle est un XGBoost, c’est-à-dire du boosting d’arbres. Il a été construit sur près de cinq mille aires sous la courbe pour les patients traités deux fois par jour. Sur les données de test, l’erreur relative est inférieure à dix pour cent. Le modèle a ensuite été évalué sur six jeux de données indépendants, où il fait mieux que la méthode bayésienne de référence. Retenez la démarche : un modèle simple, beaucoup de données, et une validation sur des données extérieures.",
           band="Évalué ensuite sur six jeux de données indépendants : c’est cette étape qui fonde la confiance.")
    S.ex("Lire un arbre", ["Reprenez l’arbre : première question « dose &gt; 6 mg/jour ? », seconde question « CYP3A5 expresseur ? ».", "Patient A : 4 mg/jour, non expresseur. Patient B : 8 mg/jour, expresseur. Patient C : 8 mg/jour, non expresseur. Quel risque l’arbre annonce-t-il pour chacun ?", "Sur les 200 visites, combien de surexpositions au total ?", "Pourquoi l’arbre ne demande-t-il pas le statut CYP3A5 du patient A ?"],
         dict(time="6 minutes", mat="L’arbre, une calculatrice", out="Trois risques, un total, une phrase"),
         "À vous. Reprenez l’arbre. Trois patients : A reçoit quatre milligrammes par jour et n’exprime pas le CYP3A5. B reçoit huit milligrammes et l’exprime. C reçoit huit milligrammes et ne l’exprime pas. Quel risque l’arbre annonce-t-il pour chacun ? Ensuite, calculez le nombre total de surexpositions sur les deux cents visites. Enfin, expliquez pourquoi l’arbre ne s’intéresse pas au CYP3A5 du patient A. Six minutes.")
    S.sol("Lire un arbre", ["<b>A</b> : dose ≤ 6, feuille de gauche : 5 %. <b>B</b> : dose &gt; 6, expresseur : 10 %. <b>C</b> : dose &gt; 6, non expresseur : 46 %.", "Total : 5 % de 120 = 6 ; 10 % de 30 = 3 ; 46 % de 50 = 23. Soit <b>32 surexpositions sur 200</b> (16 %).", "Pour le patient A, le CYP3A5 n’est pas demandé : dans ces données, à faible dose, il ne séparait pas mieux les cas."],
          "La correction. A : quatre milligrammes, on part à gauche, cinq pour cent. B : huit milligrammes, expresseur, dix pour cent. C : huit milligrammes, non expresseur, quarante-six pour cent. Le total : six, plus trois, plus vingt-trois, soit trente-deux surexpositions sur deux cents, seize pour cent. Enfin, pourquoi le CYP3A5 n’est-il pas demandé à faible dose ? Parce que dans ces données, il n’apportait rien de plus à cet endroit. Attention à la lecture : cela ne veut pas dire que le CYP3A5 est sans effet à faible dose, seulement que l’arbre n’en a pas eu besoin.",
          fig=fig_tree(), band="Un arbre décrit ses données : il ne dit pas ce qui cause quoi.")
    S.tbl("Quel modèle essayer ?", "Un repère pour commencer, pas une règle absolue.", ["Modèle", "Ses points forts", "Ses limites"],
          [["Linéaire ou logistique", "Se lit directement ; fonctionne avec peu de données", "Effets supposés additifs"],
           ["Arbre seul", "Se lit comme un raisonnement", "Instable, peu précis"],
           ["Forêt, boosting", "Très performants sur les tableaux ; captent les interactions", "Plus difficiles à lire"],
           ["Réseau de neurones", "Images, textes, signaux, séquences", "Demande beaucoup de données"]],
          "Comment choisir ? Voici un repère. Le modèle linéaire ou logistique : il se lit, il fonctionne avec peu de données ; commencez toujours par lui. L’arbre seul se lit bien, mais il est instable. Les forêts et le boosting sont les plus performants sur des données en tableau, au prix d’une lecture plus difficile. Les réseaux de neurones, que nous verrons à la séance quatre, dominent pour les images, les textes et les signaux, mais demandent beaucoup de données. Un conseil : un modèle complexe doit toujours être comparé à un modèle simple.",
          widths=[24, 42, 34], band="Toujours comparer un modèle complexe à un modèle simple.")
    S.quiz([("Prédire la clairance d’un patient en L/h, c’est :", ["Une classification", "Une régression", "Du non supervisé"], 1, "La cible est un nombre."),
            ("Une régression logistique produit :", ["Une catégorie directement", "Une probabilité entre 0 et 1", "Une concentration"], 1, "La décision vient ensuite, avec un seuil."),
            ("Pourquoi combiner des centaines d’arbres ?", ["Pour rendre le modèle plus lisible", "Parce qu’un arbre seul est instable", "Pour utiliser moins de données"], 1, "La moyenne de nombreux arbres est plus stable et plus précise.")],
           "Trois questions. Prédire une clairance en litres par heure : la cible est un nombre, c’est une régression. La régression logistique : elle produit une probabilité, la catégorie vient ensuite avec un seuil. Pourquoi combiner des centaines d’arbres ? Parce qu’un arbre seul est instable ; la moyenne est plus stable et plus précise. En revanche, on y perd en lisibilité.")
    S.take(["Régression : la cible est un nombre. Classification : la cible est une catégorie.", "Un modèle linéaire est une somme pondérée : chaque poids se lit comme un effet.", "Un classifieur annonce une probabilité ; la décision dépend d’un seuil.", "Sur des données en tableau, les arbres combinés sont la référence."],
           "Quatre idées. Un : régression pour un nombre, classification pour une catégorie. Deux : un modèle linéaire est une somme pondérée, et chaque poids se lit comme un effet. Trois : un classifieur annonce une probabilité ; la décision dépend d’un seuil, que l’on choisit. Quatre : sur des données en tableau, les arbres combinés sont la référence.")
    S.refs(["J.-B. Woillard, M. Labriffe, J. Debord, P. Marquet, « Tacrolimus Exposure Prediction Using Machine Learning », <i>Clin Pharmacol Ther</i>, 2021 ; 110(2) : 361-369. doi:10.1002/cpt.2123",
            "G. James et al., <i>An Introduction to Statistical Learning</i>, 2ᵉ éd., Springer, 2021 (chapitres 3, 4 et 8).",
            "T. Chen, C. Guestrin, « XGBoost: A Scalable Tree Boosting System », <i>KDD</i>, 2016."],
           "Les références. L’article de l’équipe de Limoges sur l’estimation de l’exposition au tacrolimus. Les chapitres trois, quatre et huit du livre d’introduction. Et l’article qui décrit XGBoost.")
    S.end("Séance 3 · Généraliser : surapprentissage et évaluation", "C’est la fin de la séance deux. Nous savons construire des modèles. La prochaine fois, nous verrons la question la plus importante de tout le cours : comment savoir si un modèle fonctionnera sur de nouveaux patients ?")
    return S
