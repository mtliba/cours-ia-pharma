from lib import *
import numpy as np

rng = np.random.default_rng(388)
emax = lambda c: 90 * c / (3 + c)
CTR = np.array([1.0, 2.5, 4.0, 6.0, 8.0, 10.5, 13.0, 16.0, 19.0, 22.5])
ETR = emax(CTR) + rng.normal(0, 5, 10)
CTE = rng.uniform(1, 22.5, 300); ETE = emax(CTE) + rng.normal(0, 5, 300)
sc = lambda c: (c - 12) / 12
FITS = {d: np.polyfit(sc(CTR), ETR, d) for d in range(1, 10)}
rm = lambda d, c, e: float(np.sqrt(np.mean((np.polyval(FITS[d], sc(c)) - e) ** 2)))
TR = {d: rm(d, CTR, ETR) for d in FITS}; TE = {d: rm(d, CTE, ETE) for d in FITS}
BEST = min(TE, key=TE.get)
fr = lambda v, n=1: f"{v:.{n}f}".replace(".", ",")

def fig_fits(degs=(1, 2, 3, 4, 9)):
    f = Fig(800, 600, "Dix mesures et trois modèles : une droite, une courbe douce, une courbe qui passe par tous les points")
    f.axes(130, 70, 760, 500, (0, 24), (0, 120), [0, 6, 12, 18, 24], [0, 30, 60, 90, 120], "Concentration (ng/mL)", "Effet mesuré (%)")
    xs = np.linspace(0.6, 23.2, 240)
    for d, c, sw, dash in [(1, GREY, 4, "10 9"), (9, RED, 4, None), (BEST, BLUE, 6, None)]:
        if d not in degs: continue
        ys = np.clip(np.polyval(FITS[d], sc(xs)), -2, 121)
        seg = [(a, b) for a, b in zip(xs, ys) if -1 < b < 120.5]
        f.curve([a for a, b in seg], [b for a, b in seg], c, sw, dash)
    f.dots(CTR, ETR, INK, 10)
    f.lab(f.X(14), f.Y(42), "trop souple", 220, cls="axh", color=RED, bg=True)
    f.lab(f.X(14), f.Y(29), "équilibré", 200, cls="axh", bg=True)
    f.lab(f.X(14), f.Y(16), "trop simple", 220, cls="axh", color=GREY, bg=True)
    return f

def fig_u():
    f = Fig(800, 600, "Erreur d’entraînement et erreur de test en fonction de la complexité du modèle")
    top = 16
    f.axes(130, 70, 760, 500, (1, 9), (0, top), list(range(1, 10)), [0, 4, 8, 12, 16], "Complexité du modèle (degré du polynôme)", "Erreur moyenne (points)")
    ds = list(range(1, 10))
    f.curve(ds, [min(TR[d], top) for d in ds], INK, 5); f.dots(ds, [min(TR[d], top) for d in ds], INK, 8)
    te = [(d, TE[d]) for d in ds if TE[d] <= top]
    last = te[-1][0]
    xs = [d for d, _ in te]; ys = [v for _, v in te]
    if last < 9:
        frac = (top - TE[last]) / (TE[last + 1] - TE[last]); xs.append(last + frac); ys.append(top)
    f.curve(xs, ys, RED, 5); f.dots([d for d, _ in te], [v for _, v in te], RED, 8)
    f.line(f.X(BEST), 70, f.X(BEST), 500, BLUE, 3, "10 9")
    f.lab(f.X(BEST) + 12, 78, "le meilleur compromis", 330, cls="axh")
    f.lab(f.X(2.2), f.Y(2.3), "entraînement", 230, cls="axh", color=INK)
    f.lab(f.X(6.0), f.Y(TE[7]) - 78, "test", 100, cls="axh", color=RED)
    return f

def fig_split():
    f = Fig(1500, 330, "Découpage des données : 60 % entraînement, 20 % validation, 20 % test")
    for x, w, t, sub, fill, st in [(0, 900, "Entraînement · 60 %", "Le modèle règle ses paramètres sur ces patients.", PALE, BLUE), (900, 300, "Validation · 20 %", "On compare les modèles et on choisit les réglages.", "#F2F4F8", MUTE), (1200, 300, "Test · 20 %", "On l’ouvre une seule fois, à la fin.", PINK, RED)]:
        f.rect(x + 4, 10, w - 8, 120, fill, st, 3, 8)
        f.labc(x + w / 2, 70, t, w - 30, "axw ax-b")
        f.lab(x + 14, 152, sub, w - 28, "left", "axw")
    f.lab(0, 270, "24 patients", 900, "center", "axh"); f.lab(900, 270, "8 patients", 300, "center", "axh", MUTE); f.lab(1200, 270, "8 patients", 300, "center", "axh", RED)
    return f

