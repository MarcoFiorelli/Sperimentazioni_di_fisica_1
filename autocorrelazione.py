import matplotlib.pyplot as plt
import numpy as np
import math
import os
import glob


covarianza_1_periodo=[]

# 1. Definisci il percorso della cartella "Pendolo a torsione"
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
cartella_input = os.path.join(desktop_path, "Pendolo a torsione")

# 2. Cerca tutti i file che iniziano con "frequenza_" e finiscono in ".txt"
pattern_ricerca = os.path.join(cartella_input, "frequenza_*.txt")
percorsi_file = glob.glob(pattern_ricerca)

# Inizializza le liste vuote che andremo a riempire
files = []
frequenze_list = []

# 3. Estrai i percorsi e le frequenze
for percorso in percorsi_file:
    nome_file = os.path.basename(percorso)
    files.append(percorso) # Salviamo il percorso completo per np.loadtxt
    
    # Estraiamo il numero: da "frequenza_0.95.txt" togliamo il testo e teniamo "0.95"
    stringa_numero = nome_file.replace("frequenza_", "").replace(".txt", "")
    frequenza_estratta = float(stringa_numero)
    frequenze_list.append(frequenza_estratta)

# Convertiamo la lista in un array NumPy come nel tuo codice originale
frequenze = np.array(frequenze_list)
periodi=1/frequenze
#Iniziamo il ciclo sui file
for i in range(len(files)):
    nome_file_originale = os.path.basename(files[i])
    print(f"Elaborazione e salvataggio grafico per: {nome_file_originale}")
    data_grezzi=np.loadtxt(files[i])
    forzante=data_grezzi[:, 1]
    #Riconoscimo quando la forzante si stoppa
    indici_motore_acceso = np.where(forzante != 0)[0]
    ultimo_indice_acceso = indici_motore_acceso[-1]
    #print(ultimo_indice_acceso)
    #Introduciamo un limite inferiore sul tempo
    limite_tempo=60.0
    data_1=data_grezzi[: ultimo_indice_acceso+1]
    data=data_1[data_1[:, 0] >= limite_tempo]
    tempi=data[:, 0]
    angoli_interi=data[:, 2]
    #print(f"La lunghezza grezza è {len(angoli_interi)}")
    #Calcoliamo il coefficiente di correlazione
    coefficienti_correlazione=[]
    for k in range(10):
        angoli_shiftati=[]
        angoli=[]
        shift_totale = int(round((periodi[i] * k) / 0.02))
        if k==0:
            angoli_shiftati=angoli_interi
            angoli=angoli_interi
        else:
            angoli_shiftati=angoli_interi[shift_totale :] #QUESTO ARRAY È UGUALE A QUELLO DI PRIMA SOLO CHE VENGONO SALTATI K PERIODI
            angoli=angoli_interi[: -shift_totale]
        somma=0
        media_angoli=np.mean(angoli)
        media_angoli_shiftati=np.mean(angoli_shiftati)
        for a in range(len(angoli)):
            somma=somma+(angoli[a]-media_angoli)*(angoli_shiftati[a]-media_angoli_shiftati)
        covarianza=somma/(len(angoli)-1)
        if k==1:
            covarianza_1_periodo.append(covarianza)
            print(f"La covarianza tra i periodi vale {covarianza}")
        somma_x=0
        somma_y=0
        for b in range(len(angoli)):
            somma_x=somma_x+pow(angoli[b]-media_angoli, 2)
            somma_y=somma_y+pow(angoli_shiftati[b]-media_angoli_shiftati, 2)
        varianza_x=somma_x/(len(angoli)-1)
        varianza_y=somma_y/(len(angoli_shiftati)-1)
        coefficiente_correlazione=covarianza/math.sqrt(varianza_x*varianza_y)
        coefficienti_correlazione.append(coefficiente_correlazione)

    numeri=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    plt.figure(figsize=(10, 6))
    #plt.title(f"Frequenza: {frequenze[i]} Hz")
    plt.xlabel("k periodi di shift", fontsize=12)
    plt.ylabel("Coefficiente Correlazione", fontsize=12)
    plt.errorbar(numeri, coefficienti_correlazione, xerr=None, yerr=None, fmt='o', capsize=5, ecolor='red') 
    plt.tick_params(axis="both", labelsize=12) 
    plt.grid(alpha=0.5)
    

    # Generiamo il nome dell'immagine e la salviamo direttamente in "Pendolo a torsione"
    nome_immagine = nome_file_originale.replace(".txt", ".png")
    percorso_salvataggio = os.path.join(cartella_input, nome_immagine)
    
    plt.savefig(percorso_salvataggio, dpi=300, bbox_inches='tight')
    
    #plt.show()
    plt.close()
#print(covarianza_1_periodo)    
    
