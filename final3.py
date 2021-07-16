from tkinter import *
from tkinter import messagebox
import sqlite3

con = sqlite3.connect('database_kirill.db')
cursor = con.cursor()
#print("Подключен к SQLite")
with con:    
    cur = con.cursor()    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    #print (cur.fetchall())
    rows = cursor.fetchall()
    tables_suffix_list = [t for t in rows if t[0].endswith('_o')]

with con:    
    cur = con.cursor()
    cursor = con.execute('select * from suit_attributes')
    raws_in_attr = [description[0] for description in cursor.description]
    #print (raws_in_attr)

    
root = Tk()
f_top = Frame(root)
f_bot0 = Frame(root)
f_bot1 = Frame(root)


 
f_top.grid()
f_bot0.grid()
f_bot1.grid()

#update dropdown menu
paddle2_values =[''] *len(tables_suffix_list)

#getting values from menus
paddle_indexes =[''] *len(tables_suffix_list)
def OptionMenu_SelectionEvent(selection):


    paddle2_values.clear()
    
    for listvariables in range(0,len(radio_list)):
        paddle2_values.append(radio_list[listvariables].get())

    print (paddle2_values)
    
    paddle_indexes.clear()
    for i in paddle2_values:
        i= str(i)
        split_string = i. split(",", 1)
        substring = split_string[0]
        i = substring[1:]
        print (i)
        paddle_indexes.append(i)
        print (paddle_indexes)
    
OptionMenu_SelectionEvent
#dropdown menu
radio_list = []
list_of_raws_ordered = []

paddle_list =[] #for cleaning
for idx, table in enumerate(tables_suffix_list):
    for table in tables_suffix_list[idx]:
        with con:    
            cur = con.cursor()
            sql1 ="SELECT * FROM "
            sql2 =str(table)
            sql_select_query = sql1+sql2
            
            cursor.execute(sql_select_query)
            rows = cursor.fetchall()
            from_o_tables = rows
            variable = StringVar(root)
            variable.set("") # default value
            
            
            paddle2 = OptionMenu(f_top, variable, *from_o_tables, command = OptionMenu_SelectionEvent)
            paddle_list.append(variable)
            
            label_radio = Label(f_top, text=(table))
            radio_list.append(variable)
            list_of_raws_ordered.append(label_radio['text'])

    
    
    label_radio.grid(row=1, column=idx)

    paddle2.grid(row=0, column=idx)
print (radio_list)


counter = -1
counter_raws = 0

entries = []
final_entries = []
labels = []

#cleaning the 'o' list

banned_tables = list(map(''.join, tables_suffix_list))
banned_tables=[w[23:] for w in banned_tables]
#print (banned_tables)
#taht where we get 7 columns from menus
labels += banned_tables

#cleaning every paddle value

row_list =[] #for cleaning
for idx, n in enumerate(raws_in_attr):
    if n not in banned_tables:
        label = Label(f_bot0, text=[n])
        
        inputs = Entry(f_bot0)
        row_list.append(inputs)
        labels.append(n)
        entries.append(inputs)
    
        counter += 1
        if counter == 9:
            counter = 0
            counter_raws += 1
        label.grid(row=1+counter_raws*2, column=counter)
        inputs.grid(row=2+counter_raws*2, column=counter)
    
def writedata():
    try:
        final_entries.clear()
        

        for entry in entries:
            value = entry.get()
            final_entries.append(value)
            
        for label in labels:
            value = label
        
        with con:
            cur = con.cursor()
            sql1 ="INSERT INTO suit_attributes (" 
            sql_21 =  str(labels)[1:-1]
            sql2 = sql_21
            sql3 =") VALUES ("
            paddles = str(paddle_indexes)[1:-1]
            sql4 = str(final_entries)[1:-1]
            sql5 =");"
            
            sql_select_query = sql1+sql2+sql3+paddles+","+sql4+sql5
            print (sql_select_query)
            cursor.execute(sql_select_query)
            messagebox.showinfo("showinfo", "DATA SAVED")
    except sqlite3.IntegrityError:
        messagebox.showinfo("ERROR", "ERROR index")

a = Button (f_bot1, text ="Write data", command = writedata ).grid(row=12, column=1)



def cleandata():
    print (paddle_list)
    print (row_list)
    for n in row_list:
        n.delete(0, END)
    for z in paddle_list:
        z.set('') # default value

    #update dropdown menu
    paddle2_values =[''] *len(tables_suffix_list)

    #getting values from menus
    global paddle_indexes
    paddle_indexes.clear()
    paddle_indexes =[''] *len(tables_suffix_list)
    print('saved')
    print (saved_menus)
    print ('final ent')
    print(final_entries)
    print('paddle_ind')
    print(paddle_indexes)
    
b2 = Button ( f_bot1, text ="Clean data", command=cleandata ).grid(row=12, column=2)

saved_rows = [''] * len(row_list) #warning- unusable placeholders.
saved_menus =[''] *len(banned_tables) 

def savedata():
    paddle2_values.clear()
    
    for listvariables in range(0,len(radio_list)):
        paddle2_values.append(radio_list[listvariables].get())
        print('values')
        print (paddle2_values)
    saved_menus.clear()
    saved_rows.clear()
    # for i in paddle2_values:
        # i= str(i)
        # split_string = i. split(",", 1)
        # substring = split_string[0]
        # i = substring[1:]
        # print (i)
        # saved_menus.append(i)
    for n in row_list:
        value = n.get()
        saved_rows.append(value)
        print ("saved_buffer")
        print (saved_rows)
    for z in range(0,len(paddle_list)):
        saved_menus.append(paddle2_values[z])

    paddle_indexes = saved_menus
    print('saved_menus@@')
    print (saved_menus)
    print ('final ent')
    print(final_entries)
    print('paddle_ind')
    print(paddle_indexes)
        
    

c = Button ( f_bot1, text ="Save data", command = savedata  ).grid(row=12, column=3)



def restoredata():
    for n in range(0,len(row_list)):
        row_list[n].delete(0, END)
        row_list[n].insert(0, saved_rows[n])
        

        
    #paddle_indexes=saved_menus
        
    for z in range(0,len(saved_menus)):
        paddle_list[z].set(saved_menus[z])
    OptionMenu_SelectionEvent(selection)
    print('saved')
    print (saved_menus)
    print ('final ent')
    print(final_entries)
    print('paddle_ind')
    print(paddle_indexes)
    
d = Button ( f_bot1, text ="Restore data", command = restoredata ).grid(row=12, column=4)

var = StringVar()
var.trace("w", OptionMenu_SelectionEvent)
selection = OptionMenu_SelectionEvent(1)

root.mainloop()
