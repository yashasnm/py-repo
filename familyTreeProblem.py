class Node(object):
    def __init__(self,val):
        self.val = val
        self.next = None

    def get_data(self):
        return self.val

    def set_data(self,val):
        self.val = val

    def get_next(self):
        return self.next

    def set_next(self,next):
        self.next = next


class LinkedList(object):

    def __init__(self,*values):
        self.count = len(values) -1
        self.head = Node(values[0])
        node = self.head
        for idx, val in enumerate(values):
            if idx == 0:
                continue
            else:
                tempnode = Node(val)
                node.set_next(tempnode)
                node = node.get_next()


    def get_count(self):
        return self.head

    def insert(self,data):
        new_node = Node(data)
        new_node.set_next(self.head)
        self.head = new_node
        self.count +=1

    def insert_at(self,idx,val):
        if idx > self.count +2:
            return

        if idx == 0:
            self.insert(val)
        else:
            tempIdx = 0
            node = self.head
            while tempIdx < idx -1:
                node = node.get_next()
                tempIdx += 1
            continuation = node.get_next()
            insertion = Node(val)
            node.set_next(insertion)
            node.get_next().set_next(continuation)
            self.count += 1

    def find(self,val):
        item = self.head
        while item != None:
            if item.get_data() == val:
                return item
            else:
                item = item.get_next()

        return None

    def deleteAt(self,idx):
        if idx > self.count+1:
            return
        if idx == 0:
            self.head = self.head.get_next()
        else:
            tempIdx = 0
            node = self.head
            while tempIdx < idx -1:
                node = node.get_next()
                tempIdx +=1
            node.set_next(node.get_next().get_next())
            self.count -= 1

    def dump_list(self):
        tempnode = self.head
        while (tempnode != None):
            print("Node: ",tempnode.get_data())
            tempnode = tempnode.get_next()


    def swap(self,idx_a,idx_b):
        if idx_a == idx_b:
            return
        elif idx_a > idx_b:
            idx_2,idx_1 = idx_a,idx_b
        else:
            idx_2,idx_1 = idx_b,idx_a

        node = self.head
        tempIdx = 0

        while tempIdx < idx_2:
            if tempIdx != idx_1:
                node = node.get_next()
                tempIdx += 1
            else:
                elem_1 = node.get_data()
                node = node.get_next()
                tempIdx += 1
        elem_2 = node.get_data()

        self.deleteAt(idx_1)
        self.deleteAt(idx_2-1)
        self.insert_at(idx_1,elem_2)
        self.insert_at(idx_2,elem_1)

    def move_min(self,sorted_idx):
        temp_idx = 0
        node = self.head
        selection = self.head.get_data()
        while temp_idx <= self.count:

            if temp_idx <= sorted_idx:
                node = node.get_next()
                temp_idx += 1

            elif temp_idx == sorted_idx +1:
                selection = node.get_data()
                selected_idx = temp_idx
                node = node.get_next()
                temp_idx += 1

            else:
                if node.get_data() < selection:
                    selection = node.get_data()
                    selected_idx = temp_idx
                try:
                    node = node.get_next()
                    temp_idx +=1
                except:
                    break

        self.deleteAt(selected_idx)
        self.insert_at(sorted_idx, selection)
        return sorted_idx + 1

    def selection_sort(self):
        """
        Note, move_min() method assumes that the element at first index is already sorted. As such, after
        iteratively calling move_min(), the first element will be moved to the final index. Logic must be
        built in to ID the final element and move it to its appropriate home.
        """

        # part 1: sorts elements, pushing first element to last position
        sorted_idx = 0
        while sorted_idx < self.count:
            sorted_idx = self.move_min(sorted_idx)


        # part 2: identifies final element and relocates appropriately
        temp_idx = 0
        node = self.head
        while temp_idx < self.count:
            node = node.get_next()
            temp_idx += 1
        final_elem = node.get_data()
        final_idx = temp_idx

        temp_idx = 0
        node = self.head
        while temp_idx < self.count:
            if node.get_data() < final_elem:
                temp_idx += 1
                node = node.get_next()
            else:
                self.deleteAt(final_idx)
                self.insert_at(temp_idx,final_elem)
                break


if __name__ == '__main__':
    t1 = LinkedList(4,2,1,0,3)
    t1.selection_sort()
    t1.dump_list()

