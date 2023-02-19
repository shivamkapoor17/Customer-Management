
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3 as sq
from datetime import datetime, date

con = sq.connect('database.db')
c=con.cursor()


root = Tk()

root.title("GS GALAXY")
root.minsize(width=1000,height=800)
root.maxsize(width=1000,height=800)
s = ttk.Style()
s.theme_use('clam')
s.configure('Treeview', rowheight=20)



pane = Frame(root, bg='red')
pane.pack(fill = BOTH, expand = 1, side=TOP)


#s = ttk.Style()
#s.theme_use('default')
#s.configure('TNotebook.Tab', background="black")
#s.map("TNotebook", background= [("selected", "white")])

tab_parent = ttk.Notebook(pane)
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)
tab5 = ttk.Frame(tab_parent)
tab_parent.add(tab1, text = 'Home')
tab_parent.add(tab2, text = 'Customer')
tab_parent.add(tab3, text = 'Electricians')
tab_parent.add(tab4, text = 'Subscriptions')
tab_parent.add(tab5, text = 'Address')
tab_parent.pack(side=LEFT, expand=1, fill=BOTH)

root.iconbitmap('Asset8.ico')

def calculateCustomerPoints(ammount,newammount=0 ):
    ammount1= ammount + newammount
    ammount = int(ammount1/100)
    ammount = ammount*2
    return (ammount, ammount1)



########################################    HOME tab         ################################
homeFrame=Frame(tab1, relief=SUNKEN)
homeFrame.pack(fill=BOTH, expand=True)

# def display_selected(choice):
#     choice = variable.get()
#     return choice




def search():
    val=variable.get()


    if (ehn.get().strip() == "" or ehm.get().strip() == "" or val == "choose options"):
        messagebox.showinfo('Notice', 'Please Fill All Entries')

    elif (val=="Customers" and ehn.get().strip() != "" and ehm.get().strip() != ""):
        mobile=ehm.get()
        findCustomer(mobile)

    elif (val=="Electricians" and ehn.get().strip() != "" and ehm.get().strip() != ""):
        mobile = ehm.get()
        findElectrician(mobile)

    elif (val=="Subscriptions" and ehn.get().strip() != "" and ehm.get().strip() != ""):
        name = ehn.get()
        mobile = ehm.get()
        findSubscription(name,mobile)


def findCustomer(mobile):
    refresh()
    c.execute('SELECT * FROM Customers WHERE mobile_no=?',(mobile,))
    row = c.fetchone()
    if (not row):
        messagebox.showinfo('notice','no such Customer')
    else:
        ehcn.focus_set()
        ehcn.bind('<Return>', updateCust)
        ehcm.bind('<Return>', updateCust)
        ehca.bind('<Return>', updateCust)
        ehcp.bind('<Return>', updateCust)
        ehcap.bind('<Return>', updateCust)
        ehen.unbind('<Return>')
        ehem.unbind('<Return>')
        ehep.unbind('<Return>')

        ehcn.insert(0, row[1])
        ehcm.insert(0, row[2])
        ehca.insert(0, row[3])
        ehcp.insert(0, row[4])



def findElectrician(mobile):
    refresh()
    c.execute('SELECT * FROM Electricians WHERE mobile_no=?', (mobile,))
    row = c.fetchone()
    if (not row):
        messagebox.showinfo('notice','no such Electrician')
    else:
        ehen.focus_set()
        ehcn.unbind('<Return>')
        ehcm.unbind('<Return>')
        ehcp.unbind('<Return>')
        ehca.unbind('<Return>')
        ehcap.unbind('<Return>')
        ehen.bind('<Return>', updateElec)
        ehem.bind('<Return>', updateElec)
        ehep.bind('<Return>', updateElec)

        ehen.insert(0, row[1])
        ehem.insert(0, row[2])
        ehep.insert(0, row[3])

def findSubscription(name,mobile):

    c.execute('SELECT * FROM Subscriptions WHERE mobile_no=? AND name =?', (mobile, name))
    rows= c.fetchall()
    if (not rows):
        messagebox.showinfo('notice','no such subscription')
    else:
        count = 0
        for row in rows:
            count = count + 1
        j = count
        for i in range(0, j):
            subscriptionsTable.insert(parent='', index='end', text='', values=( rows[i][1], rows[i][2], rows[i][3],rows[i][4], rows[i][5], rows[i][7]))
            j = j - 1


def updateCust(event=None):


    mobile=ehm.get()

    ammount=ehca.get()
    newammount = ehcap.get()
    value = calculateCustomerPoints(int(ammount), int(newammount))
    points = value[0]
    hcp.set("")
    ehcp.insert(0,points)
    if(mobile):
        data=(
            ehcn.get(),
            ehcm.get(),
            value[1],
            points,
            datetime.now()
        )
        c.execute("UPDATE Customers SET (name, mobile_no,ammount, points, updated_date)=(?,?,?,?,?) WHERE mobile_no=?",
                  (data[0], data[1], data[2], data[3],data[4], mobile))
        con.commit()
        messagebox.showinfo('notice', 'update successfully')
    refresh()


def deleteCust():
    mobile = ehm.get()
    if(mobile):
        c.execute('DELETE FROM Customers WHERE mobile_no=?', (mobile,))
        con.commit()
        messagebox.showinfo('notice', 'deleted successfully')
    refresh()


def updateElec(event=None):
    mobile = ehm.get()
    if(mobile):
        data = (
            ehen.get(),
            ehem.get(),
            ehep.get(),
            datetime.now()
        )
        c.execute("UPDATE Electricians SET (name, mobile_no, points, updated_date)=(?,?,?,?) WHERE mobile_no=?",
                (data[0], data[1], data[2], data[3], mobile))
        con.commit()
        messagebox.showinfo('notice', 'update successfully')
    refresh()

def deleteElec():

    mobile = ehm.get()
    if(mobile):
        c.execute('DELETE FROM Electricians WHERE mobile_no=?', (mobile,))
        con.commit()
        messagebox.showinfo('notice', 'deleted successfully')
    refresh()

def extraFunction4():
    selected1 = subscriptionsTable.focus()
    value = subscriptionsTable.item(selected1, 'value')
    return value[5]


