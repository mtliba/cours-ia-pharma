from lib import *
import numpy as np

def fig_neuron():
    f = Fig(800, 560, "Un neurone artificiel : trois entrées pondérées, une somme, une fonction d’activation, une sortie")
    ys = [110, 270, 430]
    for i, y in enumerate(ys):
        f.circle(90, y, 46, WHITE, INK, 4)
        f.labc(90, y, f"<b>x{'₁₂₃'[i]}</b>", 80, "axw")
        ye = 270 + (y - 270) * 0.22
        f.arrow(140, y, 352, ye, BLUE, 5)
        ym = (y + ye) / 2
        f.lab(215, ym - 58 if i < 2 else ym + 10, f"w{'₁₂₃'[i]}", 80, "center", "axh")
    f.circle(410, 270, 62, PALE, BLUE, 5); f.labc(410, 270, "<b>somme</b><br>+ b", 110, "axw", lines=2)
    f.arrow(474, 270, 548, 270, INK, 5)
    f.rect(552, 215, 110, 110, WHITE, RED, 5, 12); f.labc(607, 270, "<b>f</b>", 100, "axw", RED)
    f.arrow(664, 270, 728, 270, INK, 5); f.labc(762, 270, "<b>a</b>", 50, "axw")
    f.lab(330, 356, "1. somme", 160, "center", "ax"); f.lab(517, 356, "2. activation", 180, "center", "ax")
    f.lab(690, 356, "3. sortie", 110, "center", "ax")
    f.lab(20, 496, "Entrées : dose, poids, délai depuis la greffe…", 760, "left", "ax")
    return f

def fig_act():
    f = Fig(800, 600, "Deux fonctions d’activation : ReLU et sigmoïde")
    f.axes(130, 70, 760, 500, (-4, 4), (-0.5, 4), [-4, -2, 0, 2, 4], [0, 1, 2, 3, 4], "Somme pondérée z", "Sortie du neurone")
    xs = np.linspace(-4, 4, 100)
    f.curve(xs, np.maximum(0, xs), BLUE, 6)
    f.curve(xs, 1 / (1 + np.exp(-xs)), RED, 5, "12 9")
    f.lab(f.X(-3.8), f.Y(3.7), "ReLU : max(0, z)", 330, cls="axh", bg=True)
    f.lab(f.X(-3.8), f.Y(1.7), "sigmoïde", 200, cls="axh", color=RED, bg=True)
    return f