def fig_cv():
    f = Fig(800, 560, "Validation croisée à cinq blocs : chaque bloc sert une fois de validation")
    for i in range(5):
        y = 20 + i * 96
        for j in range(5):
            val = (i == j)
            f.rect(160 + j * 124, y, 114, 70, PINK if val else PALE, RED if val else BLUE, 3, 6)
        f.lab(0, y + 18, f"Essai {i + 1}", 150, "left", "axw ax-b")
    f.lab(160, 508, "en rouge : le bloc de validation de l’essai", 620, cls="axh", color=RED)
    return f

def fig_leak():
    f = Fig(800, 600, "Fuite de données : découper par visite mélange les patients ; découper par patient les sépare")
    r = np.random.default_rng(1)
    for k, (y0, title) in enumerate([(60, "Découpage par visite"), (350, "Découpage par patient")]):
        f.lab(0, y0 - 48, title, 500, "left", "axw ax-b", RED if k == 0 else BLUE)
        for p in range(8):
            for v in range(6):
                test = (r.random() < 0.25) if k == 0 else (p >= 6)
                f.rect(120 + p * 84, y0 + v * 34, 72, 26, RED if test else PALE, None, rx=4)
        f.lab(0, y0 + 60, "6 visites", 110, "left", "ax")
    f.lab(120, 566, "une colonne = un patient ; en rouge, le test", 660, cls="ax")
    return f

