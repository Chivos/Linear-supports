import os
import PySimpleGUI as sg


sg.theme('TanBlue')
left_col = [[sg.Listbox(values=('0AB', 'C', 'D'), size=(10, 3), key='listbox')],
    [sg.Listbox(values=('IPN', 'IPE', 'UPN', 'UPE', 'Corniere', 'Carre'), size=(10, 5), enable_events=True, key="-PROFILE-")],
    [sg.Text('Longueur:'), sg.Input(key='-LONGUEUR-', size=(10,1))],
    [sg.Text('Coefficient de longueur K:'), sg.Input(key='-KLONGUEUR-', size=(10,1))],
    [sg.Table([[0,0,0,0,0,0], [0,0,0,0,0,0]], ['N','Fx','Fy', 'Mx','My','Mz'], num_rows=3, auto_size_columns=True)]]

right_col = [[sg.Text('----', key='-CHOIXPROFILE-')],
    [sg.Image(key='-IMAGEPROFILE-')],
    [sg.Text('Choisir un fichier', size=(35, 1))],
    [sg.InputText('Default Folder', key='folder'), sg.FolderBrowse()],
    [sg.Button('Exit'), sg.Text(' ' * 40), sg.Button('Run')]]

layout = [[sg.Column(left_col, element_justification='c'), sg.VSeperator(),sg.Column(right_col, element_justification='c')]]



window = sg.Window('Dépouillement supports linéaires RCCM ZVI', layout, default_element_size=(40, 1), grab_anywhere=False, resizable=True)

while True:
    event, values = window.read()
    if event in ('Exit', None):
        break
    if event == "-PROFILE-":  # un profilé a été selectinné
        nom_profile = values["-PROFILE-"]
        window["-CHOIXPROFILE-"].update(nom_profile[0])
        adresse = os.path.dirname(os.path.realpath(__file__)) + "\\images\\" + nom_profile[0] +".png"
        window['-IMAGEPROFILE-'].update(adresse)

        #if "IPN" in nom_profile:
            #adresse = os.path.dirname(os.path.realpath(__file__)) + "\\images\\IPN.png"
            

window.close()



