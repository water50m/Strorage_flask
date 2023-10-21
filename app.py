from flask import Flask,render_template,request, redirect, url_for,flash,jsonify
from flask_mail import Mail, Message
import pickle
import uuid
import json
import main
from copy import deepcopy
import secrets

bt = main.BinaryTree()

app = Flask(__name__)
app.secret_key = "some_secret_key"
app.secret_key = 'your_secret_key_here'
# ตั้งค่าสำหรับ Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'pporn7172@gmail.com'
app.config['MAIL_PASSWORD'] = 'epkb sfut ujey bvze'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)



@app.route('/',methods=['POST','GET'])
def index():       
    return render_template("newlogin.html")

@app.route('/newlogin')
def newlogin():
    return render_template("newlogin.html")

@app.route('/call_register')
def call_register():
    return render_template("register.html")

@app.route('/register2')
def register2():
    return render_template("register2.html")


# Edit already============================================================================================================
def uploadUser():
    User = bt.load_from_txt('static/User_data.txt')
    try:
        for account in User:
            bt.insert(account['number_box'], account['username'], account['email'], account['password'])
            bt.insert_time(account['number_box'],0,account['timeleft'])
            bt.insert_price(account['number_box'],0)

            for item in account['item']:
                bt.insert_item_BY_BN(account['number_box'],item)
    except TypeError as e:
        print(f"An error occurred: {e}")

    
@app.route('/trysave')
def saveinfo():
    bt.save_txt('static/User_data.txt')
    return render_template("sign_in.html")

@app.route('/inbox<userid>')
def call_inbox(userid):    
    node = bt.search(int(userid))
    

    
    return render_template("inbox.html",iUser=node,lastbox = bt.lastbox(),empty_box = allemptybox())

def allemptybox():
    empty_box = []
    
    for i in range(1,bt.lastbox(),1) :
        if not bt.search(i):
            empty_box.append(i)
    return empty_box

# Edit already============================================================================================================

@app.route('/registerloginpage',methods=['POST','GET'])
def registerloginpage():                  
    username=request.form.get('username')
    email=request.form.get('email')
    password=request.form.get('password')
    confirm_password=request.form.get('confirm_password')  
    num_box = bt.Temporary_numberbox()             
    if request.method == "POST":            
        if bt.search_by_username(username):
            flash('This username is used','error')
            return redirect(url_for('registerloginpage'))
        if bt.searchEmail(email):
            flash('This email is used','error')
            return redirect(url_for('registerloginpage'))
        
        elif password == confirm_password:                
                bt.insert(int(num_box), username, email, password)
                saveinfo()
                subject = f'Hello {username}'
                recipient = email                
                content = f"Welcome to our strorage. \nThank you for using our service.\nUsername:{username},\nPassword:{password}\nHave a good day."
                try:
                    msg = Message(subject, sender='Strorage company', recipients=[recipient])
                    msg.body = content
                    mail.send(msg)
                    flash("congratulations! ",'success')                    
                except:
                    flash("congratulations! ",'success')
                    flash("Your email look like incorrect","info")
                    flash("But you still use this account","info")
                    return redirect(url_for('registerloginpage'))
                return redirect(url_for('registerloginpage'))                            
        flash("password don't match!!",'error')
        return redirect(url_for('registerloginpage')) 
    return render_template('newlogin.html')   



# Edit already============================================================================================================
@app.route('/login',methods=['POST','GET'])
def login():
    
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    try:
        node = bt.search_by_username(username)
        if request.method == "POST":
            if username == 'admin' and password == '@1234':
                    return admin()
            elif node:
                
                if (node.username == username or node.email == username) and str(node.password)==password:
                    return render_template('inbox.html', iUser=node,lastbox =  bt.lastbox(),empty_box = allemptybox())
                        
            flash("username or password incorrect!",'error')
            return redirect(url_for('index'))
    
    except Exception as e:
        print(e)  # ล็อกข้อผิดพลาด
        return "An error occurred", 500
    
    return redirect(url_for('index'))
            
                        
# Edit already============================================================================================================
@app.route('/info_user')
def info_user():
    User = bt.load_from_txt('static/User_data.txt')
    return User

