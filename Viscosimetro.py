#CARICO LE LIBRERIE UTILI
import numpy as np #CALCOLI
import matplotlib.pyplot as plt #GRAFICI
from scipy import odr #FIT
import math

#LETTURA DA FILE, COSTRUSICO LA MATRICE
files=['raggio1.txt', 'raggio2.txt', 'raggio3.txt', 'raggio4.txt', 'raggio5.txt', 'raggio6.txt', 'raggio7.txt', 'raggio8.txt']
lista_incertezze=[] #CONTIENE 10 INCERTEZZE, UNA PER OGNI TRAGUARDO
matrice_medie_tempi=[] #È UNA LISTA DI LISTE: LA LISTA I-ESIMA CONTIENE LE MEDIE DEI TEMPI AI VARI INTERVALLI
for file in files:
    data=np.loadtxt(file)
    t1=data[:, 0]
    t2=data[:, 1]
    t3=data[:, 2]
    matrice_tempi=np.column_stack((t1, t2, t3)) #È UNA MATRICE LE CUI 3 COLONNE SONO I TEMPI CHE LA PALLINA IMPIEGA PER RAGGIUNGERE I VARI INTERVALLI (È UGUALE A QUELLA DI EXCEL)
    

    #COSTRUISCO LISTA MEDIE TEMPI
    medie_tempi=[] #È UNA LISTA DI 10 ELEMENTI: LE MEDIE DEI TEMPI AI TEMPI AI VARI TRAGUARDI
    for riga in matrice_tempi:
        a=0
        for elemento in riga:
            a=a+elemento
        
        media=a/3
        medie_tempi.append(media)

    #print(medie_tempi)
    matrice_medie_tempi.append(medie_tempi)


    #CALCOLO L'INCERTEZZA DA ASSOCIARE AL TEMP0
    varianze_tempi=[]
    for i in range(len(matrice_tempi)):
        a=0
        for elemento in matrice_tempi[i]:
            a=a+pow((elemento-medie_tempi[i]),2)

        varianza=a/2
        varianze_tempi.append(varianza)
        



    b=0
    for varianza in varianze_tempi:
        b=b+varianza
    varianza_tot=b/len(varianze_tempi)
    delta_t=(math.sqrt(varianza_tot))/math.sqrt(3)
    lista_incertezze.append(delta_t)



#print(lista_incertezze) #QUESTA È UNA LISTA IN CUI L'ENTRATA I-ESIMA È L'INCERTEZZA ASSOCIATA AI TEMPI PER L'I-ESIMO RAGGIO
#print(matrice_medie_tempi) #QUESTA È UNA LISTA DI LISTE: L'I-ESIMA LISTA CONTIENE LE MEDIE DEI TEMPI PER L'I-ESIMO INTERVALLO


#COSTRUISCO LA LISTA DELLO SPAZIO CON LA SUA INCERTEZZA
spazio=[0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]
spazio_ridotto=[0, 0.10, 0.20, 0.30, 0.40, 0.50]
diametri_con_incertezze=np.loadtxt('raggi.txt')
diametri=diametri_con_incertezze[:, 0]
diametri_incertezze=diametri_con_incertezze[:, 1]
raggi=[]
for diametro in diametri:
    raggio=diametro/2
    raggi.append(raggio)
incertezze_raggi=[]
for a in diametri_incertezze:
    b=a/2
    incertezze_raggi.append(b)
incertezze_spazio=[] #LISTA CON INCERTEZZE SULLO SPAZIO
for raggio in raggi:
    delta_r=raggio/math.sqrt(6)
    incertezze_spazio.append(delta_r)
print(incertezze_spazio)

#ADESSO HO TUTTO,TEMPI E SPAZIO. FACCIAMO IL FIT!
raggi_legenda=[]
for raggio in raggi:
    a=f'r={raggio*1000:.2f} mm'
    raggi_legenda.append(a)

plt.figure(figsize=(10, 6))
plt.xlabel(r'Spazio (m)', fontsize=13)
plt.ylabel(r'Tempo (s)', fontsize=13)
colori=[]
for i in range(4):
    punti1=plt.errorbar( spazio, matrice_medie_tempi[i],  xerr=incertezze_spazio[i], yerr=lista_incertezze[i],
                fmt='o',  capsize=2, capthick=2, markersize=4,
                linewidth=2, label=raggi_legenda[i])
    colore1=punti1[0].get_color()
    colori.append(colore1)
