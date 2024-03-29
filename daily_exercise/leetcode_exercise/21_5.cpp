#include<iostream>
#include<deque>
#include<queue>
#include<vector>
#include<algorithm>
#include<functional>
#include<math.h>
#include<string>
#include<cstring>
#include<unordered_map>
#include<unordered_set>
#include<map>
#include<set>
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


//1:hash表
class Solution {
public:
//比较直接的做法是首先进行排序，然后二分查找相应的值
//但是如果可以根据差值找到相应的值更直接，但是如果直接使用数组并且value作为index，那么会很浪费空间
//使用map，key为数值，value为index
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int,int> hash;
        vector<int> ans;
        int n = nums.size();
        for(int i = 0;i<n;++i)
        {
            int num  = nums[i];
            auto pos = hash.find(target-num);
            if(pos == hash.end())
            {
                hash[num] = i;
            }
            else
            {
                ans.push_back(pos->second);
                ans.push_back(i);
                break;
            }
        }
        return ans;
    }
};

//128:使用set进行去重，并且hash表在O（1）时间内进行查找
class Solution {
public:
//遍历每个数作为开始，看连续的数是否在在hash表中
//并且不要重复判断
    int longestConsecutive(vector<int>& nums) {
        unordered_set<int> s;
        int n = nums.size();
        //因为要找连续的，所以先除掉连续的数字
        for(int i = 0;i<n;++i)
        s.insert(nums[i]);
        int max_len = 0;
        int cur_len = 0;
        int cur_num = 0;
        for(const int& num:s)
        {
            //如果之前的那个数已经作为开始进行计算了，那么就直接跳过这个数字
            if(!s.count(num-1))
            {
                cur_len = 1;
                cur_num = num;
            while(s.count(cur_num+1))
            {
                cur_num += 1;
                cur_len += 1;
            }
            max_len = max(max_len,cur_len);
            }
        }
        return max_len;
    }
};

//149:hash表+数学知识
class Solution {
public:
//关键知识：一个点加上斜率可以确定一条直线
//遍历每个点，以该点作为中心点，然后考虑所有可能的斜率，为避免所有重复的考虑，只需要考虑之后的点
//需要注意的是点可能有重复的，还有斜率不存在的情况
    int maxPoints(vector<vector<int>>& points) {
        unordered_map<double,int> hash;//<斜率，点数>
        int max_num = 0;
        int same = 0;
        int same_x = 0;
        int n = points.size();
        for(int i = 0;i<n;++i)
        {
            same = 1;
            same_x = 1;
            for(int j = i+1;j<n;++j)
            {
                //斜率不存在的情况
                if(points[j][0]==points[i][0])
                {
                    same_x ++;
                    //重复点的情况
                    if(points[j][1]==points[i][1])
                    same++;
                }
                //考虑不同的斜率
                else
                {
                    double dx = points[i][0]-points[j][0];
                    double dy = points[i][1]-points[j][1];
                    hash[dy/dx]++;
                }
            }
            max_num = max(max_num,same_x);
            for(auto tmp:hash)
            max_num = max(max_num,same+tmp.second);
            //换点的时候要清空
            hash.clear();
        }
        return max_num;
    }
};


//332：多重集合和映射
class Solution {
public:
//多重集合和映射
//使用hash表储存从起点可以到达的位置
//要获得行程，那么从最后的终点出发，即没有可去地方的出发，倒序即利用栈
//然后再倒序
    vector<string> findItinerary(vector<vector<string>>& tickets) {
        unordered_map<string,multiset<string>>hash;
        vector<string> ans;
        int n = tickets.size();
        if(n==0)
        return {};
        //每个起点可以到达的位置
        for(int i = 0;i<n;++i)
        hash[tickets[i][0]].insert(tickets[i][1]);
        stack<string> s;
        s.push("JFK");
        while(!s.empty())
        {
            string cur = s.top();
            if(hash[cur].empty())
            {
            ans.push_back(cur);
            s.pop();
            }
            else
            {
                //入栈
                s.push(*hash[cur].begin());
                //并删除
                hash[cur].erase(hash[cur].begin());
            }
        }
        reverse(ans.begin(),ans.end());
        return ans;
    }
};

