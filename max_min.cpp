#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>

using namespace std;

int main(){

//oggetti di cui ho bisogno
vector<double>v={0.35, 1.90};

vector<double>tempo;
vector<double>pendolo;

double t, p, T, t_0;
double M, m;

int i_M, i_m;


//ciclo su tutti i file
for(auto x : v){

    int i=0;

    tempo.clear();
    pendolo.clear();

    ostringstream name;
    name << fixed << setprecision(2) << x;

    string ifilename = "ROI_f_" + name.str() + ".txt";
    string ofilename = "output_f_" + name.str() + ".txt";

    ifstream ifile(ifilename);

    if(!ifile){
        cerr << "Errore apertura file: " << ifilename << endl;
        continue;
    }

    ofstream ofile(ofilename, ios::app);

    string l;

    while(getline(ifile, l)){
        
        if(l.empty()) continue;
        if(l[0]=='#') continue;
        
        stringstream st(l);
        st>>t>>p;

        tempo.push_back(t);
        pendolo.push_back(p);

    }

    ifile.close();


    //trova il periodo e il tempo di inizio
    T=1/x;
    t_0=tempo.front();
    
    ofile<<"#Massimi e minimi delle ampiezze delle oscillazioni del pendolo a torsione:"<<endl;


    //IDEA 2: massimi e minimi
    while(t_0+T<=tempo.back()){

        M=pendolo.at(i);
        m=pendolo.at(i);

        i_M=i;
        i_m=i;

        while(i<tempo.size() && tempo.at(i)<t_0+T){
            
            if(pendolo.at(i)>M){

                M=pendolo.at(i);
                i_M=i;
            }

            if(pendolo.at(i)<m){

                m=pendolo.at(i);
                i_m=i;
            }

            ++i;
        }
        

        bool max_ok = false;
        bool min_ok = false;

        if(i_M >= 3 && i_M + 3 < pendolo.size()){

            max_ok =
            (pendolo.at(i_M-1) <= pendolo.at(i_M)) &&
            (pendolo.at(i_M-2) <= pendolo.at(i_M-1)) &&
            (pendolo.at(i_M-3) <= pendolo.at(i_M-2)) &&

            (pendolo.at(i_M) >= pendolo.at(i_M+1)) &&
            (pendolo.at(i_M+1) >= pendolo.at(i_M+2)) &&
            (pendolo.at(i_M+2) >= pendolo.at(i_M+3));
        }

        if(i_m >= 3 && i_m + 3 < pendolo.size()){

            min_ok =
            (pendolo.at(i_m-1) >= pendolo.at(i_m)) &&
            (pendolo.at(i_m-2) >= pendolo.at(i_m-1)) &&
            (pendolo.at(i_m-3) >= pendolo.at(i_m-2)) &&

            (pendolo.at(i_m) <= pendolo.at(i_m+1)) &&
            (pendolo.at(i_m+1) <= pendolo.at(i_m+2)) &&
            (pendolo.at(i_m+2) <= pendolo.at(i_m+3));
        }

        if(max_ok && min_ok){
            ofile << M << " " << m << endl;
        }   


        ofile<<tempo.at(i_M)<<" "<<M<<" "<<tempo.at(i_m)<<" "<<m<<endl;

        t_0+=T;
    }

    ofile.close();
}

    return 0;
}