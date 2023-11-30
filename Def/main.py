import pandas as pd
from functions import *
import folium
from folium.plugins import HeatMap
import threading
import multiprocessing



numfichier = [1,2,4,5,6,7,8,9,11,13,14,15,16,17,18,21,23,24,25,26,27,28,29,30,31,32,34,35,36,37,38,39,41,42,43,44,48,49,50,51,52,53,54,55,58,59,60,62,63,65,66,67,68,69,70,71,72,73,75,77,78,81,83,84,87,89,98,107,110]


if __name__ == "__main__":

    noms_fichiers = [f"../../User/sous_ensemble_{i}.csv" for i in numfichier]

    # Nombre de threads à utiliser
    nombre_threads =4 

    processes = []

    # Divisez la liste des fichiers en groupes pour chaque thread
    fichiers_par_thread = [noms_fichiers[i:i + len(noms_fichiers)//nombre_threads] for i in range(0, len(noms_fichiers), len(noms_fichiers)//nombre_threads)]


    # Créez et lancez un thread pour chaque groupe de fichiers
    for groupe_fichiers in fichiers_par_thread:
        process = multiprocessing.Process(target=traitement_par_thread, args=(groupe_fichiers,))
        processes.append(process)
        process.start()
        
    # Attendez que tous les threads de traitement aient terminé
    for process in processes:
        process.join()

    print("Tous les fichiers ont été traités.")