//303:前缀和
//利用前缀数组进行求和
class NumArray {
    //前缀数组的使用
    //vector的函数partial_sum计算所有前缀的和
    //如果psum[i]储存的是0到i的数字的和
    //那么i到j的和为：psum[j]-psum[i]+num[i]
    //如果psum[i]为0到i-1的前缀和，那么i到j的和为：psum[j+1]-psum[i]
    vector<int> psum;//前缀和数组
public:
    NumArray(vector<int>& nums):psum(nums.size()+1,0){
        partial_sum(nums.begin(),nums.end(),psum.begin()+1);
    }
    
    int sumRange(int left, int right) {
        return psum[right+1]-psum[left];

    }
};

/**
 * Your NumArray object will be instantiated and called as such:
 * NumArray* obj = new NumArray(nums);
 * int param_1 = obj->sumRange(left,right);
 */


//304：积分图的使用
class NumMatrix {
    //数据预处理，建立积分图
    vector<vector<int>> integral;
public:
    NumMatrix(vector<vector<int>>& matrix) {
        //动态规划建立积分图
        int m = matrix.size();
        int n;
        if(m>0)
        n = matrix[0].size();
        integral = vector<vector<int>>(m+1,vector<int>(n+1,0));
        for(int i = 1;i<=m;++i)
        for(int j = 1;j<=n;++j)
        {
            integral[i][j] = integral[i-1][j]+integral[i][j-1]-integral[i-1][j-1]+matrix[i-1][j-1];
        }
    }
    
    int sumRegion(int row1, int col1, int row2, int col2) {
        return integral[row2+1][col2+1]-integral[row2+1][col1]-integral[row1][col2+1]+integral[row1][col1];
    }
};

/**
 * Your NumMatrix object will be instantiated and called as such:
 * NumMatrix* obj = new NumMatrix(matrix);
 * int param_1 = obj->sumRegion(row1,col1,row2,col2);
 */


//560：前缀和的使用
class Solution {
public:
//前缀和的使用，假设从0开始的前缀和为psum，其数量为hash[psum]
//那么和为k的数量为hash[psum-k]
    int subarraySum(vector<int>& nums, int k) {
        unordered_map<int,int> hash;
        int n = nums.size();
        int psum = 0;
        int cnt = 0;
        hash[0] = 1;
        //下面的实现保证了k=0的时候不重复计数，但是也要保证num[0]=k成立，所以hash[0]=1
        for(int i = 0;i<n;++i)
        {
            psum += nums[i];
            //++hash[psum];
            //这里的顺序很重要
            //当k=0的时候，第一次更新的时候，并且连续和并不等于0，这里cnt加上的是hash[psum]
            //此时应该加上0，所以先更新cnt，然后再更新hash，并且初始化的时候为1
            cnt += hash[psum-k];
            ++hash[psum];
        }
        return cnt;
    }
};

//566：数组操作的基本练习
class Solution {
public:
    vector<vector<int>> matrixReshape(vector<vector<int>>& mat, int r, int c) {
        //首先判断能否转化，不能则直接返回空
        //如果可以转化，那么遍历第一个矩阵同时对第二个矩阵进行填充
        int m = mat.size();
        vector<vector<int>> res;
        int n;
        if(m==0)
        return res;
        n = mat[0].size();
        if(m*n!=r*c)
        return mat;
        res = vector<vector<int>>(r,vector<int>(c));
        int k1 = 0;
        int k2 = 0;
        for(int i = 0;i<m;++i)
        for(int j = 0;j<n;++j)
        {
            //填充完一行
            if(k2==c)
            {
                k1++;
                k2 = 0;
            }
            res[k1][k2] = mat[i][j];
            k2++;
        }
        return res;
    }
};


//225：使用队列实现栈的功能
//思路：使用一个队列作为中间的过度
class MyStack {
public:
queue<int> q1;
queue<int> q2;
//用两个队列模拟一个栈：将一个队列作为中间的过度
//两个队列q1和q2，如果q1中有元素那么先将q1中的全部加入到q2中，然后将加入的元素加入q1中，再将q2中加入q1
    /** Initialize your data structure here. */
    MyStack() {
        //这里是初始化，公共结构的声明要在类的申明处
        //queue<int> q1;
        //queue<int> q2;
    }
    
    /** Push element x onto stack. */
    void push(int x) {
        while(!q1.empty())
        {
            int tmp = q1.front();
            q2.push(tmp);
            q1.pop();
        }
        q1.push(x);
        while(!q2.empty())
        {
            int tmp = q2.front();
            q1.push(tmp);
            q2.pop();
        }
    }
    
    /** Removes the element on top of the stack and returns that element. */
    int pop() {
        int res = q1.front();
        q1.pop();
        return res;
    }
    
