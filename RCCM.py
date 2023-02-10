from math import pi

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
        
        Ft=r * min(Sy*0.6, Su*0.5) #ZVI2212 Traction
        Fv=r * min(Sy*0.4, Su*0.33) #ZVI2213 Cisaillement

        #L'interprétation du RCC-M pour limites en flexion sont en partie issus de la note de qualification RSTAB D02ARV01074335 (I, H, U, Carré) et de notes de calcul pour les cornières (PWY05E020333000MINC)
        #Cela traduit donc des choix proches de RSTAB, sauf pour la flexion des U ou RSTAB applique les mêmes règles que celles des I ou H (cf note de qualification RSTAB)
        #Pour les U, l'ASD de l'AISC indique un critère à 0.66, ce qui pourrait être plus en phase avec l'ASME III NF
        if type_profile == "IH" :
                print('pour un profilé en I ou H')
                if ixx_c >= iyy_c :
                        Fbx=r * min(Sy*0.66, Su*0.55) #ZVI2215.2 Flexion
                        Fby=r * min(Sy*0.75, Su*0.63) #ZVI2215.4 Flexion
                elif ixx_c < iyy_c :
                        Fby=r * min(Sy*0.66, Su*0.55) #ZVI2215.2 Flexion
                        Fbx=r * min(Sy*0.75, Su*0.63) #ZVI2215.4 Flexion
        elif type_profile == "U" :
                print('pour un profilé en U')
                Fbx=r * min(Sy*0.60, Su*0.50) #ZVI2215.6 Flexion
                Fby=Fbx
        elif type_profile == "L" :
                print('pour un profilé en L')
                Fbx=r * min(Sy*0.60, Su*0.50) #ZVI2215.6 Flexion
                Fby=Fbx
        elif type_profile == "R" :
                print('pour un profilé rectangulaire')
                Fbx=r * min(Sy*0.66, Su*0.66) #ZVI2215.2 Flexion
                Fby=Fbx
                
        elancement = K*l/r_g
        Cc=((2*pi**2*E)/Sy)**0.5
        if elancement <= Cc:
                Fa=r * (1 - elancement**2/(2*Cc**2))*Sy / (5/3 + 3*elancement/(8*Cc) - elancement**3/(8*Cc**3))
        else:
                Fa=r * 12*pi**2*E/(23*elancement**2) #equation 5 ZVI2214.2
        
        return (Fa, Ft, Fv, Fbx, Fby)
