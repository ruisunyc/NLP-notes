1. #### [200. 岛屿数量](https://leetcode-cn.com/problems/number-of-islands/)

   ```python
#深度优先搜索
   class Solution:
       def numIslands(self, grid: List[List[str]]) -> int:
           m,n=len(grid),len(grid[0])        
           def dfs(i,j):
               grid[i][j]='0'
               for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                   x,y=i+dx,j+dy
                   if 0<=x<m and 0<=y<n and grid[x][y]=='1':
                       dfs(x,y)
           ans = 0
           for i in range(m):
               for j in range(n):
                   if grid[i][j]=='1':
                       ans+=1
                       dfs(i,j)
           return ans
   ```
   
   ```python
    # 广度优先搜索
   class Solution:
       def numIslands(self, grid: List[List[str]]) -> int:
           m,n=len(grid),len(grid[0])  
           def bfs(i,j):
               q = deque([(i,j)])
               grid[i][j]='0'
               while q:
                   i,j = q.popleft()
                   for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                       x,y=i+dx,j+dy
                       if 0<=x<m and 0<=y<n and grid[x][y]=='1':
                           q.append((x,y))
                           grid[x][y]='0' #避免重复添加坐标，如果把这句放到for循环之前，则需要额外一个集合去重添加的坐标
           ans = 0
           for i in range(m):
               for j in range(n):
                   if grid[i][j]=='1':
                       ans+=1
                       bfs(i,j)
           return ans
   ```
   
   ```python
   class DSU:
       #并查集
       def __init__(self):
           self.f = {}
       def find(self,x):
           self.f.setdefault(x,x)
           if self.f[x]!=x:
               self.f[x] = self.find(self.f[x])
           return self.f[x]
       def unio(self,x,y):
           fx = self.find(x)
           fy = self.find(y)
           if fx!=fy:
               self.f[fx] = fy
   class Solution:    
       def numIslands(self, grid: List[List[str]]) -> int:
           dsu = DSU()
           m,n=len(grid),len(grid[0])        
           for i in range(m):
               for j in range(n): 
                   if grid[i][j]=='1':                  
                       for dx,dy in ((1,0),(0,1)):
                           x,y=i+dx,j+dy
                           if 0<=x<m and 0<=y<n and grid[x][y]=='1':
                               dsu.unio(x*n+y,i*n+j)
           res = set()
           for i in range(m):
               for j in range(n):
                   if grid[i][j]=='1':                   
                       res.add(dsu.find(i*n+j))
           return len(res)
   ```
   
   
   
2. #### [37. 解数独](https://leetcode-cn.com/problems/sudoku-solver/)

   要点:集合交集&

   ```python
   class Solution:
       def solveSudoku(self, board: List[List[str]]) -> None:
           """
           Do not return anything, modify board in-place instead.
           """
   
           row = [set(map(str,[i for i in range(1,10)])) for _ in range(9)]
           col = [set(map(str,[i for i in range(1,10)])) for _ in range(9)]
           block = [set(map(str,[i for i in range(1,10)])) for _ in range(9)]
           ans = []
           for i in range(9):
               for j in range(9):
                   cur = board[i][j]
                   if cur!='.':
                       row[i].remove(cur)
                       col[j].remove(cur)
                       block[i//3*3+j//3].remove(cur)
                   else:
                       ans.append([i,j])        
           def dfs(i):
               if i==len(ans):return True
               x,y = ans[i]
               for one in row[x] & col[y] & block[x//3*3+y//3]:
                   board[x][y] = one
                   row[x].remove(one)
                   col[y].remove(one)
                   block[x//3*3+y//3].remove(one)
                   if dfs(i+1):return True
                   row[x].add(one)
                   col[y].add(one)
                   block[x//3*3+y//3].add(one)
           dfs(0)
   ```