def deleteSubs():
    try:
        updated_date = extraFunction4()
    except:
        messagebox.showinfo('notice', 'anything is not selected for delete')
    else:
        x = subscriptionsTable.selection()[0]
        subscriptionsTable.delete(x)

        c.execute('DELETE FROM Subscriptions WHERE updated_date=?', (updated_date,))
        con.commit()



def refresh():
    hcn.set("")
    hcm.set("")
    hcp.set("")
    hcz.set("")
    hczx.set("")
    hen.set("")
    hem.set("")
    hep.set("")


def clear():
    tables = subscriptionsTable.get_children()
    for table in tables:
        subscriptionsTable.delete(table)

lable_h=Label(homeFrame, text='SEARCH PAGE', font='Helvetica 18 bold' )
lable_h.place(x=380, y=10)


lhd= Label(homeFrame, text ='CHOOSE OPTIONS', font = "50")
lhd.place(x=320,y=140)
selections = ['Customers', 'Electricians', 'Subscriptions']
variable = StringVar()
variable.set('choose options')

dropdown = OptionMenu(
    homeFrame,
    variable,
    *selections,
    # command=display_selected
)
dropdown.place(x=550,y=140)


lhn= Label(homeFrame, text ='NAME', font = "50")
lhn.place(x=320, y=60)
ehn = Entry(homeFrame,bd=5, width=25)
ehn.place(x= 550,y=60)
ehn.focus_set()

lhm= Label(homeFrame, text ='MOBILE_NO', font = "50")
lhm.place(x=320, y=100)
ehm = Entry(homeFrame,bd=5, width=25)
ehm.place(x=550,y=100)


B1 = Button(homeFrame,bg='black',command=search,font='Helvetica 10 bold',activeforeground='green', fg='white',text ="SEARCH", width=20, relief=RAISED)
B1.place(x= 420, y=210)



hcn=StringVar()
hcm=StringVar()
hcp=StringVar()
hcz = StringVar()
hen=StringVar()
hem=StringVar()
hep=StringVar()
hczx=IntVar()



lablec1= Label(homeFrame, text ='Customer', font = "Helvetica 20 underline")
lablec1.place(x=50, y=280)

lhcn = Label(homeFrame, text='NAME', font='50')
lhcn.place(x=55,y=330)
ehcn=Entry(homeFrame,textvariable=hcn,bd=5,width=25)
ehcn.place(x=285, y=330)
lhcm = Label(homeFrame, text='MOBILE_NO', font='50')
lhcm.place(x=55,y=370)
ehcm=Entry(homeFrame,bd=5,textvariable=hcm,width=25)
ehcm.place(x=285,y=370)
lhca = Label(homeFrame, text='AMOUNT', font='50')
lhca.place(x=55,y=410)
ehca=Entry(homeFrame,bd=5,textvariable=hcz,width=12)
ehca.place(x=285,y=410)
ehcap=Entry(homeFrame,bd=5,textvariable=hczx,width=11)
ehcap.place(x=375,y=410)
lhcp = Label(homeFrame, text='POINTS', font='50')
lhcp.place(x=55,y=450)
ehcp=Entry(homeFrame,bd=5,textvariable=hcp,width=25)
ehcp.place(x=285,y=450)
# lhcp = Label(homeFrame, text='POINTS', font='50')
# lhcp.place(x=55,y=450)
# ehcp=Entry(homeFrame,bd=5,width=25)
# ehcp.place(x=155,y=450)

Bcup = Button(homeFrame, command=updateCust, bg='black',font='Helvetica 10 bold',activeforeground='blue', fg='white',text ="UPDATE", width=20, relief=RAISED)
Bcup.place(x=75,y=510)
Bcdel = Button(homeFrame,command=deleteCust, bg='black', font='Helvetica 10 bold', activeforeground='red', fg='white',
                 text="DELETE", width=20, relief=RAISED)
Bcdel.place(x=245,y=510)

lablee1= Label(homeFrame, text ='Electrician', font = "Helvetica 20 underline")
lablee1.place(x=500, y=280)

lhen = Label(homeFrame, text='NAME', font='50')
lhen.place(x=505,y=330)
ehen=Entry(homeFrame,bd=5,textvariable=hen,width=25)
ehen.place(x=735, y=330)
lhem = Label(homeFrame, text='MOBILE_NO', font='50')
lhem.place(x=505,y=370)
ehem=Entry(homeFrame,bd=5,textvariable=hem,width=25)
ehem.place(x=735,y=370)
lhep = Label(homeFrame, text='AMOUNT', font='50')
lhep.place(x=505,y=410)
ehep=Entry(homeFrame,textvariable=hep,bd=5,width=25)
ehep.place(x=735,y=410)
# lhep = Label(homeFrame, text='AMMOUNT', font='50')
# lhep.place(x=365,y=450)
# ehep=Entry(homeFrame,bd=5,width=25)
# ehep.place(x=475,y=450)

Beup = Button(homeFrame, command=updateElec, bg='black',font='Helvetica 10 bold',activeforeground='blue', fg='white',text ="UPDATE", width=20, relief=RAISED)
Beup.place(x=530,y=470)
Bedel = Button(homeFrame,command=deleteElec, bg='black', font='Helvetica 10 bold', activeforeground='red', fg='white',
                 text="DELETE", width=20, relief=RAISED)
Bedel.place(x=700,y=470)

lables1= Label(homeFrame, text ='Subscription', font = "Helvetica 20 underline")
lables1.place(x=50, y=560)

subscriptionsScroll = Scrollbar(homeFrame)


subscriptionsTable = ttk.Treeview(homeFrame, yscrollcommand=subscriptionsScroll.set, height =4)
subscriptionsScroll.config(orient="vertical",command=subscriptionsTable.yview)
subscriptionsScroll.place(x=730+5+5, y=600,height=108)
subscriptionsTable['columns'] = ('NAME', 'MOBILE', 'YEARS',  'ITEM', 'AMOUNT', 'DATE')

subscriptionsTable.column("#0", width=0, stretch=NO)
subscriptionsTable.column("NAME", anchor=CENTER, width=140)
subscriptionsTable.column("MOBILE", anchor=CENTER, width=145)
subscriptionsTable.column("YEARS", anchor=CENTER, width=50)
subscriptionsTable.column("ITEM", anchor=CENTER, width=135)
subscriptionsTable.column("AMOUNT", anchor=CENTER, width=110)
subscriptionsTable.column("DATE", anchor=CENTER, width=100)


