
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier

import tkinter 
from tkinter import *
from tkinter import filedialog as fd
import tkinter.messagebox
from decimal import Decimal
import re
from tkinter import font
import webbrowser
from sklearn.model_selection import train_test_split
top = tkinter.Tk()

width = top.winfo_screenwidth()
height = top.winfo_screenheight()
top.geometry('%sx%s' % (width, height))
helv1 = font.Font(family='Helvetica', size=20, weight='bold')
helv=font.Font(family='Helvetica',size=20,weight='normal')


data=pd.read_csv('train.csv')
data['Gender'].fillna(data['Gender'].mode()[0],inplace=True)
data['Married'].fillna(data['Married'].mode()[0],inplace=True)
data['Dependents'].fillna(data['Dependents'].mode()[0],inplace=True)
data['Self_Employed'].fillna(data['Self_Employed'].mode()[0],inplace=True)
data['LoanAmount'].fillna(data['LoanAmount'].median(),inplace=True)
data['Loan_Amount_Term'].fillna(data['Loan_Amount_Term'].median(),inplace=True)
data['Credit_History'].fillna(data['Credit_History'].mode()[0],inplace=True)
data['Combined_Income']=data['ApplicantIncome']+data['CoapplicantIncome']
data.drop(['ApplicantIncome','CoapplicantIncome'],axis=1,inplace=True)


# Change 1
data['Income_Loan_Ratio']=(data['LoanAmount']/data['Combined_Income'])/data['Loan_Amount_Term']

mean=np.mean(data['Income_Loan_Ratio'])
std=np.std(data['Income_Loan_Ratio'])
mean=float(mean)
std=float(std)
data['Income_Loan_Ratio']=(data['Income_Loan_Ratio']-mean)/std
data=data[data['Income_Loan_Ratio']<=2]

data['Gender'] = data['Gender'].map({'Male':1,'Female':0})
data['Married'] = data['Married'].map({'Yes':1,'No':0})
data['Dependents'] = data['Dependents'].map({'3+':3,'0':0, '1':1, '2':2})
data['Education'] = data['Education'].map({'Graduate':1,'Not Graduate':0})
data['Self_Employed'] = data['Self_Employed'].map({'Yes':1,'No':0})
data['Property_Area'] = data['Property_Area'].map({'Rural':0,'Semiurban':1,'Urban':2})
data['Loan_Status'] = data['Loan_Status'].map({'Y':1,'N':0})

train,test=train_test_split(data,test_size=0.2)

train = train[['Loan_ID', 'Gender', 'Married','Dependents','Education','Self_Employed','LoanAmount','Loan_Amount_Term','Credit_History','Property_Area','Combined_Income','Income_Loan_Ratio','Loan_Status']]


def browser():
	name= fd.askopenfilename(title="select file",filetypes= (("csv files","*.csv"),)) 
	url = name
	data=pd.read_csv(url)
	data['Gender'].fillna(data['Gender'].mode()[0],inplace=True)
	data['Married'].fillna(data['Married'].mode()[0],inplace=True)
	data['Dependents'].fillna(data['Dependents'].mode()[0],inplace=True)
	data['Self_Employed'].fillna(data['Self_Employed'].mode()[0],inplace=True)
	data['LoanAmount'].fillna(data['LoanAmount'].median(),inplace=True)
	data['Loan_Amount_Term'].fillna(data['Loan_Amount_Term'].median(),inplace=True)
	data['Credit_History'].fillna(data['Credit_History'].mode()[0],inplace=True)
	data['Combined_Income']=data['ApplicantIncome']+data['CoapplicantIncome']
	data.drop(['ApplicantIncome','CoapplicantIncome'],axis=1,inplace=True)


	# Change 2
	data['Income_Loan_Ratio']=(data['LoanAmount']/data['Combined_Income'])/data['Loan_Amount_Term']
	data['Income_Loan_Ratio']=(data['Income_Loan_Ratio']-mean)/std
	

	data['Gender'] = data['Gender'].map({'Male':1,'Female':0})
	data['Married'] = data['Married'].map({'Yes':1,'No':0})
	data['Dependents'] = data['Dependents'].map({'3+':3,'0':0, '1':1, '2':2})
	data['Education'] = data['Education'].map({'Graduate':1,'Not Graduate':0})
	data['Self_Employed'] = data['Self_Employed'].map({'Yes':1,'No':0})
	data['Property_Area'] = data['Property_Area'].map({'Rural':0,'Semiurban':1,'Urban':2})

	
	important_test = data[['Dependents','Credit_History','Property_Area','Income_Loan_Ratio']]
	important_train = train[['Dependents','Credit_History','Property_Area','Income_Loan_Ratio']]
	new_clf = RandomForestClassifier(n_estimators=300,random_state=5,min_samples_split=4,class_weight={0:0.6,1:0.4})
	new_clf.fit(important_train, train.iloc[:,-1])
	y_pred = new_clf.predict(important_test)
	output = y_pred.astype(int)
	df_output = pd.DataFrame()
	aux = pd.read_csv(url)
	df_output['Loan_ID'] = aux['Loan_ID']
	df_output['Loan_Status'] = np.vectorize(lambda s: 'Loan Approved' if s == 1 else 'Loan Not Approved')(output)
	df_output[['Loan_ID', 'Loan_Status']].to_csv('output.csv', index=False)
	
	def show():
		webbrowser.open('output.csv')
	button1 = tkinter.Button(frame3,text = "Loan  Status  Approval  Data",command = show,font=helv1,width=30,height=10,borderwidth=20)
	button1.grid(row=15,column=20)
    
