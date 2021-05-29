#include<iostream>
#include<string>
#include<string.h>
#include<vector>
#include<unordered_map>
#include<unordered_set>
using namespace std;
int main()
{
    vector<int> nums = {1,1,1,1,1};
    int n = nums.size();
    unordered_map<int,int> hash;
    //遍历原来的数组
    for(int i = 0;i<n;++i)
    {
        if(hash.count(nums[i]))
        hash[nums[i]]++;
        else
        {
            hash[nums[i]] = 1;
        }
    }
    //遍历hash表
    int res = 0;
    for(auto & tmp:hash)
    {
        cout<<tmp.first<<" "<<tmp.second<<endl;
        if(hash.count(tmp.first+1))
        res = max(res,tmp.second+hash[tmp.first+1]);
    }
    cout<<res<<endl;
}