subscriptionsTable.heading("#0", text="", anchor=CENTER)
subscriptionsTable.heading("NAME", text="NAME", anchor=CENTER)
subscriptionsTable.heading("MOBILE", text="MOBILE", anchor=CENTER)
subscriptionsTable.heading("YEARS", text="YEARS", anchor=CENTER)
subscriptionsTable.heading("ITEM", text="ITEM", anchor=CENTER)
subscriptionsTable.heading("AMOUNT", text="AMOUNT", anchor=CENTER)
subscriptionsTable.heading("DATE", text="DATE", anchor=CENTER)


#fetchAllSubscriptions(con)

Bsdel = Button(homeFrame, bg='black',command=deleteSubs, font='Helvetica 10 bold', activeforeground='red', fg='white',
                 text="DELETE", width=20, relief=RAISED)
Bsdel.place(x=780,y=620)

Bclear = Button(homeFrame,bg='black',command=clear,font='Helvetica 10 bold',activeforeground='blue', fg='white',text ="CLEAR", width=20, relief=RAISED)
Bclear.place(x= 780, y=660)



subscriptionsTable.place(x=55, y=600)






###################       CUSTOMER TAB      ############################
addCustomerFrame=Frame(tab2, relief=SUNKEN)
addCustomerFrame.pack(fill=BOTH, expand=True)
#sqlite 3 database started hare

c.execute("CREATE TABLE if not exists Customers(id integer PRIMARY  KEY AUTOINCREMENT NOT NULL, name text NOT NULL, mobile_no text NOT NULL UNIQUE, ammount text NOT NULL, points integer NOT NULL, updated_date timestamp)")
con.commit()

def refreshCustomer():
    deleteCustomerTable()
    fetchAllCustomers(con)
    Bcu['state'] = 'disabled'
    Bcu.config(bg='SystemButtonFace')
    Bca.config(bg='black')
    Bca['state'] = 'normal'
    ecp.unbind('<Return>')
    ecn.unbind('<Return>')
    ecm.unbind('<Return>')
    eca.unbind('<Return>')
    ecap.unbind('<Return>')
    ecap['state'] = "disabled"
    eca['state'] = "normal"
    ecp.bind('<Return>', addCustomersData)
    eca.bind('<Return>', addCustomersData)
    cn.set("")
    cm.set("")
    ca.set("")
    cp.set("")
    ci.set("")
    cap.set("")
    ecn.focus_set()

def deleteCustomerTable():
    tables = customerTable.get_children()
    for table in tables:
        customerTable.delete(table)


def addCustomersData(event=None):

    if (ecn.get().strip()=="" or ecm.get().strip()=="" or eca.get().strip()==""):
        messagebox.showinfo('Notice', 'Please Fill All Entries')
    else:
        ammount = eca.get()
        value = calculateCustomerPoints(int(ammount))
        points = value[0]
        cp.set('')
        ecp.insert(0, points)
        ecp.focus_set()
        entries=(
        ecn.get(),
        ecm.get(),
        value[1],
        points,
        datetime.now())
        try:
            c.execute('''INSERT INTO Customers(name, mobile_no, ammount, points, updated_date) VALUES(?,?,?,?,?)''',entries)
            con.commit()
        except:
            messagebox.showinfo('Notice', 'The Mobile No. is Already Added or You Entered something Wrong')

        else:
            deleteCustomerTable()
            fetchAllCustomers(con)
            #customerTable.insert("", index='end',text="", values=(eci.get(),ecn.get(),ecm.get(),ecp.get()))
            messagebox.showinfo('Notice', 'Customer Added Successfully with ' + str(points) + ' points')
            cn.set("")
            cm.set("")
            cp.set("")
            ci.set("")
            ca.set("")
            cap.set("")

            ecn.focus_set()



def editCustomer():
    eci['state']='normal'
    cn.set("")
    cm.set("")
    cp.set("")
    ca.set("")
    ci.set("")
    selected = customerTable.focus()
    values = customerTable.item(selected, 'values')
    eci.insert(0, values[0])
    eci['state'] = 'disabled'
    ecn.insert(0, values[1])
    ecm.insert(0, values[2])
    eca.insert(0, values[3])
    ecp.insert(0, values[4])
    ecap['state'] = 'normal'
    ecn.focus_set()
    Bca.config(bg='SystemButtonFace')
    Bca['state']='disabled'
    Bcu['state']='normal'
    Bcu['bg']='black'
    ecp.unbind('<Return>')
    ecn.bind('<Return>', updateCustomersData)
    ecm.bind('<Return>', updateCustomersData)
    ecap.bind('<Return>', updateCustomersData)
    ecp.bind('<Return>', updateCustomersData)

def extraFunction():
    selected1 = customerTable.focus()
    value = customerTable.item(selected1, 'value')
    return value[2]

def updateCustomersData(event=None):
    mobile=extraFunction()
    ammount = eca.get()
    newammount = ecap.get()
    value = calculateCustomerPoints(int(ammount), int(newammount))
    points = value[0]

    cp.set("")
    ecp.insert(0, points)
    ecp.focus_set()
    data=(
        ecn.get(),
        ecm.get(),
        value[1],
        points,
        datetime.now()
    )

    c.execute("UPDATE Customers SET (name, mobile_no, ammount, points, updated_date)=(?,?,?,?,?) WHERE mobile_no=?",(data[0],data[1],data[2],data[3],data[4],mobile))
    con.commit()
    selected2 = customerTable.focus()
    # save new data
    customerTable.item(selected2, text="", values=(eci.get(),ecn.get(), ecm.get(),eca.get(), points))
    deleteCustomerTable()
    fetchAllCustomers(con)
    messagebox.showinfo("Notice", "Updated Successfully")
    Bcu['state'] = 'disabled'
    Bcu.config(bg='SystemButtonFace')
    Bca.config(bg='black')
    Bca['state'] = 'normal'
    ecp.unbind('<Return>')
    ecn.unbind('<Return>')
    ecm.unbind('<Return>')
    eca.unbind('<Return>')
    ecap.unbind('<Return>')
    ecap['state']="disabled"
    eca['state'] = "normal"
    ecp.bind('<Return>', addCustomersData)
    eca.bind('<Return>', addCustomersData)
    cn.set("")
    cm.set("")
    ca.set("")
    cp.set("")
    ci.set("")
    cap.set("")
    ecn.focus_set()

