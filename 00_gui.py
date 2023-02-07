import os
import PySimpleGUI as sg


sg.theme('TanBlue')
col_parametres = [[sg.Text('Niveau RCCM'), sg.Listbox(values=('0AB', 'C', 'D'), size=(10, 3), key='listbox')],
    [sg.Text('Type profilé'), sg.Listbox(values=('IPN', 'IPE', 'UPN', 'UPE', 'Corniere', 'Carre'), size=(10, 6), enable_events=True, key="-PROFILE-")],
    [sg.Text('Longueur:'), sg.Input(key='-LONGUEUR-', size=(10,1))],
    [sg.Text('Coefficient de longueur K:'), sg.Input(key='-KLONGUEUR-', size=(10,1))],
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
    [sg.Button('Quitter'), sg.Text(' ' * 40), sg.Button('Run')]]

col_IPN = [[sg.Text('d, hauteur'), sg.Input(key='-HAUTEUR-', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(size=(5,1))],
    [sg.Text('r_r, rayon en racine'), sg.Input(size=(5,1))],
    [sg.Text('r_f, rayon de l\'aile'), sg.Input(size=(5,1))],
    [sg.Text('alpha, angle en degrés de l\'aile'), sg.Input(size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation des rayons'), sg.Input(size=(5,1))]
    ]

col_IPE = [[sg.Text('d, hauteur'), sg.Input(key='-HAUTEUR-', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(size=(5,1))],
    [sg.Text('r, rayon en racine'), sg.Input(size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(size=(5,1))]
    ]

col_UPN = [[sg.Text('d, hauteur'), sg.Input(key='-HAUTEUR-', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(size=(5,1))],
    [sg.Text('r_r, rayon en racine'), sg.Input(size=(5,1))],
    [sg.Text('r_f, rayon de l\'aile'), sg.Input(size=(5,1))],
    [sg.Text('alpha, angle en degrés de l\'aile'), sg.Input(size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation des rayons'), sg.Input(size=(5,1))]
    ]

col_UPE = [[sg.Text('d, hauteur'), sg.Input(key='-HAUTEUR-', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(size=(5,1))],
    [sg.Text('t_f, épaisseur de l\'aile'), sg.Input(size=(5,1))],
    [sg.Text('t_w, épaisseur de l\'ame'), sg.Input(size=(5,1))],
    [sg.Text('r, rayon en racine'), sg.Input(size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(size=(5,1))]
    ]

col_Corniere = [[sg.Text('d, hauteur'), sg.Input(key='-HAUTEUR-', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(size=(5,1))],
    [sg.Text('t, épaisseur'), sg.Input(size=(5,1))],
    [sg.Text('r_r, rayon en racine'), sg.Input(size=(5,1))],
    [sg.Text('r_t, rayon en pied'), sg.Input(size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(size=(5,1))]
    ]

col_Carre = [[sg.Text('d, hauteur'), sg.Input(key='-HAUTEUR-', size=(5,1))],
    [sg.Text('b, largeur'), sg.Input(size=(5,1))],
    [sg.Text('t, épaisseur'), sg.Input(size=(5,1))],
    [sg.Text('r_out, rayon extérieur'), sg.Input(size=(5,1))],
    [sg.Text('n_r, nombre de points de discrétisation du rayon'), sg.Input(size=(5,1))]
    ]

layout = [[sg.Column(col_parametres, element_justification='c'),
        sg.VSeperator(),
        sg.Column(col_image, element_justification='c'),
        sg.Column(col_IPN, element_justification='r', visible=False, key='col_IPN'),
        sg.Column(col_IPE, element_justification='r', visible=False, key='col_IPE'),
        sg.Column(col_UPN, element_justification='r', visible=False, key='col_UPN'),
        sg.Column(col_UPE, element_justification='r', visible=False, key='col_UPE'),
        sg.Column(col_Corniere, element_justification='r', visible=False, key='col_Corniere'),
        sg.Column(col_Carre, element_justification='r', visible=False, key='col_Carre')
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

        #Effacer les colonnes éventuellement affichées
        window['col_IPE'].update(visible=False)
        window['col_IPN'].update(visible=False)
        window['col_UPN'].update(visible=False)
        window['col_UPE'].update(visible=False)
        window['col_Corniere'].update(visible=False)
        window['col_Carre'].update(visible=False)

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

        if nom_profile[0] == "Carre":
            window['col_Carre'].update(visible=True)

window.close()



