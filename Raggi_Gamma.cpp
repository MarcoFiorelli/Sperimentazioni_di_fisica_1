#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>

using namespace std;

double chi (vector<double>, vector<double>, vector<double>, double, double);

int main(){


// FILE DI OUTPUT

    ofstream ofile("prova.txt", ios::app);


//LETTURA DA FILE

    //oggetti per la lettura dei dati
    double x, y, s;

    vector<double>bin;
    vector<double>yield;
    vector<double>s_canali;

    vector<double>bin_1;
    vector<double>yield_1;
    vector<double>s_canali_1;

    string l;

    //lettura da file
    string ifilename="2h16m_fondo_picco.txt";
    ifstream ifile(ifilename);

     while(getline(ifile, l)){
        
        if(l[0]=='#') continue;
        if(l.empty()) continue;
        
        stringstream st(l);
        st>>x>>y;
        
        bin.push_back(x);
        yield.push_back(y);
        s_canali.push_back(sqrt(y));

        
        bin_1.push_back(x);
        yield_1.push_back(y);
        s_canali_1.push_back(sqrt(y));
    }


    //vettori per la regressione lineare ( l'erase cancella in intervalli del tipo [) )

    if(ifilename=="1m_fondo_picco_rebin2.txt"){

    bin_1.erase(bin_1.begin()+7, bin_1.begin()+39);
    yield_1.erase(yield_1.begin()+7, yield_1.begin()+39);
    s_canali_1.erase(s_canali_1.begin()+7, s_canali_1.begin()+39);
    }


    else if(ifilename=="1m_fondo_picco_rebin3.txt"){

    bin_1.erase(bin_1.begin()+5, bin_1.begin()+27);
    yield_1.erase(yield_1.begin()+5, yield_1.begin()+27);
    s_canali_1.erase(s_canali_1.begin()+5, s_canali_1.begin()+27);
    }

    else{
    bin_1.erase(bin_1.begin()+15, bin_1.begin()+78);
    yield_1.erase(yield_1.begin()+15, yield_1.begin()+78);
    s_canali_1.erase(s_canali_1.begin()+15, s_canali_1.begin()+78);
    }

//REGRESSIONE LINEARE

    //calcolo delta

double Delta;

    double sum_1=0; //somma dei raciproci delle varianze
    double sum_2=0; //somma di x_i frattio le varianze
    double sum_3=0; //somma di x_i quadro fratto le varianze

    for(int i=0; i<bin_1.size(); ++i){

        sum_1+=1/pow(s_canali_1.at(i), 2);
        sum_2+=bin_1.at(i)/pow(s_canali_1.at(i), 2);
        sum_3+=pow(bin_1.at(i), 2)/pow(s_canali_1.at(i), 2);
    };

Delta=(sum_1)*(sum_3)-pow(sum_2, 2);

    //calcolo l'intercetta

double a;

    double sum_4=0; //somma di y_i fratto le varianze
    double sum_5=0; //somma di x_i * y_i fratto le varianze
    
    for(int i=0; i<bin_1.size(); ++i){

        sum_4+=yield_1.at(i)/pow(s_canali_1.at(i), 2);
        sum_5+=bin_1.at(i)*yield_1.at(i)/pow(s_canali_1.at(i), 2);
    };

a=(1/Delta)*(sum_3*sum_4-sum_2*sum_5);

    //calcolo il coefficiente angolare

double b;

    b=(1/Delta)*(sum_1*sum_5-sum_2*sum_4);

    //calcolo le incertezze su a e b

double s_a, s_b;

s_a=sqrt((1/Delta)*sum_3);
s_b=sqrt((1/Delta)*sum_1);

//stampo i risultati

ofile<<"I parametri del fit lineare sono:"<<endl;
ofile<<a<<" +/- "<<s_a<<endl;
ofile<<b<<" +/- "<<s_b<<endl<<endl;

ofile<<"MODELLO LINEARE"<<"y = "<<a<<" + "<<b<<" x"<<endl<<endl;


//CHI QUADRO

    double X=chi(bin_1, yield_1, s_canali_1, a, b);

    ofile<<"La variabile chi-quadro calcolata: X="<<X<<endl;
    
    double chi_ridotto;
    chi_ridotto=X/(bin_1.size()-1);

    ofile<<"Il chi-quadro ridotto vale: "<<chi_ridotto<<endl<<endl;


//CALCOLO DELLE AREE

    double S;
    double F;

    ofile<<"si considera ampiezza dei bin uguale a 1"<<endl;

    for(auto x:yield){
        S+=x;
    }

    double bM=a+b*bin.at(0);
    double bm=a+b*bin.at(bin.size()-1);

    F=((bM+bm)*bin.size())/2;
    
    ofile<<"area segnale: S= "<<S<<endl;
    ofile<<"area fondo: F= "<<F<<endl<<endl;

    double P=S-F;
    ofile<<"area picco: A= "<<P<<endl<<endl;


//PROPAGAZIONE DELLE INCERTEZZE

    double var_F, var_S;
    double x_f, x_0, cov_ab;

    x_f=bin.at(bin.size()-1);
    x_0=bin.at(0);

    cov_ab=(-sum_2)/Delta;

    var_F=pow((x_f-x_0)*s_a, 2)+pow(((pow(x_f, 2)-pow(x_0, 2))/2)*s_b, 2)+pow(x_f-x_0, 2)*(x_f+x_0)*cov_ab;

    var_S=S; //per Poisson


//COMPATIBILITA GAUSSIANA

    double lambda; 

    lambda=P/sqrt(var_F+var_S);

    ofile<<"il valore di lambda: "<<lambda<<endl;


    return 0;
}


// FUNZIONE CHI-QUADRO

double chi (vector<double>x, vector<double> y, vector<double>s_y, double q, double m){

    double X=0;
    
    ofstream ofile_1("controllo_gamma.txt", ios::app);

    ofile_1<<"Valori attesi:"<<endl<<endl;

    for(int i=0; i<y.size(); ++i){
        X+=pow(y.at(i)-(q+m*x.at(i)), 2)/pow(s_y.at(i), 2);

        ofile_1<<q+m*x.at(i)<<endl;
    };

return X; 

};