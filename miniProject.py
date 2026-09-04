from tkinter import *

root = Tk()
root.geometry("1000x500")
root.title("Bill Management Calculator")
root.resizable(False,False)

def Reset():
    entry_cookies.delete(0,END)
    entry_tea.delete(0,END)
    entry_coffee.delete(0,END)
    entry_juice.delete(0,END)
    entry_cake.delete(0,END)
    entry_curd.delete(0,END)
    entry_eggs.delete(0,END)

def Total():
    try : a1 = int(cookies.get())
    except : a1 = 0

    try : a2 = int(tea.get())
    except : a2 = 0

    try : a3 = int(coffee.get())
    except : a3 = 0

    try : a4 = int(juice.get())
    except : a4 = 0

    try : a5 = int(cake.get())
    except : a5 = 0

    try : a6 = int(curd.get())
    except : a6 = 0

    try : a7 = int(eggs.get())
    except : a7 = 0

                        # COST OF EACH ITEM/QUANTITY

    c1 = 40*a1
    c2 = 10*a2
    c3 = 15*a3
    c4 = 50*a4
    c5 = 350*a5
    c6 = 35*a6
    c7 = 10*a7

    lbl_total = Label(f2,font=("aria",20,"bold"),text="Total Amount :)",width=16,fg="lightyellow",bg="black")
    lbl_total.place(x=0,y=90)

    entry_total = Entry(f2,font=("aria",20,"bold"),textvariable=Total_bill,bd=6,width=15,bg="lightgreen")
    entry_total.place(x=20,y=150)

    totalCost = c1+c2+c3+c4+c5+c6+c7
    string_bill = "Rs.",str("%.2f" %totalCost)
    Total_bill.set(string_bill)

Label(text="Bill Management...",bg="black",fg="white",font=("Algerian",33),width="300",height="2").pack()

                     # MENU CARD

f = Frame(root, bg="lightgreen",highlightbackground="black",highlightthickness=1,width=300,height=370)
f.place(x=10,y=118)

Label(f,text="Menu",font=("Gabriola",40,"bold"),fg="black",bg="lightgreen").place(x=80,y=0)
Label(f,font=("Lucida Calligraphy",15,"bold"),text="Cookies.....Rs.40/plate",fg="black",bg="lightgreen").place(x=10,y=80)
Label(f,font=("Lucida Calligraphy",15,"bold"),text="Tea..........Rs.10/cup",fg="black",bg="lightgreen").place(x=10,y=110)
Label(f,font=("Lucida Calligraphy",15,"bold"),text="Coffee......Rs.15/cup",fg="black",bg="lightgreen").place(x=10,y=140)
Label(f,font=("Lucida Calligraphy",15,"bold"),text="Juice.......Rs.50/glass",fg="black",bg="lightgreen").place(x=10,y=170)
Label(f,font=("Lucida Calligraphy",15,"bold"),text="Cake........Rs.350/pack",fg="black",bg="lightgreen").place(x=10,y=200)
Label(f,font=("Lucida Calligraphy",15,"bold"),text="Curd........Rs.35/bowl",fg="black",bg="lightgreen").place(x=10,y=230)
Label(f,font=("Lucida Calligraphy",15,"bold"),text="Eggs........Rs.10/egg",fg="black",bg="lightgreen").place(x=10,y=260)

                    #BILL

f2 = Frame(root,bg="lightyellow",highlightbackground="black",highlightthickness=1,width=300,height=370)
f2.place(x=690, y=118)

Bill = Label(f2,text="Bill",font=("Gabriola",40,"bold"),bg="lightyellow")
Bill.place(x=120,y=10)


                     #ENTRY

f1 = Frame(root,bd=5,height=370,width=300,relief=GROOVE) 
f1.pack()

cookies = StringVar()
tea = StringVar()
coffee = StringVar()
juice= StringVar()
cake = StringVar()
curd = StringVar()
eggs = StringVar()
Total_bill = StringVar()

                     #LABEL

lbl_cookies = Label(f1,font=("aria",20,"bold"),text="Cookies",width=12,fg="blue4")
lbl_tea = Label(f1,font=("aria",20,"bold"),text="Tea",width=12,fg="blue4")
lbl_coffee = Label(f1,font=("aria",20,"bold"),text="Coffee",width=12,fg="blue4")
lbl_juice = Label(f1,font=("aria",20,"bold"),text="Juice",width=12,fg="blue4")
lbl_cake = Label(f1,font=("aria",20,"bold"),text="Cake",width=12,fg="blue4")
lbl_curd = Label(f1,font=("aria",20,"bold"),text="Curd",width=12,fg="blue4")
lbl_eggs = Label(f1,font=("aria",20,"bold"),text="Eggs",width=12,fg="blue4")
lbl_cookies.grid(row=1,column=0) 
lbl_tea.grid(row=2,column=0)
lbl_coffee.grid(row=3,column=0)
lbl_juice.grid(row=4,column=0)
lbl_cake.grid(row=5,column=0)
lbl_curd.grid(row=6,column=0)
lbl_eggs.grid(row=7,column=0)

entry_cookies=Entry(f1,font=("aria",20,"bold"),textvariable=cookies,bd=6,width=8,bg="lightpink")
entry_tea=Entry(f1,font=("aria",20,"bold"),textvariable=tea,bd=6,width=8,bg="lightpink")
entry_coffee=Entry(f1,font=("aria",20,"bold"),textvariable=coffee,bd=6,width=8,bg="lightpink")
entry_juice=Entry(f1,font=("aria",20,"bold"),textvariable=juice,bd=6,width=8,bg="lightpink")
entry_cake=Entry(f1,font=("aria",20,"bold"),textvariable=cake,bd=6,width=8,bg="lightpink")
entry_curd=Entry(f1,font=("aria",20,"bold"),textvariable=curd,bd=6,width=8,bg="lightpink")
entry_eggs=Entry(f1,font=("aria",20,"bold"),textvariable=eggs,bd=6,width=8,bg="lightpink")
entry_cookies.grid(row=1,column=1)
entry_tea.grid(row=2,column=1)
entry_coffee.grid(row=3,column=1)
entry_juice.grid(row=4,column=1)
entry_cake.grid(row=5,column=1)
entry_curd.grid(row=6,column=1)
entry_eggs.grid(row=7,column=1)

                       #BUTTONS
    
btn_reset = Button(f1,bd=5,fg="black",bg="lightblue",font=("ariel",16,"bold"),width=10,text="Reset",command=Reset)
btn_reset.grid(row=8,column=0)

btn_total = Button(f1,bd=5,fg="black",bg="lightblue",font=("ariel",16,"bold"),width=10,text="Total",command=Total)
btn_total.grid(row=8,column=1)
 
root.mainloop()