# Edit already============================================================================================================
@app.route('/in_box_page')
def in_box():
    
    node = bt.search_by_username('G')
    return render_template('inbox.html',iUser = node,lastbox=bt.lastbox(),empty_box = allemptybox())

# Edit already============================================================================================================
@app.route('/give/<userid>' ,methods=['POST','GET'])
def give_item(userid):
    
    
    
    # num_box=request.form.get('number_box')
    node = bt.search(int(userid))
    itemnew = request.form.get('itemName')
    if request.method == 'POST':
        if node.timeleft == 0 :
            flash('Please hire this box frist!')
            itemnew = request.form.get('itemName')
            return redirect(url_for('call_inbox',userid=userid))
        else:
            if itemnew:  
                bt.insert_item_BY_BN(int(userid),itemnew)
                saveinfo()

                return redirect(url_for('call_inbox',userid=userid))
        
    return render_template('inbox.html', iUser=node,lastbox=bt.lastbox(),empty_box = allemptybox())

@app.route('/giveitem/<userid>' ,methods=['POST','GET'])
def giveitem(userid):
    node = bt.search(int(userid))
    if request.method == 'POST':
        itemnew1 = request.form.get('item1')
        itemnew2 = request.form.get('item2')
        if itemnew1  :  
            bt.insert_item_BY_BN(int(userid),itemnew1)
            saveinfo()
            
        if itemnew2:
            bt.insert_item_BY_BN(int(userid),itemnew1)
            saveinfo()
            
        return redirect(url_for('call_inbox',userid=userid))
    return render_template('inbox.html', iUser=node,lastbox=bt.lastbox(),empty_box = allemptybox())

    

@app.route('/delete/<userid>', methods=['POST','GET','DELETE'])
def delete_item(userid):
    
    
    node = bt.search(int(userid))
    
    if request.method == 'POST':
        input_item=request.form.get('hiddenItemName')        
        items=request.form.getlist('multiitem')       
        items.append(input_item)           
        
        all_items = [item for item in items if item is not None ]
        
        if all_items  :            
                for i in all_items[:]:
                    if i in node.item :   
                        node.item.remove(i)
                        saveinfo()                                                  
                        flash('Item  '+i+"  deleted")                                            
                    elif i:
                        
                        flash('Item  '+i+"  isn't in your list items")                                                
                return redirect(url_for('delete_item', userid=userid))
        return redirect(url_for('delete_item', userid=userid))     
    return render_template('inbox.html', iUser=node,lastbox=bt.lastbox(),empty_box = allemptybox())

@app.route('/test',methods=['POST','GET'])
def test():
    # return render_template('test.html')
    return bt.save_to_data()
    

@app.route('/search/<userid>' ,methods=['POST','GET','DELETE'])    
def search(userid):
    print(userid)
    node = bt.search(int(userid))
    nodesearch = deepcopy(node)
    if request.method == 'GET':
        return render_template('inbox.html', iUser=node,lastbox=bt.lastbox(),empty_box = allemptybox())
    if request.method == 'POST':
        input_item=request.form.get('itemName')
        likeitem = []
        if input_item:
            for i in  node.item:
                if i.startswith(input_item):                                
                    likeitem.append(i)
            
            nodesearch.item = likeitem
            if len(likeitem) > 0:
                flash("Press Search button again to show all item")               
                return render_template('inbox.html',iUser=nodesearch,lastbox=bt.lastbox() ,empty_box = allemptybox())
            
            elif len(likeitem) == 0:
                flash("No item name "+input_item)
                
        # else:
        #     return redirect(url_for('search', userid=userid))     
    return render_template('inbox.html',iUser=node,lastbox=bt.lastbox(),empty_box = allemptybox())

@app.route('/selectbox/<userid>',methods=['POST','GET'])
def selectbox(userid):
    
    node = bt.search(int(userid))
        
    if request.method == 'POST':
        selected_box = int(request.form.get("selected_box"))
        bt.insert(selected_box,node.username,node.email,node.password)
        for item in node.item:
            bt.insert_item_BY_BN(selected_box,item)        
        bt.delete(node.number_box)
        saveinfo()
        return redirect(url_for('call_inbox',userid=selected_box))
        # return render_template('inbox.html',iUser=bt.search(selected_box),lastbox=bt.lastbox(),empty_box = allemptybox())
        
    return render_template('inbox.html',iUser=node,lastbox=bt.lastbox(),empty_box = allemptybox())



