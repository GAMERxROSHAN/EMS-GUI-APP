#---->REQUIRED LIBRARYS
from tkinter import*
from tkinter.messagebox import*
from tkinter.scrolledtext import*
from sqlite3 import*
import requests
import csv
import matplotlib.pyplot as plt
import pandas as pd


#----->ADD, VIEW AND CHART FUNCTIONS
def f1():
	root.withdraw()
	aw.deiconify()
def f2():
	root.deiconify()
	aw.withdraw()
def f3():
	root.withdraw()
	vw.deiconify()
	vw_st_data.delete(1.0,END)
	con=None
	try:
		con=connect('EMS.db')
		cursor=con.cursor()
		sql='select * from employees order by id'
		cursor.execute(sql)
		data=cursor.fetchall()
		info=''
		for d in data:
			info=info+'id = '+str(d[0])+', name = '+str(d[1])+', salary = '+str(d[2])+'\n'
		vw_st_data.insert(INSERT,info)
	except ValueError:
		showerror('Error','Enter values correct')	
	except Exception as e:
		showerror('issue',e)
		
	finally:
		if con is not None:
			con.close()
def f33():
	root.withdraw()
	up.deiconify()
def f40():
	root.withdraw()
	delete.deiconify()
def f4():
	vw.withdraw()
	root.deiconify()
def f5():
	con=None
	try:
		con=connect('EMS.db')
		cursor=con.cursor()
		sql="insert into employees values('%d','%s','%d')"
		id=aw_ent_id.get()
		name=aw_ent_name.get()
		salary=aw_ent_salary.get()
		
		if id.isalpha() :
		    showerror('Failure','ID should be integers not in alphabets, It should be in +ve integers')
		elif len(id)==0:
			showerror('Failure','ID should not be empty, It should be in +ve integers')
		elif '-' in id:
		    showerror('Failure','ID should not be -ve, It should be in +ve integers')
		elif id.isdigit():
			id1=int(id)
			if id==0:
				showerror('Failure','ID should be +ve integer')
			else:
				if name.isdigit():
					showerror('Failure','Name shoulde be in alphabets not in numbers')
				elif len(name)==0:
					showerror('Failure','Name should not be empty')
				elif name.isalpha and len(name)<2:
					showerror('Failure','Name is too short , atleast it has 2 alphabets')
				elif name.isalpha() and len(name)>=2:
					if salary.isalpha() :
						showerror('Failure','Salary shoulde be in integers not in alphabets')
					elif len(salary)==0:
						showerror('Failure','Salary should not be empty')
					elif salary.isdigit():
						salary1=int(salary)
						if salary1<8000:
							showerror('Failure','Salary should not be less than 8000')
						elif salary1>8000:
							cursor.execute(sql%(id1,name,salary1))
							con.commit()
							showinfo('Success',str(id1)+' is succesfully added')
						else:
							showerror('Failure','Salary should be in +ve integers')
					else:
						showerror('Failure','Salary is invalid, It should be in +ve integers')
				else:
					showerror('Failure','Name is invalid , it should contain only alphabets')  
		elif id.isalnum():
			showerror('Failure','ID contain alphanumeric value, it should contain only +ve integers') 
		else:
			showerror('Failure','Enter Values Correct')
	except Exception as e:
		con.rollback()
		showerror('Failure',str(id1)+' Already Exists')

	finally:
		if con is not None:
			con.close()
		aw_ent_id.delete(0,END)
		aw_ent_name.delete(0,END)
		aw_ent_salary.delete(0,END)
		aw_ent_id.focus()
def f50():
	conn = connect('EMS.db')
	cursor = conn.cursor()
	cursor.execute("select * from employees order by salary DESC limit 5;")
	with open("out.csv", 'w',newline='') as csv_file:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow([i[0] for i in cursor.description])
		csv_writer.writerows(cursor)
	conn.close()
	
	data=pd.read_csv('out.csv')
	name=data['name']
	salary=data['salary']
	plt.bar(name,salary,width=0.30,color='green')
	plt.xlabel('Name')
	plt.ylabel('Salary')
	plt.title('TOP 5 EMPLOYEES SCORE')
	plt.show()



#----->ROOT GUI
root=Tk()
root.title('Employee Management App')
root.geometry('500x600+50+50')
f=('Kristen ITC',20,'bold','italic')
root.configure(bg='chartreuse2')