for i in range(4, 8):
    punti2=plt.errorbar(spazio_ridotto, matrice_medie_tempi[i], xerr=incertezze_spazio[i], yerr=lista_incertezze[i], 
                fmt='o',  capsize=2, capthick=2, markersize=4,
                linewidth=2, label=raggi_legenda[i])
    colore2=punti2[0].get_color()
    colori.append(colore2)
    
#ADESSO FACCIO IL FIT
def funzione_lineare(B, x):
    return B[0]*x+B[1]
velocità=[]
velocità_incertezze=[]
intercette=[]
intercette_incertezze=[]
for i in range (4):
    modello_lineare=odr.Model(funzione_lineare)
    data=odr.RealData( spazio, matrice_medie_tempi[i],  sx=incertezze_spazio[i], sy=lista_incertezze[i])
    mio_odr=odr.ODR(data, modello_lineare, beta0=[1.0, 1.0])
    risultato=mio_odr.run()
    pendenza_calcolata=risultato.beta[0]
    intercetta_calcolata=risultato.beta[1]
    errore_pendenza=risultato.sd_beta[0]
    errore_intercetta=risultato.sd_beta[1]
    print(f'\nPendenza:{pendenza_calcolata}\u00B1{errore_pendenza}')
    print(f'Intercetta: {intercetta_calcolata}\u00B1{errore_intercetta}')

    a=risultato.beta[0]
    b=risultato.beta[1]
    err_a=risultato.sd_beta[0]
    err_b=risultato.sd_beta[1]
    x_linea=np.linspace(0,max(spazio), 100)
    y_linea=a*x_linea+b
    plt.plot(x_linea, y_linea, linestyle='-', color=colori[i], linewidth=1)


    c=1/a
    velocità.append(c)
    err_c=err_a/pow(a, 2)
    velocità_incertezze.append(err_c)
    intercette.append(b)
    intercette_incertezze.append(err_b)


for i in range (4, 8):
    modello_lineare=odr.Model(funzione_lineare)
    data=odr.RealData( spazio_ridotto, matrice_medie_tempi[i],  sx=incertezze_spazio[i], sy=lista_incertezze[i])
    mio_odr=odr.ODR(data, modello_lineare, beta0=[1.0, 1.0])
    risultato=mio_odr.run()
    pendenza_calcolata=risultato.beta[0]
    intercetta_calcolata=risultato.beta[1]
    errore_pendenza=risultato.sd_beta[0]
    errore_intercetta=risultato.sd_beta[1]
    print(f'\nPendenza:{pendenza_calcolata}\u00B1{errore_pendenza}')
    print(f'Intercetta: {intercetta_calcolata}\u00B1{errore_intercetta}')

    a=risultato.beta[0]
    b=risultato.beta[1]
    err_a=risultato.sd_beta[0]
    err_b=risultato.sd_beta[1]
    x_linea=np.linspace(0,max(spazio_ridotto), 100)
    y_linea=a*x_linea+b
    plt.plot(x_linea, y_linea, linestyle='-', color=colori[i], linewidth=1)

    c=1/a
    velocità.append(c)
    err_c=err_a/pow(a, 2)
    velocità_incertezze.append(err_c)
    intercette.append(b)
    intercette_incertezze.append(err_b)


plt.grid(alpha=0.3)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.minorticks_on()
plt.legend()
plt.tight_layout()

plt.savefig('fit_newtoniano.png')
plt.show()

print(velocità)
with open('velocità.txt', 'w') as file:
    for i in range(8):
        file.write(f"{velocità[i]}\t{velocità_incertezze[i]}\n")

#CORREZIONE FONDO-PARETE
velocità_corrette=[]
velocità_corrette_incertezze=[]
for i in range(8):
    v_inf=velocità[i]*(1+2.4*raggi[i]/0.045)*(1+3.3*raggi[i]/0.7)
    velocità_corrette.append(v_inf)
for i in range(8):
    incertezza=math.sqrt(pow(velocità_incertezze[i]*(1+(3.3/0.7+2.4/0.045)*raggi[i]+(2.4*3.3)/(0.7*0.045)*pow(raggi[i], 2)),2)+
                         pow(incertezze_raggi[i]*(velocità[i]*(3.3/0.7+2.4/0.045)+velocità[i]*2*2.4*3.3/(0.7*0.045)*raggi[i]), 2))
    velocità_corrette_incertezze.append(incertezza)

