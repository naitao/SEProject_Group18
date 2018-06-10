=================
SEProject_Group18
=================
This is SEProject Group18 Web Application Final Code repo

Description
===========
1.How to a install this web application

	1)Deploy EC2 install Linux (ubuntu) and RDS MySQL first, make sure both Operation and MySQL Server all work well. Our MySQL information:
		Hostname: ucdgroup18.ck04mjz0uhn8.us-west-2.rds.amazonaws.com
		username: root	password: 1234qwer
	2)On Ubuntu, get the git bits from: https://github.com/naitao/SEProject_Group18.git
	3)Install the necessary python modules, such as mysql-python, python3-mysqldb, libmysqlclient-dev, flask-mysql, statsmodels, etc.
	4)Under SEProject_Group18, execute “sudo python setup.py develop” to make command line. It will compile a command  “dublinbike” under “/user/local/bin/”


2.How to boot up flask server and DB query automation
	As we have integrated all operations into script (including the RDS data inserting and querying automatically), everything could be quite simple. Just executing the following command:
 ubuntu@ip-172-31-24-252:~/SEProject_Group18/docs/Peng$ dublinbike 
	
To get more instructions, you can run with:
ubuntu@ip-172-31-24-252:~/SEProject_Group18/docs/Peng$ dublinbike 
/usr/local/bin/dublinbike {webstart|dbstart|allstart|status|webstatus|stop|webstop}

3.How to monitor the server’s status and how to debug it.
There is a log which can provide all running process of the server. It is located here:
ubuntu@ip-172-31-24-252:~$ tail SEProject_Group18/log/DublinBike.log


Note
====

This project has been set up using PyScaffold 3.0.1. For details and usage
information on PyScaffold see http://pyscaffold.org/.
