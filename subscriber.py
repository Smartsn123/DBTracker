
from bottle import route,run,template
import pymongo
import bottle
import os
from tracker import tracker
from multiprocessing import Process


c = pymongo.MongoClient()
db = c.socialcops
table_list =  db.collection_names()
print table_list



@route('/')
def index():
	form = '''<html> 
	          <h1>DB operation tracker Subscription</h1><br>
	          <form  method="post"><br>
	       '''
	form+=" <h1>enter column names (comma separated)from table that u want to subscribe</h1><br>"
	for table in table_list : 
		form+= table+"</br>"
		form+= "<input type = 'text'  name ='"+table+"'></br></br>"
	form+="EMAIL : <input type ='text'  name ='mailId' value=''><br>"
	form+="<input type ='submit' value='subscribe'></form>"
	form+="</html>"
	return template(form)


@route('/',method='POST')
def subscriber():
   db_subs = c.subscriber
   mail = bottle.request.forms.get('mailId')
   report=""
   for table in table_list:	
   	    try:
   	    	feilds = [ fl.strip() for fl in bottle.request.forms.get(table).split(",")]
   	    	print feilds
   	    	for feild in feilds :
   	    		exists = db_subs.subscription.find_one({'table':table,'feild':feild})
   	    		print feild,exists
   	    		if exists != None:
   	    			db_subs.subscription.update({'table':table,'feild':feild},{'$addToSet':{'emails':mail}})
   	    		else:
   	    		    db_subs.subscription.insert({'table':table,'feild':feild,'emails':[mail]})
   	    	report += "success  subscribing!"
   	    except:
   	    	report += "error  subscribing !"

   return "<html>"+report+"<br><a href='/'>back</a></html>"

def start_server():
	run(host='localhost', port=8082)


if __name__ == '__main__':
  p1 = Process(target=start_server)
  p1.start()
  p2 = Process(target=tracker)
  p2.start()
  p1.join()
  p2.join()



