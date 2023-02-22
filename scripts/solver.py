from scripts import RCCM
from sectionproperties.pre.library.steel_sections import channel_section #UAP, UPE
from sectionproperties.pre.library.steel_sections import tapered_flange_channel #UPN
from sectionproperties.pre.library.steel_sections import i_section #HEA, HEB, HEC, IPE
from sectionproperties.pre.library.steel_sections import tapered_flange_i_section #IPN
from sectionproperties.pre.library.steel_sections import rectangular_hollow_section #Carré, rectangle
from sectionproperties.pre.library.steel_sections import angle_section #Cornière
from sectionproperties.pre.library.steel_sections import circular_hollow_section #Tube
from sectionproperties.analysis.section import Section
from texttable import Texttable
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import os #pour couleurs
os.system("color") #pour couleur


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


        #####################################DEPOUILLEMENT CONTRAINTES###########################################
        stresses = stress_post.get_stress()
        for stress in stresses:
                fa=(max(stress['sig_zz_n']))
                fv=max( (max(stress['sig_zxy'])) , abs((min(stress['sig_zxy']))))
                fbx_max=(max(stress['sig_zz_mxx']))
                fby_max=(max(stress['sig_zz_myy']))
                fb_max=(max(stress['sig_zz_m']))
                fbx_min=(min(stress['sig_zz_mxx']))
                fby_min=(min(stress['sig_zz_myy']))
                fb_min=(min(stress['sig_zz_m']))

        fbx=fbx_min if abs(fbx_min)>fbx_max else fbx_max
        fby=fby_min if abs(fby_min)>fby_max else fby_max


        #################################################CALCUL LIMITES###############################################
        (Fa, Ft, Fv, Fbx, Fby) = RCCM.criteres(Sy, Su, ixx_c, iyy_c, r_g, type_profile, niveau_RCCM, K, l, E)

        #########################################CALCUL ET AFFICHAGE RATIOS########################################

        ratios = RCCM.ratios(fa, Fa, Ft, fv, Fv, fbx, fbx_min, fbx_max, Fbx, fby, fby_min, fby_max, Fby, E, K, l, r_g, cmx, cmy)
        ratio_max = max(ratios.values())

        print('Facteurs de signes sur torseur : ', facteurs)

        table = PrettyTable()
        table.field_names = ["/", "Contrainte", "\\", "Limite", "Ratio", "Description"]
        table.align['Description'] = 'l'
        
        #Traction et compression
        table.add_row(["fa", fa if N>0 else 0, "Ft", Ft, ratios['T_2212'], "Traction ZVI2212"])
        table.add_row(["fa", fa if N<0 else 0, "Fa", Fa, ratios['C_2214'], "Compression ZVI2214"])
        
        #Cisaillement
        table.add_row(["fv", fv, "Fv", Fv, ratios['S_2213'], "Cisaillement ZVI2213"]) #la contrainte n'est pas un calcul moyenné, mais prend en compte les coeffs de cisaillement

        #Flexion
        table.add_row(["fbx", fbx, "Fbx", Fbx, ratios['F_2215_x'], "Flexion ZVI2215"])
        table.add_row(["fby", fby, "Fby", Fby, ratios['F_2215_y'], "Flexion ZVI2215"])

        #Combinaison compression et flexion
        if abs(fa/Fa) <= 0.15:
                table.add_row(["(22)", "", "", "", ratios['SC_2216.1_22'], "Compression et flexion ZVI2216.1"]) #RSTAB semble ne pas considérer fa/Fa si cela va dans le sens opposé (si traction, le critère de compression n'est vérifié qu'avec la flexion)
        else :
                table.add_row(["(20)", "", "", "", ratios['SC_2216.1_20'], "Compression et flexion ZVI2216.1"]) #S'affiche avec un torseur de traction pure
                table.add_row(["(21)", "", "", "", ratios['SC_2216.1_21'], "Compression et flexion ZVI2216.1"]) #S'affiche avec un torseur de traction pure

        #Combinaison traction et flexion
        table.add_row(["(21)", "", "", "", ratios['SC_2216.2_21'], "Traction et flexion ZVI2216.2"])

        if ratio_max > 1:
                ratio_max_text = '\x1b[41m' + str("{0:.3f}".format(ratio_max)) + '\x1b[0m'
        else:
                ratio_max_text = '\x1b[42m' + str("{0:.3f}".format(ratio_max)) + '\x1b[0m'

        table.add_row(["MAX", "", "", "", ratio_max_text, "Ratio maximal"])
        table.float_format = '0.3'

        print(table)


        ###########################################FIN##################################################################