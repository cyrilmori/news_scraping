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
            

def process_data_all_sites(sites_dict):
    processed_dict = {}
    vector = []
    for site_name in list(sites_dict.keys()):
        processed_list, vector = process_site_data(sites_dict[site_name], vector)
        processed_dict.update({site_name: processed_list})
    return processed_dict, vector
        




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

    test_rss_dict = {'lemonde': [{'title': 'UE-Mercosur\xa0: l’accord commercial entrera en vigueur sans attendre le vote du Parlement européen', 'desc': 'La présidente de la Commission, Ursula von der Leyen, en a précipité l’annonce vendredi, au grand regret de la France.'}, {'title': 'LFI sera bien classée à l’«\xa0extrême gauche\xa0» par le ministère de l’intérieur, juge le Conseil d’Etat', 'desc': 'La plus haute juridiction administrative a rejeté, vendredi 27\xa0février, le recours du mouvement de Jean-Luc Mélenchon contre la décision du ministère de l’intérieur de sortir ses candidats du «\xa0bloc de gauche\xa0» pour les élections municipales.'}, {'title': 'Le drone à proximité du porte-avions «\xa0Charles-de-Gaulle\xa0» était bien russe, confirment les forces armées suédoises', 'desc': 'Ce drone a été brouillé mercredi à environ 13\xa0kilomètres du «\xa0Charles-de-Gaulle\xa0» dans le détroit d’Oresund, près de la ville de Malmö, où le navire amiral français est arrivé pour une escale avant de participer à des exercices de l’OTAN.'}, {'title': 'Donald Trump se dit «\xa0pas très content\xa0» de la teneur des négociations avec Téhéran et affirme ne pas avoir pris de «\xa0décision finale\xa0» sur de possibles frappes américaines', 'desc': 'Ces annonces interviennent au lendemain d’une troisième session de pourparlers à Genève sous médiation omanaise entre l’Iran et les Etats-Unis, perçue comme l’une des dernières chances pour éviter une guerre.'}, {'title': 'James Char, spécialiste de l’armée chinoise\xa0: «\xa0L’ampleur des mises à l’écart sous Xi Jinping dépasse de loin ce qu’ont fait ses prédécesseurs\xa0»', 'desc': 'L’éviction, en janvier, du général le plus haut gradé de l’Armée populaire de libération témoigne de la volonté du président Xi d’assurer sa prééminence politique et de lutter contre la corruption, bien réelle, des élites, décrypte le chercheur James Char dans un entretien au «\xa0Monde\xa0».'}, {'title': 'Avec l’album «\xa0The Mountain\xa0», Gorillaz approche à nouveau les sommets', 'desc': 'Le dernier disque du groupe, aux sonorités indiennes, reprend les principes de l’hybridation, des voyages et des collaborations chers à la formation.'}, {'title': 'EN DIRECT, guerre en Ukraine\xa0: deux femmes tuées dans l’oblast de Soumy, cinq blessés dans celui de Kharkiv après des frappes russes', 'desc': 'Deux femmes, âgées de 72\xa0et 67\xa0ans, employées d’une exploitation agricole, sont mortes lors d’une frappe russe dans la ville de Chostka. Les forces russes ont également mené une frappe de drone sur le village de Verkhnia Rohanka, faisant cinq blessés dont deux enfants.'}, {'title': 'A Milan, un tramway déraille, faisant deux morts et 38\xa0blessés', 'desc': 'L’accident s’est produit vers 16\xa0heures dans la rue Vittorio Veneto, alors que le tramway circulait de la place de la République vers Porta Venezia.'}, {'title': 'Donald Trump évoque une possible «\xa0prise de contrôle pacifique\xa0» de Cuba alors que Washington accentue la pression sur l’île', 'desc': 'Alors que Cuba traverse une grave crise économique, le président américain laisse entendre un possible changement de cap dans les relations entre Washington et La\xa0Havane.'}, {'title': 'L’Arcom saisie dès la première semaine de «\xa0100\xa0% Frontières\xa0» sur CNews', 'desc': 'Le nouveau programme quotidien diffusé depuis le 23\xa0février est déjà visé par plusieurs saisines adressées au régulateur de l’audiovisuel.'}, {'title': 'Des ONG internationales obtiennent un sursis de la Cour suprême israélienne pour poursuivre leur travail dans les territoires palestiniens occupés', 'desc': 'Dix-huit ONG devraient éviter une fermeture de force de leurs bureaux, mais elles craignent que des obstructions à leur travail se poursuivent sur le terrain.'}, {'title': 'Bill Clinton assure n’avoir «\xa0eu aucune idée des crimes que commettait\xa0» Jeffrey Epstein', 'desc': 'L’ancien président américain, qui a dirigé le pays entre 1993 et 2001, est mentionné à de multiples reprises dans le dossier, sans qu’aucun fait répréhensible lui ait jamais été imputé.'}, {'title': 'Eric Woerth, candidat à la présidence du PMU, quitte l’Assemblée nationale après plus de vingt ans en poste', 'desc': 'Missionné depuis début septembre par le gouvernement pour proposer une réforme de la gouvernance du PMU, il a vu sa mission récemment prolongée. En dépassant les six mois, son mandat de député tombe donc automatiquement.'}, {'title': 'Philippines\xa0: la sanglante «\xa0guerre contre la drogue\xa0» de Rodrigo Duterte devant la Cour pénale internationale', 'desc': 'Pendant quatre\xa0jours, le bureau du procureur de la CPI s’est efforcé de convaincre les juges de cette cour de mettre en accusation l’ancien président pour crimes contre l’humanité commis dans le cadre de sa lutte contre la drogue. Les juges ont soixante jours pour décider s’ils renvoient en procès l’ex-dirigeant.'}, {'title': 'En Corée du Nord, un congrès qui consacre la toute-puissance de Kim Jong-un', 'desc': 'Le 9ᵉ congrès du Parti du travail a défini les grandes lignes des politiques de la Corée du Nord pour les cinq années à venir. La priorité va à l’économie. La défense reste importante. Et Pyongyang n’exclut pas de renouer le dialogue avec Washington. Le tout sous le contrôle renforcé du dirigeant Kim Jong-un.'}, {'title': 'Rwanda\xa0: Claude Muhayimana condamné en appel pour «\xa0complicité de génocide\xa0» à 14\xa0années de réclusion', 'desc': 'La cour d’assises de Paris a condamné l’ancien cantonnier de Rouen pour avoir transporté des miliciens sur différents lieux de massacres en avril\xa01994.'}, {'title': 'Bruno Mars, toujours aussi «\xa0feel good\xa0» avec son nouvel album «\xa0The Romantic\xa0»', 'desc': 'Le chanteur américain publie son quatrième opus solo, dix ans après le succès de «\xa024K Magic\xa0».'}, {'title': 'A Moscou, le «\xa0pont Nemtsov\xa0», fragile mémorial d’une opposition traquée', 'desc': 'Le 27\xa0février\xa02015, Boris Nemtsov, figure de l’opposition au régime de Vladimir Poutine, était tué à coups de pistolet dans le dos. Le pont où a eu lieu l’assassinat, en face du Kremlin, est devenu un lieu symbolique.'}, {'title': 'Vins rouges de la vallée du Rhône septentrionale\xa0: la\xa0sélection du «\xa0Monde\xa0»', 'desc': 'Près de 150\xa0rouges du nord de la vallée du Rhône ont été goûtés à l’aveugle par Rémi Barroux, Stéphane Davet, Laure Gasparotto et Sébastien Jenvrin. Le choix de\xa040\xa0cuvées a été difficile, tant la qualité des côte-rôtie, crozes-hermitage, hermitages et saint-joseph était au rendez-vous.'}], 
                  'mediapart': [{'title': 'Jean-Luc Mélenchon: la faute de trop', 'desc': 'Par ses égarements antisémites et complotistes, Jean-Luc Mélenchon dessert le combat antifasciste, son unité et sa moralité. Sa sortie lyonnaise à propos de l’affaire du pédocriminel Epstein est la faute de trop.'}, {'title': 'Complotisme et antisémitisme: Jean-Luc Mélenchon scandalise la gauche', 'desc': 'Lors d’un meeting à Lyon, le leader de La France insoumise a ironisé sur la prononciation du nom du pédocriminel Jeffrey Epstein par les médias, ajoutant à ses nombreuses fautes sur l’antisémitisme. Immédiatement le reste de la gauche a condamné en bloc, et demande une clarification.'}, {'title': 'Pantouflage, aides publiques et revente controversée: le fonds Tikehau se justifie face aux députés', 'desc': 'Le fonds français est critiqué pour avoir vendu une PME stratégique de la défense à un groupe états-unien, mais aussi pour ses liens avec les pouvoirs publics. Face aux députés de la commission d’enquête sur les fonds spéculatifs, il a tenté de se défendre, sans totalement convaincre.'}, {'title': 'Didier Chaudet: «Le but du Pakistan est de forcer les talibans à un changement d’attitude»', 'desc': 'Le Pakistan a choisi de frapper l’Afghanistan dans la nuit du jeudi 26 au vendredi 27 février. Selon le spécialiste Didier Chaudet, Islamabad cherche à «sécuriser sa frontière», dans un contexte géopolitique incertain, après des intermédiations infructueuses.'}, {'title': 'L’Iran sous pression maximale d’une intervention des États-Unis', 'desc': 'Tout en assurant privilégier la voie du dialogue avec la dictature des mollahs, le président Trump brandit la menace d’une intervention militaire en Iran, où les manifestations repartent dans plusieurs universités.'}, {'title': '«Même si je suis facho, je suis fière de l’être»: à Marseille, une candidate venue du RN écartée des listes de Martine Vassal', 'desc': 'Dans une vidéo que «Marsactu» s’est procurée, l’ancienne élue RN Élisabeth Philippe, recrutée sur les listes de la droite marseillaise, tient des propos ouvertement islamophobes et xénophobes. En réaction, le retrait de cette candidate a été annoncé.'}, {'title': 'Rachat de la Warner: à Hollywood, la menace d’un géant pro-Trump', 'desc': 'Netflix a fini par jeter l’éponge jeudi 26 février dans la bataille pour le rachat de la Warner qui semble promise à Paramount. Cet abandon ouvre la voie à la constitution d’un nouveau géant du cinéma et de l’information proche du président états-unien.'}, {'title': 'Une enquête pour escroquerie et blanchiment éclabousse plusieurs clubs de Ligue\xa01', 'desc': 'Ancien joueur de l’OM reconverti en agent, Jean-Christophe Cano est au cœur d’une enquête judiciaire pour escroquerie, blanchiment et fraude fiscale aggravée, liée à la gestion de la carrière de plusieurs joueurs professionnels. Les clubs de Montpellier, Brest, Lorient et Bastia ont été auditionnés.'}, {'title': 'Élection partielle au Royaume-Uni: une défaite cinglante pour le pouvoir travailliste', 'desc': 'Les écologistes britanniques ont remporté leur premier siège de député dans le nord de l’Angleterre, en gagnant la partielle organisée dans la circonscription de Gordon and Denton, avec plus de 40% des suffrages. Le Labour au pouvoir, qui détenait le siège, finit à la troisième place.'}, {'title': 'La pronucléaire Maud Bregeon chargée de l’énergie: le ministère du mélange des genres', 'desc': 'Dans le cadre d’un remaniement, le premier ministre Sébastien Lecornu a nommé Maud Bregeon aux questions énergétiques le 26 février. Ancienne ingénieure d’EDF, elle est une ardente défenseuse de la filière atomique et a été rapporteuse du projet de loi d’accélération nucléaire en 2023.'}]}


    processed_dict, vector = process_data_all_sites(test_rss_dict)
    print(processed_dict)
    print(vector)



