import pandas as pd
import numpy as np
import unicodedata
import regex
import re


def normalize_chars(string):
    processed_string = unicodedata.normalize('NFKD', string)
    processed_string = processed_string.lower()
    return processed_string


def separate_subexpressions(string):
    list_markers = ',\.:;"!\?\\/#。，“”．…、«»¿¡\(\)\[\]\{\}—'   # most common Latin punctuation chars
    regex_str = '['+list_markers+']+'
    list_sentences = re.split(regex_str, string)
    filtered_list = list( filter(lambda x: len(x)>0, list_sentences) ) # remove empty lists
    return filtered_list


def tokenize_sentence(sentence):
    word_separators = '‘’\'\s\-–'
    regex_str = '[' + word_separators + ']+'
    list_words = re.split(regex_str, sentence)
    filtered_list = list( filter(lambda x: len(x)>0, list_words) ) # remove empty lists
    return filtered_list


def convert_sentence_to_indices(word_list, vector):
    # Uses vector indices to convert word_list to sequence of numbers
    converted_list = []
    for w in word_list:
        try:
            converted_list.append(vector.index(w))
        except:
            vector.append(w)
            converted_list.append(len(vector)-1)
    return converted_list, vector


def process_raw_string(string, vector):
    normalized = normalize_chars(string)
    sentences = separate_subexpressions(normalized)
    double_list_words = []
    for sub_sentence in sentences:
        tokenized = tokenize_sentence(sub_sentence)
        converted, vector = convert_sentence_to_indices(tokenized, vector)
        double_list_words.append(converted)
    filtered = list( filter(lambda x: len(x)>0, double_list_words) ) # remove empty lists
    return filtered, vector


def process_site_data(site_dict_list, vector):
    processed_list = []
    for item_dict in site_dict_list:
        proc_item_dict = {}
        for key in list(item_dict.keys()):
            proc_string, vector = process_raw_string(item_dict[key], vector)
            proc_item_dict.update({key: proc_string})
        processed_list.append(proc_item_dict)
    return processed_list, vector
            





