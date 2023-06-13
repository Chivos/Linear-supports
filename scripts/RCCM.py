from math import pi
from rich.console import Console

def criteres(Sy, Su, ixx_c, iyy_c, r_g, type_profile, niveau_RCCM, K, l, E): #CALCUL LIMITES
        if niveau_RCCM in "0AB":
                r=1
                print('Dépouillement pour un niveau 0AB', end=", ")
        elif niveau_RCCM=="C":
                r=4/3
                print('Dépouillement pour un niveau C', end=", ")
        elif niveau_RCCM=="D":
                if Su >= 1.2*Sy:
                        r=min(1.66, 1.167*Su/Sy)
                else:
                        r=1.4
                print('Dépouillement pour un niveau D', end=", ")
        else:
                print('ERREUR, niveau RCCM non reconnu')
                r=0
        
        limites={}
        limites['Ft']=r * min(Sy*0.6, Su*0.5) #ZVI2212 Traction
        limites['Fv']=r * min(Sy*0.4, Su*0.33) #ZVI2213 Cisaillement

        #L'interprétation du RCC-M pour limites en flexion sont en partie issus de la note de qualification RSTAB D02ARV01074335 (I, H, U, Carré) et de notes de calcul pour les cornières (PWY05E020333000MINC)
        #Cela traduit donc des choix proches de RSTAB, sauf pour la flexion des U ou RSTAB applique les mêmes règles que celles des I ou H (cf note de qualification RSTAB)
        #Pour les U, l'ASD de l'AISC indique un critère à 0.66, ce qui pourrait être plus en phase avec l'ASME III NF
        if type_profile == "IH" :
                print('pour un profilé en I ou H')
                if ixx_c >= iyy_c :
                        limites['Fbx']=r * min(Sy*0.66, Su*0.55) #ZVI2215.2 Flexion
                        limites['Fby']=r * min(Sy*0.75, Su*0.63) #ZVI2215.4 Flexion
                elif ixx_c < iyy_c :
                        limites['Fby']=r * min(Sy*0.66, Su*0.55) #ZVI2215.2 Flexion
                        limites['Fbx']=r * min(Sy*0.75, Su*0.63) #ZVI2215.4 Flexion
        elif type_profile == "U" :
                print('pour un profilé en U')
                limites['Fbx']=r * min(Sy*0.60, Su*0.50) #ZVI2215.6 Flexion
                limites['Fby']=limites['Fbx']
        elif type_profile == "L" :
                print('pour un profilé en L')
                limites['Fbx']=r * min(Sy*0.60, Su*0.50) #ZVI2215.6 Flexion
                limites['Fby']=limites['Fbx']
        elif type_profile == "R" :
                print('pour un profilé rectangulaire')
                limites['Fbx']=r * min(Sy*0.66, Su*0.55) #ZVI2215.2 Flexion
                limites['Fby']=limites['Fbx']
        elif type_profile == "T" :
                print('pour un tube')
                limites['Fbx']=r * min(Sy*0.66, Su*0.55) #ZVI2215.2 Flexion
                limites['Fby']=limites['Fbx']
        elif type_profile == "P" :
                console = Console()
                Console.print("pour un profilé personnalisé" + "[red] - VERIFIER LES LIMITES ADMISSIBLES -[/red]")
                limites['Fbx']=r * min(Sy*0.60, Su*0.50) #ZVI2215.6 Flexion
                limites['Fby']=limites['Fbx']
        
        elancement = K*l/min(r_g)
        Cc=((2*pi**2*E)/Sy)**0.5
        
        if elancement <= Cc:
                limites['Fa']=min( r * (1 - elancement**2/(2*Cc**2))*Sy / (5/3 + 3*elancement/(8*Cc) - elancement**3/(8*Cc**3)) , r*0.5*Su)
        else:
                limites['Fa']=r * 12*pi**2*E/(23*elancement**2) #equation 5 ZVI2214.2
        
        return limites


def ratios(contraintes, limites, E, K, l, r_g, cmx, cmy):
        
        for k, v in contraintes.items(): #Crée variables à partir du dictionnaire, pour facilier la lecture des formules ci-après
                globals()[k] = v #exemple : fa = contraintes['fa']
        for k, v in limites.items():
                globals()[k] = v

        ratios = {}
        ratios['T_2212'] = abs(fa/Ft) if fa>0 else 0
        ratios['C_2214'] = abs(fa/Fa) if fa<0 else 0
        ratios['S_2213'] = abs(fv/Fv) #la contrainte n'est pas un calcul moyenné, mais prend en compte les coeffs de cisaillement
        ratios['F_2215_x']= abs(fbx/Fbx)
        ratios['F_2215_y']= abs(fby/Fby)

        if (fa/Fa) >= -0.15: #Permet de traiter la compression (petite valeurs négatives) et la traction dans le même if
                if fa < 0:
                        ratios['SC_2216.1_22'] = abs(fa/Fa + fbx_min/Fbx + fby_min/Fby)
                else:
                        ratios['SC_2216.1_22'] = abs(fbx_min/Fbx + fby_min/Fby)  #RSTAB semble ne pas considérer fa/Fa si cela va dans le sens opposé (si traction, le critère de compression n'est vérifié qu'avec la flexion)
        else:
                Fpex = (12*pi**2*E)/(23*(K*l/r_g[0])**2)
                Fpey = (12*pi**2*E)/(23*(K*l/r_g[1])**2)
                ratios['SC_2216.1_20'] = abs( fa/Fa + (cmx*fbx_min)/((1-fa/Fpex)*Fbx) + (cmy*fby_min)/((1-fa/Fpey)*Fby) )
                ratios['SC_2216.1_21'] = abs(fa/Ft + fbx_min/Fbx + fby_min/Fby)
                

        ratios['SC_2216.2_21'] = abs( (fa/Ft if fa>=0 else 0) + fbx_max/Fbx + fby_max/Fby)

        ratios['MAX'] = max(ratios.values())

        return ratios