def deleteCustomer():
    try:
        mobile=extraFunction()
    except:
        messagebox.showinfo('notice', 'anything is not selected for delete')
    else:
        x=customerTable.selection()[0]
        customerTable.delete(x)

        c.execute('DELETE FROM Customers WHERE mobile_no=?', (mobile,))
        con.commit()
        deleteCustomerTable()
        fetchAllCustomers(con)
        messagebox.showinfo('notice',"Deleted Successfully")
        ecn.focus_set()


def fetchAllCustomers(con):

    c.execute('SELECT * FROM Customers ORDER BY updated_date DESC ')
    rows = c.fetchall()
    count =0
    for row in rows:
        count=count+1
    j=count
    for i in range(0, j):
        customerTable.insert(parent='', index='end', iid=j, text='', values=(j, rows[i][1], rows[i][2], rows[i][3], rows[i][4]))
        j=j-1



customerScroll = Scrollbar(addCustomerFrame)


customerTable = ttk.Treeview(addCustomerFrame, yscrollcommand=customerScroll.set, height =15)
customerScroll.config(orient="vertical",command=customerTable.yview)
customerScroll.place(x=80+200+200+100+100+5, y=350,height=329)
customerTable['columns'] = ('ID','NAME', 'MOBILE', 'AMOUNT', 'POINTS')

customerTable.column("#0", width=0, stretch=NO)
customerTable.column("ID", anchor=CENTER, width=60)
customerTable.column("NAME", anchor=CENTER, width=150)
customerTable.column("MOBILE", anchor=CENTER, width=150)
customerTable.column("AMOUNT", anchor=CENTER, width=120)
customerTable.column("POINTS", anchor=CENTER, width=100)


customerTable.heading("#0", text="", anchor=CENTER)
customerTable.heading("ID", text="ID", anchor=CENTER)
customerTable.heading("NAME", text="NAME", anchor=CENTER)
customerTable.heading("MOBILE", text="MOBILE", anchor=CENTER)
customerTable.heading("AMOUNT", text="AMOUNT", anchor=CENTER)
customerTable.heading("POINTS", text="POINTS", anchor=CENTER)


fetchAllCustomers(con)


Bcedit = Button(addCustomerFrame,command=editCustomer,bg='black', font='Helvetica 10 bold',
                 activeforeground='blue', fg='white', text="EDIT", width=20, relief=RAISED)
Bcedit.place(x=710,y=440)
Bcdelete = Button(addCustomerFrame,command=deleteCustomer, bg='black', font='Helvetica 10 bold', activeforeground='red', fg='white',
                 text="DELETE", width=20, relief=RAISED)
Bcdelete.place(x=710,y=480)
Bcrefresh = Button(addCustomerFrame,command=refreshCustomer, bg='black', font='Helvetica 10 bold', activeforeground='blue', fg='white',
                 text="REFRESH", width=20, relief=RAISED)
Bcrefresh.place(x=710,y=520)



customerTable.place(x=100, y=350)






#c.execute('drop table if exists Customers')
#con.commit()



lable_c=Label(addCustomerFrame, text='ADD CUSTOMER', font='Helvetica 18 bold' )
lable_c.place(x=380, y=10)

cn = StringVar()
cm = StringVar()
cp = StringVar()
ca = StringVar()
ci = StringVar()
cap = IntVar()

lci= Label(addCustomerFrame, text ='ID', font = "50")
lci.place(x=320, y=60)
eci = Entry(addCustomerFrame,textvariable=ci,bd=5, width=5)
eci['state']= "disabled"
eci.place(x= 550,y=60)

lcn= Label(addCustomerFrame, text ='NAME', font = "50")
lcn.place(x=320, y=100)
ecn = Entry(addCustomerFrame,textvariable=cn,bd=5, width=25)
ecn.place(x= 550,y=100)
ecn.focus_set()

lcm= Label(addCustomerFrame, text ='MOBILE_NO', font = "50")
lcm.place(x=320, y=140)
ecm = Entry(addCustomerFrame,textvariable=cm,bd=5, width=25)
ecm.place(x=550,y=140)

lca= Label(addCustomerFrame, text ='AMOUNT', font = "50")
lca.place(x=320, y=180)
eca = Entry(addCustomerFrame,textvariable=ca,bd=5, width=25)
eca.place(x=550,y=180)
ecap = Entry(addCustomerFrame,textvariable=cap,bd=5, width=25)
ecap.place(x=730,y=180)
ecap['state'] = 'disabled'

lcp= Label(addCustomerFrame, text ='POINTS', font = "50")
lcp.place(x=320,y=220)
ecp = Entry(addCustomerFrame,textvariable=cp,bd=5, width=25)
ecp.place(x=550,y=220)


Bca = Button(addCustomerFrame, command=addCustomersData, bg='black',font='Helvetica 10 bold',activeforeground='green', fg='white',text ="ADD", width=20, relief=RAISED)
Bca.place(x= 340, y=280)
Bcu = Button(addCustomerFrame,command=updateCustomersData,font='Helvetica 10 bold',activeforeground='green', fg='white',text ="UPDATE", width=20, relief=RAISED)
Bcu.place(x= 510, y=280)
#Bcu['state']='disabled'

#less required code
if (Bca['state']=='normal'):
    Bcu['state']='disabled'
    eca.bind('<Return>',addCustomersData)
    ecp.bind('<Return>', addCustomersData)
#not required code
elif (Bcu['state']=='normal'):
    Bca['state'] = 'disabled'
    ecp.unbind('<Return>')
    ecp.bind('<Return>', updateCustomersData)






##########################    SUBSCRIPTION tab    ########################################

addSubscriptionFrame=Frame(tab4, relief=SUNKEN)
addSubscriptionFrame.pack(fill=BOTH, expand=True)

c.execute("CREATE TABLE if not exists Subscriptions(id integer PRIMARY  KEY AUTOINCREMENT NOT NULL, name text NOT NULL, mobile_no text NOT NULL, years integer NOT NULL,item text NOT NULL, ammount text NOT NULL, date text NOT NULL, updated_date timestamp)")
con.commit()

