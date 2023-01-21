#include <iostream>
#include <thread>
#include <cstdlib>
#include <unistd.h>
#include <mutex>
#include <queue>

using namespace std;


std::mutex mtx;
queue<int> img_data;
queue<int> result_data;
int control = 0;

void read1(){
    for (int i = 1; i<20 ; i++){
        img_data.push(i);
        //cout <<" Read : "<< i << endl;
        sleep(1);
    }
    control = 0;
}
void filter1(){
    while(control){
        mtx.lock();
        if (img_data.empty()){mtx.unlock();continue;}
        int temp = img_data.front();
        img_data.pop();
        mtx.unlock();
        // Filter
        sleep(2);
        result_data.push(temp);

    }
}
void filter2(){
    while(control){
        mtx.lock();
        if (img_data.empty()){mtx.unlock();continue;}
        int temp = img_data.front();
        img_data.pop();
        mtx.unlock();
        // Filter
        sleep(2);
        result_data.push(temp);
    }
}

void filter3(){
    while(control){
        mtx.lock();
        if (img_data.empty()){mtx.unlock();continue;}
        int temp = img_data.front();
        img_data.pop();
        mtx.unlock();
        // Filter
        sleep(2);
        result_data.push(temp);
    }
}


void show1(){
    while (control) {
        if (result_data.empty()){continue;}
		cout << "Show "<< result_data.front()<<endl;
		result_data.pop();
		sleep(1);
	}
}


int main(){


    control=1;
    thread th1(read1);
    thread th2(filter1);
    thread th3(filter2);
    //thread th4(filter3);
    thread th5(show1);

    th1.join();
    th2.join();
    th3.join();
    //th4.join();
    th5.join();

	return 0;
}