def build():
    S = Session(3, "fr", "Partie I · Fondamentaux", "Généraliser : surapprentissage et évaluation", "Comment savoir si un modèle fonctionnera sur de nouveaux patients.")
    S.sec("Ouverture : deux modèles, dont l’un ne fait aucune erreur.")
    S.cover("Bonjour. Nous savons maintenant construire des modèles. Cette séance répond à la question la plus importante du cours : comment savoir si un modèle fonctionnera sur des patients qu’il n’a jamais vus ? Si vous ne deviez retenir qu’une séance de cette première partie, ce serait celle-ci.")
    S.sit("Un modèle sans erreur", f"Deux modèles sont ajustés sur les mêmes dix mesures : l’effet d’un médicament en fonction de sa concentration.<br><br>Le premier se trompe en moyenne de <b>{fr(TR[BEST])} points</b>.<br><br>Le second ne fait <b>aucune erreur</b> : sa courbe passe exactement par les dix mesures.",
          "Le modèle sans erreur est-il le meilleur ?",
          f"Voici la situation. Deux modèles sont ajustés sur les mêmes dix mesures : l’effet d’un médicament, en pourcentage, en fonction de sa concentration. Le premier se trompe en moyenne de {fr(TR[BEST])} points. Le second ne fait aucune erreur : sa courbe passe exactement par les dix mesures. Lequel choisiriez-vous ? Prenez quelques secondes. La réponse spontanée est : le second. Nous allons voir pourquoi c’est le mauvais choix.")
    S.obj(["Expliquer la différence entre apprendre et mémoriser.", "Reconnaître un sous-apprentissage et un surapprentissage.", "Découper correctement un jeu de données, sans fuite.", "Choisir une mesure d’erreur et une référence de comparaison."],
          "À la fin de la séance, vous saurez expliquer la différence entre apprendre et mémoriser. Vous saurez reconnaître les deux défauts possibles d’un modèle : trop simple, ou trop souple. Vous saurez découper un jeu de données sans tricher involontairement. Et vous saurez choisir une mesure d’erreur et un point de comparaison.")
    S.plan([("Apprendre ou mémoriser", "L’erreur qui compte est celle sur de nouveaux patients"), ("Trop simple, trop souple", "Sous-apprentissage et surapprentissage"), ("Découper les données", "Entraînement, validation, test ; la fuite de données"), ("Mesurer et comparer", "Mesures d’erreur, référence, remèdes")],
           "Quatre parties. D’abord l’idée centrale : apprendre n’est pas mémoriser. Ensuite les deux défauts opposés d’un modèle. Puis la façon de découper les données pour évaluer honnêtement. Enfin les mesures d’erreur et les remèdes.")
    S.sec("Apprendre ou mémoriser : sous-apprentissage et surapprentissage sur dix mesures.")
    S.st("Ce qui compte, c’est l’erreur sur des patients que le modèle n’a jamais vus.", "On appelle cela la capacité de généralisation. Tout le reste de la séance en découle.",
         "Voici la phrase à retenir. Ce qui compte, ce n’est pas l’erreur sur les données d’entraînement. C’est l’erreur sur des patients que le modèle n’a jamais vus. On appelle cela la capacité de généralisation. Un étudiant qui apprend par cœur les annales réussit les annales ; cela ne dit rien de sa réussite à un nouveau sujet. Pour un modèle, c’est exactement la même chose.")
    S.pts("Trois modèles pour dix mesures", "Les mêmes points, trois courbes de souplesse croissante.",
          ["<b>La droite</b> est trop simple : elle manque la courbure. C’est le <b>sous-apprentissage</b>.", "<b>La courbe rouge</b> passe par tous les points, y compris par leurs erreurs de mesure. C’est le <b>surapprentissage</b>.", "<b>La courbe bleue</b> suit la tendance sans suivre le bruit."],
          "Regardons les trois modèles. En gris, une droite. Elle est trop simple : l’effet plafonne à forte concentration, et la droite ne peut pas le représenter. C’est le sous-apprentissage. En rouge, une courbe très souple, qui passe exactement par les dix points. Mais regardez entre les points : elle oscille de façon absurde. Elle a appris les erreurs de mesure avec le reste. C’est le surapprentissage. En bleu, une courbe de souplesse intermédiaire : elle suit la tendance, sans suivre le bruit. Entre deux mesures, c’est elle qui donnera la meilleure prédiction.",
          fig=fig_fits(), widget="overfit")
    S.pts("La courbe qui révèle tout", "On augmente la souplesse du modèle, et l’on mesure deux erreurs.",
          ["L’erreur d’<b>entraînement</b> ne fait que baisser : un modèle plus souple colle toujours mieux à ses données.", f"L’erreur de <b>test</b>, sur 300 nouvelles mesures, baisse puis remonte.", f"Le minimum est ici au degré {BEST} : {fr(TE[BEST])} points en test."],
          f"Voici la figure la plus importante de la séance. En horizontal, la souplesse du modèle. En noir, l’erreur sur les données d’entraînement : elle ne fait que baisser, jusqu’à zéro. En rouge, l’erreur sur trois cents nouvelles mesures, que le modèle n’a jamais vues. Elle baisse d’abord, puis remonte, et finit par sortir du graphique. Le meilleur modèle est celui du minimum de la courbe rouge : ici le degré {BEST}, avec {fr(TE[BEST])} points d’erreur. La droite faisait {fr(TE[1])}. Le modèle sans erreur d’entraînement fait {fr(TE[9], 0)} points en test. Il était le pire.",
          fig=fig_u(), band="On ne choisit jamais un modèle sur son erreur d’entraînement.")
    S.sec("Découper les données : entraînement, validation, test, et le piège de la fuite.")
    S.wide("Trois parts, trois rôles", "On met de côté des patients que le modèle ne verra pas pendant l’apprentissage.", fig_split(),
           "En pratique, comment faire ? On découpe les données en trois parts avant de commencer. La part d’entraînement, la plus grande, sert à régler les paramètres. La part de validation sert à comparer les modèles et à choisir les réglages, par exemple la souplesse. La part de test, enfin, est mise sous clé. On ne l’ouvre qu’une seule fois, à la toute fin, pour annoncer la performance. Si l’on regarde le test plusieurs fois pour ajuster le modèle, il cesse d’être un test. Avec nos quarante patients : vingt-quatre, huit et huit.",
           band="Le jeu de test ne sert qu’une fois. Sinon, ce n’est plus un test.")
    S.pts("Avec peu de données : la validation croisée", "Chaque patient sert tour à tour à entraîner, puis à valider.",
          ["On découpe les données en 5 blocs.", "On entraîne sur 4 blocs, on valide sur le cinquième.", "On recommence 5 fois, en changeant le bloc de validation.", "On fait la moyenne des 5 erreurs."],
          "Avec quarante patients, mettre de côté huit patients pour la validation, c’est beaucoup, et le résultat dépend du hasard du tirage. La solution s’appelle la validation croisée. On découpe les données en cinq blocs. On entraîne sur quatre, on valide sur le cinquième. Puis on recommence, en changeant le bloc de validation. Au bout de cinq essais, chaque patient a servi une fois à valider. On fait la moyenne des cinq erreurs : l’estimation est plus stable. Le jeu de test, lui, reste toujours à part.",
          fig=fig_cv())
    S.pts("Le piège : la fuite de données", "40 patients, 6 visites chacun : 240 lignes. Comment les répartir ?",
          ["<b>Par visite</b> : le même patient se retrouve des deux côtés. Le modèle le reconnaît, et l’erreur de test est trop belle.", "<b>Par patient</b> : toutes les visites d’un patient vont du même côté.", "Autre fuite classique : une variable qui contient déjà la réponse."],
          "Voici le piège le plus fréquent en santé. Nous avons quarante patients et six visites chacun : deux cent quarante lignes. Si l’on tire les lignes au hasard, en haut, le même patient se retrouve à la fois dans l’entraînement et dans le test. Le modèle n’a pas besoin de comprendre la pharmacologie : il reconnaît le patient. L’erreur de test est excellente, et fausse. C’est une fuite de données. La bonne méthode, en bas : découper par patient. Toutes les visites d’un patient vont du même côté. Autre fuite classique : une variable qui contient déjà la réponse, par exemple une dose modifiée à cause de la concentration que l’on cherche à prédire.",
          fig=fig_leak(), band="En santé, on découpe par patient, jamais par ligne.")
    S.sec("Mesurer, comparer, corriger.")
    S.tbl("Mesurer l’erreur", "La mesure dépend du type de cible.", ["Cible", "Mesure", "Elle se lit ainsi"],
          [["Un nombre", "Erreur absolue moyenne (MAE)", "« Je me trompe de 1,8 ng/mL en moyenne »"],
           ["Un nombre", "Racine de l’erreur quadratique (RMSE)", "Même unité ; les grosses erreurs comptent davantage"],
           ["Une catégorie", "Sensibilité, spécificité", "Parmi les vrais cas, et parmi les non-cas : combien sont bien classés"],
           ["Une catégorie", "Aire sous la courbe ROC (AUC)", "Capacité à placer un cas avant un non-cas ; 0,5 = le hasard"]],
          "Comment exprimer l’erreur ? Pour un nombre, deux mesures. L’erreur absolue moyenne se lit directement : je me trompe en moyenne de un virgule huit nanogramme par millilitre. La racine de l’erreur quadratique est dans la même unité, mais pénalise davantage les grosses erreurs. Pour une catégorie, on utilise la sensibilité et la spécificité, et l’aire sous la courbe ROC. Je ne les détaille pas ici : elles font l’objet d’une séance entière du cours sur l’IA responsable.",
          widths=[18, 37, 45], small=True, band="Ces mesures sont reprises en détail dans le cours « IA responsable », séance 2.")
    S.st("Un chiffre de performance ne veut rien dire sans point de comparaison.", "Avant tout modèle, on calcule une référence simple : prédire la moyenne, ou reprendre la dernière valeur mesurée.",
         "Une erreur de deux nanogrammes par millilitre, est-ce bien ? Impossible de répondre sans point de comparaison. Avant de construire un modèle, calculez toujours une référence simple. Par exemple : prédire pour tout le monde la moyenne. Ou encore : prédire que la prochaine concentration sera égale à la dernière mesurée. Si votre modèle sophistiqué ne fait pas mieux que cette règle d’une ligne, il ne sert à rien. Vous serez surpris du nombre de publications où cette comparaison manque.")
    S.cols("Quatre remèdes au surapprentissage", "Ils se combinent.",
           [("Plus de données", "Plus il y a d’exemples, moins le modèle peut les apprendre par cœur."), ("Un modèle plus simple", "Moins de paramètres, moins de variables, un arbre moins profond."), ("La régularisation", "On ajoute au coût une pénalité pour les poids trop grands : le modèle reste « lisse »."), ("L’arrêt précoce", "On arrête l’entraînement quand l’erreur de validation recommence à monter.")],
           "Que faire en cas de surapprentissage ? Quatre remèdes. Le premier, le plus efficace : davantage de données. Le deuxième : un modèle plus simple, avec moins de paramètres ou moins de variables. Le troisième : la régularisation. On ajoute à la fonction de coût une pénalité pour les poids trop grands, ce qui empêche les oscillations que nous avons vues. Le quatrième : l’arrêt précoce, on stoppe l’entraînement quand l’erreur de validation recommence à monter. Nous le reverrons avec les réseaux de neurones.")
    S.ex("Quatre modèles, quatre diagnostics", ["Le bruit de mesure est d’environ 5 points. Voici l’erreur d’entraînement puis l’erreur de test de quatre modèles.", "Modèle A : 9,8 puis 10,1. Modèle B : 0,4 puis 12,6. Modèle C : 4,7 puis 5,2.", "Modèle D : 0,3 puis 0,3, avec un test tiré au hasard parmi les visites.", "Pour chacun : sous-apprentissage, surapprentissage, bon compromis, ou résultat suspect ?"],
         dict(time="5 minutes", mat="Une feuille", out="Un diagnostic et une action par modèle"),
         "À vous. Le bruit de mesure est d’environ cinq points : aucun modèle honnête ne peut faire beaucoup mieux. Voici quatre modèles, avec leur erreur d’entraînement, puis leur erreur de test. A : neuf virgule huit, puis dix virgule un. B : zéro virgule quatre, puis douze virgule six. C : quatre virgule sept, puis cinq virgule deux. D : zéro virgule trois, puis zéro virgule trois, mais avec un test tiré au hasard parmi les visites. Donnez un diagnostic et une action pour chacun.")
    S.sol("Quatre modèles, quatre diagnostics", ["<b>A</b> : les deux erreurs sont élevées. Sous-apprentissage : essayer un modèle plus souple.", "<b>B</b> : presque parfait à l’entraînement, mauvais en test. Surapprentissage : simplifier, régulariser.", "<b>C</b> : les deux erreurs sont proches, au niveau du bruit. Bon compromis.", "<b>D</b> : meilleur que le bruit, et test tiré par visite. Fuite de données probable : redécouper par patient."],
          "La correction. A : les deux erreurs sont élevées et proches. Le modèle est trop simple : sous-apprentissage. B : presque parfait à l’entraînement, mauvais en test. Surapprentissage. C : les deux erreurs sont proches, et au niveau du bruit de mesure. C’est le bon modèle. D est le plus intéressant : une erreur bien inférieure au bruit de mesure, c’est impossible sans tricher. Et le test a été tiré par visite. C’est une fuite de données. Un résultat trop beau doit toujours éveiller le doute.",
          band="Un résultat trop beau est d’abord un résultat à vérifier.")
    S.quiz([("Un modèle a 0 % d’erreur à l’entraînement. On peut en conclure :", ["Qu’il est excellent", "Rien, sans erreur de test", "Qu’il est trop simple"], 1, "Seule l’erreur sur des données nouvelles renseigne sur la généralisation."),
            ("Le jeu de test sert à :", ["Régler les paramètres", "Choisir entre plusieurs modèles", "Estimer la performance finale, une fois"], 2, "Le choix entre modèles se fait sur la validation."),
            ("240 visites de 40 patients. On découpe :", ["Par visite, au hasard", "Par patient", "Peu importe"], 1, "Sinon le même patient figure des deux côtés : fuite de données.")],
           "Trois questions. Zéro erreur à l’entraînement : on ne peut rien conclure sans l’erreur de test. Le jeu de test : il sert à estimer la performance finale, une seule fois ; le choix entre modèles se fait sur la validation. Deux cent quarante visites de quarante patients : on découpe par patient.")
    S.take(["Un bon modèle est un modèle qui généralise, pas un modèle qui mémorise.", "L’erreur de test baisse puis remonte quand la souplesse augmente.", "On découpe par patient ; le test ne sert qu’une fois.", "Toute performance se compare à une référence simple."],
           "Quatre idées. Un : un bon modèle généralise, il ne mémorise pas. Deux : quand la souplesse augmente, l’erreur de test baisse, puis remonte. Trois : on découpe par patient, et le jeu de test ne sert qu’une fois. Quatre : toute performance se compare à une référence simple.")
    S.refs(["G. James et al., <i>An Introduction to Statistical Learning</i>, 2ᵉ éd., Springer, 2021 (chapitres 2 et 5).", "S. Kapoor, A. Narayanan, « Leakage and the reproducibility crisis in machine-learning-based science », <i>Patterns</i>, 2023 ; 4(9) : 100804.", "G. S. Collins et al., « TRIPOD+AI statement », <i>BMJ</i>, 2024 ; 385 : e078378. doi:10.1136/bmj-2023-078378"],
           "Trois références. Les chapitres deux et cinq du livre d’introduction. Un article sur les fuites de données, qui recense des centaines d’études touchées. Et la recommandation TRIPOD+AI, qui décrit ce qu’une étude de modèle prédictif doit rapporter.")
    S.end("Séance 4 · Réseaux de neurones et apprentissage profond", "C’est la fin de la séance trois. La prochaine fois, nous ouvrirons la boîte des réseaux de neurones : de quoi ils sont faits, comment ils apprennent, et quand ils valent la peine.")
    return S