btn_add=Button(root,text='Add Employees',font=f,width=15,command=f1)
btn_add.pack(pady=20)
btn_view=Button(root,text='View Employees',font=f,width=15,command=f3)
btn_view.pack(pady=20)
btn_Update=Button(root,text='Update Employees',font=f,width=15,command=f33)
btn_Update.pack(pady=10)
btn_Delete=Button(root,text='Delete Employees',font=f,width=15,command=f40)
btn_Delete.pack(pady=10)
btn_Charts=Button(root,text='Charts',font=f,width=15,command=f50)
btn_Charts.pack(pady=10)
#----->LOCATION AND TEMP
wa = 'https://ipinfo.io/'
res=requests.get(wa)
data=res.json()
city=data['city']

a1 = "https://api.openweathermap.org/data/2.5/weather"
a2 = "?q=" + city
a3 = "&appid=" + "c6e315d09197cec231495138183954bd"
a4 = "&units=" + "metric"
wa=a1+a2+a3+a4
res=requests.get(wa)
data=res.json()
temp=data['main']['temp']

m=Label(root,font=f)
m.pack(pady=10)
msg=str('location : ')+city+str('   Temp : ')+str(temp)+"8\u00b0"+str('C')
m.configure(text=msg,bg='chartreuse2')



#----->ADD GUI
aw=Toplevel(root)
aw.title('Add Employees Record')
aw.geometry('500x600+50+50')
aw.configure(bg='light sky blue')

aw_lab_id=Label(aw,text='Enter employee id',font=f,bg='light sky blue')
aw_ent_id=Entry(aw,font=f,bd=2)
aw_lab_name=Label(aw,text='Enter  name',font=f,bg='light sky blue')
aw_ent_name=Entry(aw,font=f,bd=2)
aw_lab_salary=Label(aw,text='Enter  salary',font=f,bg='light sky blue')
aw_ent_salary=Entry(aw,font=f,bd=2)
aw_btn_save=Button(aw,text='Save',font=f,command=f5)
aw_btn_back=Button(aw,text='Back',font=f,command=f2)
aw_lab_id.pack(pady=10)
aw_ent_id.pack(pady=10)
aw_lab_name.pack(pady=10)
aw_ent_name.pack(pady=10)
aw_lab_salary.pack(pady=10)
aw_ent_salary.pack(pady=10)
aw_btn_save.pack(pady=10)
aw_btn_back.pack(pady=10)

def f7():
	f5()
aw_btn_save.bind('<Return>',f7)
aw.withdraw()
#------>VIEW GUI 
f1=('Arial',20,'bold')
vw=Toplevel(root)
vw.title('View student')
vw.geometry('700x600+50+50')
vw.configure(bg='orange3')

vw_st_data=ScrolledText(vw,width=40,height=10,font=f1)
vw_btn_back=Button(vw,text='Back',font=f1,command=f4)
vw_st_data.pack(pady=10)
vw_btn_back.pack(pady=10)
vw.withdraw()



#------>UPDATE FUNCTION 
def f34():
	root.deiconify()
	up.withdraw()
def f56():
	con=None
	try:
		con=connect('EMS.db')
		cursor=con.cursor()
		sql="update employees set name='%s', salary='%s' where id='%s' "

		id=ent_id56.get()
		name=ent_name56.get()
		salary=ent_salary56.get()
		cursor.execute(sql %(name, salary, id))

		if id.isalpha():
			showerror('Failure','ID should be integers not in alphabets, It should be in +ve integers')
		elif len(id)==0:
			showerror('Failure','ID should not be empty, It should be in +ve integers')

		elif '-' in id:
			showerror('Failure','ID should not be -ve, It should be in +ve integers')
		elif id.isdigit():
			id1=int(id)
			if id==0:
				showerror('Failure','ID should be not zero')
			else:
				if name.isdigit():
					showerror('Failure','Name shoulde be in alphabets not in numbers')
				elif len(name)==0:
					showerror('Failure','Name should not be empty')
				elif  name.isalpha() and len(name)<2 :
					showerror('Failure','Name is too short , atleast it has 2 alphabets')

				elif name.isalpha() and len(name)>=2:
					if salary.isalpha() :
						showerror('Failure','Salary shoulde be in integers not in alphabets')
					elif len(salary)==0:
						showerror('Failure','Salary should not be empty')

					elif salary.isdigit():
						salary1=int(salary)
						if salary1<8000:
							showerror('Failure','Salary should not be less than 8000')
					elif salary.isalnum():
						showerror('Failure','Salary contain alphanumeric value, it should contain only +ve integers')
				elif name.isalnum():
					showerror('Failure','Name contain alphanumeric value, it should contain atleast  2 alphabets')
		elif id.isalnum():
			showerror('Failure','ID contain alphanumeric value, it should contain only +ve integers')



		elif (id.isalpha() or id.isalnum() or id.isdigit() or (len(id)==0)):
			if (name.isalpha() or name.isalnum() or name.isdigit() or (len(name)==0)):
				if (salary.isalpha() or salary.isalnum() or salary.isdigit() or (len(salary)==0)):
					if cursor.rowcount==1 and int(id)>0 and len(name)>2 and int(salary)>8000:
						con.commit()
						showinfo('updated',str(id)+' is updated')
					elif cursor.rowcount==0 and id.isdigit():
						showerror('Failure',str(id)+' is not exists')
				else:
					showerror('Failure','Salary is invalid, It should be in +ve integers')					
			else:
				showerror('Failure','Name is invalid, It should be in alphabets')
		else:
			showerror('Failure','ID is invalid, It should be in +ve integers')


	except Exception as e:
		print(e)
	finally:
		if con is not None:
			con.close()
	ent_id56.delete(0,END)
	ent_name56.delete(0,END)
	ent_salary56.delete(0,END)
	ent_id56.focus()


