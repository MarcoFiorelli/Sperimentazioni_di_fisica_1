import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit

medie=[]
deviazioni=[]
files=['1_min.txt', '3_min.txt', '6_min.txt', '10_min.txt', '15_min.txt', '20_min.txt', '30_min.txt', 
       '40_min.txt', '1_h_16_min.txt', '1_h_46_min.txt', 'boh_min.txt', '15_h_30_min.txt']
for file in files:
    file_isto="file"
    isto=np.loadtxt(file)

    bin=isto[:, 0]
    occurences=isto[:, 1]


    plt.figure(figsize=(10, 8))
    plt.bar(bin, occurences, width=1, color='g')
    plt.xlabel('Bin', fontsize=13)
    plt.ylabel('Occurences', fontsize=13)
    plt.grid(alpha=0.3)

    plt.xticks(np.arange(0, 4097, 200), fontsize=13)
    plt.yticks(fontsize=13)
    #plt.show()
    plt.close()



    #FACCIAMO FIT LINEARE FONDO
    x_fit_1=bin[2500:2539]
    occurences_fit_1=occurences[2500:2539]
    x_fit_2=bin[2801:2840]   
    occurences_fit_2=occurences[2801:2840]
    x_fit=np.concatenate((x_fit_1, x_fit_2))
    occurences_fit=np.concatenate((occurences_fit_1, occurences_fit_2))
    incertezze_fit=[]
    for f in occurences_fit:
        if f==0:
            s=1.0
        else:
             s=math.sqrt(f)     

        incertezze_fit.append(s)

    def modello_lineare(x, m, q):
        return m*x+q
    popt, pcov=curve_fit(modello_lineare, x_fit, occurences_fit, sigma=incertezze_fit, absolute_sigma=True)
    m_fit, q_fit=popt




    #TROVIAMO IL CENTRO
    #SELEZIONO I DATI
    bin_gauss=bin[2540: 2800]
    occurences_gauss=occurences[2540: 2800]
    #print(bin_gauss)
    x_gauss=bin_gauss*(occurences_gauss-(m_fit*bin_gauss+q_fit))
    tot_occurences=0
    for i in range(len(bin_gauss)):
        tot_occurences=tot_occurences+occurences_gauss[i]-(m_fit*bin_gauss[i]+q_fit)
    somma=0
    for a in x_gauss:
        somma=somma+a
    media=somma/tot_occurences

    somma_dev=0
    for b in range(len(bin_gauss)):
        conteggi_netti_b=occurences_gauss[b]-(m_fit*bin_gauss[b]+q_fit)
        if conteggi_netti_b<0:
            conteggi_netti_b=0
        somma_dev=somma_dev+(media-bin_gauss[b])*(media-bin_gauss[b])*(conteggi_netti_b)
    dev_std= (math.sqrt(somma_dev/(tot_occurences-1)))/math.sqrt(tot_occurences) 
    #print(f"{media}±{dev_std}")
    medie.append(media)
    deviazioni.append(dev_std)

aaa=np.mean(medie)
plt.figure(figsize=(12, 7))
x=np.arange(1, 13)
colors=['red', 'green', 'green', 'green', 'green', 'green', 'green', 'green', 'blue', 'blue', 'blue', 'orange']
tempi=['1 min', '3 min', '6 min', '10 min', '15 min', '20 min', '30 min', '40 min', '1 h 16 min', '1 h 46 min', '2 h 16 min', '15 h 30 min']
for i in range(len(medie)):
    plt.errorbar(x[i], medie[i], yerr=deviazioni[i], fmt='o', capsize=5, color=colors[i], ecolor=colors[i])
plt.xlabel('Tempo di acquisizione (h, min)', fontsize=13)
plt.ylabel('Posizione del picco del K', fontsize=13)
plt.grid(alpha=0.3)
plt.xticks(x, tempi, fontsize=11)
plt.yticks(fontsize=13)
plt.tight_layout()
#plt.axhline(y=aaa, color='r', linestyle='--')
plt.savefig("Potassio.pdf")
plt.show()