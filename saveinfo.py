import main


bt = main.BinaryTree()
# bt.insert(4, "I",888)
bt.insert(8, "H",'lobalkobabalo@gmail.com',888)
bt.insert(7, "G",'@7',777)
bt.insert(5, "F",'@5',888)
bt.insert(9, "E",'@9',888)
bt.insert(1, "D",'@1',777)
bt.insert(12, "C",'@12',888)
bt.insert(15, "B",'@15',888)
bt.insert(17, "A",'@17',777)

bt.insert_item_BY_BN(8,'bat')
bt.insert_item_BY_BN(8,'gat')
bt.insert_item_BY_BN(1,'dog')
bt.insert_item_BY_BN(1,'cock')
bt.insert_item_BY_BN(5,'cocks')

bt.insert(150,"aa","@56",578)
# bt.insert(0,"admin","Admin@",'@1234')
bt.save_txt('login/static/User_data.txt')
# print(bt.display_bst())
print(bt.max_value().number_box)
# print(bt.display_bst())
# print(bt.search_by_username("C").password)


bt.showItem(8)
# print(bt.display_bst())