def deleteSubscriptionTable():
    tables = subscriptionTable.get_children()
    for table in tables:
        subscriptionTable.delete(table)


def addSubscriptionsData(event=None):

    if (esn.get().strip()=="" or esm.get().strip()=="" or esy.get().strip()=="" or esa.get().strip()==""
            or esg.get().strip() == ""):
        messagebox.showinfo('Notice', 'Please Fill All Entries')
    else:
        entries=(
        esn.get(),
        esm.get(),
        esy.get(),
        esg.get(),
        esa.get(),
        date.today(),
        datetime.now())
        #try:
        c.execute('''INSERT INTO Subscriptions(name, mobile_no, years, item, ammount, date, updated_date) VALUES(?,?,?,?,?,?,?)''',entries)
        con.commit()
        #except:
            #messagebox.showinfo('Notice', 'The Mobile No. is Already Added or You Entered something Wrong')


        deleteSubscriptionTable()
        fetchAllSubscriptions(con)
        #customerTable.insert("", index='end',text="", values=(eci.get(),ecn.get(),ecm.get(),ecp.get()))
        messagebox.showinfo('Notice', 'Subscription Added Successfully')
        sn.set("")
        sm.set("")
        sy.set("")
        si.set("")
        sa.set("")
        sg.set("")
        esn.focus_set()

# def editSubscription():
#     esi['state']='normal'
#     sn.set("")
#     sm.set("")
#     sy.set("")
#     si.set("")
#     sa.set("")
#     sg.set("")
#     selected = subscriptionTable.focus()
#     values = subscriptionTable.item(selected, 'values')
#     esi.insert(0, values[0])
#     esi['state'] = 'disabled'
#     esn.insert(0, values[1])
#     esm.insert(0, values[2])
#     esy.insert(0, values[3])
#     esg.insert(0, values[4])
#     esa.insert(0, values[5])
#     esn.focus_set()
#     Bsa.config(bg='SystemButtonFace')
#     Bsa['state']='disabled'
#     Bsu['state']='normal'
#     Bsu['bg']='black'
#     esy.unbind('<Return>')
#     esn.bind('<Return>', updateSubscriptionsData)
#     esm.bind('<Return>', updateSubscriptionsData)
#     esy.bind('<Return>', updateSubscriptionsData)
#     esg.bind('<Return>', updateSubscriptionsData)
#     esa.bind('<Return>', updateSubscriptionsData)

def extraFunction2():
    selected1 = subscriptionTable.focus()
    value = subscriptionTable.item(selected1, 'value')
    return value[6]

def refreshSubscription():
    deleteSubscriptionTable()
    fetchAllSubscriptions(con)

# def updateSubscriptionsData(event=None):
#     mobile=extraFunction2()
#
#     data=(
#         esn.get(),
#         esm.get(),
#         esy.get(),
#         esg.get(),
#         esa.get(),
#         date.today(),
#         datetime.now()
#     )
#
#     c.execute("UPDATE Subscriptions SET (name, mobile_no, Years, updated_date)=(?,?,?,?) WHERE mobile_no=?",(data[0],data[1],data[2],data[3],mobile))
#     con.commit()
#     selected2 = subscriptionTable.focus()
#     # save new data
#     subscriptionTable.item(selected2, text="", values=(esi.get(),esn.get(), esm.get(), esy.get()))
#     messagebox.showinfo("Notice", "Updated Successfully")
#     Bsu['state'] = 'disabled'
#     Bsu.config(bg='SystemButtonFace')
#     Bsa.config(bg='black')
#     Bsa['state'] = 'normal'
#     esy.unbind('<Return>')
#     esn.unbind('<Return>')
#     esm.unbind('<Return>')
#     esg.unbind('<Return>')
#     esa.unbind('<Return>')
#     esy.bind('<Return>', addSubscriptionsData)
#     sn.set("")
#     sm.set("")
#     sy.set("")
#     si.set("")
#     sg.set("")
#     sa.set("")
#     esn.focus_set()

def deleteSubscription():
    try:
        updated_date=extraFunction2()
    except:
        messagebox.showinfo('notice', 'anything is not selected for delete')
    else:
        x=subscriptionTable.selection()[0]
        subscriptionTable.delete(x)

        c.execute('DELETE FROM Subscriptions WHERE updated_date=?', (updated_date,))
        con.commit()
        deleteSubscriptionTable()
        fetchAllSubscriptions(con)
        messagebox.showinfo('notice',"Deleted Successfully")
        esn.focus_set()


def fetchAllSubscriptions(con):

    c.execute('SELECT * FROM Subscriptions ORDER BY updated_date DESC ')
    rows = c.fetchall()
    count =0
    for row in rows:
        count=count+1
    j=count
    for i in range(0, j):
        subscriptionTable.insert(parent='', index='end', iid=j, text='', values=(j, rows[i][1], rows[i][2], rows[i][3], rows[i][4], rows[i][5], rows[i][7]))
        j=j-1



subscriptionScroll = Scrollbar(addSubscriptionFrame)


subscriptionTable = ttk.Treeview(addSubscriptionFrame, yscrollcommand=subscriptionScroll.set, height =12)
subscriptionScroll.config(orient="vertical",command=subscriptionTable.yview)
subscriptionScroll.place(x=730+5, y=400,height=271)
subscriptionTable['columns'] = ('ID','NAME', 'MOBILE', 'YEARS',  'ITEM','AMOUNT', 'DATE')

subscriptionTable.column("#0", width=0, stretch=NO)
subscriptionTable.column("ID", anchor=CENTER, width=40)
subscriptionTable.column("NAME", anchor=CENTER, width=130)
subscriptionTable.column("MOBILE", anchor=CENTER, width=135)
subscriptionTable.column("YEARS", anchor=CENTER, width=50)
subscriptionTable.column("ITEM", anchor=CENTER, width=125)
subscriptionTable.column("AMOUNT", anchor=CENTER, width=100)
subscriptionTable.column("DATE", anchor=CENTER, width=100)