with open('velocità_corrette.txt', 'w') as file:
    for i in range(8):
        file.write(f"{velocità_corrette[i]}\t{velocità_corrette_incertezze[i]}\n")

#CALCOLO LA VISCOSITÀ (CORRETTA PER L'EFFETTO FONDO PARETE)
viscosità=[]
viscosità_incertezze=[]
for i in range(8):
    eta=2/9*pow(raggi[i], 2)/velocità_corrette[i]*(7870-1260)*9.8106
    viscosità.append(eta)
for i in range (8):
    delta_eta=math.sqrt(pow(incertezze_raggi[i]*4/9*raggi[i]/velocità_corrette[i]*(7870-1260)*9.8106, 2)+
                        pow(velocità_corrette_incertezze[i]*2/9*pow(raggi[i]/velocità_corrette[i], 2)*(7870-1260)*9.8106, 2)+
                        pow(1*2/9*pow(raggi[i], 2)/velocità_corrette[i]*9.8106, 2)+
                        pow(10*2/9*pow(raggi[i], 2)/velocità_corrette[i]*9.8106, 2))
    viscosità_incertezze.append(delta_eta)


#CALCOLO LE VISCOSITÀ NON CORRETTE
viscosità_non_corrette=[]
viscosità_incertezze_non_corrette=[]
for i in range(8):
    eta=2/9*pow(raggi[i], 2)/velocità[i]*(7870-1260)*9.8106
    viscosità_non_corrette.append(eta)
for i in range (8):
    delta_eta=math.sqrt(pow(incertezze_raggi[i]*4/9*raggi[i]/velocità[i]*(7870-1260)*9.8106, 2)+
                        pow(velocità_incertezze[i]*2/9*pow(raggi[i]/velocità[i], 2)*(7870-1260)*9.8106, 2)+
                        pow(1*2/9*pow(raggi[i], 2)/velocità[i]*9.8106, 2)+
                        pow(10*2/9*pow(raggi[i], 2)/velocità[i]*9.8106, 2))
    viscosità_incertezze_non_corrette.append(delta_eta)



#CORREZIONE VISCOSITÀ TEMPERATURA
temperature=[]
temp=np.loadtxt('Temperature.txt')
temp1=temp[:, 0]
temp2=temp[:, 1]
temp3=temp[:, 2]
for i in range (8):
    a=(temp1[i]+temp2[i]+temp3[i])/3
    temperature.append(a)

print(temperature)
viscosità_teoriche=[]
for T in temperature:
    glycerolVisc=0.001*12100*np.exp((-1233+T)*T/(9900+70*T))
    viscosità_teoriche.append(glycerolVisc)
fattori_correttivi=[]
for i in range (8):
    c=viscosità_teoriche[0]/viscosità_teoriche[i]
    fattori_correttivi.append(c)
viscosità_finali=[]
viscosità_finali_incertezze=[]
for i in range(8):
    a=fattori_correttivi[i]*viscosità[i]
    viscosità_finali.append(a)
for i in range(8):
    a=fattori_correttivi[i]*viscosità_incertezze[i]
    viscosità_finali_incertezze.append(a)


#PLOT
plt.figure(figsize=(10, 6))
plt.xlabel(r'Raggi (m)')
plt.ylabel(r'Viscosità (Pa*s)')
plt.errorbar(raggi, viscosità_non_corrette, xerr=incertezze_raggi, yerr=viscosità_incertezze_non_corrette,
             fmt='o', color='red', ecolor='red', capsize=2, capthick=2, markersize=4, linewidth=2, label='Nessuna correzione')

plt.errorbar(raggi, viscosità, xerr=incertezze_raggi, yerr=viscosità_incertezze,
             fmt='o', color='blue', ecolor='blue', capsize=2, capthick=2, markersize=4, linewidth=2, label='Correzione fondo-parete')
plt.errorbar(raggi, viscosità_finali, xerr=incertezze_raggi, yerr=viscosità_finali_incertezze,
             fmt='o', color='green', ecolor='green', capsize=2, capthick=2, markersize=4, linewidth=2, label='Correzione fondo-parete+temperatura')

plt.grid(alpha=0.3)
plt.xticks(fontsize=14) 
plt.yticks(fontsize=14)
plt.minorticks_on()
plt.legend()
plt.tight_layout()
plt.savefig('viscosità.png')
plt.show()


