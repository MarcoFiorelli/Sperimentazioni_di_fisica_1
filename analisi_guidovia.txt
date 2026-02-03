#include<iostream>
#include<iomanip>
#include<cmath>
#include<sstream>
#include<fstream>
#include<string>
#include<vector>

using namespace std;

double media (vector<double>);
double devst (vector<double>);
double coeff_ang_reg(vector<double>, vector<double>, double);

int main(){
//LETTURA FILE E CONVERSIONE TETO-VALORI
  string ifile_name = "dati, potenza 3 peso 78g.txt" ;
  ifstream ifile (ifile_name);
    if(!ifile.is_open()){
     cerr<<"errore lettura file"<<endl;
     return 1;
    }
   
  string ofile_name = "analisi.ronaldinho" ;
  ofstream ofile (ofile_name);
  
  vector<string> nomi_gruppi;
  vector<vector<double>> dati;
  
  vector<double> gruppoCorrente;
  string s;
  string riga;
  
  while(getline(ifile,riga)){
    if((riga[0]=='/' ) || (riga.empty()) ){continue;}
   
   stringstream ss(riga);
  
  while (ss>>s) {//a differenza di getline che legge per riga, lui legge per singola parola
    if (s[0] == '#') {
          if (!gruppoCorrente.empty()) {
                dati.push_back(gruppoCorrente);
                gruppoCorrente.clear();
          }
       nomi_gruppi.push_back(s.substr(1));//subtr(1) salva tutte le lettere dalla seconda posizione in poi
        } else {
            try { 
                 gruppoCorrente.push_back(stod(s)); //stod(s) trasforma la stringa (fatta di righe e non parole)
                } catch (...) {	} //ignora eventuali errori
               }
  }}
    if (!gruppoCorrente.empty()) {
        dati.push_back(gruppoCorrente);
    }
   
    ifile.close();

//CIFRE SIGNIFICATIVE
    ofile << fixed << setprecision(5); // Formattazione numeri decimali

//VISUALIZZA SU TESTO OUTPUT
    ofile << "Ho caricato " << nomi_gruppi.size() << " gruppi.\n" << endl;

    for (size_t i = 0; i < nomi_gruppi.size(); i++) {//size_t inizializza solo valori positivi o 0
        ofile << "Gruppo: " << nomi_gruppi[i] <<"cm"<< endl; 
        ofile << "  Dati: ";
          for (size_t k = 0; k < dati[i].size(); k++) {
            ofile << dati[i][k] << "s  ";
          }
        ofile<<endl<<"  Media= "<<media(dati[i])<<"s"<<endl;
        ofile<<"  Deviazione Standard (singolo dato)= "<<devst(dati[i])<<"s"<<endl;
        ofile<<"  Deviazione Standard (media)= "<<((devst(dati[i]))/(sqrt(dati[i].size())))<<"s"<<endl;
        ofile <<endl<< "-------------------" << endl;
    }
  
  //ofile<<endl<<"Media totale"<<media(dati)<<endl;
  //ofile<<"Deviazione standard totale"<<devst(dati)<<endl;
  
  /* VISUALIZZA SU TERMINALE
      cout << "Ho caricato " << nomi_gruppi.size() << " gruppi.\n" << endl;

    for (size_t i = 0; i < nomi_gruppi.size(); i++) {//size_t inizializza solo valori positivi o 0
        cout << "Gruppo: " << nomi_gruppi[i] << endl; 
        cout << "  Dati: ";
          for (size_t k = 0; k < dati[i].size(); k++) {
            cout << dati[i][k] << " ";
          }
        cout << endl << "-------------------" << endl;
    }
  */


//GLOBALMENTE
vector<double> tuttoInsieme;

//SOMMIAMO I VETTORI IN UN UNO
    for (size_t i = 0; i < dati.size(); i++) {
        for (double valore : dati[i]) {
            tuttoInsieme.push_back(valore);
        }
    }

    ofile << "--- STATISTICHE GLOBALI (Tutti i dati) ---" << endl;
    
    if (!tuttoInsieme.empty()) {
        double m_globale = media(tuttoInsieme);
        double s_globale = devst(tuttoInsieme);

        ofile << "Totale dati analizzati: " << tuttoInsieme.size() << endl;
        ofile << "Media globale: " << m_globale <<"s"<< endl;
        ofile << "Deviazione Std globale(singola misura): " << s_globale <<"s"<< endl;
        ofile << "Deviazione Std globale(media): " << s_globale/sqrt((tuttoInsieme.size()))<<"s" <<endl;
    } else {
        ofile << "Nessun dato trovato nel file." << endl;
    }

//VETTORE VELOCITA' ISTANTANEA (ORDINATA)
vector<double> velocità_istantanee;
double velocità;


for(int i=0;i<dati.size();i++){
  double t_medio = media(dati[i]);
  
  velocità_istantanee.push_back(0.1/t_medio);
}




//VETTORE ASCISSA
vector<double> ascisse;
double tempo_pos=media(dati[0])/2;
 ascisse.push_back(tempo_pos);

for(int i = 1;i<velocità_istantanee.size();i++){
  tempo_pos=tempo_pos+(media(dati[i])+media(dati[i-1]))/2;  
  ascisse.push_back(tempo_pos);
}

	for(auto x : ascisse){
	cout<< x<<endl;
	}

ofile<<endl<<"------POSIZIONE PER VELOCITÀ ISTANTANEA-------"<<endl;
for(int i=0;i<velocità_istantanee.size();i++){
  ofile<<velocità_istantanee[i]<<"m/s	"<<ascisse[i]<<"s"<<endl;
}

/*
ofile<<endl<<"------STIMA COEFFICIENTE ANGOLARE------"<<endl;
FUNZIONE PRONTA (ABBIAMO USATO PITON MA ANCHE QUELLA IN FONDO A QUESTO FILE VA BENE"
*/

 return 0;
}
 
 
 
 
//FUNZIONI
double media(vector<double> serie){
 double somma=0.;
 int conteggio=0;

 for(auto x : serie){
  somma = somma +x;
  conteggio ++;
 } 
 if (conteggio>0){return somma/conteggio;}
 else {
  cerr<<"errore nella media"<<endl;
  return 0;
 }
}
 
double devst(vector<double> serie){
 double somma2=0;
 int conteggio=0;
 double med = media(serie);
 
 for (auto x : serie){
  somma2 = somma2 + (x-med)*(x-med);
  conteggio ++; 
 }
 if(conteggio>1){return sqrt((somma2)/(conteggio - 1));}
 else {
  cerr<<"errore nella stima di sigma"<<endl;
  return 0;
 }
}


double coeff_ang_reg(vector<double> y, vector<double> x, double X){
 double somma_numeratore =0.;
 double somma_denominatore =0.;
 for(int i=0;i<y.size();i++){
   somma_numeratore=somma_numeratore + y[i]*(x[i]-X);
 }
 for(int i=0;i<y.size();i++){
   somma_denominatore=somma_denominatore + (x[i]-X)*(x[i]-X);
 }
 return ((somma_numeratore)/(somma_denominatore));
}