@app.route('/cancle/<userid>' ,methods=['Post','GET'])
def cancleaddingtime(userid):
    node = bt.search(int(userid))
    node.price=0
    node.time=0
    saveinfo()
    return redirect(url_for('call_inbox',userid=userid))


@app.route('/addtime/<userid>' ,methods=['POST'])
def addtime(userid):
    node = bt.search(int(userid))
    
    if request.method == 'POST':
        time = int(request.form.get('thedaytime'))
        node.time =  time
        bt.insert_time(int(userid),time,node.timeleft)
            
        a = time%30
        price_mouth = ((time - a)/30)*150
        b = a%7
        price_week = ((a-b)/7)*50
        price_day = b*10
        price = price_mouth + price_week + price_day
        node.price =  price
        bt.insert_price(int(userid),node.price)
        return redirect(url_for('call_inbox',userid=userid))
        
    return render_template('inbox.html',iUser=node,lastbox=bt.lastbox(),empty_box = allemptybox())



@app.route('/confirm/<userid>')
def confirm(userid):

    node = bt.search(int(userid))
    node.timeleft = node.timeleft + node.time
    bt.insert_time(int(userid),0,node.timeleft)
    node.price = 0
    bt.insert_price(int(userid),0)
    saveinfo()
    subject = f'Hello {node.username}'
    recipient = node.email
    item = ', '.join(node.item)
    time = node.item
    content = f'This is your item \n{item}, \n\nYou can use this box for another {time} day'
    try:
        msg = Message(subject, sender='Strorage company', recipients=[recipient])
        msg.body = content
        mail.send(msg)
        flash('email send!')
    except:
        flash("Can't send email!")
        return redirect(url_for('call_inbox',userid=userid))      
    return redirect(url_for('call_inbox',userid=userid))


@app.route('/admin2',methods=['POST','GET'])
def admin():
    
    node = bt.search(int(0))
    allaccount = bt.save_to_data()
    
    alluser = []
    num = 1
    for i in allaccount:

        if i['username'] != 'Admin' and i['number_box'] != 0 :
            if i['number_box'] > bt.lastbox():
                i['num'] = num
                
                alluser.append(i)
                num+=1
            
            else:
                i['num'] = num               
                alluser.append(i)
                num+=1
            
                
        else:
            continue
    
    return render_template('admin2.html',iUser = node,lastbox=bt.lastbox(),empty_box = allemptybox(),user=alluser)




@app.route('/edituser/<userid>',methods=['POST','GET'])
def edituser(userid):
    node = bt.search(int(userid))
    return render_template('edituser.html',iUser = node,lastbox=bt.lastbox(),empty_box = allemptybox())


@app.route('/editusername/<userid>',methods=['POST','GET'])
def editusername(userid):
    node = bt.search(int(userid))
    new_username = request.form.get('username_edit')
    if node.username != new_username:
        node.username = new_username
        saveinfo()
        nodenew = bt.search(int(userid))
        return render_template('edituser.html',iUser = nodenew,lastbox=bt.lastbox(),empty_box = allemptybox())
    return render_template('edituser.html',iUser = node,lastbox=bt.lastbox(),empty_box = allemptybox())

@app.route('/editpassword/<userid>',methods=['POST','GET'])
def editpassword(userid):
    node = bt.search(int(userid))
    new_password = request.form.get('password_edit')
    if  node.password != new_password:
        node.password = new_password
        saveinfo()
        nodenew = bt.search(int(userid))
        return render_template('edituser.html',iUser = nodenew,lastbox=bt.lastbox(),empty_box = allemptybox())
    return render_template('edituser.html',iUser = node,lastbox=bt.lastbox(),empty_box = allemptybox())