subscriptionTable.heading("#0", text="", anchor=CENTER)
subscriptionTable.heading("ID", text="ID", anchor=CENTER)
subscriptionTable.heading("NAME", text="NAME", anchor=CENTER)
subscriptionTable.heading("MOBILE", text="MOBILE", anchor=CENTER)
subscriptionTable.heading("YEARS", text="YEARS", anchor=CENTER)
subscriptionTable.heading("ITEM", text="ITEM", anchor=CENTER)
subscriptionTable.heading("AMOUNT", text="AMOUNT", anchor=CENTER)
subscriptionTable.heading("DATE", text="DATE", anchor=CENTER)


fetchAllSubscriptions(con)


# Bsedit = Button(addSubscriptionFrame,command=editSubscription,bg='black', font='Helvetica 10 bold',
#                  activeforeground='blue', fg='white', text="EDIT", width=20, relief=RAISED)
# Bsedit.place(x=710,y=440)
Bsdelete = Button(addSubscriptionFrame,command=deleteSubscription, bg='black', font='Helvetica 10 bold', activeforeground='red', fg='white',
                 text="DELETE", width=20, relief=RAISED)
Bsdelete.place(x=780,y=450)
Bsrefresh = Button(addSubscriptionFrame,command=refreshSubscription, bg='black', font='Helvetica 10 bold', activeforeground='red', fg='white',
                 text="REFRESH", width=20, relief=RAISED)
Bsrefresh.place(x=780,y=490)





subscriptionTable.place(x=50, y=400)


lable_s=Label(addSubscriptionFrame, text='ADD SUBSCRIPTION', font='Helvetica 18 bold' )
lable_s.place(x=380, y=10)

sn = StringVar()
sm = StringVar()
sy = IntVar()
si = StringVar()
sg = StringVar()
sa = StringVar()

lsi= Label(addSubscriptionFrame, text ='ID', font = "50")
lsi.place(x=320, y=60)
esi = Entry(addSubscriptionFrame,textvariable=si,bd=5, width=5)
esi['state']= "disabled"
esi.place(x= 550,y=60)

lsn= Label(addSubscriptionFrame, text ='NAME', font = "50")
lsn.place(x=320, y=100)
esn = Entry(addSubscriptionFrame,textvariable=sn,bd=5, width=25)
esn.place(x= 550,y=100)
esn.focus_set()

lsm= Label(addSubscriptionFrame, text ='MOBILE_NO', font = "50")
lsm.place(x=320, y=140)
esm = Entry(addSubscriptionFrame,textvariable=sm,bd=5, width=25)
esm.place(x=550,y=140)

lsg= Label(addSubscriptionFrame, text ='ITEM', font = "50")
lsg.place(x=320, y=180)
esg = Entry(addSubscriptionFrame,textvariable=sg,bd=5, width=25)
esg.place(x=550,y=180)

lsa= Label(addSubscriptionFrame, text ='AMOUNT', font = "50")
lsa.place(x=320, y=220)
esa = Entry(addSubscriptionFrame,textvariable=sa,bd=5, width=25)
esa.place(x=550,y=220)

lsy= Label(addSubscriptionFrame, text ='YEARS', font = "50")
lsy.place(x=320,y=260)
esy = Entry(addSubscriptionFrame,textvariable=sy,bd=5, width=25)
esy.place(x=550,y=260)
esy.bind('<Return>',addSubscriptionsData)

Bsa = Button(addSubscriptionFrame, command=addSubscriptionsData, bg='black',font='Helvetica 10 bold',activeforeground='green', fg='white',text ="ADD", width=20, relief=RAISED)
Bsa.place(x= 420, y=320)
# Bsu = Button(addSubscriptionFrame,font='Helvetica 10 bold',activeforeground='green', fg='white',text ="UPDATE", width=20, relief=RAISED)
# Bsu.place(x= 510, y=320)



#less required code
# if (Bsa['state']=='normal'):
#     print('yes')
#     #Bsu['state']='disabled'
#     esy.bind('<Return>',addSubscriptionsData)
# #not required code
# elif (Bsu['state']=='normal'):
#     print('no')
#     Bsa['state'] = 'disabled'
#     ecp.unbind('<Return>')
#     #ecp.bind('<Return>', updateSubscriptionsData)



########################       electricians tab         ##############################

addElectriciansFrame=Frame(tab3, relief=SUNKEN)
addElectriciansFrame.pack(fill=BOTH, expand=True)

c.execute("CREATE TABLE if not exists Electricians(id integer PRIMARY  KEY AUTOINCREMENT NOT NULL, name text NOT NULL, mobile_no text NOT NULL UNIQUE, points integer NOT NULL, updated_date timestamp)")
con.commit()

def refreshElectrician():
    deleteElectriciansTable()
    fetchAllElectricians(con)
    Beu['state'] = 'disabled'
    Beu.config(bg='SystemButtonFace')
    Bea.config(bg='black')
    Bea['state'] = 'normal'
    eep.unbind('<Return>')
    een.unbind('<Return>')
    eem.unbind('<Return>')
    eep.bind('<Return>', addElectriciansData)
    en.set("")
    em.set("")
    ep.set("")
    ei.set("")
    een.focus_set()

def deleteElectriciansTable():
    tables = electricianTable.get_children()
    for table in tables:
        electricianTable.delete(table)


def addElectriciansData(event=None):

    if (een.get().strip()=="" or eem.get().strip()=="" or eep.get().strip()==""):
        messagebox.showinfo('Notice', 'Please Fill All Entries')
    else:
        entries=(
        een.get(),
        eem.get(),
        eep.get(),
        datetime.now())
        try:
            c.execute('''INSERT INTO Electricians(name, mobile_no, points, updated_date) VALUES(?,?,?,?)''',entries)
            con.commit()
        except:
            messagebox.showinfo('Notice', 'The Mobile No. is Already Added or You Entered something Wrong')

        else:
            deleteElectriciansTable()
            fetchAllElectricians(con)
            #customerTable.insert("", index='end',text="", values=(eci.get(),ecn.get(),ecm.get(),ecp.get()))
            messagebox.showinfo('Notice', 'Electrician Added Successfully with ' + eep.get() + ' Ammount')
            en.set("")
            em.set("")
            ep.set("")
            ei.set("")
            een.focus_set()

def extraFunction1():
    selected1 = electricianTable.focus()
    value = electricianTable.item(selected1, 'value')
    return value[2]