    /** Get the top element. */
    int top() {
        int res = q1.front();
        return res;
    }
    
    /** Returns whether the stack is empty. */
    bool empty() {
        if(q1.empty())
        return true;
        else
        return false;
    }
};

/**
 * Your MyStack object will be instantiated and called as such:
 * MyStack* obj = new MyStack();
 * obj->push(x);
 * int param_2 = obj->pop();
 * int param_3 = obj->top();
 * bool param_4 = obj->empty();
 */


//503:单调栈+循环数组
class Solution {
public:
//首先直接想到的是遍历寻找每个数的后面找到比其大的数字
//换一种思路，固定每个数，看这个数是哪些数刚好比这个数小
//因为是最近的原则，也就是说固定每个数的时候应该考虑是否为离其最近的数字的大数
//index靠后的先判断
//所以用栈储存index
//如果当前的数大于栈顶的数就弹栈找到符合条件的数
//单调栈+循环数组
    vector<int> nextGreaterElements(vector<int>& nums) {
        int n = nums.size();
        //初始化为-1，因为当没有符合的数字的时候返回的是-1
        vector<int> res(n,-1);
        stack<int> s;
        if(n==0)
        return res;
        for(int i = 0;i<2*n-1;++i)
        {
            while(!s.empty() && nums[s.top()]<nums[i%n])
            {
                res[s.top()] = nums[i%n];
                s.pop();
            }
            s.push(i%n);
        }
        return res;
    }
};


//217：hash数据结构的使用，set不能加入重复的数字
class Solution {
public:
//方法一：进行排序，时间复杂度为o(nlogn)
//方法二：使用set判断，因为set是基于hash表，所以判断插入元素是否存在的时间复杂度为o(1)
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> s;
        int n = nums.size();
        for(int i = 0;i<n;++i)
        {
            if(s.find(nums[i])!=s.end())
            return true;
            s.insert(nums[i]);
        }
        return false;
    }
};


//594:hash表的应用
class Solution {
public:
//注意题目求的是子序列，是可以对元素进行删除的
//方法一：遍历每个子序列的最小值，如果是x，那么再看x+1在序列中有多少个，num(x)+num(x+!)就是以x
//作为Min的最长的子序列，这里需要对原数组和hash表都遍历一遍
//方法二：遍历原数组一遍，对于x，需要对x-1和x+1进行数量判断，当遍历完成也就得到最长的子序列
//关键是对x-1、x、x+1都要判断
/*
    int findLHS(vector<int>& nums) {
//方法一：两次遍历
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
        if(hash.count(tmp.first+1))
        res = max(res,tmp.second+hash[tmp.first+1]);
    }
    return res;
    }*/

    //方法二：只遍历一遍
    int findLHS(vector<int>& nums)
    {
        int n = nums.size();
        int res = 0;
        unordered_map<int,int> hash;
        for(int i = 0;i<n;++i)
        {
            if(hash.count(nums[i]))
            hash[nums[i]]++;
            else
            hash[nums[i]] = 1;
            //对x-1判断
            //首先要判断是否存在
            if(hash.count(nums[i]-1))
            res = max(res,hash[nums[i]]+hash[nums[i]-1]);
            //对x+1的判断
            if(hash.count(nums[i]+1))
            res = max(res,hash[nums[i]]+hash[nums[i]+1]);
        }
        return res;
    }
};


//697：hash表的应用
class Solution {
public:
//储存每个数字出现的次数和出现的最小和最大jindex
//使用hash数据结构
    int findShortestSubArray(vector<int>& nums) {
        unordered_map<int,vector<int>> hash;
        int n = nums.size();
        for(int i = 0;i<n;++i)
        {
            if(hash.count(nums[i]))
            {
                hash[nums[i]][0]++;
                hash[nums[i]][2]= i; 
            }
            else
            {
                //因为这里已经初始化vector为3，所以上面可以直接用下标
                hash[nums[i]] = {1,i,i};
            }
        }
        //遍历hash数组得到最多次数和最短的长度
        int maxnum =0;
        int minlen = 0;
        for(auto& [_,vec]:hash)
        {
            if(vec[0]>maxnum)
            {
                maxnum = vec[0];
                minlen = vec[2]-vec[1]+1;
            }
            else if(vec[0]==maxnum)
            {
                minlen = min(minlen,vec[2]-vec[1]+1);
            }
        }
        return minlen;
    }
};