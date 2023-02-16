import os
import PySimpleGUI as sg
import csv
from scripts import solver
from itertools import product


def charger_profile(adresse):
    try:
        dic_dim = {}
        with open(adresse, 'r') as file:
            csvreader = csv.reader(file,  delimiter=';')
            column_count = len(next(csvreader))

            dic_dim = {}
            for row in csvreader:

                new_key = row[0]
                dic_dim[new_key] = []
                
                for column in range(column_count-1):
                    dic_dim[new_key].append(row[column+1])

        return(dic_dim)
    except:
        print('Pas de fichier liste à charger à l\'adresse', adresse)

#Chargement des proprietes de charge profilé
dic_dim_IPE = charger_profile(os.path.dirname(os.path.realpath(__file__)) + "\\liste_profiles\\IPE-HE.csv")
dic_dim_IPN = charger_profile(os.path.dirname(os.path.realpath(__file__)) + "\\liste_profiles\\IPN.csv")
dic_dim_UPN = charger_profile(os.path.dirname(os.path.realpath(__file__)) + "\\liste_profiles\\UPN.csv")
dic_dim_UPE = charger_profile(os.path.dirname(os.path.realpath(__file__)) + "\\liste_profiles\\UPE-UAP.csv")
dic_dim_COR = charger_profile(os.path.dirname(os.path.realpath(__file__)) + "\\liste_profiles\\Cornieres.csv")

sg.theme('TanBlue')
col_parametres = [[sg.Text('Niveau RCCM'), sg.Listbox(values=('0AB', 'C', 'D'), default_values='0AB', size=(10, 3), key='-NIVEAU_RCCM-')],
    [sg.Text('Type profilé'), sg.Listbox(values=('IPN', 'IPE-HE', 'UPN', 'UPE-UAP', 'Corniere', 'Rectangle', 'Tube'), size=(10, 7), enable_events=True, key="-PROFILE-")],
    [sg.Text('Longueur'), sg.Input(key='-LONGUEUR-', tooltip='mm', size=(10,1))],
    [sg.Text('Coefficient de longueur K'), sg.Input(2, key='-KLONGUEUR-', size=(10,1))],
    [sg.Frame('Torseur', [[sg.Text('N'), sg.Input(0, key='-TORSEUR_N-', tooltip='N', size=(10,1))],
                             [sg.Text('Fx'), sg.Input(0, key='-TORSEUR_FX-', tooltip='N', size=(10,1))],
                             [sg.Text('Fy'), sg.Input(0, key='-TORSEUR_FY-', tooltip='N', size=(10,1))],
                             [sg.Text('Mx'), sg.Input(0, key='-TORSEUR_MX-', tooltip='N.m', size=(10,1))],
                             [sg.Text('My'), sg.Input(0, key='-TORSEUR_MY-', tooltip='N.m', size=(10,1))],
                             [sg.Text('Mz'), sg.Input(0, key='-TORSEUR_MZ-', tooltip='N.m', size=(10,1))],
                             [sg.Checkbox('Itérer signes', key='-ITER_SIGNS-')]
                             ],
                element_justification='r')
    ],
    [sg.Frame('Matériau', [[sg.Text('Sy'), sg.Input(235, key='-SY-', tooltip='MPa', size=(5,1))],
                             [sg.Text('Su'), sg.Input(360, key='-SU-', tooltip='MPa', size=(5,1))],
                             [sg.Text('E'), sg.Input(210000, key='-MODULE-', tooltip='MPa', size=(8,1))],
                             ],
                element_justification='r')
    ]
    ]

col_image = [
    [sg.Image(key='-IMAGEPROFILE-')],
    [sg.Text('Angle de rotation'), sg.Input(0, key='-ANGLEROT-', tooltip='Degrés, sens trigonométrique', size=(5,1))],
    [sg.Text('Taille du maillage'), sg.Input(10, key='-MESH_SIZE-', size=(5,1))],
    ]

########################COLONNES MASQUEES / AFFICHEES SELON LES PROFILES###############################