def editElectrician():
    eei['state']='normal'
    en.set("")
    em.set("")
    ep.set("")
    ei.set("")
    selected = electricianTable.focus()
    values = electricianTable.item(selected, 'values')
    eei.insert(0, values[0])
    eei['state'] = 'disabled'
    een.insert(0, values[1])
    eem.insert(0, values[2])
    eep.insert(0, values[3])
    een.focus_set()
    Bea.config(bg='SystemButtonFace')
    Bea['state']='disabled'
    Beu['state']='normal'
    Beu['bg']='black'
    eep.unbind('<Return>')
    een.bind('<Return>', updateElectriciansData)
    eem.bind('<Return>', updateElectriciansData)
    eep.bind('<Return>', updateElectriciansData)

def updateElectriciansData(event=None):
    mobile=extraFunction1()

    data=(
        een.get(),
        eem.get(),
        eep.get(),
        datetime.now()
    )

    c.execute("UPDATE Electricians SET (name, mobile_no, points, updated_date)=(?,?,?,?) WHERE mobile_no=?",(data[0],data[1],data[2],data[3],mobile))
    con.commit()
    selected2 = electricianTable.focus()
    # save new data
    electricianTable.item(selected2, text="", values=(eei.get(),een.get(), eem.get(), eep.get()))
    deleteElectriciansTable()
    fetchAllElectricians(con)
    messagebox.showinfo("Notice", "Updated Successfully")
    Beu['state'] = 'disabled'
    Beu.config(bg='SystemButtonFace')
    Bea.config(bg='black')
    Bea['state'] = 'normal'
    eep.unbind('<Return>')
    een.unbind('<Return>')
    eem.unbind('<Return>')
    eep.bind('<Return>', addElectriciansData)
    en.set("")
    em.set("")
    ep.set("")
    ei.set("")
    een.focus_set()

def deleteElectrician():
    try:
        mobile=extraFunction1()
    except:
        messagebox.showinfo('notice', 'anything is not selected for delete')
    else:
        x=electricianTable.selection()[0]
        electricianTable.delete(x)

        c.execute('DELETE FROM Electricians WHERE mobile_no=?', (mobile,))
        con.commit()
        deleteElectriciansTable()
        fetchAllElectricians(con)
        messagebox.showinfo('notice',"Deleted Successfully")
        een.focus_set()

def fetchAllElectricians(con):

    c.execute('SELECT * FROM Electricians ORDER BY updated_date DESC ')
    rows = c.fetchall()
    count = 0
    for row in rows:
        count = count + 1
    j = count
    for i in range(0, j):
        electricianTable.insert(parent='', index='end', iid=j, text='', values=(j, rows[i][1], rows[i][2], rows[i][3]))
        j=j-1



electricianScroll = Scrollbar(addElectriciansFrame)


electricianTable = ttk.Treeview(addElectriciansFrame, yscrollcommand=electricianScroll.set, height =15)
electricianScroll.config(orient="vertical",command=electricianTable.yview)
electricianScroll.place(x=80+200+200+100+100+5, y=350,height=329)
electricianTable['columns'] = ('ID','NAME', 'MOBILE', 'AMOUNT')

electricianTable.column("#0", width=0, stretch=NO)
electricianTable.column("ID", anchor=CENTER, width=80)
electricianTable.column("NAME", anchor=CENTER, width=150)
electricianTable.column("MOBILE", anchor=CENTER, width=200)
electricianTable.column("AMOUNT", anchor=CENTER, width=150)


electricianTable.heading("#0", text="", anchor=CENTER)
electricianTable.heading("ID", text="ID", anchor=CENTER)
electricianTable.heading("NAME", text="NAME", anchor=CENTER)
electricianTable.heading("MOBILE", text="MOBILE", anchor=CENTER)
electricianTable.heading("AMOUNT", text="AMOUNT", anchor=CENTER)


fetchAllElectricians(con)

Beedit = Button(addElectriciansFrame,command=editElectrician,bg='black', font='Helvetica 10 bold',
                 activeforeground='blue', fg='white', text="EDIT", width=20, relief=RAISED)
Beedit.place(x=710,y=440)
Bedelete = Button(addElectriciansFrame,command=deleteElectrician, bg='black', font='Helvetica 10 bold', activeforeground='red', fg='white',
                 text="DELETE", width=20, relief=RAISED)
Bedelete.place(x=710,y=480)
Berefresh = Button(addElectriciansFrame,command=refreshElectrician, bg='black', font='Helvetica 10 bold', activeforeground='blue', fg='white',
                 text="REFRESH", width=20, relief=RAISED)
Berefresh.place(x=710,y=520)



electricianTable.place(x=100, y=350)


lable_e=Label(addElectriciansFrame, text='ADD ELECTRICIAN', font='Helvetica 18 bold' )
lable_e.place(x=380, y=10)

en = StringVar()
em = StringVar()
ep = IntVar()
ei = StringVar()

lei= Label(addElectriciansFrame, text ='ID', font = "50")
lei.place(x=320, y=60)
eei = Entry(addElectriciansFrame,textvariable=ei,bd=5, width=5)
eei['state']= "disabled"
eei.place(x= 550,y=60)

len= Label(addElectriciansFrame, text ='NAME', font = "50")
len.place(x=320, y=100)
een = Entry(addElectriciansFrame,bd=5,textvariable=en, width=25)
een.place(x= 550,y=100)
een.focus_set()

lem= Label(addElectriciansFrame, text ='MOBILE_NO', font = "50")
lem.place(x=320, y=140)
eem= Entry(addElectriciansFrame,bd=5,textvariable=em, width=25)
eem.place(x=550,y=140)

lep= Label(addElectriciansFrame, text ='SALE AMOUNT', font = "50")
lep.place(x=320,y=180)
eep = Entry(addElectriciansFrame,bd=5,textvariable=ep, width=25)
eep.place(x=550,y=180)

Bea = Button(addElectriciansFrame,bg='black',command=addElectriciansData ,font='Helvetica 10 bold',activeforeground='green', fg='white',text ="ADD", width=20, relief=RAISED)
Bea.place(x= 340, y=240)
Beu = Button(addElectriciansFrame,command=updateElectriciansData,font='Helvetica 10 bold',activeforeground='green', fg='white',text ="UPDATE", width=20, relief=RAISED)
Beu.place(x= 510, y=240)

