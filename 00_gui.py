import os
import PySimpleGUI as sg
import solver


sg.theme('TanBlue')
col_parametres = [[sg.Text('Niveau RCCM'), sg.Listbox(values=('0AB', 'C', 'D'), default_values='C', size=(10, 3), key='-NIVEAU_RCCM-')],
    [sg.Text('Type profilé'), sg.Listbox(values=('IPN', 'IPE', 'UPN', 'UPE', 'Corniere', 'Rectangle'), size=(10, 6), enable_events=True, key="-PROFILE-")],
    [sg.Text('Longueur:'), sg.Input(key='-LONGUEUR-', size=(10,1))],
    [sg.Text('Coefficient de longueur K:'), sg.Input(2, key='-KLONGUEUR-', size=(10,1))],
    [sg.Frame('Torseur:', [[sg.Text('N'), sg.Input(0, key='-TORSEUR_N-', size=(10,1))],
                             [sg.Text('Fx'), sg.Input(0, key='-TORSEUR_FX-', size=(10,1))],
                             [sg.Text('Fy'), sg.Input(0, key='-TORSEUR_FY-', size=(10,1))],
                             [sg.Text('Mx'), sg.Input(0, key='-TORSEUR_MX-', size=(10,1))],
                             [sg.Text('My'), sg.Input(0, key='-TORSEUR_MY-', size=(10,1))],
                             [sg.Text('Mz'), sg.Input(0, key='-TORSEUR_MZ-', size=(10,1))]
                             ])],
    [sg.Frame('Matériau:', [[sg.Text('Sy'), sg.Input(235, key='-SY-', size=(5,1))],
                             [sg.Text('Su'), sg.Input(360, key='-SU-', size=(5,1))],
                             [sg.Text('E'), sg.Input(210000, key='-MODULE-', size=(8,1))],
                             ])]
    ]

col_image = [[sg.Text('----', key='-CHOIXPROFILE-')],
    [sg.Image(key='-IMAGEPROFILE-')],
    [sg.Text('Angle de rotation (degrés, sens trigonométrique)'), sg.Input(0, key='-ANGLEROT-', size=(5,1))],
    [sg.Text('Taille du maillage'), sg.Input(10, key='-MESH_SIZE-', size=(3,1))],
    #[sg.Text('Choisir un fichier', size=(35, 1))],
    #[sg.InputText('Default Folder', key='folder'), sg.FolderBrowse()],
    [sg.Button('Quitter'), sg.Text(' ' * 40), sg.Button('Calcul')]]

#####################COLONNES MASQUEES / AFFICHEES SELON LES PROFILES###############################