def user():
	

	top1=tkinter.Tk()
	top1.geometry('%sx%s' % (width, height))
	top1.configure(background='light blue')
	frame4=Frame(top1)
	frame4.place(relx=.26,rely=.08)
	frame5=Frame(top1)
	frame5.place(relx=.37,rely=.001)
	frame6=Frame(top1)
	frame6.place(relx=.30,rely=.80)
	Label(frame5,text="Loan Application Form",font=("Helvetica",32)).grid(row=0)


	 
	mystring = StringVar(top1)
	Label(frame4, text="Loan ID",font=helv).grid(row=0)
	Entry(frame4, textvariable=mystring,width="50").grid(row=0,column=1)
	Label(frame4,text="--------------------------------------------------------------------------").grid(row=5,column=1)
	
	
	
	Label(frame4,text="Choose Gender:",font=helv).grid(row=10)
	OPTIONS=["SelectGender","Male","Female"]
	variable=StringVar(top1)
	variable.set(OPTIONS[0])
	w=OptionMenu(frame4,variable,*OPTIONS)
	w.grid(row=10,column=1)
	Label(frame4,text="--------------------------------------------------------------------------").grid(row=15,column=1)

	
	
	Label(frame4,text="Married  ",font=helv).grid(row=20)
	options=["Choose one : married ?:","yes","no"]	
	variable1=StringVar(top1)
	variable1.set(options[0])
	w1=OptionMenu(frame4,variable1,*options)
	w1.grid(row=20,column=1)
	Label(frame4,text="--------------------------------------------------------------------------").grid(row=25,column=1)
	
	
	
	Label(frame4,text="Number of dependents:",font=helv).grid(row=30)
	opt=["choose no of dependents:","0","1","2","equal to or more than 3"]
	variable2=StringVar(top1)
	variable2.set(opt[0])
	w2=OptionMenu(frame4,variable2,*opt)
	w2.grid(row=30,column=1)
	Label(frame4,text="--------------------------------------------------------------------------").grid(row=35,column=1)
	
	
	Label(frame4,text="Education:",font=helv).grid(row=40)
	opt1=["choose one option (education) :","Graduate","Not Graduate"]
	variable3=StringVar(top1)
	variable3.set(opt1[0])
	w3=OptionMenu(frame4,variable3,*opt1)
	w3.grid(row=40,column=1)
	Label(frame4,text="--------------------------------------------------------------------------").grid(row=45,column=1)
	
	
	Label(frame4,text="Self Employed:",font=helv).grid(row=50)
	opt2=["self employed ? choose one :","yes","no"]
	variable4=StringVar(top1)
	variable4.set(opt2[0])
	w4=OptionMenu(frame4,variable4,*opt2)
	w4.grid(row=50,column=1)
	Label(frame4,text="--------------------------------------------------------------------------").grid(row=55,column=1)
	
	
	var = StringVar(top1)
	Label(frame4,text="Applicant Income:",font=helv).grid(row=60)
	Entry(frame4,textvariable=var,width="50").grid(row=60,column=1)
	Label(frame4,text="per month").grid(row=60,column=2)
	
	
	var1 = StringVar(top1)
	Label(frame4,text="CoapplicantIncome:",font=helv).grid(row=70)
	Entry(frame4,textvariable=var1,width="50").grid(row=70,column=1)
	Label(frame4,text="per month").grid(row=70,column=2)
	

	
	var2 = StringVar(top1)
	Label(frame4,text="Loan Amount:(in thousands)",font=helv).grid(row=80)
	Entry(frame4,textvariable=var2,width="50").grid(row=80,column=1)
	Label(frame4,text="thousands").grid(row=80,column=2)
	
	
	var3 = StringVar(top1)
	Label(frame4,text="Loan Amount Term:(in months)",font=helv).grid(row=90)
	Entry(frame4,textvariable=var3,width="50").grid(row=90,column=1)
	Label(frame4,text="months").grid(row=90,column=2)
	Label(frame4,text="--------------------------------------------------------------------------").grid(row=95,column=1)
	

	Label(frame4,text="Credit History:",font=helv).grid(row=100)
	opt5=["credit history: choose one option :","0-(not meets guidelines)","1-(meets guidelines)"]
	var4=StringVar(top1)
	var4.set(opt5[0])
	w5=OptionMenu(frame4,var4,*opt5)
	w5.grid(row=100,column=1)
	Label(frame4,text="--------------------------------------------------------------------------").grid(row=105,column=1)
	
	

	Label(frame4,text="Property Area:",font=helv).grid(row=110)
	opt6=["property area-- choose one :","Rural","Semiurban","Urban"]
	variable5=StringVar(top1)
	variable5.set(opt6[0])
	w6=OptionMenu(frame4,variable5,*opt6)
	w6.grid(row=110,column=1)
	Label(frame4,text="  ").grid(row=115,column=1)
	Label(frame4,text=" ").grid(row=116,column=1)
	
	

	
	
	def fun():
		
		prog = re.compile(r'^[0-9]*[.]{0,1}[0-9]*$')

		
		if mystring.get()=="" or var2.get()=="" or var3.get()=="" or var.get()=="" or var1.get()=="" or variable.get()==OPTIONS[0] or variable1.get()==options[0] or variable2.get()==opt[0] or variable3.get()==opt1[0] or variable4.get()==opt2[0] or var4.get()==opt5[0] or variable5.get()==opt6[0]:
			tkinter.messagebox.showinfo("Missing entries","Missing values..Fill the loan application form completely")

			
		elif not(prog.match(var.get())) or not(prog.match(var1.get())) or not(prog.match(var2.get())) or not(prog.match(var3.get())):
			tkinter.messagebox.showinfo("Invalid values","Invalid numeric values..Fill the loan application form correctly ")	
				

		else:
			loan_amount=Decimal(var2.get())
			loan_amount_term=Decimal(var3.get())
			applicant_income=Decimal(var.get())
			coapp_income=Decimal(var1.get())	

			if  loan_amount==0.0:
				tkinter.messagebox.showinfo("Missing values","Loan amount should be greater than zero ..Fill the loan application form correctly")
				
				
			elif  loan_amount_term==0.0:
				tkinter.messagebox.showinfo("Invalid values","Loam amount term should be greater than zero.. Fill the loan application form correctly")
				
				
			elif loan_amount<0 or loan_amount_term<0 or applicant_income<0 or coapp_income<0 :
				tkinter.messagebox.showinfo("Invalid values","Invalid numeric values.. Fill the loan application form correctly.."+mystring.get())
				
				

			else:
				
				if var4.get() == opt5[1]:
					credit_history=0
				elif var4.get() == opt5[2]:
					credit_history=1
				combined_income = applicant_income + coapp_income
				
				# change 3
				Income_Loan_Ratio = (loan_amount/combined_income)/loan_amount_term
				Income_Loan_Ratio=float(Income_Loan_Ratio)
				Income_Loan_Ratio=(Income_Loan_Ratio-mean)/std


				if variable2.get() == opt[1] :
					dependents=0
				elif variable2.get() == opt[2]:
					dependents=1
				elif variable2.get() == opt[3]:
					dependents=2
				else:
					dependents=3
				if variable5.get() == opt6[1]:
					prop_area=0
				elif variable5.get() == opt6[2]:
					prop_area=1
				else:
					prop_area=2



				
				
				important_train = train[['Dependents','Credit_History','Property_Area','Income_Loan_Ratio']]
				new_clf = RandomForestClassifier(n_estimators=300,random_state=6,min_samples_split=4,class_weight={0:0.6,1:0.4})
				new_clf.fit(important_train, train.iloc[:,-1])
				a=[dependents,credit_history,prop_area,Income_Loan_Ratio]
				a=np.array(a)


				a=np.expand_dims(a,0)
				
				y_pred=new_clf.predict(a)
				if y_pred == 0:
					tkinter.messagebox.showinfo("LOAN STATUS","LOAN STATUS NOT APPROVED FOR LOAN ID :"+mystring.get())
					
				else:
					tkinter.messagebox.showinfo("LOAN STATUS","LOAN STATUS APPROVED FOR LOAN ID :"+mystring.get())

	b4 = tkinter.Button(frame6,text = "SUBMIT FORM",font=helv1,bg="light green",width=50,height=3,borderwidth=10,command=lambda:[top1.destroy(),fun()])
	b4.grid(row=0,column=1)
	top1.mainloop()		
		
					
   
frame1=Frame(top)

frame2=Frame(top)

frame3=Frame(top)

b1 = tkinter.Button(frame1,text = "BROWSE THE FILE  ",height=5,width=40,command = browser,font=helv1,activeforeground="green",fg="black",bg="light blue",borderwidth=10)

b3 = tkinter.Button(frame1,text= "FILL IN DETAILS FOR SINGLE USER",height=5,width=40,command = user,activeforeground="black",fg="black",bg="light green",font=helv1,borderwidth=10)

b5 = tkinter.Button(frame1,text="QUIT",command=quit,activeforeground="green",fg="black",width=40,height=3,font=helv1,bg="light blue",borderwidth=10)
Label(frame2,text="LOAN      STATUS     PREDICTION",font=("Helvetica",42)).grid(row=1,column=12)

frame1.place(relx=.1,rely=.2)

b1.grid(row=10,column=1)
b3.grid(row=20,column=1)
b5.grid(row=30,column=1)
top.configure(background='white')
frame2.place(relx=.2,rely=.01)
frame3.place(relx=.60,rely=.30)



top.mainloop()