class GeneralTree():
    """
    Parameters:
    @root: root node
    @first_born: leftmost child of root node
    @current_node: initalized as first born
    @current-value: initialized as value of first born (current node)
    @visited: Linked list of all values whichg have previously been visited
    @path: FULL path, traversing siblings, from root to search value (LL)
    @child_path: path, sibling traversal not captured, more closely resembles typical tree design/behavior (LL)
    
    Methods:
    @check_visited: Determines if a tree node has been visited yet to prevent cyclical movements
    @check_child_path: Determines if a tree node is already captured in child_path
    @depth_first_traversal: Explores entire tree via depth first protocol
    @depth_first_search: Captures all necessary node traversals required to move from root to search value
        including sibling node traversals
    @child_depth_first_search: modification to @depth_first_search such that sibling traversals are eliminated.
        This more closely mimics general tree behavior. In a file system, for example, traversing siblings is 
        not necessary. This method allows for the correct capture of path.
    """
    
    def __init__(self,root=None):
        self.root = root
        self.first_born = self.root.get_child()        
        self.current_node = self.first_born
        self.current_value = self.current_node.get_value()
        self.start = self.current_value
        self.visited = LinkedList(self.root.get_value())
        self.path = LinkedList(self.root.get_value())
        self.child_path = LinkedList(self.root.get_value())
        
    def check_visited(self,val):
        if self.visited.find(val):
            return True
        else:
            return False
        
    def check_child_path(self,val):
        if self.child_path.find(val):
            return True
        else:
            return False        
        
        
    def depth_first_traversal(self):

        if self.current_value == self.root.get_value():
            self.visited.insert_at(idx=1,val=self.start)
            
            # copy self.visited then reset for future method calls
            self.completed_visited = self.visited
            self.current_node = self.first_born
            self.current_value = self.current_node.get_value()
            self.start = self.current_value
            self.visited = LinkedList(self.root.get_value())
            
            return self.completed_visited.dump_list() 
        
        else:
            # ==== tree traversal logic ====
            if self.current_node.get_child() and self.check_visited(self.current_node.get_child().get_value()) == False:
                # parent -> child (not yet visited)
                self.current_node = self.current_node.get_child()
                self.current_value = self.current_node.get_value()
                self.visited.append(self.current_value)                  

            elif self.current_node.get_right() and self.check_visited(self.current_node.get_right().get_value()) == False:            
                # sibling -> right_sibling (not yet visited)
                self.current_node = self.current_node.get_right()
                self.current_value = self.current_node.get_value() 
                self.visited.append(self.current_value)                                           
                
            elif self.current_node.get_right() == None and self.current_node.get_left():
                # right_most_sibling -> left_sibling (already visited)
                self.current_node = self.current_node.get_left()
                self.current_value = self.current_node.get_value()
                
            elif self.current_node.get_left() != None and self.check_visited(self.current_node.get_right().get_value()) == True:
                # sibling (not left-most or right-most) -> left_sibling (already visited)
                self.current_node = self.current_node.get_left()
                self.current_value = self.current_node.get_value()
                
            else:
                # left_most_sibling -> parent (already visited)
                self.current_node = self.current_node.get_parent()
                self.current_value = self.current_node.get_value()               
                
            # ==== recursively apply logic ====
            self.depth_first_traversal()
            
            
    def depth_first_search(self,search_val):
        self.search_val = search_val

        if self.current_value == search_val or self.current_value == self.root.get_value():
            self.visited.insert_at(idx=1,val=self.start)
            self.path.insert_at(idx=1,val=self.start)
            
            
            if self.check_visited(self.search_val) == True:
                condition = 1
            else:
                condition = 0
            
            # copy self.path and reset for future method calls
            self.completed_path = self.path      
            self.current_node = self.first_born
            self.current_value = self.current_node.get_value()
            self.start = self.current_value
            self.visited = LinkedList(self.root.get_value())
            self.path = LinkedList(self.root.get_value())
            
            if condition == 1:
                return self.completed_path.dump_list() 
            else:
                print("Value not found")
        
        else:
            # ==== tree traversal logic ====
            if self.current_node.get_child() and self.check_visited(self.current_node.get_child().get_value()) == False:
                # parent -> child (not yet visited)
                self.current_node = self.current_node.get_child()
                self.current_value = self.current_node.get_value()
                self.visited.append(self.current_value)
                self.path.append(self.current_value)                    

            elif self.current_node.get_right() and self.check_visited(self.current_node.get_right().get_value()) == False:            
                # sibling -> right_sibling (not yet visited)
                self.current_node = self.current_node.get_right()
                self.current_value = self.current_node.get_value() 
                self.visited.append(self.current_value)                    
                self.path.append(self.current_value)                         
                
            elif self.current_node.get_right() == None and self.current_node.get_left():
                # right_most_sibling -> left_sibling (already visited)
                self.current_node = self.current_node.get_left()
                self.current_value = self.current_node.get_value()
                
            elif self.current_node.get_left() != None and self.check_visited(self.current_node.get_right().get_value()) == True:
                # sibling (not left-most or right-most) -> left_sibling (already visited)
                self.current_node = self.current_node.get_left()
                self.current_value = self.current_node.get_value()
                self.path.deleteAt(idx=self.path.count)
                
            else:
                # left_most_sibling -> parent (already visited)
                self.current_node = self.current_node.get_parent()
                self.current_value = self.current_node.get_value() 
                self.path.deleteAt(idx=self.path.count)                
                
            # ==== recursively apply logic ====
            self.depth_first_search(search_val=self.search_val)           
            
            
    def child_depth_first_search(self,search_val):
        self.search_val = search_val

        if self.current_value == search_val or self.current_value == self.root.get_value():
            self.visited.insert_at(idx=1,val=self.start)
            self.path.insert_at(idx=1,val=self.start)         
            
            
            if self.check_visited(self.search_val) == True:
                condition = 1
            else:
                condition = 0
            
            # copy self.path and reset for future method calls
            self.completed_child_path = self.child_path            
            self.current_node = self.first_born
            self.current_value = self.current_node.get_value()
            self.start = self.current_value
            self.visited = LinkedList(self.root.get_value())
            self.child_path = LinkedList(self.root.get_value())            
            
            if condition == 1:
                return self.completed_child_path.dump_list() 
            else:
                print("Value not found")
        
        else:
            # ==== tree traversal logic ====
            if self.current_node.get_child() and self.check_visited(self.current_node.get_child().get_value()) == False:
                # parent -> child (not yet visited)
                if self.check_child_path(self.current_node.get_value()) == False:
                    self.child_path.append(self.current_value)                  
                self.current_node = self.current_node.get_child()
                self.current_value = self.current_node.get_value()
                self.visited.append(self.current_value) 
                self.child_path.append(self.current_value)                  

            elif self.current_node.get_right() and self.check_visited(self.current_node.get_right().get_value()) == False:            
                # sibling -> right_sibling (not yet visited)
                self.child_path.deleteAt(idx=self.child_path.count)
                self.current_node = self.current_node.get_right()
                self.current_value = self.current_node.get_value() 
                self.visited.append(self.current_value)                                  
                self.child_path.append(self.current_value)
                
            elif self.current_node.get_right() == None and self.current_node.get_left():
                # right_most_sibling -> left_sibling (already visited)
                self.current_node = self.current_node.get_left()
                self.current_value = self.current_node.get_value()
                
            elif self.current_node.get_left() != None and self.check_visited(self.current_node.get_right().get_value()) == True:
                # sibling (not left-most or right-most) -> left_sibling (already visited)
                self.current_node = self.current_node.get_left()
                self.current_value = self.current_node.get_value()
                self.child_path.deleteAt(idx=self.child_path.count)                
                
            else:
                # left_most_sibling -> parent (already visited)
                self.current_node = self.current_node.get_parent()
                self.current_value = self.current_node.get_value() 
                self.child_path.deleteAt(idx=self.child_path.count)                 
                
            # ==== recursively apply logic ====
            self.child_depth_first_search(search_val=self.search_val)            
            
if __name__ == '__main__':
  a1 = GeneralTreeNode(value='a1')
  b1 = GeneralTreeNode(value='b1')
  b2 = GeneralTreeNode(value='b2')
  b3 = GeneralTreeNode(value='b3')
  a1.set_child(b1)
  b1.set_parent(a1)
  b1.set_right(b2)
  b2.set_left(b1)
  b2.set_right(b3)
  b3.set_left(b2)

  c1 = GeneralTreeNode(value='c1')
  c1.set_parent(b3)
  b3.set_child(c1)

  d1 = GeneralTreeNode(value='d1')
  d1.set_parent(b1)
  b1.set_child(d1)
  
  r = GeneralTree(root=a1)
  r.depth_first_search(search_val='c1')
  r.child_depth_first_search(search_val='c1')