col_IPN = [[sg.Combo(values=list(dic_dim_IPN), readonly=True, k='-LISTE_IPN-', size=(20,1), enable_events=True)],
    [sg.Text('d, hauteur'), sg.Input(key='In_IPN_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_IPN_b', size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(key='In_IPN_t_f', size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(key='In_IPN_t_w', size=(5,1))],
    [sg.Text('r_r, rayon en racine'), sg.Input(key='In_IPN_r_r', size=(5,1))],
    [sg.Text('r_f, rayon de l\'aile'), sg.Input(key='In_IPN_r_f', size=(5,1))],
    [sg.Text('alpha, angle en degrés de l\'aile'), sg.Input(key='In_IPN_alpha', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation des rayons'), sg.Input(15, key='In_IPN_n_r', size=(5,1))]
    ]

col_IPE = [[sg.Combo(values=list(dic_dim_IPE), readonly=True, k='-LISTE_IPE-', size=(20,1), enable_events=True)],
    [sg.Text('d, hauteur'), sg.Input(key='In_IPE_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_IPE_b', size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(key='In_IPE_t_f', size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(key='In_IPE_t_w', size=(5,1))],
    [sg.Text('r, rayon en racine'), sg.Input(key='In_IPE_r', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(15, key='In_IPE_n_r', size=(5,1))]
    ]

col_UPN = [[sg.Combo(values=list(dic_dim_UPN), readonly=True, k='-LISTE_UPN-', size=(20,1), enable_events=True)],
    [sg.Text('d, hauteur'), sg.Input(key='In_UPN_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_UPN_b', size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(key='In_UPN_t_f', size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(key='In_UPN_t_w', size=(5,1))],
    [sg.Text('r_r, rayon en racine'), sg.Input(key='In_UPN_r_r', size=(5,1))],
    [sg.Text('r_f, rayon de l\'aile'), sg.Input(key='In_UPN_r_f', size=(5,1))],
    [sg.Text('alpha, angle en degrés de l\'aile'), sg.Input(key='In_UPN_alpha', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation des rayons'), sg.Input(15, key='In_UPN_n_r', size=(5,1))]
    ]

col_UPE = [[sg.Combo(values=list(dic_dim_UPE), readonly=True, k='-LISTE_UPE-', size=(20,1), enable_events=True)],
    [sg.Text('d, hauteur'), sg.Input(key='In_UPE_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_UPE_b', size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(key='In_UPE_t_f', size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(key='In_UPE_t_w', size=(5,1))],
    [sg.Text('r, rayon en racine'), sg.Input(key='In_UPE_r', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(15, key='In_UPE_n_r', size=(5,1))]
    ]

col_Corniere = [[sg.Combo(values=list(dic_dim_COR), readonly=True, k='-LISTE_COR-', size=(20,1), enable_events=True)],
    [sg.Text('d, hauteur'), sg.Input(key='In_COR_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_COR_b', size=(5,1))],
    [sg.Text('t, épaisseur'), sg.Input(key='In_COR_t', size=(5,1))],
    [sg.Text('r_r, rayon en racine'), sg.Input(key='In_COR_r_r', size=(5,1))],
    [sg.Text('r_t, rayon en pied'), sg.Input(key='In_COR_r_t', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(15, key='In_COR_n_r', size=(5,1))]
    ]

col_Rectangle = [[sg.Text('d, hauteur'), sg.Input(key='In_REC_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_REC_b', size=(5,1))],
    [sg.Text('t, épaisseur'), sg.Input(key='In_REC_t', size=(5,1))],
    [sg.Text('r_out, rayon extérieur'), sg.Input(key='In_REC_r_out', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(15, key='In_REC_n_r', size=(5,1))]
    ]

col_Tube = [[sg.Text('d, diamètre extérieur'), sg.Input(key='In_TUB_d', size=(5,1))],
    [sg.Text('t, épaisseur'), sg.Input(key='In_TUB_t', size=(5,1))],
    [sg.Text('n, nombre de points de discrétisation des cercles'), sg.Input(key='In_TUB_n', size=(5,1))]
    ]

#############################FIN COLONNES SPECIFIQUES AU CHOIX DU PROFILE##########################

lig_Cal = [[sg.Push(), sg.Checkbox('Imprimer paramètres de section', key='-PRINT_PARAM-'), sg.Checkbox('Tracer résultats', key='-DRAW_RESULTS-')],
    [sg.Push(), sg.Button('Quitter'), sg.Button('Calcul')]]

layout = [[sg.Column(col_parametres, element_justification='r'),
        sg.VSeperator(),
        sg.Column(col_image, element_justification='r'),
        sg.Column(col_IPN, element_justification='r', visible=False, key='col_IPN'),
        sg.Column(col_IPE, element_justification='r', visible=False, key='col_IPE'),
        sg.Column(col_UPN, element_justification='r', visible=False, key='col_UPN'),
        sg.Column(col_UPE, element_justification='r', visible=False, key='col_UPE'),
        sg.Column(col_Corniere, element_justification='r', visible=False, key='col_Corniere'),
        sg.Column(col_Rectangle, element_justification='r', visible=False, key='col_Rectangle'),
        sg.Column(col_Tube, element_justification='r', visible=False, key='col_Tube')
        ],
        lig_Cal]

window = sg.Window('Dépouillement supports linéaires RCCM ZVI', layout, default_element_size=(40, 1), grab_anywhere=False, resizable=True)

while True:
    event, values = window.read()
    if event in ('Quitter', None):
        break
    if event == "-PROFILE-":  # un profilé a été selectionné
        nom_profile = values["-PROFILE-"]
        adresse_image = os.path.dirname(os.path.realpath(__file__)) + "\\images\\" + nom_profile[0] +".png"
        window['-IMAGEPROFILE-'].update(adresse_image)

        #Effacer les colonnes éventuellement affichées lors d'une sélection
        window['col_IPE'].update(visible=False)
        window['col_IPN'].update(visible=False)
        window['col_UPN'].update(visible=False)
        window['col_UPE'].update(visible=False)
        window['col_Corniere'].update(visible=False)
        window['col_Rectangle'].update(visible=False)
        window['col_Tube'].update(visible=False)

        #Afficher colonnes en fonction de la section
        if nom_profile[0] == "IPN":
            window['col_IPN'].update(visible=True)
        if nom_profile[0] == "IPE-HE":
            window['col_IPE'].update(visible=True)
        if nom_profile[0] == "UPN":
            window['col_UPN'].update(visible=True)
        if nom_profile[0] == "UPE-UAP":
            window['col_UPE'].update(visible=True)
        if nom_profile[0] == "Corniere":
            window['col_Corniere'].update(visible=True)
        if nom_profile[0] == "Rectangle":
            window['col_Rectangle'].update(visible=True)
        if nom_profile[0] == "Tube":
            window['col_Tube'].update(visible=True)

    if event == "-LISTE_IPN-":
        window['In_IPN_d'].update(value=dic_dim_IPN[values['-LISTE_IPN-']][0])
        window['In_IPN_b'].update(value=dic_dim_IPN[values['-LISTE_IPN-']][1])
        window['In_IPN_t_f'].update(value=dic_dim_IPN[values['-LISTE_IPN-']][2])
        window['In_IPN_t_w'].update(value=dic_dim_IPN[values['-LISTE_IPN-']][3])
        window['In_IPN_r_r'].update(value=dic_dim_IPN[values['-LISTE_IPN-']][4])
        window['In_IPN_r_f'].update(value=dic_dim_IPN[values['-LISTE_IPN-']][5])
        window['In_IPN_alpha'].update(value=dic_dim_IPN[values['-LISTE_IPN-']][6])

    if event == "-LISTE_IPE-":
        window['In_IPE_d'].update(value=dic_dim_IPE[values['-LISTE_IPE-']][0])
        window['In_IPE_b'].update(value=dic_dim_IPE[values['-LISTE_IPE-']][1])
        window['In_IPE_t_f'].update(value=dic_dim_IPE[values['-LISTE_IPE-']][2])
        window['In_IPE_t_w'].update(value=dic_dim_IPE[values['-LISTE_IPE-']][3])
        window['In_IPE_r'].update(value=dic_dim_IPE[values['-LISTE_IPE-']][4])

    if event == "-LISTE_UPN-":
        window['In_UPN_d'].update(value=dic_dim_UPN[values['-LISTE_UPN-']][0])
        window['In_UPN_b'].update(value=dic_dim_UPN[values['-LISTE_UPN-']][1])
        window['In_UPN_t_f'].update(value=dic_dim_UPN[values['-LISTE_UPN-']][2])
        window['In_UPN_t_w'].update(value=dic_dim_UPN[values['-LISTE_UPN-']][3])
        window['In_UPN_r_r'].update(value=dic_dim_UPN[values['-LISTE_UPN-']][4])
        window['In_UPN_r_f'].update(value=dic_dim_UPN[values['-LISTE_UPN-']][5])
        window['In_UPN_alpha'].update(value=dic_dim_UPN[values['-LISTE_UPN-']][6])

    if event == "-LISTE_UPE-":
        window['In_UPE_d'].update(value=dic_dim_UPE[values['-LISTE_UPE-']][0])
        window['In_UPE_b'].update(value=dic_dim_UPE[values['-LISTE_UPE-']][1])
        window['In_UPE_t_f'].update(value=dic_dim_UPE[values['-LISTE_UPE-']][2])
        window['In_UPE_t_w'].update(value=dic_dim_UPE[values['-LISTE_UPE-']][3])
        window['In_UPE_r'].update(value=dic_dim_UPE[values['-LISTE_UPE-']][4])

    if event == "-LISTE_COR-":
        window['In_COR_d'].update(value=dic_dim_COR[values['-LISTE_COR-']][0])
        window['In_COR_b'].update(value=dic_dim_COR[values['-LISTE_COR-']][1])
        window['In_COR_t'].update(value=dic_dim_COR[values['-LISTE_COR-']][2])
        window['In_COR_r_r'].update(value=dic_dim_COR[values['-LISTE_COR-']][3])
        window['In_COR_r_t'].update(value=dic_dim_COR[values['-LISTE_COR-']][4])



    if event == "Calcul":
        torseur = {'N':values['-TORSEUR_N-'], 'Fx':values['-TORSEUR_FX-'], 'Fy':values['-TORSEUR_FY-'],
            'Mx':values['-TORSEUR_MX-'], 'My':values['-TORSEUR_MY-'], 'Mz':values['-TORSEUR_MZ-']}

        for key, value in torseur.items(): ###Transformation string en float pour entrée dans sectionproperties
            try:
                torseur[key]=float(value)
            except:
                pass

        param_gene = {'niveau_RCCM':values['-NIVEAU_RCCM-'][0] ,'maille':values['-MESH_SIZE-'], 'L':values['-LONGUEUR-'], 'K':values['-KLONGUEUR-'], 'angle':values['-ANGLEROT-'],
            'Sy':values['-SY-'], 'Su':values['-SU-'], 'E':values['-MODULE-'], 'impr_res':values['-PRINT_PARAM-'], 'trac_res':values['-DRAW_RESULTS-']}

        for key, value in param_gene.items():
            try:
                param_gene[key]=float(value)
            except:
                pass

        if nom_profile[0] == "IPN":
            type_profile = "IH" #pour prise en compte limites de contraintes en flexion
            param_geom = {'IPN_d':values['In_IPN_d'], 'IPN_b':values['In_IPN_b'], 'IPN_t_f':values['In_IPN_t_f'], 'IPN_t_w':values['In_IPN_t_w'],
                'IPN_r_r':values['In_IPN_r_r'], 'IPN_r_f':values['In_IPN_r_f'], 'IPN_alpha':values['In_IPN_alpha'], 'IPN_n_r':values['In_IPN_n_r']}
            section = solver.calcul_geom("IPN", param_geom, param_gene)

        if nom_profile[0] == "IPE-HE":
            type_profile ="IH"
            param_geom = {'IPE_d':values['In_IPE_d'], 'IPE_b':values['In_IPE_b'], 'IPE_t_f':values['In_IPE_t_f'],
                'IPE_t_w':values['In_IPE_t_w'], 'IPE_r':values['In_IPE_r'], 'IPE_n_r':values['In_IPE_n_r']}
            section = solver.calcul_geom("IPE", param_geom, param_gene)

        if nom_profile[0] == "UPN":
            type_profile ="U"
            param_geom = {'UPN_d':values['In_UPN_d'], 'UPN_b':values['In_UPN_b'], 'UPN_t_f':values['In_UPN_t_f'], 'UPN_t_w':values['In_UPN_t_w'],
                'UPN_r_r':values['In_UPN_r_r'], 'UPN_r_f':values['In_UPN_r_f'], 'UPN_alpha':values['In_UPN_alpha'], 'UPN_n_r':values['In_UPN_n_r']}
            section = solver.calcul_geom("UPN", param_geom, param_gene)

        if nom_profile[0] == "UPE-UAP":
            type_profile = "U"
            param_geom = {'UPE_d':values['In_UPE_d'], 'UPE_b':values['In_UPE_b'], 'UPE_t_f':values['In_UPE_t_f'], 'UPE_t_w':values['In_UPE_t_w'],
                'UPE_r':values['In_UPE_r'], 'UPE_n_r':values['In_UPE_n_r']}
            section = solver.calcul_geom("UPE", param_geom, param_gene)

        if nom_profile[0] == "Rectangle":
            type_profile = "R"
            param_geom = {'REC_d':values['In_REC_d'], 'REC_b':values['In_REC_b'], 'REC_t':values['In_REC_t'], 'REC_r_out':values['In_REC_r_out'], 'REC_n_r':values['In_REC_n_r']}
            section = solver.calcul_geom("Rectangle", param_geom, param_gene)

        if nom_profile[0] == "Corniere":
            type_profile = "L"
            param_geom = {'COR_d':values['In_COR_d'], 'COR_b':values['In_COR_b'], 'COR_t':values['In_COR_t'], 'COR_r_r':values['In_COR_r_r'],
                'COR_r_t':values['In_COR_r_t'], 'COR_n_r':values['In_COR_n_r']}
            section = solver.calcul_geom("Corniere", param_geom, param_gene)

        if nom_profile[0] == "Tube":
            type_profile = "T"
            param_geom = {'TUB_d':values['In_TUB_d'], 'TUB_t':values['In_TUB_t'], 'TUB_n':values['In_TUB_n']}
            section = solver.calcul_geom("Tube", param_geom, param_gene)

        
        if values['-ITER_SIGNS-'] == True:
            facteurs = list(product([1, -1], repeat=6))
        else:
            facteurs = [[1,1,1,1,1,1]]

        for i in range(len(facteurs)):
            solver.calcul_contraintes(section, torseur, param_gene, type_profile, facteurs[i])


window.close()