import json

class BOX:
    def __init__(self, number_box, username, email, password ):
        self.number_box = number_box
        self.username = username
        self.email = email
        self.password = password        
        self.item = []
        self.time= 0
        self.timeleft = 0
        self.price = 0
        self.num=None
        self.left = None
        self.right = None

    def delete_Userpass(self):
        self.username = None
        self.password = None

    def add_item(self, item):
        self.item.append(item)

    def remove_item(self, item):
        if item in self.item:
            self.item.remove(item)

    def addtime(self,time,timeleft):
        self.time = time
        self.timeleft=timeleft

    def addprice(self,price):
        self.price = price

    def get_item(self):
        return self.item
    
    def pre_order_traversal(self):
        result = [{'number_box':self.number_box, 'username':self.username, 'email':self.email, 'password':self.password,'item':self.item,'time':self.time,'timeleft':self.timeleft,'price':self.price}]
        if self.left:
            result.extend(self.left.pre_order_traversal())
        if self.right:
            result.extend(self.right.pre_order_traversal())
        return result


class BinaryTree:
    def __init__(self):

        self.root = None

    # ... [other methods as before]
    def create(self, number_box, username, email, password):
        
        newBox = BOX(number_box, username,email, password)
        return newBox
        # return self.insert(newBox.number_box,newBox.username,newBox.password)

    def insert(self, number_box, username, email, password ):
        
        if not self.root:
            self.root = BOX(number_box, username, email, password)
            # self.save_to_txt(number_box, username, password, email)
   
        else:
            self._insert_recursive(self.root, number_box, username,email, password)

    def _insert_recursive(self, Box, number_box, username , email, password):
        
        if number_box < Box.number_box:
            if Box.left is None:
                Box.left = BOX(number_box, username, email, password)
                # self.save_to_txt(number_box, username, password, email)
            else:
                self._insert_recursive(Box.left, number_box, username,email, password)
        elif number_box > Box.number_box:
            if Box.right is None:
                Box.right = BOX(number_box, username, email, password)
                # self.save_to_txt(number_box, username, password, email)
            else:
                self._insert_recursive(Box.right, number_box, username,email, password)

    def insert_item_BY_BN(self, box_number, item):
        box = self.search(box_number)
        if box:
            box.add_item(item)
        

    def insert_item_BY_User(self, username, password, item):
        user_box = self.searchUser(username)
        pass_box = self.searchPass(password)

        # Ensure that both the username and password point to the same box
        if user_box and pass_box and user_box == pass_box:
            user_box.add_item(item)
        else:
            print("Please check your Username and Password again.")

    def insert_time(self,box_number,time,timeleft):
        box = self.search(box_number)
        if box:
            box.addtime(time,timeleft)

    def insert_price(self,box_number,price):
        box = self.search(box_number)
        if box:
            box.addprice(price)

    def search(self, number_box):
        return self._search_recursive(self.root, number_box)

    def _search_recursive(self, node, number_box):
        
        # If current node is None or value matches the node's value
        if node is None :
            
            return None
        if node.number_box == number_box:
            return node
        # If value is greater than current node's value, search the right subtree
        if number_box > node.number_box:
            return self._search_recursive(node.right, number_box)

        # If value is less than current node's value, search the left subtree
        return self._search_recursive(node.left, number_box)



    def search_by_username(self, username):
        return self._search_by_username_recursive(self.root, username)

    def _search_by_username_recursive(self, node, username):
        if node is None:
            return None

        # หากเราพบ username
        if node.username == username:
            return node

        # ค้นหาใน left subtree
        left_result = self._search_by_username_recursive(node.left, username)
        if left_result:
            return left_result

        # ถ้าไม่พบใน left, ค้นหาใน right subtree
        return self._search_by_username_recursive(node.right, username)
    
    def searchEmail(self, email):
        return self._searchEmail_recursive(self.root, email)

    def _searchEmail_recursive(self, node, email):
        if node is None:
            return None
        if node.email == email:
            return node

        # Search in left subtree
        left_search = self._searchEmail_recursive(node.left,email)
        if left_search:
            return left_search

        # If not found in left, search in right subtree
        return self._searchEmail_recursive(node.right, email)

    def searchPass(self, password):
        return self._searchPass_recursive(self.root, password)

    def _searchPass_recursive(self, node, password):
        if node is None:
            return None
        if node.password == password:
            return node

        # Search in left subtree
        left_search = self._searchPass_recursive(node.left, password)
        if left_search:
            return left_search

        # If not found in left, search in right subtree
        return self._searchPass_recursive(node.right, password)

    def delete(self, number_box):
        box_to_delete = self.search(number_box)
        if box_to_delete:
            box_to_delete.username = None
            box_to_delete.password = None
            box_to_delete.item = None
        self.root = self._delete_recursive(self.root, number_box)

    def delete_item(self, number_box, item):

        box = self.search(number_box)
        if box:
            box.remove_item(item)

    def delete_User(self, number_box):
        yourbox = self.search(number_box)
        if yourbox:
            yourbox.delete_Userpass()

    def _delete_recursive(self, node, number_box):
        if not node:
            return node

        if number_box == node.number_box:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            node.number_box = self.min_value(node.right).number_box
            node.right = self._delete_recursive(node.right, node.number_box)
        elif number_box < node.number_box:
            node.left = self._delete_recursive(node.left, number_box)
        else:
            node.right = self._delete_recursive(node.right, number_box)
        return node

    def update_username(self, number_box, username):
        box = self.search(number_box)
        if box:
            box.username = username

    def update_password(self, number_box, password):
        box = self.search(number_box)
        if box:
            box.password = password

    def print_tree(self):
        if not self.root:
            return

        tree_height = self._height(self.root)
        queue = [(self.root, 0)]

        current_level = 0
        while queue:
            level_nodes = len(queue)
            next_nodes = []
            output = ' ' * (2 ** (tree_height - current_level) - 1)
            between = ' ' * (2 ** (tree_height - current_level + 1) - 2)

            for _ in range(level_nodes):
                node, position = queue.pop(0)
                if node:
                    print(node.number_box, end=between)
                    next_nodes.append(node.left)
                    next_nodes.append(node.right)
                else:
                    print(' ', end=between)
                    next_nodes.append(None)
                    next_nodes.append(None)

            print()
            current_level += 1

            # Prepare the nodes of the next level for processing
            for n in next_nodes:
                queue.append((n, position))

            if current_level == tree_height:
                break

    def _height(self, node):
        if not node:
            return 0
        left_height = self._height(node.left)
        right_height = self._height(node.right)
        return max(left_height, right_height) + 1

    def showUser(self, username):
        boxx = self.searchUser(username)
        print("User", username, " in Box number", boxx.number_box)
        self.showItem(boxx.number_box)

    def showItem(self, number_box):
        search_result = self.search(number_box)
        if search_result:
            result0 = [item for item in self.search(number_box).get_item() if item is not None]
            num_item = len(result0)                

            if search_result.get_item() :
                print("Found item", end=" ")
                for item in result0:
                    if num_item == 2:
                        print(item, end=" and ")

                        num_item -= 1
                    elif num_item == 1:

                        print(item, end=" ")
                    else:
                        print(item, end=", ")

                        num_item -= 1

                print("is in box number", number_box)

        else:
            print("Not found", number_box)

    def min_value(self,node):
        current = node

        # วนซ้ำไปยังโหนดซ้ายสุด
        while current.left is not None:
            current = current.left

        return current

    def max_value(self):
        current = self.root
        max_box = None
        while current.right is not None :

            if  current.right.number_box < self.lastbox() :
                current = current.right

                max_box = current
                continue
                
            else :
                return max_box

    def max_value_over(self):
        current = self.root
        while current.right is not None:
            current = current.right
        return current

    def Temporary_numberbox(self):
        lastnumbox = self.max_value_over()
        maxbox = self.lastbox()
        if lastnumbox.number_box >= maxbox:
            return lastnumbox.number_box+1
        elif lastnumbox.number_box < maxbox:
            return maxbox

    def lastbox(self):#=====================================================max box==============================================================
        return 100

  
    def save_to_data(self):
        return self.save_to_data_recursive(self.root)
    def save_to_data_recursive(self,root,all_data=None):#save data-----------------------------------------------------------
            if all_data==None:
                all_data = []
            if root:
                self.save_to_data_recursive(root.left,all_data)
                
                data = {
                            'number_box':root.number_box,
                            "username": root.username,
                            "email":root.email,
                            "password": root.password,
                            "item": root.item,
                            "time":root.time,
                            "timeleft":root.timeleft,
                            "price":root.price,
                            "num":root.num
                             
                            }
                all_data.append(data)
                self.save_to_data_recursive(root.right,all_data)   
            return all_data
    def save_txt(self,filename): 
        data = self.save_to_data()                 
        with open(filename, 'w') as h:                
            json.dump(data, h)

    def load_from_txt(self,filename):       
        with open(filename, 'r') as h:
            loaded_data = json.load(h)
        return loaded_data
    