def fig_net():
    f = Fig(800, 600, "Réseau de neurones à quatre couches : 3 entrées, deux couches cachées de 4 neurones, 1 sortie")
    layers = [3, 4, 4, 1]; xs = [90, 300, 510, 720]; pos = []
    for n, x in zip(layers, xs):
        pos.append([(x, 270 + (j - (n - 1) / 2) * 112) for j in range(n)])
    for a, b in zip(pos[:-1], pos[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b: f.line(x1 + 30, y1, x2 - 30, y2, "#AEB9E6", 2)
    for li, col in enumerate(pos):
        for (x, y) in col: f.circle(x, y, 30, WHITE if li == 0 else PALE, INK if li in (0, 3) else BLUE, 4)
    f.lab(10, 520, "Entrée", 160, "center", "axw ax-b"); f.lab(265, 520, "Couches cachées", 280, "center", "axw ax-b"); f.lab(640, 520, "Sortie", 160, "center", "axw ax-b")
    f.lab(100, 2, "chaque trait est un poids à régler", 640, "center", "axh")
    return f

def fig_loop():
    f = Fig(800, 560, "Boucle d’entraînement : prédire, mesurer le coût, calculer les gradients, ajuster les poids")
    B = [(20, 40, "<b>1. Prédiction</b><br>sur un lot d’exemples"), (420, 40, "<b>2. Coût</b><br>écart aux réponses"), (420, 360, "<b>3. Gradients</b><br>rétropropagation"), (20, 360, "<b>4. Mise à jour</b><br>un petit pas")]
    for x, y, t in B: f.box(x, y, 360, 130, t, PALE, BLUE, "axw", lines=2)
    f.arrow(386, 105, 414, 105, INK, 5); f.arrow(600, 176, 600, 354, INK, 5); f.arrow(414, 425, 386, 425, INK, 5); f.arrow(200, 354, 200, 176, INK, 5)
    f.labc(400, 266, "des milliers de fois", 300, "axh")
    return f

def fig_curves():
    f = Fig(800, 600, "Coût d’entraînement et coût de validation au fil des époques, avec arrêt précoce")
    ep = np.arange(0, 61)
    tr = 0.18 + 0.82 * np.exp(-ep / 9.0); va = 0.36 + 0.64 * np.exp(-ep / 7.5) + 0.0045 * np.maximum(0, ep - 14) ** 1.25
    f.axes(130, 70, 760, 500, (0, 60), (0, 1.2), [0, 10, 20, 30, 40, 50, 60], [0, 0.4, 0.8, 1.2], "Époques (passages sur les données)", "Coût", fmt=lambda v: str(v).replace(".", ","))
    f.curve(ep, tr, INK, 5); f.curve(ep, va, RED, 5)
    b = int(np.argmin(va))
    f.line(f.X(b), 70, f.X(b), 500, BLUE, 3, "10 9")
    f.lab(f.X(b) + 12, 80, "on s’arrête ici", 260, cls="axh")
    f.lab(f.X(24), f.Y(float(va[40])) - 78, "validation", 190, cls="axh", color=RED)
    f.lab(f.X(38), f.Y(float(tr[45])) + 16, "entraînement", 230, cls="axh", color=INK)
    return f, b

def build():
    S = Session(4, "fr", "Partie I · Fondamentaux", "Réseaux de neurones et apprentissage profond", "De quoi ils sont faits, comment ils apprennent, et quand ils valent la peine.")
    curves, best = fig_curves()
    S.sec("Ouverture : pourquoi une droite ou un arbre ne suffisent pas toujours.")
    S.cover("Bonjour. C’est la dernière séance de la première partie. Jusqu’ici, nos modèles lisaient des tableaux : une ligne par patient, une colonne par variable. Aujourd’hui, nous ouvrons la boîte des réseaux de neurones, qui savent lire des images, des textes et des séquences. Vous verrez que la recette d’apprentissage est exactement celle de la première séance.")
    S.sit("Quand les données ne sont plus un tableau", "Une lame de biopsie rénale numérisée : plusieurs milliards de pixels.<br><br>Le compte rendu d’une consultation : du texte libre.<br><br>Une molécule : des atomes reliés par des liaisons.<br><br>Aucune de ces données ne tient dans quelques colonnes bien choisies.",
          "Comment un modèle peut-il apprendre lui-même ce qu’il faut regarder ?",
          "Jusqu’ici, quelqu’un avait choisi les colonnes du tableau : la dose, le poids, le CYP3A5. Mais prenez une lame de biopsie numérisée : des milliards de pixels. Un compte rendu : du texte libre. Une molécule : des atomes et des liaisons. Quelles colonnes en tirer ? Pendant des décennies, des experts ont construit ces variables à la main. L’idée de l’apprentissage profond est différente : laisser le modèle apprendre lui-même ce qu’il faut regarder.")
    S.obj(["Décrire un neurone artificiel et calculer sa sortie.", "Expliquer ce qu’est une couche, et ce que « profond » veut dire.", "Décrire la boucle d’entraînement d’un réseau.", "Dire quand un réseau profond se justifie, et quand il ne se justifie pas."],
          "À la fin de la séance, vous saurez décrire un neurone artificiel et calculer sa sortie à la main. Vous saurez expliquer ce qu’est une couche et ce que veut dire « profond ». Vous saurez décrire la boucle d’entraînement. Et vous saurez dire quand un réseau profond se justifie, et quand un modèle plus simple suffit.")
    S.plan([("Le neurone artificiel", "Une somme pondérée, puis une activation"), ("Du neurone au réseau", "Les couches, et ce qu’elles apprennent"), ("L’entraînement", "La même descente qu’à la séance 1, en plus grand"), ("Quelle architecture, et quand ?", "Images, texte, molécules ; les limites")],
           "Quatre parties. Le neurone, brique de base. Le réseau, qui empile ces briques en couches. L’entraînement, qui reprend la descente de gradient de la première séance. Et enfin les grandes architectures, avec la question pratique : quand utiliser un réseau profond ?")
    S.sec("Le neurone artificiel : somme pondérée et fonction d’activation.")
    S.pts("Le neurone artificiel", "Une petite unité de calcul, en trois temps.",
          ["Il reçoit des <b>entrées</b>, chacune multipliée par un <b>poids</b>.", "Il en fait la <b>somme</b>, et ajoute un biais.", "Il applique une <b>fonction d’activation</b>, et transmet le résultat."],
          "Voici un neurone artificiel. Le nom vient d’une analogie lointaine avec le neurone biologique ; n’y cherchez pas plus. C’est une petite unité de calcul. Elle reçoit des entrées : par exemple la dose, le poids, le délai depuis la greffe. Chaque entrée est multipliée par un poids. Le neurone fait la somme, ajoute un biais : vous reconnaissez la somme pondérée de la séance deux. Puis vient la nouveauté : il applique une fonction, dite d’activation, et transmet le résultat.",
          fig=fig_neuron())
    S.eq("Le calcul d’un neurone", "La régression de la séance 2, suivie d’une fonction.", [r"z = w_1 x_1 + w_2 x_2 + w_3 x_3 + b", r"a = f(z)"],
         [(r"x_1, x_2, x_3", "Les <b>entrées</b> du neurone."), (r"w_1, w_2, w_3,\ b", "Les <b>poids</b> et le <b>biais</b> : les paramètres que l’entraînement règle."),
          (r"z", "La <b>somme pondérée</b> : un nombre quelconque, positif ou négatif."), (r"f", "La <b>fonction d’activation</b>. La plus courante, ReLU, laisse passer z s’il est positif et renvoie 0 sinon."), (r"a", "La <b>sortie</b> du neurone, transmise à la couche suivante.")],
         "La formule tient en deux lignes. Première ligne : z, la somme pondérée des entrées, plus le biais. Deuxième ligne : a, la sortie, obtenue en appliquant la fonction f. Avec une sigmoïde pour f, un neurone seul est exactement la régression logistique de la séance deux. La fonction la plus utilisée aujourd’hui est plus simple encore. Elle s’appelle ReLU : si z est positif, elle le laisse passer ; s’il est négatif, elle renvoie zéro.")
    S.pts("Pourquoi une fonction d’activation ?", "Sans elle, un réseau entier ne ferait pas mieux qu’une droite.",
          ["<b>ReLU</b> coupe les valeurs négatives : le neurone est « éteint » ou « allumé ».", "Empiler des sommes pondérées sans activation redonne une somme pondérée.", "C’est le coude de l’activation qui permet de dessiner des courbes."],
          "Pourquoi cette fonction ? Regardez ReLU, en bleu : elle vaut zéro pour les valeurs négatives, puis monte en ligne droite. Le neurone est éteint, ou allumé. Sans activation, empiler des couches ne servirait à rien : une somme pondérée de sommes pondérées reste une somme pondérée, donc une droite. C’est le coude de la fonction qui change tout. En combinant beaucoup de petits coudes, le réseau peut dessiner n’importe quelle courbe : un effet qui plafonne, un seuil, une interaction.",
          fig=fig_act(), widget="neuron")
    S.sec("Du neurone au réseau : les couches, et les représentations qu’elles apprennent.")
    S.pts("Un réseau : des neurones en couches", "La sortie d’une couche devient l’entrée de la suivante.",
          ["<b>Couche d’entrée</b> : les données du patient.", "<b>Couches cachées</b> : des calculs intermédiaires, que personne n’a définis à l’avance.", "<b>Couche de sortie</b> : la prédiction.", "Ce petit réseau a déjà <b>41 paramètres</b>."],
          "Un réseau, ce sont des neurones rangés en couches. À gauche, la couche d’entrée : les données. À droite, la couche de sortie : la prédiction. Entre les deux, les couches cachées. Chaque neurone d’une couche reçoit les sorties de la couche précédente. Chaque trait du dessin est un poids à régler. Ce tout petit réseau en compte déjà quarante et un, biais compris. Un réseau est dit profond quand il a beaucoup de couches. Les grands modèles de langage ont des dizaines de couches et des milliards de poids.",
          fig=fig_net())
    S.wide("Ce que les couches apprennent", "Chaque couche construit une description un peu plus abstraite que la précédente.",
           flow(["<b>Pixels</b><br>d’une lame", "<b>Bords</b><br>et textures", "<b>Formes</b> : noyaux,<br>tubules", "<b>Structures</b> :<br>glomérule, infiltrat", "<b>Décision</b> :<br>rejet probable"], 1500, 250, "Des pixels à la décision : chaque couche construit une description plus abstraite", subs=["l’entrée", "premières couches", "couches intermédiaires", "couches profondes", "la sortie"], gap=44),
           "Que se passe-t-il dans les couches cachées ? Prenons l’analyse d’une lame de biopsie. Les premières couches apprennent à détecter des bords et des textures. Les suivantes combinent ces bords en formes : des noyaux, des tubules. Les plus profondes reconnaissent des structures entières. La dernière prend la décision. Personne n’a programmé ces étapes. Le réseau les a construites parce qu’elles réduisaient son erreur. Ces descriptions intermédiaires s’appellent des représentations. C’est l’idée centrale de l’apprentissage profond, et le sujet de toute la deuxième partie du cours.",
           band="Un réseau profond apprend ses propres variables : on les appelle des représentations.")
    S.sec("L’entraînement : la descente de gradient de la séance 1, à grande échelle.")
    S.pts("L’entraînement d’un réseau", "La recette de la séance 1, répétée des milliers de fois.",
          ["On présente un <b>lot</b> d’exemples ; le réseau prédit.", "On mesure le coût.", "La <b>rétropropagation</b> calcule, pour chaque poids, dans quel sens le modifier.", "On ajuste tous les poids d’un petit pas."],
          "Comment règle-t-on des millions de poids ? Avec la recette de la première séance. Un : on présente au réseau un petit lot d’exemples, et il prédit. Deux : on mesure le coût, l’écart aux bonnes réponses. Trois : on calcule, pour chaque poids, dans quel sens le modifier pour réduire ce coût. Cette étape s’appelle la rétropropagation : l’erreur est renvoyée de la sortie vers l’entrée, couche après couche. Quatre : on ajuste tous les poids d’un petit pas. Et l’on recommence. Un passage complet sur les données s’appelle une époque.",
          fig=fig_loop())
    S.pts("Surveiller l’entraînement", "On trace deux courbes : le coût d’entraînement et le coût de validation.",
          ["Le coût d’entraînement baisse sans cesse.", "Le coût de validation baisse, puis remonte : le réseau commence à mémoriser.", f"On garde le modèle du minimum de validation : ici, l’époque {best}."],
          f"Un réseau a tellement de paramètres qu’il peut tout mémoriser. Vous connaissez le remède depuis la séance trois : on surveille une part de validation. En noir, le coût d’entraînement : il baisse sans cesse. En rouge, le coût de validation : il baisse, atteint un minimum, puis remonte. À partir de là, le réseau mémorise. On garde donc le modèle du minimum, ici à l’époque {best} : c’est l’arrêt précoce. Ces deux courbes sont le premier réflexe de toute personne qui entraîne un réseau.",
          fig=curves, band="C’est la courbe de la séance 3, lue au fil du temps.")
    S.sec("Quelle architecture pour quelles données, et quand ne pas utiliser un réseau profond.")
    S.tbl("Une architecture par type de données", "La forme du réseau reflète la forme des données.", ["Données", "Architecture", "Exemple pharmaceutique"],
          [["Tableaux cliniques", "Arbres combinés, petits réseaux", "Risque de surexposition"], ["Images", "Réseaux convolutifs, transformers de vision", "Lame de biopsie, radiographie"], ["Texte, séquences", "Transformers", "Notices, comptes rendus, séquences de protéines"], ["Molécules", "Réseaux sur graphes", "Prédire une propriété à partir de la structure"]],
          "Il existe plusieurs familles de réseaux, adaptées à la forme des données. Pour les images, les réseaux convolutifs et les transformers de vision. Pour le texte et les séquences, les transformers : c’est l’architecture des assistants conversationnels, mais aussi des modèles de protéines. Pour les molécules, les réseaux sur graphes, où les atomes sont des nœuds et les liaisons des arêtes. Et pour les tableaux cliniques ? Les arbres combinés de la séance deux restent le plus souvent le meilleur choix.",
          widths=[24, 38, 38])
    S.nums("Un exemple : chercher un antibiotique", "Un réseau entraîné à reconnaître les molécules antibactériennes (Stokes et al., Cell, 2020).",
           [("107 M", "107 millions de molécules d’une base publique passées au crible par le modèle"), ("23", "prédictions retenues et testées au laboratoire"), ("8", "se sont révélées antibactériennes, avec des structures éloignées des antibiotiques connus")],
           "Un exemple réel. En 2020, une équipe du MIT entraîne un réseau de neurones à reconnaître, à partir de sa structure, si une molécule a une activité antibactérienne. Le modèle identifie d’abord, dans une bibliothèque de médicaments existants, une molécule baptisée halicine, active sur des bactéries résistantes. Il passe ensuite au crible plus de cent sept millions de molécules d’une base publique. Vingt-trois prédictions sont testées au laboratoire : huit se révèlent antibactériennes. Remarquez l’ordre : le modèle propose, l’expérience vérifie.",
           band="Le modèle propose ; l’expérience vérifie.")
    S.cols("Modèles de fondation et IA générative", "Deux idées qui prolongent tout ce que nous venons de voir.",
           [("Pré-entraîner, puis adapter", "Un très grand réseau apprend d’abord sur d’immenses données sans étiquettes, en devinant des parties cachées.<br><br>On l’adapte ensuite à une tâche précise avec peu d’exemples. C’est un <b>modèle de fondation</b>."),
            ("Générer", "Le même type de réseau peut produire du nouveau : un texte, une image, une molécule candidate.<br><br>Il produit ce qui est <b>plausible</b> d’après ses données, pas ce qui est vérifié.")],
           "Deux idées pour finir cette partie. La première : pré-entraîner, puis adapter. Un très grand réseau apprend d’abord sur d’immenses quantités de données sans étiquettes, par apprentissage auto-supervisé. On l’adapte ensuite à une tâche précise, avec peu d’exemples. On appelle cela un modèle de fondation. La seconde : générer. Ces réseaux peuvent produire du nouveau, un texte ou une molécule candidate. Mais attention : ils produisent ce qui est plausible, pas ce qui est vérifié. La deuxième partie du cours détaille ces modèles ; le cours sur l’IA responsable apprend à les évaluer.",
           band="La partie II du cours, en anglais, détaille ces modèles pour les étudiants de master et les chercheurs.")
    S.pts("Quand ne pas utiliser un réseau profond", "Un modèle plus simple est souvent le bon choix.",
          ["<b>Peu de données, en tableau</b> : un modèle linéaire ou des arbres combinés font aussi bien, pour bien moins cher.", "<b>Besoin de lire la règle</b> : un réseau ne s’explique pas simplement.", "<b>Coût</b> : calcul, énergie, maintenance.", "Un réseau profond se justifie quand les données sont riches (images, texte, séquences) et nombreuses."],
          "Terminons par une mise en garde. L’apprentissage profond n’est pas toujours la bonne réponse. Avec quelques centaines de patients et un tableau de variables, un modèle linéaire ou des arbres combinés font le plus souvent aussi bien, pour bien moins cher. Si vous devez lire et justifier la règle, un réseau n’est pas le bon outil. Et il a un coût : en calcul, en énergie, en maintenance. Un réseau profond se justifie quand les données sont riches, images, textes ou séquences, et nombreuses.")
    S.ex("Un neurone, à la main", ["Un neurone a trois entrées : x₁ = 1,0 ; x₂ = −0,5 ; x₃ = 2,0.", "Ses poids : w₁ = 0,8 ; w₂ = 1,2 ; w₃ = −0,5. Son biais : b = 0,1. Son activation : ReLU.", "Calculez z, puis la sortie a. Recommencez avec x₃ = 0.", "Combien de paramètres compte un réseau à 3 entrées, une couche cachée de 4 neurones et 1 sortie ?"],
         dict(time="6 minutes", mat="Une calculatrice", out="Deux sorties et un nombre de paramètres"),
         "À vous. Un neurone a trois entrées : un ; moins zéro virgule cinq ; deux. Ses poids : zéro virgule huit ; un virgule deux ; moins zéro virgule cinq. Son biais : zéro virgule un. Son activation est ReLU. Calculez la somme pondérée z, puis la sortie a. Recommencez en mettant la troisième entrée à zéro. Dernière question : combien de paramètres compte un réseau à trois entrées, une couche cachée de quatre neurones et une sortie ? N’oubliez pas les biais.")
    S.sol("Un neurone, à la main", ["z = 0,8 × 1,0 + 1,2 × (−0,5) + (−0,5) × 2,0 + 0,1 = 0,8 − 0,6 − 1,0 + 0,1 = <b>−0,7</b>. ReLU : <b>a = 0</b>. Le neurone est éteint.", "Avec x₃ = 0 : z = 0,8 − 0,6 + 0 + 0,1 = <b>0,3</b>. ReLU : <b>a = 0,3</b>.", "Paramètres : (3 × 4 poids + 4 biais) + (4 × 1 poids + 1 biais) = 16 + 5 = <b>21</b>."],
          "La correction. Zéro virgule huit, moins zéro virgule six, moins un, plus zéro virgule un : z vaut moins zéro virgule sept. ReLU renvoie zéro : le neurone est éteint. Avec la troisième entrée à zéro, z vaut zéro virgule trois, et la sortie aussi. Pour les paramètres : douze poids et quatre biais dans la couche cachée, quatre poids et un biais en sortie. Vingt et un au total. Vous venez de faire, à la main, ce qu’un processeur graphique fait des milliards de fois par seconde.")
    S.quiz([("Sans fonction d’activation, un réseau à dix couches équivaut à :", ["Un arbre de décision", "Un simple modèle linéaire", "Un modèle de langage"], 1, "Une composition de sommes pondérées reste une somme pondérée."),
            ("La rétropropagation sert à :", ["Lire les données", "Calculer dans quel sens modifier chaque poids", "Choisir le nombre de couches"], 1, "Elle calcule les gradients du coût par rapport à tous les poids."),
            ("300 patients, 12 variables en tableau. Premier modèle à essayer :", ["Un réseau très profond", "Un modèle linéaire ou des arbres combinés", "Un modèle génératif"], 1, "Peu de données en tableau : un modèle simple est la référence.")],
           "Trois questions. Sans activation, dix couches équivalent à un simple modèle linéaire. La rétropropagation calcule dans quel sens modifier chaque poids. Trois cents patients et douze variables : on commence par un modèle linéaire ou des arbres combinés.")
    S.take(["Un neurone : une somme pondérée, puis une activation.", "Un réseau profond apprend lui-même ses représentations, couche après couche.", "Il s’entraîne par descente de gradient, sous surveillance d’une courbe de validation.", "Il se justifie pour des données riches et nombreuses, pas pour un petit tableau."],
           "Quatre idées. Un neurone, c’est une somme pondérée suivie d’une activation. Un réseau profond apprend lui-même ses représentations, couche après couche. Il s’entraîne par descente de gradient, sous la surveillance d’une courbe de validation. Et il se justifie pour des données riches et nombreuses, pas pour un petit tableau.")
    S.refs(["J. M. Stokes et al., « A Deep Learning Approach to Antibiotic Discovery », <i>Cell</i>, 2020 ; 180(4) : 688-702. doi:10.1016/j.cell.2020.01.021", "Y. LeCun, Y. Bengio, G. Hinton, « Deep learning », <i>Nature</i>, 2015 ; 521 : 436-444.", "S. J. D. Prince, <i>Understanding Deep Learning</i>, MIT Press, 2023 (chapitres 1 à 4 ; libre accès sur udlbook.com)."],
           "Trois références. L’article sur la découverte de l’halicine. L’article de synthèse de 2015 sur l’apprentissage profond. Et un manuel récent, en libre accès, très bien illustré.")
    S.end("Session 5 · Optimization and generalization in deep networks (Part II, in English)", "C’est la fin de la première partie. Vous avez maintenant le vocabulaire et les idées pour lire une étude d’apprentissage automatique. La deuxième partie, en anglais, s’adresse à celles et ceux qui veulent construire ces modèles : optimisation, transformers, apprentissage de représentations, modèles génératifs et modèles de fondation. Merci, et à bientôt.")
    return S
