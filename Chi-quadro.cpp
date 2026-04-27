#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cmath>

using namespace std;
 
double chi (vector<double>, vector<double>, double);

int main(){

    //definisco gli oggetti
    vector<double>y;
    vector<double>s;

    double y_i, s_i, n, lambda;
    string l;

    //richiesta da terminale
    cout<<"inserire il valore atteso"<<endl;
    cin>>n;

    //lettura da file
    string ifilename="eta.txt";
    ifstream ifile(ifilename);

     while(getline(ifile, l)){
        
        if(l[0]=='#') continue;
        if(l.empty()) continue;
        
        stringstream st(l);
        st>>y_i>>s_i;
        
        y.push_back(y_i);
        s.push_back(s_i);
    }

    cout<<"valore della variabile chi-quadro: X="<<chi(y, s, n)<<endl;
    cout<<"i contributi al chi-quadro sono:"<<endl;

    for(int i=0; i<y.size(); ++i){

        lambda=pow(y.at(i)-n, 2)/pow(s.at(i), 2);
        cout<<lambda<<endl;

        lambda=0;
    }
    

    return 0;
}

double chi (vector<double>x, vector<double>s_x, double n){
    
    double X;
    double lambda;
    vector<double>contributi;
    
    for(int i=0; i<x.size(); ++i){

        X+=pow(x.at(i)-n, 2)/pow(s_x.at(i), 2);
    };

return X; 
}