#------>UPDATE GUI
up=Tk()
up.title('Update Employee')
up.geometry('500x600+50+50')
up.configure(bg='salmon')
f=('Arial',20,'bold','italic')

lab_id=Label(up,text='enter old id :',font=f,bg='salmon')
ent_id56=Entry(up,font=f,bd=4)
lab_name=Label(up,text='enter new name :',font=f,bg='salmon')
ent_name56=Entry(up,font=f,bd=4)
lab_salary=Label(up,text='enter new salary :',font=f,bg='salmon')
ent_salary56=Entry(up,font=f,bd=4)
lab_id.pack(pady=10)
ent_id56.pack(pady=10)
lab_name.pack(pady=10)
ent_name56.pack(pady=10)
lab_salary.pack(pady=10)
ent_salary56.pack(pady=10)

btn_save=Button(up,text='Save',font=f,command=f56)
btn_back=Button(up,text='Back',font=f,command=f34)
btn_save.pack(pady=10)
btn_back.pack(pady=10)
up.withdraw()
#-------->DELETE FUNCTION 
def f8():
	root.deiconify()
	delete.withdraw()
def f66():
	con=None
	try:
		con=connect('EMS.db')
		cursor=con.cursor()
		sql="delete from employees where id='%s' "
		id=ent_id.get()
		cursor.execute(sql %(id))
		if id.isalpha() :
		    showerror('Failure','ID should be integers not in alphabets, It should be in +ve integers')
		elif len(id)==0:
			showerror('Failure','ID should not be empty, It should be in +ve integers')
		elif '-' in id:
		    showerror('Failure','ID should not be -ve, It should be in +ve integers')
		elif id.isdigit():
			id1=int(id)
			if id==0:
				showerror('ID should be +ve integer')
			else:
				con.commit()
			if cursor.rowcount==0:
				showerror('Failure',str(id)+'  is not exists')
			else:
				showinfo('Success',str(id)+' is deleted')
		else:
			showerror('Failure','Invalid ID, It should be in +ve integers')
	except ValueError:
		showerror('Error','Enter id correct')
	except Exception as e:
		showerror(id1,' not exists')
	finally:
		if con is not None:
			con.close()
		ent_id.delete(0,END)
		ent_id.focus()



#------->DELETE GUI
delete=Tk()
delete.title('Delete Employee ')
delete.geometry('500x500+50+50')
delete.configure(bg='slateblue2')
f=('Arial',20,'bold','italic')

lab_id=Label(delete,text='enter id :',font=f,bg='slateblue2')
ent_id=Entry(delete,font=f,bd=4)
lab_id.pack(pady=10)
ent_id.pack(pady=10)

btn_save=Button(delete,text='Save',font=f,command=f66)

btn_back=Button(delete,text='Back',font=f,command=f8)
btn_save.pack(pady=10)

btn_back.pack(pady=10)
delete.withdraw()

#------->EXIT FUNCTION
def  f6():
	answer=askyesno(title='confirm',message='u want to exit ?')
	if answer:
		root.destroy()
root.protocol('WM_DELETE_WINDOW',f6)
root.mainloop()