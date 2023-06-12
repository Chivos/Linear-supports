from scripts import RCCM
from sectionproperties.pre.library.steel_sections import channel_section #UAP, UPE
from sectionproperties.pre.library.steel_sections import tapered_flange_channel #UPN
from sectionproperties.pre.library.steel_sections import i_section #HEA, HEB, HEC, IPE
from sectionproperties.pre.library.steel_sections import tapered_flange_i_section #IPN
from sectionproperties.pre.library.steel_sections import rectangular_hollow_section #Carré, rectangle
from sectionproperties.pre.library.steel_sections import angle_section #Cornière
from sectionproperties.pre.library.steel_sections import circular_hollow_section #Tube

from sectionproperties.pre.geometry import Geometry
from sectionproperties.pre.geometry import CompoundGeometry
from sectionproperties.analysis.section import Section

from sectionproperties.analysis.section import Section
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table


def calcul_geom(profile, param_geom, param_gene):

        ###############################DONNEES D'ENTREE#######################################
                
        for key, value in param_geom.items(): ###Transformation string en float pour entrée dans sectionproperties
            try:
                param_geom[key]=float(value)
            except:
                pass

        if profile == "IPN":
                geometry_0 = tapered_flange_i_section(d=param_geom['IPN_d'], b=param_geom['IPN_b'], t_f=param_geom['IPN_t_f'], t_w=param_geom['IPN_t_w'], r_r=param_geom['IPN_r_r'],
                                r_f=param_geom['IPN_r_f'], alpha=param_geom['IPN_alpha'], n_r=int(param_geom['IPN_n_r']))

        if profile == "IPE": #concerne les IPE et les H (HEA, HEB, HEC...)
                geometry_0 = i_section(d=param_geom['IPE_d'], b=param_geom['IPE_b'], t_f=param_geom['IPE_t_f'], t_w=param_geom['IPE_t_w'], r=param_geom['IPE_r'], n_r=int(param_geom['IPE_n_r']))
        
        if profile == "UPE":
                geometry_0 = channel_section(d=param_geom['UPE_d'], b=param_geom['UPE_b'], t_f=param_geom['UPE_t_f'], t_w=param_geom['UPE_t_w'], r=param_geom['UPE_r'], n_r=int(param_geom['UPE_n_r']))
        
        if profile == "UPN":
                geometry_0 = tapered_flange_channel(d=param_geom['UPN_d'], b=param_geom['UPN_b'], t_f=param_geom['UPN_t_f'],
                                t_w=param_geom['UPN_t_w'], r_r=param_geom['UPN_r_r'], r_f=param_geom['UPN_r_f'], alpha=param_geom['UPN_alpha'], n_r=int(param_geom['UPN_n_r']))
        
        if profile == "Rectangle":
                geometry_0 = rectangular_hollow_section(d=param_geom['REC_d'], b=param_geom['REC_b'], t=param_geom['REC_t'], r_out=param_geom['REC_r_out'], n_r=int(param_geom['REC_n_r']))

        if profile == "Corniere":
                geometry_0 = angle_section(d=param_geom['COR_d'], b=param_geom['COR_b'], t=param_geom['COR_t'], r_r=param_geom['COR_r_r'], r_t=param_geom['COR_r_t'], n_r=int(param_geom['COR_n_r']))

        if profile == "Tube":
                geometry_0 = circular_hollow_section(d=param_geom['TUB_d'], t=param_geom['TUB_t'], n=int(param_geom['TUB_n']))

        if profile == "Personnalisé":
                geometry_0 = Geometry.from_dxf(param_geom)

        geometry = geometry_0.rotate_section(angle=param_gene['angle']) #sens trigonométrique
        geometry.create_mesh(mesh_sizes=[param_gene['maille']])
        

        ####################################CALCULS#################################################

        section = Section(geometry, time_info=True)
        #section.display_mesh_info() #affichage informations maillage

        section.calculate_geometric_properties()
        section.calculate_warping_properties()
        section.calculate_plastic_properties() #Nécessaire ? Peut être optimisation possible

        return section




