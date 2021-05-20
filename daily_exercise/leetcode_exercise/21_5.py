"""
218
两种方法：扫描线法和分治法
参考链接：https://coordinate.blog.csdn.net/article/details/102757308
方法一：扫描线法
首先要找到关键数据，转折点要么是左坐标和右坐标
因此对左坐标和右坐标进行排序，然后维护一个小根堆
小根堆中储存的应该是高度和右端点，因为右端点会影响其余的坐标的位置
扫描到当前建筑的时候，如果其左坐标比当前最高高度的有坐标大：
那么说明后面的建筑不会影响前面的建筑，堆中的建筑可以去掉（因为其右端点也会入堆，所以可以直接删掉）
否则要入堆，因为其会影响之后建筑出现转折
每次扫描一个建筑，如果出现不同的高度，那么就需要将其加入结果中
"""
class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        #方法一：扫描线法
        #首先获得关键点
        """
        points = [(L,-H,R) for L,R,H in buildings]+[(R,0,0) for R in set(r for _,r,_ in buildings)]
        points.sort()
        heap,res = [(0,float('inf'))],[[0,0]]
        for l,h,r in points:
            while heap[0][1] <= l:
                heapq.heappop(heap)
            if h:
                heapq.heappush(heap,(h,r))
            if res[-1][1] != -heap[0][0]:
                res += [[l,-heap[0][0]]]
        return res[1:]
        """
        #方法二：分治
        if not buildings:
            return []
        if len(buildings) == 1:
            return [[buildings[0][0],buildings[0][2]],[buildings[0][1],0]]
        mid = len(buildings)//2
        left = self.getSkyline(buildings[:mid])
        right = self.getSkyline(buildings[mid:])
        return self.merge(left,right)

    def merge(self,left,right):
        lh = rh = l = r = 0
        res = []
        while l < len(left) and r < len(right):
            if left[l][0] < right[r][0]:
                cp = [left[l][0],max(left[l][1],rh)]
                lh = left[l][1]
                l += 1
            elif left[l][0] > right[r][0]:
                cp = [right[r][0],max(right[r][1],lh)]
                rh = right[r][1]
                r += 1
            else:
                cp = [left[l][0],max(left[l][1],right[r][1])]
                lh,rh = left[l][1],right[r][1]
                l += 1
                r += 1
            if len(res) == 0 or res[-1][1] != cp[1]:
                res.append(cp)
        res += left[l:] +  right[r:]
        return res
