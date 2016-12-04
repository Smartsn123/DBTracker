# DBTracker
Track the changes in the MySQL DB and send notifications to subscribers on each column level

Requirements :
1. MongoDB with replication and oplog enabled
2. smtp server running

1.make sure replication is set and oplog is enabled in mongoDB before running



Setting up Tailable MonogoDB oplog to monitor the changes in the mongoDB:
Add in the config-File following:

replSet=rs0 (name is variable) (necessary because starting mongod with replSet option didn't work)
oplogSize=[MemSize]


Restart the mongoDB server 

Set replicaset:

  rs.initiate({"_id" : "rs0","version" : 1,"members" : [{"_id" : 0,"host" :"localhost:27017"}]})
Check with rs.status()



2. to track the mails on the local host run the following command on the terminal:

python -m smtpd -n -c DebuggingServer localhost:1025



Make sure to modify the mail-sending code to use the non-standard port number:

server = smtplib.SMTP(SERVER, 1025)
server.sendmail(FROM, TO, message)
server.quit()




To Test :

run mongo in shell, make insertion deletion or updation to the feilds you subscribed from the subscriber server




