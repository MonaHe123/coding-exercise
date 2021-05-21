#include<iostream>
#include<deque>
#include<queue>
#include<vector>
#include<algorithm>
#include<functional>
#include<math.h>
using namespace std;

//239-双端队列
class Solution {
public:
//关键是每次加入一个元素和删除
//在这过程中会导致最大值的改变
//方法一：使用大根堆，窗口右移的时候就加入一个元素
//为了保证目前的堆最大是在窗口范围内，堆中的元素需要包括index信息，当最大值的index不在窗口范围内就删除
//C++中优先队列默认是大根堆
/*
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        priority_queue<pair<int,int>> heap;
        int n = nums.size();
        vector<int> res;
        //首先加入k个元素
        for(int i = 0;i<k;++i)
        {
            heap.emplace(nums[i],i);
        }
        res.push_back(heap.top().first);
        //窗口开始移动
        for(int i = k;i<n;++i)
        {
            //加入一个新的元素
            heap.emplace(nums[i],i);
            //将不符合的最大值删除
            while(heap.top().second<=i-k)
            heap.pop();
            res.push_back(heap.top().first);
        }
        return res;
    }
    */

    //方法二：使用双端队列queue
    //思路为：将数据的index进入队列，如果队尾的元素的值比新进的小，那么其肯定不是窗口最大的，那么直接出队
    //否则不出队，那么队列左边是当前窗口内最大的，但是也需要对队首的元素进行是否在窗口中的判断
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        deque<int> q;
        vector<int> res;
        int n = nums.size();
        //首先对k个元素进行操作
        for(int i = 0;i<k;++i)
        {
            while(!q.empty() && nums[i]>=nums[q.back()])
            q.pop_back();
            q.push_back(i);
        }
        res.push_back(nums[q.front()]);
        for(int i = k;i<n;++i)
        {
            while(!q.empty()&&nums[i]>=nums[q.back()])
            q.pop_back();
            q.push_back(i);
            while(q.front()<=i-k)
            q.pop_front();
            res.push_back(nums[q.front()]);
        }
        return res;
    }
};


//218-堆、分治
class Solution {
public:
//两种方法：方法一扫描线法，利用了堆；方法二分治法
//方法一：首先关键点是（left_index,height)和(right_index,0)
//按照left_index从小到大排序，高度从高到底，因为建筑的右端点会影响后面建筑的范围，所以要将其储存在
//堆中，每遇到一个新的建筑的时候进行判断是否有新的转折点
//如果没有交集，那么当前的高度不会影响后面的建筑，直接出堆
//注意点：右边的坐标加入应该是唯一的，其次set的排序当坐标相等的时候高度高的排在前

/*
    vector<vector<int>> getSkyline(vector<vector<int>>& buildings) {
        //首先获得关键点，按照优先级index和height进行排序
        set<vector<int>> points;
        int n = buildings.size();
        vector<vector<int>>res;
        for(int i = 0;i<n;++i)
        {
        //左边的坐标相等的时候高度应该从大到小排序
        points.insert({buildings[i][0],-buildings[i][2],buildings[i][1]});
        points.insert({buildings[i][1],0,0});
        }
        //首先去掉重复的右坐标
        n = points.size();
        priority_queue<pair<int,float>> heap;//大根堆
        //这样可以保证堆不为空
        heap.emplace(0,FLT_MAX);
        res.push_back({0,0});
        for(auto it = points.begin();it!=points.end();++it)
        {
            while(heap.top().second<=(*it)[0])
            heap.pop();
            if((*it)[1])
            heap.emplace(-(*it)[1],(*it)[2]);
            //遇到不同的高度的时候才进行结果的保存
            //这里只有当堆中只剩下最后(0,无穷大)的时候才会输出(r,0)
            if(res.back()[1]!=heap.top().first)
            res.push_back({(*it)[0],int(heap.top().first)});
        }
        return vector(res.begin()+1,res.end());
    }*/

    //方法二：使用分治的方法
    //考虑两个建筑进行合并，考虑左边和右边的关键点进行合并
    //当前的考虑的点的高度是已知的，但是这并不是目前已经合并的暂时结果的最新高度
    //合并是左右交替的，所以需要记录合并过程中左右的高度，选择左边时，需考虑右边保存的高度
    //选择右边时，需要考虑左边保存的高度
    vector<vector<int>> merge(vector<vector<int>> left,vector<vector<int>> right)
    {
        int l = 0;
        int r = 0;
        int rh = 0;
        int lh = 0;
        vector<vector<int>> res;
        vector<int> tmp(2);
        while(l<left.size() && r<right.size())
        {
            if(left[l][0]<right[r][0])
            {
                tmp[0]=left[l][0];
                tmp[1]=max(left[l][1],rh);
                lh = left[l][1];
                l += 1;
            }
            else if(left[l][0]>right[r][0])
            {
                tmp[0]=right[r][0];
                tmp[1]=max(right[r][1],lh);
                rh = right[r][1];
                r += 1;
            }
            else
            {
                tmp[0]= left[l][0];
                tmp[1]=max(left[l][1],right[r][1]);
                lh = left[l][1];
                rh = right[r][1];
                l += 1;
                r += 1;
            }
            //合并的时候需要将剩余的部分加入
            if(res.empty() || res.back()[1]!=tmp[1])
            res.push_back(tmp);
        }

        while(l<left.size())
        {
            res.push_back({left[l][0],left[l][1]});
            l += 1;
        }
        while(r<right.size())
        {
            res.push_back({right[r][0],right[r][1]});
            r += 1;
        }
        return res;
    }
    vector<vector<int>> getSkyline(vector<vector<int>>& buildings) {
        vector<vector<int>> res;
        int n  = buildings.size();
        if(n==0)
        return {};
        if(n==1)
        {
            res.push_back({buildings[0][0],buildings[0][2]});
            res.push_back({buildings[0][1],0});
            return res;
        }
        int mid = buildings.size()/2;
        //分治，首先分开
        vector<vector<int>> tmp1 = vector(buildings.begin(),buildings.begin()+mid);
        vector<vector<int>> tmp2 = vector(buildings.begin()+mid,buildings.end());
        vector<vector<int>> left = getSkyline(tmp1);
        vector<vector<int>> right = getSkyline(tmp2);
        //然后合并
        return merge(left,right);
    }
};