col_IPN = [[sg.Text('d, hauteur'), sg.Input(key='In_IPN_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_IPN_b', size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(key='In_IPN_t_f', size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(key='In_IPN_t_w', size=(5,1))],
    [sg.Text('r_r, rayon en racine'), sg.Input(key='In_IPN_r_r', size=(5,1))],
    [sg.Text('r_f, rayon de l\'aile'), sg.Input(key='In_IPN_r_f', size=(5,1))],
    [sg.Text('alpha, angle en degrés de l\'aile'), sg.Input(key='In_IPN_alpha', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation des rayons'), sg.Input(15, key='In_IPN_n_r', size=(5,1))]
    ]

col_IPE = [[sg.Text('d, hauteur'), sg.Input(key='In_IPE_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_IPE_b', size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(key='In_IPE_t_f', size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(key='In_IPE_t_w', size=(5,1))],
    [sg.Text('r, rayon en racine'), sg.Input(key='In_IPE_r', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(15, key='In_IPE_n_r', size=(5,1))]
    ]

col_UPN = [[sg.Text('d, hauteur'), sg.Input(key='In_UPN_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_UPN_b', size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(key='In_UPN_t_f', size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(key='In_UPN_t_w', size=(5,1))],
    [sg.Text('r_r, rayon en racine'), sg.Input(key='In_UPN_r_r', size=(5,1))],
    [sg.Text('r_f, rayon de l\'aile'), sg.Input(key='In_UPN_r_f', size=(5,1))],
    [sg.Text('alpha, angle en degrés de l\'aile'), sg.Input(key='In_UPN_alpha', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation des rayons'), sg.Input(15, key='In_UPN_n_r', size=(5,1))]
    ]

col_UPE = [[sg.Text('d, hauteur'), sg.Input(key='In_UPE_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_UPE_b', size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(key='In_UPE_t_f', size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(key='In_UPE_t_w', size=(5,1))],
    [sg.Text('r, rayon en racine'), sg.Input(key='In_UPE_r', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(15, key='In_UPE_n_r', size=(5,1))]
    ]

col_Corniere = [[sg.Text('d, hauteur'), sg.Input(key='In_L_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_L_b', size=(5,1))],
    [sg.Text('t, épaisseur'), sg.Input(key='In_L_t', size=(5,1))],
    [sg.Text('r_r, rayon en racine'), sg.Input(key='In_L_r_r', size=(5,1))],
    [sg.Text('r_t, rayon en pied'), sg.Input(key='In_L_r_t', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(15, key='In_L_n_r', size=(5,1))]
    ]

col_Rectangle = [[sg.Text('d, hauteur'), sg.Input(key='In_REC_d', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(key='In_REC_b', size=(5,1))],
    [sg.Text('t, épaisseur'), sg.Input(key='In_REC_t', size=(5,1))],
    [sg.Text('r_out, rayon extérieur'), sg.Input(key='In_REC_r_out', size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(15, key='In_REC_n_r', size=(5,1))]
    ]

#############################FIN COLONNES SPECIFIQUES AU CHOIX DU PROFILE##########################

layout = [[sg.Column(col_parametres, element_justification='r'),
        sg.VSeperator(),
        sg.Column(col_image, element_justification='c'),
        sg.Column(col_IPN, element_justification='r', visible=False, key='col_IPN'),
        sg.Column(col_IPE, element_justification='r', visible=False, key='col_IPE'),
        sg.Column(col_UPN, element_justification='r', visible=False, key='col_UPN'),
        sg.Column(col_UPE, element_justification='r', visible=False, key='col_UPE'),
        sg.Column(col_Corniere, element_justification='r', visible=False, key='col_Corniere'),
        sg.Column(col_Rectangle, element_justification='r', visible=False, key='col_Rectangle')
        ]]

window = sg.Window('Dépouillement supports linéaires RCCM ZVI', layout, default_element_size=(40, 1), grab_anywhere=False, resizable=True)

while True:
    event, values = window.read()
    if event in ('Quitter', None):
        break
    if event == "-PROFILE-":  # un profilé a été selectionné
        nom_profile = values["-PROFILE-"]
        window["-CHOIXPROFILE-"].update(nom_profile[0])
        adresse = os.path.dirname(os.path.realpath(__file__)) + "\\images\\" + nom_profile[0] +".png"
        window['-IMAGEPROFILE-'].update(adresse)

        #Effacer les colonnes éventuellement affichées lors d'une sélection
        window['col_IPE'].update(visible=False)
        window['col_IPN'].update(visible=False)
        window['col_UPN'].update(visible=False)
        window['col_UPE'].update(visible=False)
        window['col_Corniere'].update(visible=False)
        window['col_Rectangle'].update(visible=False)

        #Afficher colonnes en fonction de la section
        if nom_profile[0] == "IPN":
            window['col_IPN'].update(visible=True)
        if nom_profile[0] == "IPE":
            window['col_IPE'].update(visible=True)
        if nom_profile[0] == "UPN":
            window['col_UPN'].update(visible=True)
        if nom_profile[0] == "UPE":
            window['col_UPE'].update(visible=True)
        if nom_profile[0] == "Corniere":
            window['col_Corniere'].update(visible=True)
        if nom_profile[0] == "Rectangle":
            window['col_Rectangle'].update(visible=True)

    if event == "Calcul":
        torseur = {'N':values['-TORSEUR_N-'], 'Fx':values['-TORSEUR_FX-'], 'Fy':values['-TORSEUR_FY-'],
            'Mx':values['-TORSEUR_MX-'], 'My':values['-TORSEUR_MY-'], 'Mz':values['-TORSEUR_MZ-']}

        param_gene = {'niveau_RCCM':values['-NIVEAU_RCCM-'][0] ,'maille':values['-MESH_SIZE-'], 'L':values['-LONGUEUR-'], 'K':values['-KLONGUEUR-'], 'angle':values['-ANGLEROT-'],
            'Sy':values['-SY-'], 'Su':values['-SU-'], 'E':values['-MODULE-']} #paramètres génériques : longueur, matériau, maillage

        if nom_profile[0] == "IPN":
            param_geom = {'IPN_d':values['In_IPN_d'], 'IPN_b':values['In_IPN_b'], 'IPN_t_f':values['In_IPN_t_f'], 'IPN_t_w':values['In_IPN_t_w'],
                'IPN_r_r':values['In_IPN_r_r'], 'IPN_r_f':values['In_IPN_r_f'], 'IPN_alpha':values['In_IPN_alpha'], 'IPN_n_r':values['In_IPN_n_r']}
            solver.calcul("IPN", param_geom, param_gene, torseur)

        if nom_profile[0] == "IPE":
            param_geom = {'IPE_d':values['In_IPE_d'], 'IPE_b':values['In_IPE_b'], 'IPE_t_f':values['In_IPE_t_f'],
                'IPE_t_w':values['In_IPE_t_w'], 'IPE_r':values['In_IPE_r'], 'IPE_n_r':values['In_IPE_n_r']}
            solver.calcul("IPE", param_geom, param_gene, torseur)

        if nom_profile[0] == "UPN":
            param_geom = {'UPN_d':values['In_UPN_d'], 'UPN_b':values['In_UPN_b'], 'UPN_t_f':values['In_UPN_t_f'], 'UPN_t_w':values['In_UPN_t_w'],
                'UPN_r_r':values['In_UPN_r_r'], 'UPN_r_f':values['In_UPN_r_f'], 'UPN_alpha':values['In_UPN_alpha'], 'UPN_n_r':values['In_UPN_n_r']}
            solver.calcul("UPN", param_geom, param_gene, torseur)

        if nom_profile[0] == "UPE":
            param_geom = {'UPE_d':values['In_UPE_d'], 'UPE_b':values['In_UPE_b'], 'UPE_t_f':values['In_UPE_t_f'], 'UPE_t_w':values['In_UPE_t_w'],
                'UPE_r':values['In_UPE_r'], 'UPE_n_r':values['In_UPE_n_r']}
            solver.calcul("UPE", param_geom, param_gene, torseur)


window.close()