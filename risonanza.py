import os
import glob
import numpy as np
import math
from pathlib import Path
import matplotlib.pyplot as plt
# IMPORTANTE: serve scipy per l'ottimizzazione del fit non lineare
from scipy.optimize import curve_fit

    # =========================================================================
    #  FIT LORENZIANO / BREIT-WIGNER (Su tutto l'insieme di punti individuali)
    # =========================================================================
def lorenziana_breit_wigner(x, A, B, C, D):
    """
    Funzione teorica della risonanza (Breit-Wigner / Cauchy-Lorentz).
    x = frequenza (Hz)
    B = frequenza naturale al quadrato (w0^2)
    C = legato allo smorzamento al quadrato (gamma^2)
    D = fondo costante/offset dello strumento
    A = fattore di scala/ampiezza
    """
    return A / np.sqrt((B - x**2)**2 + C * x**2) + D


def analizza_dati_pendolo():
    #cartella = "MassimiMinimi"
    cartella = r"C:\Users\giuse\Desktop\MassimiMinimi"
    
    # Cerca tutti i file dentro la cartella MassimiMinimi
    file_list = glob.glob(os.path.join(cartella, "*"))
    file_list = [f for f in file_list if os.path.isfile(f) and not os.path.basename(f).startswith('.')]
    
    if not file_list:
        print(f"Nessun file trovato nella cartella '{cartella}'")
        return

    # Stampa l'intestazione della tabella nel terminale
    print(f"{'Nome File':<20} | {'Media Max':<10} | {'DevStd Max':<10} | {'Media Min':<10} | {'DevStd Min':<10} | {'Ampiezza':<10}|{'Errore ampiezza':<10}|{'Errore ampiezza medio':<10}")
    print("-" * 85)
    
    # Liste piatte: ogni file/misura genera un punto indipendente nel grafico e nei fit
    freq_grafico = []
    ampiezze_medie = []
    errori_ampiezza = []
    errori_ampiezza_media=[]

    # Elabora un file alla volta
    dati_per_salvataggio = [] # Lista per raccogliere i dati di ogni file
    for file_path in file_list:
        nome_file = os.path.basename(file_path)
        try:
            # 1. Dividiamo il nome del file usando il trattino basso '_'
            parti_del_nome = nome_file.split('_')
            
            # 2. Prendiamo l'ultimo pezzo (es. "0.93.txt")
            ultimo_pezzo = parti_del_nome[-1]
            
            # 3. Togliamo ".txt" per isolare solo il numero (es. "0.93")
            stringa_frequenza = ultimo_pezzo.replace(".txt", "")
            
            # 4. Convertiamo la stringa in un numero decimale (float)
            frequenza = float(stringa_frequenza)
            
        except (ValueError, IndexError):
            continue
            
        massimi = []
        minimi = []
        
        try:
            with open(file_path, "r") as f_in:
                for linea in f_in:
                    if linea.startswith("#") or not linea.strip():
                        continue
                    
                    parti = linea.split()
                    if len(parti) == 2:
                        massimi.append(float(parti[0]))
                        minimi.append(float(parti[1]))
            
            if not massimi:
                continue

            # Calcoli statistici veloci con numpy per il singolo file
            med_max = np.mean(massimi)
            std_max = np.std(massimi, ddof=1) if len(massimi) > 1 else 0.0
            err_media_max=std_max/math.sqrt(len(massimi))
            
            med_min = np.mean(minimi)
            std_min = np.std(minimi, ddof=1) if len(minimi) > 1 else 0.0
            err_media_min=std_min/math.sqrt(len(minimi))
            
            ampiezza = (med_max - med_min) / 2
            
            # Errore associato alla singola esecuzione (propagazione std)
            err_punto = 0.5 * np.sqrt(std_max**2 + std_min**2)
            err_punto_medio= 0.5 * np.sqrt(err_media_max**2 + err_media_min**2)
            if err_punto == 0:
                err_punto = 0.001  
            
            # AGGIUNTA DIRETTA (le doppie frequenze rimangono separate)
            freq_grafico.append(frequenza)
            ampiezze_medie.append(ampiezza)
            errori_ampiezza.append(err_punto)
            errori_ampiezza_media.append(err_punto_medio)
            # ... (dopo il calcolo di err_punto)
            dati_per_salvataggio.append((frequenza, med_max, std_max, med_min, std_min, ampiezza, err_punto, err_punto_medio))
            
            print(f"{nome_file:<20} | {med_max:<10.4f} | {std_max:<10.4f} | {med_min:<10.4f} | {std_min:<10.4f} | {ampiezza:<10.4f}|{err_punto:<10.4f}|{err_punto_medio:<10.4f}")
            
            #print(f"{nome_file:<20} | {med_max:<10.4f} | {std_max:<10.4f} | {med_min:<10.4f} | {std_min:<10.4f} | {ampiezza:<10.4f}|{err_punto:<10.4f}")
            
        except Exception as e:
            print(f"Errore nell'elaborazione del file {nome_file}: {e}")
            
    print("-" * 85)
    
    if not freq_grafico:
        print("Nessun dato valido estratto dai file. Impossibile procedere.")
        return

    # Convertiamo in array numpy per poter effettuare i calcoli dei fit
    x_punti = np.array(freq_grafico)
    y_punti = np.array(ampiezze_medie)
    y_err = np.array(errori_ampiezza)

    # Ordiniamo i vettori per frequenza crescente (indispensabile per il grafico)
    indici_ordinati = np.argsort(x_punti)
    x_punti = x_punti[indici_ordinati]
    y_punti = y_punti[indici_ordinati]
    y_err = y_err[indici_ordinati]

    print("\n=================== ANALISI DEL FIT LORENZIANO ===================")

