#	WEB INFORMATION SYSTEM#

>This is the official github repo of miniproject created by:  
**Ashwin Jayakumar, Bharadhwaj CN, Hanzal Salim** _and_ **Shafeeq K**  
>of S6CSE, NSS College of Engineering  

##Abstract##

 We propose a system for enhancing the communication between teachers and  
students of an institution by providing an integrated system for sharing  
information.The reach of such information is assured by using multiple  
messaging methods such as email,SMS etc. The system also provides a web  
based interface for revisiting such information and facilities for discussion.  
 The name given to this system is, TIM. TIM is mainly indented to enhance the  
the communication between teachers and students.  
 TIM.  
 TIM is all about S.T.U.D.I.E.S  
 (Student Teacher Unified Dynamic Information Exchange System)  

##Current features##

* User registrations for Student and Teacher
* User login, and viewing posts
* Add post for Teachers
* Attch images and files with posts
* View and download attachments
* Filter posts by category and teacher who posted them  

 The prepopulated categories are the subjects in  Calicut University's Sixth Semester  
Computer Science and Engineering (2009) scheme syllabus.  
 Example users Teacher1 and Teacher2 with Teacher privilage and Student1 and Student2  
with Student privilage are also added.  

##Usage##

1. At first, run **createdb.py** initialise the database and to populate it with sample data  
	```
	python createdb.py  
	```
2. Then run **app.py** run the project  
	```
	python app.py  
	```  
 This starts the development web server listening at port 5050  
3. Visit **localhost:5050** or **127.0.0.1:5050** in the browser to use the app.