def calcul_contraintes(section, torseur, param_gene, type_profile, facteurs):       
        
        N=torseur['N']*facteurs[0]
        Vx=torseur['Fx']*facteurs[1]
        Vy=torseur['Fy']*facteurs[2]
        Mxx=torseur['Mx']*1000*facteurs[3]
        Myy=torseur['My']*1000*facteurs[4]
        Mzz=torseur['Mz']*1000*facteurs[5]

        stress_post = section.calculate_stress(N=N, Vx=Vx, Vy=Vy, Mxx=Mxx, Myy=Myy, Mzz=Mzz)

        Sy=param_gene['Sy']
        Su=param_gene['Su']
        E=param_gene['E']

        niveau_RCCM=param_gene['niveau_RCCM'] #niveau de contraintes, 0AB, C ou D
        K=param_gene['K'] #conditions aux extremités
        l=param_gene['L'] #lambda, longueur
        cmx=param_gene['cmx']
        cmy=param_gene['cmy']

        r_g = section.get_rc() #rayons de giration pour calcul élancement
        (ixx_c, iyy_c, ixy_c) = section.get_ic() #pour déterminer axe fort et axe faible et choix de la limite en flexion pour les poutres en I et H

        #####################################IMPRESSION RESULTATS PROPRIETES DE SECTION################################################
        if bool(param_gene['impr_res']) is True:
                section.display_results()

        #####################################DEPOUILLEMENT CONTRAINTES###########################################
        contraintes = {}
        stresses = stress_post.get_stress()
        for stress in stresses:
                contraintes['fa']=(max(stress['sig_zz_n']))
                contraintes['fv']=max( (max(stress['sig_zxy'])) , abs((min(stress['sig_zxy']))))
                contraintes['fbx_max']=(max(stress['sig_zz_mxx']))
                contraintes['fby_max']=(max(stress['sig_zz_myy']))
                contraintes['fb_max']=(max(stress['sig_zz_m']))
                contraintes['fbx_min']=(min(stress['sig_zz_mxx']))
                contraintes['fby_min']=(min(stress['sig_zz_myy']))
                contraintes['fb_min']=(min(stress['sig_zz_m']))

        contraintes['fbx']=contraintes['fbx_min'] if abs(contraintes['fbx_min'])>contraintes['fbx_max'] else contraintes['fbx_max']
        contraintes['fby']=contraintes['fby_min'] if abs(contraintes['fby_min'])>contraintes['fby_max'] else contraintes['fby_max']


        #################################################CALCUL LIMITES###############################################
        limites = RCCM.criteres(Sy, Su, ixx_c, iyy_c, r_g, type_profile, niveau_RCCM, K, l, E)

        #########################################CALCUL ET AFFICHAGE RATIOS########################################

        ratios = RCCM.ratios(contraintes, limites, E, K, l, r_g, cmx, cmy)
        

        print('Facteurs de signes sur torseur : ', facteurs)

        for k in contraintes.keys(): #Conversion en string pour affichage dans Rich. Arrondi à la 3 ème décime et affichage adapté du nombre de 0 décimaux
                contraintes[k]="{0:g}".format(round(contraintes[k],2))

        for k in limites.keys():
                limites[k]="{0:g}".format(round(limites[k],2))

        for k in ratios.keys():
                ratios[k]="{0:g}".format(round(ratios[k],3))

        table = Table(title="Résultats : ", title_justify="left")
        table.add_column("/")
        table.add_column("Contrainte")
        table.add_column("/")
        table.add_column("Limite")
        table.add_column("Ratio")
        table.add_column("Description")

        #Traction et compression
        table.add_row("fa", contraintes['fa'] if N>0 else "0", "Ft", limites['Ft'], ratios['T_2212'], "Traction ZVI2212")
        table.add_row("fa", contraintes['fa'] if N<0 else "0", "Fa", limites['Fa'], ratios['C_2214'], "Compression ZVI2214")
        
        #Cisaillement
        table.add_row("fv", contraintes['fv'], "Fv", limites['Fv'], ratios['S_2213'], "Cisaillement ZVI2213") #la contrainte n'est pas un calcul moyenné, mais prend en compte les coeffs de cisaillement

        #Flexion
        table.add_row("fbx", contraintes['fbx'], "Fbx", limites['Fbx'], ratios['F_2215_x'], "Flexion ZVI2215")
        table.add_row("fby", contraintes['fby'], "Fby", limites['Fby'], ratios['F_2215_y'], "Flexion ZVI2215")

        table.add_section()

        #Combinaison compression et flexion
        if (float(contraintes['fa'])/float(limites['Fa'])) >= -0.15: #Permet de traiter la compression (petite valeurs négatives) et la traction dans le même if
                table.add_row("(22)", "", "", "", ratios['SC_2216.1_22'], "Compression et flexion ZVI2216.1") #RSTAB semble ne pas considérer fa/Fa si cela va dans le sens opposé (si traction, le critère de compression n'est vérifié qu'avec la flexion)
        else :
                table.add_row("(20)", "", "", "", ratios['SC_2216.1_20'], "Compression et flexion ZVI2216.1") #S'affiche avec un torseur de traction pure
                table.add_row("(21)", "", "", "", ratios['SC_2216.1_21'], "Compression et flexion ZVI2216.1") #S'affiche avec un torseur de traction pure

        
        #Combinaison traction et flexion
        table.add_row("(21)", "", "", "", ratios['SC_2216.2_21'], "Traction et flexion ZVI2216.2")

        table.add_section()

        #Ratio maximal        
        if float(ratios['MAX']) > 1:
                table.add_row("MAX", "", "", "", "[red]"+ratios['MAX']+"[/red]", "Ratio maximal")
        else:
                table.add_row("MAX", "", "", "", "[green]"+ratios['MAX']+"[/green]", "Ratio maximal")

        console = Console()
        console.print(table)

        #####################################AFFICHAGE CONTRAINTES################################################
        if bool(param_gene['trac_res']) is True:
                ax = stress_post.plot_stress_n_zz(nrows=3, ncols=3, figsize=(15, 10), render=False, title="Traction liée à l'effort normal")
                fig = ax.get_figure()
                stress_post.plot_stress_mxx_zz(ax=fig.axes[1], title="Flexion liée au moment suivant X")
                stress_post.plot_stress_myy_zz(ax=fig.axes[2], title="Flexion liée au moment suivant Y")
                stress_post.plot_stress_vx_zxy(ax=fig.axes[3], title="Cisaillement lié à l'effort suivant X")
                stress_post.plot_stress_vy_zxy(ax=fig.axes[4], title="Cisaillement lié à l'effort suivant Y")
                stress_post.plot_stress_mzz_zxy(ax=fig.axes[5], title="Torsion liée au moment suivant Z")
                stress_post.plot_stress_zz(ax=fig.axes[6], title="Traction tous chargements")
                stress_post.plot_stress_zxy(ax=fig.axes[7], title="Cisaillement tous chargements")
                section.plot_centroids(ax=fig.axes[8], title="Géométrie")
                plt.show()

        ###########################################RETOUR RATIO MAX######################################################
        return ratios['MAX']

        ###########################################FIN##################################################################