if __name__ == '__main__':
    # normalized = normalize_chars("Municipales à Paris : le candidat Horizons [Pierre-Yves} Bournazel affirme qu’il ne rejoindra « ni Grégoire ni Dati » au second tour ")
    # sentences = separate_subexpressions(normalized)
    # double_list_words = []
    # vector = []
    # for sub_sentence in sentences:
    #     tokenized = tokenize_sentence(sub_sentence)
    #     vector, converted = convert_sentence_to_indices(vector, tokenized)
    #     double_list_words.append(converted)
    # print(vector, '\n', double_list_words)

    test_rss_dict = {'lemonde': [{'title': 'Ukraine\xa0: «\xa0La guerre pourrait encore durer des années et, paradoxalement, le temps joue contre le Kremlin\xa0»', 'desc': 'Le chercheur Dimitri Minic estime dans un entretien au «\xa0Monde\xa0» qu’«\xa0il ne faut pas enterrer l’Ukraine trop vite\xa0», même si le rapport de force est actuellement favorable à la Russie.'}, 
                                 {'title': 'EN DIRECT, Césars 2026\xa0: «\xa0Nouvelle Vague\xa0» remporte son quatrième prix, avec celui de la meilleure réalisation pour Richard Linklater', 'desc': 'La cérémonie du cinéma français se tient jeudi. Nadia Melliti et Théodore Pellerin ont remporté les prix de meilleurs espoirs, Pierre Lottin celui du meilleur acteur dans un second rôle.'}, 
                                 {'title': 'Catherine Pégard, ancienne présidente du château de Versailles et proche d’Emmanuel Macron, remplace Rachida Dati au ministère de la culture', 'desc': 'A 71\xa0ans, l’ancienne journaliste devenue conseillère du président Nicolas Sarkozy a su, grâce à sa discrétion et à son entregent, se rendre indispensable. La nouvelle locataire de la Rue de Valois devra gérer plusieurs chantiers d’importance, dont le projet Louvre Renaissance et la réforme de l’audiovisuel public.'}, 
                                 {'title': '«\xa0La reconstitution des capacités balistiques de l’Iran apparaît plus préoccupante qu’une relance rapide du nucléaire\xa0»', 'desc': 'Dans un entretien au «\xa0Monde\xa0», la chercheuse Nicole Grajewski analyse l’état des capacités militaires de Téhéran huit mois après les frappes israélo-américaines de juin\xa02025.'}, 
                                 {'title': 'L’Afghanistan affirme avoir lancé des «\xa0attaques massives\xa0» au Pakistan, en réponse à des bombardements', 'desc': 'Ces attaques surviennent quelques jours après des échanges de tirs entre forces afghanes et pakistanaises le long de leur frontière, chaque camp en rejetant la responsabilité sur l’autre.'}, 
                                 {'title': 'Dans l’automobile, les constructeurs français affichent des pertes financières record', 'desc': 'En\xa02025, les résultats nets déficitaires cumulés de Stellantis, Renault et Forvia ont dépassé 35\xa0milliards d’euros. Ils reflètent la phase de transformation à hauts risques que traverse le secteur, bousculé par le stop-and-go des politiques d’électrification de la mobilité.'}, 
                                 {'title': 'La SNCF engrange de copieux profits grâce à une fréquentation record', 'desc': 'La société ferroviaire a dégagé un bénéfice net de 1,8\xa0milliard d’euros en\xa02025, en hausse de 16\xa0%, tiré par les performances financières du TGV.'}, 
                                 {'title': 'Amiante\xa0dans des jouets pour enfants\xa0: la répression des fraudes appelle à suspendre la vente de tous ceux «\xa0à base de sable\xa0»', 'desc': '«\xa0Les produits concernés sont par exemple des jouets contenant du sable coloré pour des activités créatives, du sable à modeler aussi appelé “sable magique”\xa0», précise la DGCCRF.'}, 
                                 {'title': 'La commission d’enquête sur l’audiovisuel public fait une pause bienvenue au terme d’une nouvelle journée mouvementée', 'desc': 'Le coactionnaire du groupe audiovisuel Mediawan Xavier Niel (également actionnaire à titre individuel du «\xa0Monde\xa0») ne s’est pas présenté à son audition, écourtant de ce fait la dernière journée des travaux de la commission avant les élections municipales.'}, 
                                 {'title': 'Liban\xa0: l’armée israélienne annonce avoir frappé huit bases militaires du Hezbollah dans l’est du pays', 'desc': 'Le ministère de la santé libanais a fait état d’un mort. Selon l’armée israélienne, les infrastructures stockaient «\xa0des armes à feu et des roquettes\xa0».'}, 
                                 {'title': 'Quelques centaines d’euros pour 60\xa0heures de travail par semaine\xa0: avec les jeunes précaires de la collecte de dons', 'desc': 'Entre promesse d’argent rapide et discours de réussite, l’entreprise Geninc et ses franchises recrutent des 18-25\xa0ans pour des missions de porte-à-porte sous statut précaire. D’anciens «\xa0ambassadeurs\xa0» dénoncent des conditions de travail éprouvantes, des dérives managériales et une grande opacité.'}, 
                                 {'title': '«\xa0La trajectoire de Jeffrey Epstein rappelle que l’esbroufe et l’entourloupe restent monnaie courante\xa0»', 'desc': 'Les détenteurs de pouvoirs cultivent un entre-soi qui les protège et les conforte dans un sentiment de puissance semblant légitimer leurs abus, soulignent, dans une tribune au «\xa0Monde\xa0», les sociologues François Denord, Paul Lagneau-Ymonet et Sylvain Thine.'}, 
                                 {'title': 'Iran - Etats-Unis\xa0: Téhéran salue de «\xa0bons progrès\xa0» et envisage de nouveaux pourparlers avec Washington «\xa0dans moins d’une semaine\xa0»', 'desc': 'Les Etats-Unis veulent arracher un accord empêchant notamment l’Iran de se doter de l’arme nucléaire, une crainte des Occidentaux alimentant de longue date les tensions avec Téhéran. La République islamique dément nourrir cette ambition, mais campe sur son «\xa0droit\xa0» au nucléaire civil.'}, 
                                 {'title': 'Après l’examen «\xa0acrobatique\xa0» des derniers budgets, le Sénat veut encadrer les règles du jeu', 'desc': 'Le Palais du Luxembourg a adopté, jeudi 26\xa0février, une proposition de loi visant à sécuriser les procédures dérogatoires prévues par la Constitution en cas d’absence de budget. Dans son viseur notamment\xa0: les ordonnances financières.'}, 
                                 {'title': 'La justice allemande offre au parti d’extrême droite AfD une victoire symbolique', 'desc': 'Le tribunal de Cologne a confirmé, jeudi, la suspension du classement du parti Alternative für Deutschland comme organisation «\xa0d’extrême droite avérée\xa0», décidée par les services de renseignement. Le jugement ne préjuge toutefois pas de la procédure au fond, qui se poursuit.'}, 
                                 {'title': 'Affaire Epstein\xa0: Hillary Clinton demande devant une commission d’enquête parlementaire que Donald Trump témoigne «\xa0sous serment\xa0»', 'desc': 'La déposition à huis clos d’Hillary Clinton se tient à Chappaqua, près de New York, où réside le couple Clinton. Son époux, photographié plusieurs fois en compagnie de Jeffrey Epstein, doit témoigner vendredi, au même endroit.'}, 
                                 {'title': 'En Turquie, Recep Tayyip Erdogan qualifie de «\xa0fanatiques\xa0» les signataires d’une pétition pour la défense de la laïcité', 'desc': 'Signée par 168\xa0intellectuels, artistes et représentants d’associations professionnelles, la pétition critique une directive du ministère turc de l’éducation nationale recommandant notamment d’emmener à la mosquée les enfants de 4\xa0à 6\xa0ans, accompagnés de leurs enseignants.'}, 
                                 {'title': 'Les pays de l’UE pourront financer avec des fonds européens des avortements dans des pays où la législation est contraignante', 'desc': 'Cette mesure a été votée en réponse à une pétition signée par plus d’1\xa0million de personnes et réclamant des financements pour des avortements «\xa0sûrs\xa0».'}]}
    vector = []
    processed_list, vector = process_site_data(test_rss_dict['lemonde'], vector)
    print(len(processed_list))
    print(processed_list)
    print(vector)



