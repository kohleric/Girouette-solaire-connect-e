# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 22:26:45 2024

@author: kohle
"""
import schedule
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import numpy as np
import time
#import msvcrt
from datetime import datetime 
import os
import glob
from tqdm import tqdm
from matplotlib.colors import ListedColormap
# Définir la taille de la police globale pour Matplotlib
plt.rc('font', size=12)

# Définir le DPI souhaité (par exemple, 150)
desired_dpi = 170

#csv_file_path = "donnees_test.csv"


# Chemin du répertoire contenant les fichiers CSV
directory_path = "C:/Users/kohle/Documents/Arduino/Girouette"

# Liste tous les fichiers CSV dans le répertoire
csv_files = glob.glob(os.path.join(directory_path, "*.csv"))

# Trie les fichiers par date de modification (du plus récent au plus ancien)
csv_files.sort(key=os.path.getmtime, reverse=True)

# Vérifie s'il y a des fichiers CSV dans le répertoire
if csv_files:
    # Prends le chemin du fichier CSV le plus récent
    latest_csv_file = csv_files[0]
    
    csv_file_path = latest_csv_file
    
    
    
    print("Fichier le plus récent chargé :", latest_csv_file)
    #print(df.head())  # Exemple d'affichage des premières lignes du dataframe
else:
    print("Aucun fichier CSV trouvé dans le répertoire.")


# suppression des données pétées
def remove_outliers(df, column_name, threshold=3 ):
    # Calculer la moyenne et l'écart-type de la colonne
    mean_value = df[column_name].mean()
    std_value = df[column_name].std()

    # Filtrer les valeurs aberrantes
    df_filtered = df[(df[column_name] >= mean_value - threshold * std_value) & 
                     (df[column_name] <= mean_value + threshold * std_value)]
    
    return df_filtered

columns_to_process = ['T','P' ]



longueur_1h = 3600
longueur_1day = 86400

def graphLagirouette():
    plt.close() 
    df = pd.read_csv(csv_file_path, sep=",", encoding='ISO-8859-1')#, skiprows=lambda x: x in range(1, len(pd.read_csv(csv_file_path, encoding='ISO-8859-1')) - longueur))
    
    if len(df) == 0:
        print("pas de données")
    else:
            print("données présentes")
            df = df.replace(" inf",np.nan)
            for column in tqdm(columns_to_process):
                    df = remove_outliers(df, column)
            # format datetime pour matplotlib
            df['time'] = pd.to_datetime(df['Timestamp'])
            df['T'] = pd.to_numeric(df['T'].dropna())
            df['position'] = pd.to_numeric(df['position'].dropna())
            df['P'] = pd.to_numeric(df['P'].dropna()) / 100  # pour passer en hPa
            df['Vbat'] = pd.to_numeric(df['Vbat'].dropna())
            df['RPM'] = pd.to_numeric(df['RPM'].dropna())
            #filtrage des RPM recopiés
            liste_RPM_diff= np.concatenate(([0], np.diff(df['RPM'])))
            liste_coeff=[]
            for coeff in liste_RPM_diff:
                if coeff ==0:
                    liste_coeff=np.concatenate((liste_coeff, [0]))
                else:
                    liste_coeff=np.concatenate((liste_coeff, [1]))
            df['RPM'] = df['RPM'] * liste_coeff
            ##########figure
            plt.figure(dpi=desired_dpi, figsize=(16, 16)) 
            # Tracer les données de la température
            plt.subplot2grid((4, 4), (1, 3), colspan=1)  # 3 lignes, 4 colonnes, premier sous-graphique
            plt.plot(df['time'], df['T'], label='Temperature', color='blue', linewidth=1)
            plt.xticks([])  
            plt.legend()
            plt.title('Température (°C)')
            
            # Tracer les données de l'orientation # Sens des aiguilles d'une montre
            plt.subplot2grid((4, 4), (0, 0), colspan=3,rowspan=3)  # 3 lignes, 4 colonnes, troisième sous-graphique
            # x = np.cos((22.5 * df['position']) - 26) * df['RPMmoy']
            # y = np.sin((22.5 * df['position']) - 26) * df['RPMmoy']
            x = np.cos(np.radians(((90-45 * df['position']) +15))) * df['RPM']
            y = np.sin(np.radians(((90-45 * df['position']) +15))) * df['RPM']
            # cmap perso pour supprimer valeurs nulles
            vmin = 0.3

            # Créer une colormap personnalisée
            cmap = plt.cm.jet  # Utilisez la carte de couleurs jet (ou toute autre de votre choix)
            colors = cmap(np.linspace(0, 1, 256))
            colors[:int(256 * (vmin / (1 - vmin)))] = [1, 1, 1, 0]  # Rendre transparent ou blanc toutes les valeurs sous vmin
            new_cmap = ListedColormap(colors)
            if len(df) >=1:
                plt.hist2d(x, y, bins=100, cmap="jet", norm=mcolors.PowerNorm(0.3))#jet 'flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                #plt.hist2d(x, y, bins=100, cmap=new_cmap, vmin=vmin)
                      #'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                      #'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                      #'turbo', 'nipy_spectral', 'gist_ncar'
            
            #plt.plot(x, y, color='purple')
            plt.plot(
                [valeur * int(df['RPM'].max()/4) for valeur in [0, 0.1, 1, 0.1, 0, -0.1, -1, -0.1, 0]],
                [valeur * int(df['RPM'].max()/4) for valeur in [1, 0.1, 0, -0.1, -1, -0.1, 0, 0.1, 1]],
                # [valeur * 10 for valeur in [0, 0.1, 1, 0.1, 0, -0.1, -1, -0.1, 0]],
                # [valeur * 10 for valeur in [1, 0.1, 0, -0.1, -1, -0.1, 0, 0.1, 1]],
                color='darkgray', linewidth=1)
            # plt.Circle((0, 0), df['RPM'].mean(), edgecolor="limegreen", lw=3, fill=False)
            # plt.Circle((0, 0), df['RPM'].max(), edgecolor="limegreen", lw=3, fill=False)
            #rose des vents
            
            
            plt.text(-0.0, int(df['RPM'].max()/4), "Nord", color='darkgray',size=20)
            plt.text(int(df['RPM'].max()/4), -0 , "Est", color='darkgray',size=20)
            plt.text(-0.0, -int(df['RPM'].max()/4), "Sud", color='darkgray',size=20)
            plt.text(-int(df['RPM'].max()/4), -0 , "Ouest", color='darkgray',size=20)
            plt.xlim(-int(df['RPM'].max()),int(df['RPM'].max()))
            plt.ylim(-int(df['RPM'].max()),int(df['RPM'].max()))
            
            plt.title(' dernières mesures - Orientation et vitesse ')
            
            # Tracer les données position brutes
            # plt.subplot2grid((4, 4), (3, 1), colspan=1)  # 3 lignes, 4 colonnes, quatrième sous-graphique
            # plt.scatter(x, y, color='black')
            # #plt.xticks([])
            # plt.legend()
            # plt.title('orientations')
            
            # Tracer les données de la pression
            plt.subplot2grid((4, 4), (2, 3), colspan=1)  # 3 lignes, 4 colonnes, deuxième sous-graphique
            plt.plot(df['time'], df['P'], label='Pressure', color='green', linewidth=1)
            #plt.text(0.05, 990, "pluie", color='blue')
            #plt.text(0.05, 1010, "variable", color='blue')
            #plt.text(0.05, 1030, "soleil", color='blue')
            plt.xticks([])
            plt.legend()
            #plt.ylim(950, 1020)
            plt.title('Pression (mbar)')
            plt.ylim(970,1040)
            
            
            # Tracer les données de la tension de la batterie
            plt.subplot2grid((4, 4), (3, 0), colspan=2)  # 3 lignes, 4 colonnes, quatrième sous-graphique
            #filtrage couleur charge décharge
            moyenne= np.mean(df['Vbat'].iloc[-20:-2])#calcul moyenne 19  mesures avant dernière
            if df['Vbat'].iloc[-1] > moyenne:
                etat=" en charge solaire "
            else:
                etat=" en décharge "
            #liste_etat= np.diff(df['Vbat'])
            liste_etat= np.concatenate(([0], np.diff(df['Vbat'])))
            liste_etat_arr=np.array(liste_etat)
            total_charge = np.sum(liste_etat_arr[liste_etat_arr > 0])
            
            liste_couleur = ['green' if val > 0.01 else 'red' for val in liste_etat]
            plt.scatter(df['time'], df['Vbat'], label='Vbat', color=liste_couleur,s=1)#, linewidth=1)
            #plt.plot(df['time'], [8.4] * len(df['time']), label='Vbat_max', color='red', linewidth=1)
            #  plt.plot(df['time'], [6.2] * len(df['time']), label='Vbat_min', color='orange', linewidth=1)
            #plt.xticks([])
            plt.legend()
            plt.title('Vbat (V)'+etat+"_ charge totale : "+str(total_charge.round(2))+" V")
            
            # Tracer les données RPMmoyen/max? en fct du temps
            plt.subplot2grid((4, 4), (3, 2), colspan=2) 
            plt.plot(df['time'], df['RPM'], label='RPM', color='purple', linewidth=1)
            #plt.xticks([])
            plt.legend()
            plt.title('Vitesse hélice (tours/min)')
            
            # Tracer les données reference
            plt.subplot2grid((4, 4), (0, 3), colspan=1)  # 3 lignes, 4 colonnes, quatrième sous-graphique
            plt.title('Identification image')
            current_time = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
            plt.text(0.05, 0.9, current_time , color='blue')
            plt.text(0.05, 0.8, csv_file_path.split("Girouette")[1], color='blue')
            plt.text(0.05, 0.6, 'T P Vbat', color='blue')
            plt.text(0.05, 0.5, str(df['T'].iloc[-1])+" "+str(df['P'].iloc[-1].round(2))+" "+str(df['Vbat'].iloc[-1]), color='green')
            plt.text(0.05, 0.3, 'orientation RPM RPMmax RPMmoy', color='blue')
            plt.text(0.05, 0.2, str(df['orientation'].iloc[-1])+" "+str(df['RPM'].iloc[-1])+" "+str(round(df['RPM'].max(), 2))+" "+str(round(df['RPM'].mean(), 2)), color='green')
            # Configurer le format de la date et de l'heure sur l'axe des x pour le deuxième sous-graphique
            plt.xticks([])
            plt.yticks([])
            plt.tight_layout()  # Ajuster automatiquement la disposition pour éviter les chevauchements
            
            plt.savefig("data\P-T-V-RPM-bat_girouette.png")
            save_time = datetime.now().strftime("%Y-%m-%d")
            plt.savefig("data\P-T-V-RPM-bat_girouette_"+save_time+".png")
            
            plt.pause(1)  # Utiliser plt.pause pour mettre à jour l'affichage sans bloquer l'exécution
            # Attendre une seconde
            # Vérifier si la touche espace est enfoncée pour arrêter le programme
            plt.close()


# graphLagirouette(longueur_1h) 
# graphLagirouette(longueur_1day)  

# schedule.every(1).minutes.do(graphLagirouette, longueur_1h)
# schedule.every(1).minutes.do(graphLagirouette, longueur_1day)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
temps_ecoule = 0
while True:
    # Mettre à jour la variable de temps
    temps_ecoule += 1

    # Vérifier si le temps écoulé est supérieur à 60 secondes
    if temps_ecoule >= 60:
        # Réinitialiser la variable de temps
        temps_ecoule = 0

        # Exécuter la fonction graphLagirouette avec les arguments appropriés
        #graphLagirouette(100)
        #graphLagirouette(1000)
        graphLagirouette()
        print("Fichier le plus récent chargé :", latest_csv_file)

    # Mettre en pause l'exécution pendant 1 seconde
    time.sleep(1)