#include<iostream>
#include<string>
#include<cstring>
#include<algorithm>
#include<vector>
#include<set>
using namespace std;
int main()
{
    set<vector<int>> s;
    s.insert({2,0,0});
    s.insert({1,0,0});
    for(auto i = s.begin();i!=s.end();++i)
    cout<<(*i)[0]<<endl;
    return 0;

}