#less required code
if (Bea['state']=='normal'):
    Beu['state']='disabled'
    eep.bind('<Return>',addElectriciansData)
#not required code
elif (Beu['state']=='normal'):
    Bea['state'] = 'disabled'
    eep.unbind('<Return>')
    eep.bind('<Return>', updateElectriciansData)

################################# ELECTRICIAN ADDRESSES    ##################################



electricianAddressFrame=Frame(tab5, relief=SUNKEN)
electricianAddressFrame.pack(fill=BOTH, expand=True)
#sqlite 3 database started hare

c.execute("CREATE TABLE if not exists ADDRESSES(id integer PRIMARY  KEY AUTOINCREMENT NOT NULL, name text NOT NULL, mobile_no text NOT NULL UNIQUE, address text NOT NULL, updated_date timestamp)")
con.commit()

def deleteElecstricianAddressTable():
    tables = elecstricianAddressTable.get_children()
    for table in tables:
        elecstricianAddressTable.delete(table)


def addElectricianAddressData(event=None):

    if (eean.get().strip()=="" or eeam.get().strip()=="" or eeaa.get().strip()==""):
        messagebox.showinfo('Notice', 'Please Fill All Entries')
    else:
        entries=(
        eean.get(),
        eeam.get(),
        eeaa.get(),
        datetime.now())
        try:
            c.execute('''INSERT INTO ADDRESSES(name, mobile_no, address, updated_date) VALUES(?,?,?,?)''',entries)
            con.commit()
        except:
            messagebox.showinfo('Notice', 'The Mobile No. is Already Added or You Entered something Wrong')

        else:
            deleteElecstricianAddressTable()
            fetchAllElectricianAddress(con)
            #customerTable.insert("", index='end',text="", values=(eci.get(),ecn.get(),ecm.get(),ecp.get()))
            messagebox.showinfo('Notice', 'Address added Successfully')
            ean.set("")
            eam.set("")
            eaa.set("")
            eean.focus_set()

def extraFunction6():
    selected1 = elecstricianAddressTable.focus()
    value = elecstricianAddressTable.item(selected1, 'value')
    return value[2]
def deleteElectricianAddress():
    try:
        mobile=extraFunction6()
    except:
        messagebox.showinfo('notice', 'anything is not selected for delete')
    else:
        x=elecstricianAddressTable.selection()[0]
        elecstricianAddressTable.delete(x)

        c.execute('DELETE FROM ADDRESSES WHERE mobile_no=?', (mobile,))
        con.commit()
        deleteElecstricianAddressTable()
        fetchAllElectricianAddress(con)
        messagebox.showinfo('notice',"Deleted Successfully")
        eean.focus_set()


def fetchAllElectricianAddress(con):

    c.execute('SELECT * FROM ADDRESSES ORDER BY updated_date DESC ')
    rows = c.fetchall()
    count =0
    for row in rows:
        count=count+1
    j=count
    for i in range(0, j):
        elecstricianAddressTable.insert(parent='', index='end', iid=j, text='', values=(j, rows[i][1], rows[i][2], rows[i][3]))
        j=j-1



elecstricianAddressTableScroll = Scrollbar(electricianAddressFrame)


elecstricianAddressTable = ttk.Treeview(electricianAddressFrame, yscrollcommand=elecstricianAddressTableScroll.set, height =15)
elecstricianAddressTableScroll.config(orient="vertical",command=elecstricianAddressTable.yview)
elecstricianAddressTableScroll.place(x=80+200+200+100+100+5, y=350,height=329)
elecstricianAddressTable['columns'] = ('ID','NAME', 'MOBILE', 'ADDRESS')

elecstricianAddressTable.column("#0", width=0, stretch=NO)
elecstricianAddressTable.column("ID", anchor=CENTER, width=30)
elecstricianAddressTable.column("NAME", anchor=CENTER, width=150)
elecstricianAddressTable.column("MOBILE", anchor=CENTER, width=150)
elecstricianAddressTable.column("ADDRESS", anchor=CENTER, width=250)


elecstricianAddressTable.heading("#0", text="", anchor=CENTER)
elecstricianAddressTable.heading("ID", text="ID", anchor=CENTER)
elecstricianAddressTable.heading("NAME", text="NAME", anchor=CENTER)
elecstricianAddressTable.heading("MOBILE", text="MOBILE", anchor=CENTER)
elecstricianAddressTable.heading("ADDRESS", text="ADDRESS", anchor=CENTER)

elecstricianAddressTable.place(x=100, y=350)

fetchAllElectricianAddress(con)


Beadelete = Button(electricianAddressFrame,command=deleteElectricianAddress,bg='black', font='Helvetica 10 bold',
                 activeforeground='blue', fg='white', text="DELETE", width=20, relief=RAISED)
Beadelete.place(x=710,y=440)


lable_ea=Label(electricianAddressFrame, text='ADDRESS BOOK', font='Helvetica 18 bold' )
lable_ea.place(x=380, y=10)

ean = StringVar()
eam = StringVar()
eaa = StringVar()



lean= Label(electricianAddressFrame, text ='NAME', font = "50")
lean.place(x=320, y=60)
eean = Entry(electricianAddressFrame,textvariable=ean,bd=5, width=25)
eean.place(x= 550,y=60)
eean.focus_set()

leam= Label(electricianAddressFrame, text ='MOBILE_NO', font = "50")
leam.place(x=320, y=100)
eeam = Entry(electricianAddressFrame,textvariable=eam,bd=5, width=25)
eeam.place(x=550,y=100)

leaa= Label(electricianAddressFrame, text ='ADDRESS', font = "50")
leaa.place(x=320,y=140)
eeaa = Entry(electricianAddressFrame,textvariable=eaa,bd=5, width=50)
eeaa.place(x=550,y=140)
eeaa.bind('<Return>',addElectricianAddressData)


Beaa = Button(electricianAddressFrame, command=addElectricianAddressData, bg='black',font='Helvetica 10 bold',activeforeground='green', fg='white',text ="ADD", width=20, relief=RAISED)
Beaa.place(x= 420, y=200)




root.mainloop()