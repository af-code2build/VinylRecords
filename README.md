# Vinyl Record



### Project Type

- [x] University Project
- [ ] Self Challenge
- [ ] Project for a Company
- [x] Team work



### Problem to solve

The company Vinyl Record Lda. needs a system that symulates the management of their online business, which essentially consists of selling vinyl music records (eg, albums) to customers and keeping their inventory up to date. Thus, it is necessary to build a database application that allows customers, for example, to search and buy disks and that allows administrators, to perform typical store management tasks (eg, add a new album or view statistics).



### Requirements

* Python 3
* PostgreSQL 
* Psycopg2 
* Access to the tool ONDA in http://onda.dei.uc.pt/v3/



### Show Project

It is possible to see how this application works through [this](https://youtu.be/TMzKpJ0WXYo) video.



### What I learned?

* Python Language 
* A bit of Object Oriented Programming in Python
* How to use PostgreSQL and creat simple Databases
* How to query PostgreSQL Databases
* How to use the PostgreSQL database adapter: Psycopg
* Create graphic applications using Tkinter



### How to run the project locally?

* You will need the Python interpreter installed on your system so you can run the program.

* Get the following packages installed on your machine:

  * Tkinter:          ` pip install tk`

  * PyPubSub:    ` pip install pypubsub`

  * Psycopg2:     `pip install psycopg2`

  * Pillow:           ` pip install Pillow`

  * DateTime:    `pip install DateTime`

    

* You will also need to install the PostgreSQL software and creat a new database named "BD". To make things easy, we can use the pgAdmin tool that comes with the installation. After the database is ready, you will need to run the following SQL scripts (saved in text file format, inside the resources folder) in the Query Editor, following this order:

  * creat_tabs.txt

  * funtion_PLSQL.txt

  * raw_data.txt

    

Now you are ready to test it!! 

You just need to run: `python project_frontend.py`



### Warnings and/or Disclaimers

* Many things in this project were written in Portuguese