3. #### [450. 删除二叉搜索树中的节点](https://leetcode-cn.com/problems/delete-node-in-a-bst/)

      ```python
      # class TreeNode:
      #     def __init__(self, val=0, left=None, right=None):
      #         self.val = val
      #         self.left = left
      #         self.right = right
      class Solution:
          def deleteNode(self, root: TreeNode, key: int) -> TreeNode:
              #找到右子树的最左节点 放到上面就行
              if not root:return 
              if root.val==key:
                  if not root.left:return root.right
                  if not root.right:return root.left
                  right = root.right
                  while right.left:
                      right = right.left
                  right.left = root.left
                  return root.right            
              elif root.val>key:
                  root.left = self.deleteNode(root.left,key)
              else:
                  root.right = self.deleteNode(root.right,key)
              return root      
      ```

4. #### [863. 二叉树中所有距离为 K 的结点](https://leetcode-cn.com/problems/all-nodes-distance-k-in-binary-tree/)

      ```python
      class Solution:
          def distanceK(self, root: TreeNode, target: TreeNode, K: int) -> List[int]:
              #创建父节点给每个节点，然后BFS孩子及父节点，用集合去重访问，开始从目标节点即可
              def dfs(root,par = None):
                  if not root:return
                  root.parent = par
                  dfs(root.left,root)
                  dfs(root.right,root)
              dfs(root)
              q = deque([(target,0)])
              tmp = []
              seen = {target}
              while q:
                  if q[0][1]==K:
                      tmp = [node.val for node,dis in q]   
                      break             
                  cur,dis = q.popleft()           
                  for i in [cur.left,cur.right,cur.parent]:
                      if i and i not in seen:
                          seen.add(i)
                          q.append((i,dis+1))               
              return tmp
      ```

5. #### [297. 二叉树的序列化与反序列化](https://leetcode-cn.com/problems/serialize-and-deserialize-binary-tree/)

      ```python
      class Codec:
      	#BFS,层序遍历
          def serialize(self, root):
              """Encodes a tree to a single string.
              
              :type root: TreeNode
              :rtype: str
              """      
              q  = deque([root])
              ans=''
              while q:
                  node = q.popleft()            
                  if node is None:
                      ans+='null,'
                  else:                
                      ans+=str(node.val)+','
                      q.append(node.left)
                      q.append(node.right)
              return ans[:-1]
              
          def deserialize(self, data):
              """Decodes your encoded data to tree.
              
              :type data: str
              :rtype: TreeNode
              """
              if data=='null':return
              datas = deque(data.split(','))
              root = TreeNode(datas[0])
              i=1
              q = deque([root])
              while q:
                  node = q.popleft()
                  if datas[i]!='null':
                      node.left = TreeNode(datas[i])
                      q.append(node.left)
                  i+=1            
                  if datas[i]!='null':
                      node.right = TreeNode(datas[i])
                      q.append(node.right)
                  i+=1
              return root
      ```

      ```python
      class Codec:
      	#DFS，栈
          def serialize(self, root):
              """Encodes a tree to a single string.
              
              :type root: TreeNode
              :rtype: str
              """
              if not root:return 'null'
              return self.serialize(root.right)+','+self.serialize(root.left)+','+str(root.val)
      
          def deserialize(self, data):
              """Decodes your encoded data to tree.
              
              :type data: str
              :rtype: TreeNode
              """
              roots = data.split(',')
              def dfs(roots):
                  cur = roots.pop()
                  if cur=='null':return
                  root = TreeNode(cur)
                  root.left = dfs(roots)   
                  root.right = dfs(roots)                     
                  return root
              return dfs(roots)
      ```

      ```python
      class Codec:
      
          def serialize(self, root):
              """Encodes a tree to a single string.
              
              :type root: TreeNode
              :rtype: str
              """
              if not root:return 'null'
              
              return str(root.val)+','+self.serialize(root.left)+','+self.serialize(root.right)
              
      
          def deserialize(self, data):
              """Decodes your encoded data to tree.
              
              :type data: str
              :rtype: TreeNode
              """
              cur = deque(data.split(','))
              def dfs(cur):
                  v = cur.popleft()
                  if v=='null':return 
                  root = TreeNode(v)
                  root.left = dfs(cur)
                  root.right = dfs(cur)
                  return root
              return dfs(cur)
      ```

