def calcul(profile, param_geom, param_gene, torseur):
        import RCCM
        from sectionproperties.pre.library.steel_sections import channel_section #UAP, UPE
        from sectionproperties.pre.library.steel_sections import tapered_flange_channel #UPN
        from sectionproperties.pre.library.steel_sections import i_section #HEA, HEB, HEC, IPE
        from sectionproperties.pre.library.steel_sections import tapered_flange_i_section #IPN
        from sectionproperties.pre.library.steel_sections import rectangular_hollow_section #Carré, rectangle
        from sectionproperties.pre.library.steel_sections import angle_section #Cornière
        from sectionproperties.pre.library.steel_sections import circular_hollow_section #Tube
        from sectionproperties.analysis.section import Section
        from texttable import Texttable
        from time import time
        import matplotlib.pyplot as plt
        start = time()

        ###############################DONNEES D'ENTREE#######################################
        
        ###Transformation string en float pour entrée dans sectionproperties
        for key, value in param_geom.items():
            try:
                param_geom[key]=float(value)
            except:
                pass
        for key, value in torseur.items():
            try:
                torseur[key]=float(value)
            except:
                pass
        for key, value in param_gene.items():
            try:
                param_gene[key]=float(value)
            except:
                pass

        if profile == "IPN":
                type_profile = "IH" #pour prise en compte limites de contraintes en flexion
                geometry_0 = tapered_flange_i_section(d=param_geom['IPN_d'], b=param_geom['IPN_b'], t_f=param_geom['IPN_t_f'], t_w=param_geom['IPN_t_w'], r_r=param_geom['IPN_r_r'],
                                r_f=param_geom['IPN_r_f'], alpha=param_geom['IPN_alpha'], n_r=int(param_geom['IPN_n_r']))

        if profile == "IPE": #concerne les IPE et les H (HEA, HEB, HEC...)
                type_profile ="IH"
                geometry_0 = i_section(d=param_geom['IPE_d'], b=param_geom['IPE_b'], t_f=param_geom['IPE_t_f'], t_w=param_geom['IPE_t_w'], r=param_geom['IPE_r'], n_r=int(param_geom['IPE_n_r']))
        
        if profile == "UPE":
                type_profile = "U"
                geometry_0 = channel_section(d=param_geom['UPE_d'], b=param_geom['UPE_b'], t_f=param_geom['UPE_t_f'], t_w=param_geom['UPE_t_w'], r=param_geom['UPE_r'], n_r=int(param_geom['UPE_n_r']))
        
        if profile == "UPN":
                type_profile ="U"
                geometry_0 = tapered_flange_channel(d=param_geom['UPN_d'], b=param_geom['UPN_b'], t_f=param_geom['UPN_t_f'],
                                t_w=param_geom['UPN_t_w'], r_r=param_geom['UPN_r_r'], r_f=param_geom['UPN_r_f'], alpha=param_geom['UPN_alpha'], n_r=int(param_geom['UPN_n_r']))
        
        if profile == "Rectangle":
                type_profile = "R"
                geometry_0 = rectangular_hollow_section(d=param_geom['REC_d'], b=param_geom['REC_b'], t=param_geom['REC_t'], r_out=param_geom['REC_r_out'], n_r=int(param_geom['REC_n_r']))

        if profile == "Corniere":
                type_profile = "L"
                geometry_0 = angle_section(d=param_geom['COR_d'], b=param_geom['COR_b'], t=param_geom['COR_t'], r_r=param_geom['COR_r_r'], r_t=param_geom['COR_r_t'], n_r=int(param_geom['COR_n_r']))

        if profile == "Tube":
                type_profile = "T"
                geometry_0 = circular_hollow_section(d=param_geom['TUB_d'], t=param_geom['TUB_t'], n=int(param_geom['TUB_n']))

        geometry = geometry_0.rotate_section(angle=param_gene['angle']) #sens trigonométrique
        geometry.create_mesh(mesh_sizes=[param_gene['maille']])
        
        N=torseur['N']
        Vx=torseur['Fx']
        Vy=torseur['Fy']
        Mxx=torseur['Mx']*1000
        Myy=torseur['My']*1000
        Mzz=torseur['Mz']*1000

        Sy=param_gene['Sy']
        Su=param_gene['Su']
        E=param_gene['E']

        niveau_RCCM=param_gene['niveau_RCCM'] #niveau de contraintes, 0AB, C ou D
        K=param_gene['K'] #conditions aux extremités
        l=param_gene['L'] #lambda, longueur

        ####################################CALCULS#################################################

        section = Section(geometry, time_info=True)
        #section.display_mesh_info() #affichage informations maillage

        section.calculate_geometric_properties()
        section.calculate_warping_properties()
        section.calculate_plastic_properties()
       
        stress_post = section.calculate_stress(N=N, Vx=Vx, Vy=Vy, Mxx=Mxx, Myy=Myy, Mzz=Mzz)

        r_g = min(section.get_rc()) #rayon de giration pour calcul élancement
        (ixx_c, iyy_c, ixy_c) = section.get_ic() #pour déterminer axe fort et axe faible et choix de la limite en flexion pour les poutres en I et H

        #####################################IMPRESSION RESULTATS PROPRIETES DE SECTION################################################
        if bool(param_gene['impr_res']) is True:
                section.display_results()

        #####################################AFFICHAGE CONTRAINTES################################################
        if bool(param_gene['trac_res']) is True:
                ax = geometry.plot_geometry(nrows=3, ncols=3, figsize=(12, 7), render=False)
                #ax = section.plot_centroids(nrows=2, ncols=3, figsize=(12, 7), render=False)
                fig = ax.get_figure()
                stress_post.plot_stress_n_zz(ax=fig.axes[1], title="Traction liée à l'effort normal")
                stress_post.plot_stress_mxx_zz(ax=fig.axes[2], title="Flexion liée au moment suivant X")
                stress_post.plot_stress_myy_zz(ax=fig.axes[3], title="Flexion liée au moment suivant Y")
                stress_post.plot_stress_vx_zxy(ax=fig.axes[4], title="Cisaillement lié à l'effort suivant X")
                stress_post.plot_stress_vy_zxy(ax=fig.axes[5], title="Cisaillement lié à l'effort suivant Y")
                stress_post.plot_stress_mzz_zxy(ax=fig.axes[6], title="Torsion liée au moment suivant Z")
                stress_post.plot_stress_zz(ax=fig.axes[7], title="Traction tous chargements")
                stress_post.plot_stress_zxy(ax=fig.axes[8], title="Cisaillement tous chargements")
                plt.show()


        #####################################AFFICHAGE CONTRAINTES################################################
        #stress_post.plot_stress_n_zz(pause=False) #Traction liée à l'effort normal
        #stress_post.plot_stress_vx_zxy(pause=False) #Cisaillement lié à l'effort suivant X
        #stress_post.plot_stress_vy_zxy(pause=False)  #Cisaillement lié à l'effort suivant Y
        #stress_post.plot_stress_mxx_zz(pause=False) #Flexion liée au moment suivant X
        #stress_post.plot_stress_myy_zz(pause=False) #Flexion liée au moment suivant Y
        #stress_post.plot_stress_mzz_zxy(pause=False) #Torsion liée au moment suivant Z
        #stress_post.plot_stress_zz(pause=False) #Traction tous chargements
        #stress_post.plot_stress_zxy(pause=False) #Cisaillement tous chargements

        #####################################DEPOUILLEMENT CONTRAINTES###########################################
        stresses = stress_post.get_stress()
        for stress in stresses:
                fa=(max(stress['sig_zz_n']))
                fv=(max(stress['sig_zxy']))
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

        #########################################AFFICHAGE ET CALCUL RATIOS########################################
                
        table = Texttable()

        #Traction ou compression
        table.header(["", "Contrainte", "", "Limite", "Ratio", "Description"]) #afficher traction ou compression selon résultat
        if N < 0:
                table.add_row(["fa", fa, "Fa", Fa, abs(fa/Fa), "Compression ZVI2214"])
        else:
                table.add_row(["fa", fa, "Ft", Ft, abs(fa/Ft), "Traction ZVI2212"])

        #Cisaillement
        table.add_row(["fv", fv, "Fv", Fv, abs(fv/Fv), "Cisaillement ZVI2213"]) #la contrainte n'est pas un calcul moyenné, mais prend en compte les coeffs de cisaillement

        #Flexion
        table.add_row(["fbx", fbx, "Fbx", Fbx, abs(fbx/Fbx), "Flexion ZVI2215"])
        table.add_row(["fby", fby, "Fby", Fby, abs(fby/Fby), "Flexion ZVI2215"])

        #Combinaison compression et flexion
        if abs(fa/Fa) <= 0.15:
                table.add_row(["(22)", "", "", "", abs( (fa/Fa if fa<0 else 0) + fbx_min/Fbx + fby_min/Fby), "Compression et flexion ZVI2216.1"]) #RSTAB semble ne pas considérer fa/Fa si cela va dans le sens opposé (si traction, le critère de compression n'est vérifié qu'avec la flexion)
        else :
                table.add_row(["", "", "", "", "", "NON PROGRAMME EQ (20) ET (21) POUR COMPRESSION"]) ###S'affiche avec un torseur de traction pure

        #Combinaison traction et flexion
        table.add_row(["(21)", "", "", "", abs( (fa/Fa if fa>=0 else 0) + fbx_max/Fbx + fby_max/Fby), "Traction et flexion ZVI2216.2"])

        print(table.draw())

        ###########################################FIN##################################################################

        print('\nDurée d\'exécution :', int(time() - start), 'secondes')