@app.route('/editemail/<userid>',methods=['POST','GET'])
def editemail(userid):    
    node = bt.search(int(userid))
    new_email = request.form.get('email_edit')
    if node.email != new_email:
        node.email = new_email
        saveinfo()
        nodenew = bt.search(int(userid))
        return render_template('edituser.html',iUser = nodenew,lastbox=bt.lastbox(),empty_box = allemptybox())
    return render_template('edituser.html',iUser = node,lastbox=bt.lastbox(),empty_box = allemptybox())
# ===========================================================================================================================================
@app.route('/addminsearch/<user>',methods=['POST','GET'])
def adminsearch(user):
    node = bt.search(int(0))
    searchword = str(request.form.get('searchName'))
    result_search = []
    alluser = bt.save_to_data()
    
    for i in alluser:
        if i['number_box'] < 100 and i['number_box'] != 0:
            if searchword == i['username'] or searchword == str(i['password']) or searchword == str(i['number_box']):
                result_search.append(i)
            elif i['username'].startswith(searchword):
                result_search.append(i)
    if not result_search:
        return 'false'
    
    all = alluser()
    return render_template('admin2.html',iUser = node,lastbox=bt.lastbox(),empty_box = allemptybox(),user=result_search)

        

def selectboxfunc(userid,selected_box):
    
    node = bt.search(int(userid))
       
    if request.method == 'POST':
        if node.number_box==selected_box:
            return node
        elif node :
            
            bt.insert(selected_box,node.username,node.email,node.password)
            for item in node.item:
                bt.insert_item_BY_BN(selected_box,item)        
            bt.delete(node.number_box)
            saveinfo()
            return bt.search(selected_box)
            
        
        return bt.search(selected_box) 
    return node    
        
@app.route('/edit_user_box/<userid>', methods=['POST','GET'])
def edit_user_box(userid):
    node = bt.search(int(userid))

    if request.method == 'POST':
        selected_box = int(request.form.get("selected_box_edit"))
        if selected_box == 0: 
            Temporary_numberbox = bt.Temporary_numberbox()
            nodenew = Temporary_numberbox
            node.number_box=nodenew
            saveinfo()
            return redirect(url_for('edituser',userid=Temporary_numberbox)) 
        
        
        nodenew = selectboxfunc(userid,selected_box)
        return redirect(url_for('edituser',userid=nodenew.number_box))
    return render_template('edituser.html',iUser=node,lastbox=bt.lastbox(),empty_box = allemptybox())


def alluser():
    allaccount = bt.save_to_data()
    
    alluser = []
    num = 1
    for i in allaccount:
        if i['username'] != 'Admin'  :
            if  i['number_box'] < bt.lastbox() and i['number_box'] != 0: 
                i['num'] = num
                alluser.append(i)
                num+=1
                
        else:
            continue
    return alluser
alluser()
@app.route('/deleteaccount/<userid>', methods=['POST','GET'])
def deleteaccount(userid): 
    node = bt.search(0)
    bt.delete(int(userid))
    saveinfo()    
    
    allaccount = alluser()
    return render_template('admin2.html',iUser = node,lastbox=bt.lastbox(),empty_box = allemptybox(),user=allaccount)


@app.route('/forgetpassword', methods=['POST','GET'])
def forgetpassword(): 
    newrandompassword = secrets.token_hex(3)
    
    username=request.form.get('username')
    email=request.form.get('email')
    checkusername = bt.search_by_username(username)        
    check_email=bt.searchEmail(email)
    saveinfo() 
    if check_email and checkusername:
        if check_email.username == checkusername.username:
            checkusername.password =  newrandompassword
            subject = f'Hello {checkusername.username}'
            recipient = check_email.email
            content = f'This is your new password \nPassword:newrandompassword'
            try:
                msg = Message(subject, sender='Strorage company', recipients=[recipient])
                msg.body = content
                mail.send(msg)
                flash('email send!')
            except:
                flash("Please check yoyr email again!","error")
                return redirect(url_for('forgetpassword'))
        flash('username or email incorrect!',"error") 
        return redirect(url_for('forgetpassword'))
    return render_template('newlogin.html')         
    
               
        


uploadUser()
if __name__=="__main__":
    app.run(debug=True)
    