# Individuiamo il picco grezzo per generare i parametri di partenza (guess)
    indice_massimo = np.argmax(y_punti)
    f_max_sperimentale = x_punti[indice_massimo]
    
    # Generazione automatica di stime iniziali intelligenti (p0)
    D_guess = np.min(y_punti)                         
    B_guess = f_max_sperimentale**2                   
    C_guess = 0.005                                    
    A_guess = (np.max(y_punti) - D_guess) * np.sqrt(C_guess * B_guess) 
    
    p0_guess = [A_guess, B_guess, C_guess, D_guess]
    
    try:
        # curve_fit applica i minimi quadrati pesati usando le incertezze individuali
        popt, pcov = curve_fit(lorenziana_breit_wigner, x_punti, y_punti, p0=p0_guess, sigma=y_err, absolute_sigma=True, maxfev=10000)
        A_lor, B_lor, C_lor, D_lor = popt
        
        # Estrazione delle varianze e covarianze dei parametri per la propagazione

        err_A = np.sqrt(pcov[0, 0])
        err_B = np.sqrt(pcov[1, 1])
        err_C = np.sqrt(pcov[2, 2])
        err_D = np.sqrt(pcov[3, 3])



        sigma_B_quad = pcov[1, 1]  # Varianza del parametro B (w0^2)
        sigma_C_quad = pcov[2, 2]  # Varianza del parametro C (g^2)
        cov_BC = pcov[1, 2]        # Covarianza tra B e C
        
        f0_stimata_lor = np.sqrt(B_lor)               
        
        # Calcolo della frequenza di risonanza e propagazione dell'errore associato
        if (B_lor - C_lor/2) > 0:
            f_res_lor = np.sqrt(B_lor - C_lor/2)
            # Formula di propagazione dei minimi quadrati inclusiva di covarianza
            varianza_f_res = (sigma_B_quad + 0.25 * sigma_C_quad - cov_BC) / (4 * B_lor - 2 * C_lor)
            err_f_res_lor = np.sqrt(varianza_f_res) if varianza_f_res > 0 else 0.0
        else:
            # Caso limite teorico senza smorzamento significativo
            f_res_lor = f0_stimata_lor
            err_f_res_lor = np.sqrt(sigma_B_quad) / (2 * f_res_lor)
            
        ampiezza_max_lor = lorenziana_breit_wigner(f_res_lor, A_lor, B_lor, C_lor, D_lor)
        
        print(f"[FIT LORENZIANO (Su tutte le {len(x_punti)} misure individuali)]")
        print(f"  -> Parametro B (w0^2):               {B_lor:.5f}\(\pm \){err_B:.5f}  Hz^2")
        print(f"  -> Parametro C (smorzamento g^2):    {C_lor:.10f}\(\pm \){err_C:.10f} ")
        print(f"  -> FREQUENZA DI RISONANZA STIMATA:   {f_res_lor:.5f} ± {err_f_res_lor:.5f} Hz")
        print(f"  -> Ampiezza massima stimata:         {ampiezza_max_lor:.5f} rad")
        print(f"  -> Parametro A:         {A_lor:.5f}\(\pm \){err_A:.5f} ")
        print(f"  -> Parametro D:         {D_lor:.5f} \(\pm \){err_D:.5f} ")
        fit_lorenziano_successo = True
    except Exception as e:
        print(f"[ERRORE] Il fit Lorenziano non è riuscito a convergere: {e}")
        fit_lorenziano_successo = False
        
    print("=======================================================")

    # =========================================================================
    # --- COSTRUZIONE DEL GRAFICO ---
    # =========================================================================
    plt.figure(figsize=(10, 6))
    
    # Punti sperimentali individuali
    plt.errorbar(x_punti, y_punti, yerr=y_err, fmt='o', color='blue', 
                 ecolor='red', capsize=4, markersize=4, label='Misure individuali', zorder=3)
    
    # Asse delle frequenze continuo per tracciare la curva fluida
    x_teorico = np.linspace(min(x_punti), max(x_punti), 500)
    
    # Grafico Linea Lorenziana Completa
    if fit_lorenziano_successo:
        y_teorico_lor = lorenziana_breit_wigner(x_teorico, A_lor, B_lor, C_lor, D_lor)
        plt.plot(x_teorico, y_teorico_lor, color='purple', linestyle='-', linewidth=2, markersize=0.01,
                 label=f'Fit Lorenziano ($f_{{res}}$ = {f_res_lor:.5f} $\\pm$ {err_f_res_lor:.5f} Hz)')
        plt.axvline(x=f_res_lor, color='red', linestyle=':', alpha=0.7)

    # Impostazioni formali del grafico
    plt.xlabel(" $\\nu_f$ (Hz)", fontsize=11)
    plt.ylabel("$\\theta_{0f}$ (rad)", fontsize=11)
    plt.xticks(fontsize=11)  
    plt.yticks(fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.5)
    #plt.legend(fontsize=10, loc='upper right')
    percorso_desktop = Path.home() / "Desktop" / "grafico_pendolo_torsione.pdf"

    # Salva usando il percorso definito
    plt.savefig(percorso_desktop, dpi=300, bbox_inches='tight')
    
    #plt.savefig('grafico_pendolo_torsione.pdf', dpi=300, bbox_inches='tight')
    plt.show()
    # =========================================================================
    # --- SALVATAGGIO DEI DATI IN OUTPUT_FINALE.TXT ---
    # =========================================================================
    # === FINE DELLA PARTE DI CALCOLO E GRAFICO ===

    # === ORA INSERISCI QUI IL BLOCCO DI SALVATAGGIO ===
    # Deve essere indentato allo stesso livello del codice qui sopra!
    try:
        percorso_output = os.path.join(cartella, "OUTPUT_FINALE.txt")
        with open(percorso_output, "w") as f_out:
            f_out.write("Freq\tMedMax\tStdMax\tMedMin\tStdMin\tAmpiezza\tErrAmp\tErrAmpMed\n")
            dati_ordinati = sorted(dati_per_salvataggio, key=lambda x: x[0])
            for d in dati_ordinati:
                f_out.write(f"{d[0]:.4f}\t{d[1]:.4f}\t{d[2]:.4f}\t{d[3]:.4f}\t{d[4]:.4f}\t{d[5]:.4f}\t{d[6]:.4f}\t{d[7]:.4f}\n")
        print(f"\n[INFO] Dati salvati correttamente in: {percorso_output}")
    except Exception as e:
        print(f"\n[ERRORE] Impossibile salvare il file di output: {e}")

# Qui finisce la funzione

if __name__ == "__main__":
    analizza_dati_pendolo()