6. #### [449. 序列化和反序列化二叉搜索树](https://leetcode-cn.com/problems/serialize-and-deserialize-bst/)

      ```python
      class Codec:
          def serialize(self,root:TreeNode)->str:
              def dfs(root):
                  if not root:return []
                  return dfs(root.left)+dfs(root.right)+[root.val]
              return ','.join(map(str,dfs(root)))
          def deserialize(self,data:str)->TreeNode:
              if not data:return
              data = list(map(int,data.split(',')))
              def dfs(low=float('-inf'),high = float('inf')):
                  if not data or data[-1]<low or data[-1]>high:return 
                  cur = data.pop()
                  root = TreeNode(cur)            
                  root.right = dfs(cur,high)
                  root.left = dfs(low,cur)
                  return root
              return dfs()
      ```

      

7. #### [1155. 掷骰子的N种方法](https://leetcode-cn.com/problems/number-of-dice-rolls-with-target-sum/)

      ```python
      #记忆化搜索
      class Solution:
          @lru_cache(None)
          def numRollsToTarget(self, d: int, f: int, target: int) -> int: 
              if d==1:
                  if f>=target:return 1
                  return 0
              count=0
              for i in range(1,f+1):
                  if i<target:
                      count += self.numRollsToTarget(d-1,f,target-i)
              return count%(10**9 + 7)
      ```

8. #### [124. 二叉树中的最大路径和](https://leetcode-cn.com/problems/binary-tree-maximum-path-sum/)

      ```python
      class Solution:
          def maxPathSum(self,root):
              self.ans = float('-inf')
              def dfs(root):
                  if not root:return 0
                  left = max(0,dfs(root.left))
                  right =max(0,dfs(root.right))
                  self.ans = max(self.ans,left+right+root.val)
                  return root.val+max(left,right)
             	dfs(root)
              return self.ans
                  
      ```

9. #### [103. 二叉树的锯齿形层序遍历](https://leetcode-cn.com/problems/binary-tree-zigzag-level-order-traversal/)

      ```python
      class Solution:
          def zigzagLevelOrder(self, root: TreeNode) -> List[List[int]]:
              if not root:return []
              height = 0
              q = collections.deque([root])
              ans = []
              while q:
                  height+=1
                  tmp =[]
                  for i in range(len(q)):
                      cur = q.popleft()
                      if height&1:
                          tmp.append(cur.val)
                      else:
                          tmp=[cur.val]+tmp
                      if cur.left:
                          q.append(cur.left)
                      if cur.right:
                          q.append(cur.right)
                  ans.append(tmp)            
              return ans
      ```

      ```python
      class Solution:
          def zigzagLevelOrder(self, root: TreeNode) -> List[List[int]]:    
              ans = []
              def dfs(root,depth):
                  if not root:return 0
                  if len(ans)==depth:
                      ans.append([])
                  if depth&1:
                      ans[depth]=[root.val]+ans[depth]
                  else:
                      ans[depth].append(root.val)
                  dfs(root.left,depth+1)
                  dfs(root.right,depth+1)
              dfs(root,0)
              return ans
      ```

10. #### [129. 求根到叶子节点数字之和](https://leetcode-cn.com/problems/sum-root-to-leaf-numbers/)

      ```python
      #DFS
      class Soloution:
          def sumNumbers(self,root:TreeNode)->int: #DFS
              def dfs(root,cur):
                  if not root:return 0
                  cur=cur*10+root.val
                  if not root.left and not root.right:
                      return cur
                  return dfs(root.left,cur)+dfs(root.right,cur)
          	return dfs(root,0)
      ```

      ```python
      #BFS
      class Solution:
          def sumNumbers(self,root:TreeNode)->int:
              ans = 0
              if not root:return 0
              q = collections.deque([(root,root.val)])
              while q:
                  cur,val = q.popleft()
                  if not cur.left and not cur.right:ans+=val
                  if cur.left:
                      q.append((cur.left,val*10+cur.left.val))
                  if cur.right:
                      q.append((cur.right,val*10+cur.right.val))
              return ans
      ```

      
