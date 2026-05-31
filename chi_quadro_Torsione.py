import math
import numpy as np
import matplotlib.pyplot as plt

# Usa np.loadtxt invece di leggere riga per riga manualmente
# delimiter='\t' specifica che le colonne sono separate da tabulazioni
# skiprows=1 salta l'intestazione
percorso_file = r"C:\Users\giuse\Desktop\Pendolo a torsione\OUTPUT_FINAL.txt"
matrice_dati = np.loadtxt(percorso_file, delimiter='\t', skiprows=1)

# Verifica le dimensioni
print(f"Dimensioni della matrice: {matrice_dati.shape}")

# Ora puoi accedere alle colonne in modo sicuro
frequenze = matrice_dati[:, 0]
ampiezze = matrice_dati[:, 5]
incertezze_ampiezze = matrice_dati[:, 6]
incertezza_media = matrice_dati[:, 7]


#print(incertezze_ampiezze)
#print(incertezza_media)
A= 0.00561 
B=  0.93320
C=0.00019
D=0.00511
chi_quadro=0
for i in range(len(ampiezze)):
	chi_quadro=chi_quadro+pow((ampiezze[i]-(A/(math.sqrt(pow(B-frequenze[i] * frequenze[i], 2)+C *frequenze[i] * frequenze[i]))+D))/incertezze_ampiezze[i], 2)
print(f"Il chiquadro vale {chi_quadro}")
GDL=len(ampiezze)-4

chi_quadro_ridotto=chi_quadro/GDL

print(f"Il chiquadro ridotto vale {chi_quadro_ridotto}")
#print(len(ampiezze))


#ERRORE A POSTERIORI
somma=0
for i in range(len(ampiezze)):
	somma=somma+pow(ampiezze[i]-(A/(math.sqrt(pow(B-frequenze[i] * frequenze[i], 2)+C *frequenze[i] * frequenze[i]))+D), 2)
errore_posteriori=math.sqrt(somma/GDL)
print(errore_posteriori)




"""


N_efficaci=[]
for i in range(len(incertezza_media)):
	N_eff=pow(errore_posteriori/incertezza_media[i], 2)
	N_efficaci.append(N_eff)



print(N_efficaci)
"""
