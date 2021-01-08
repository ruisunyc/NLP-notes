1. #### [146. LRU 缓存机制](https://leetcode-cn.com/problems/lru-cache/)

   一种数据结构:collections.OrderedDict()

   两个方法:move_to_end(last=True),popitem(last=False)

   ```python
   class LRUCache:
   
       def __init__(self, capacity: int):
           self.d = collections.OrderedDict()
           self.capacity = capacity
   
       def get(self, key: int) -> int:
           if key not in self.d:return -1
           self.d.move_to_end(key,last = True)
           return self.d[key]
   
       def put(self, key: int, value: int) -> None:
           if len(self.d)>=self.capacity and key not in self.d:
               self.d.popitem(last=False)
           self.d[key] = value
           self.d.move_to_end(key,last=True)
   ```

   

   