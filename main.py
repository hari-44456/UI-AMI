from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import json
app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def view_home():
    return render_template("index.html", title="Home Page")

@app.route("/aws")
def aws():
	
 	
 		filename = 'images.txt'
 		lines = []
 		with open(filename) as f:
 			lines = f.readlines()
 		return render_template("aws.html", title="Aws",opt=lines)   



def generateApplyCommand(pairs,st="apply"):
    str = "terraform " + st +" --auto-approve"
    for key,value in pairs.items():
    	str += " -var "+key+"=\""+value+"\""	
    return str;

@app.route("/aws", methods=['POST'])
def aws_post():

	pairs={}
	file = request.files['file']
	filename = secure_filename(file.filename) 
	file.save(filename)
	lines =[]
	with open(filename) as f:
		lines = f.readlines()
	count = 0
	length=len(lines)
	for line in lines:
		if count!=length-1:
			tmp=line[:-1]
			result = tmp.find('=')
			pairs[tmp[0:result]]=tmp[result+1:]

		else:	
		    result = line.find('=')
		    pairs[line[0:result]]=line[result+1:]
		#print(line[-1])
		#print(line[result+1:])
	prefix=request.form['vmname']
	pairs['prefix']=prefix
	user=request.form['user']
	pairs['user']=user
	password=request.form['Password']
	#pairs['password']=password
	region=request.form['region']
	pairs['region']=region
	subnet_cidr_block=request.form['scidr']
	pairs['subnet_cidr_block']=subnet_cidr_block
	vpc_cidr_block=request.form['vcidr']
	pairs['vpc_cidr_block']=vpc_cidr_block
	#os=request.form['os']
	#pairs['os']=os
	ami=request.form['ami']
	#pairs['ami']=ami
	
	
	cmd=generateApplyCommand(pairs)
	print(cmd)
	
	os.chdir("aws")
	
	os.system("terraform init")
	os.system (cmd)
	#os.system("terraform state rm \"aws_ami_from_instance.ami\" ")
	#destory =generateApplyCommand(pairs,"destory")
	#os.system(destory)
	return render_template("aws.html", title="Aws")

@app.route("/azure",methods=['GET'])
def azure():
	try:
		data = json.loads(open("input.json").read())
	except:
		print("Please provide input.json")
		exit(0)
	lines=[]
	for i in data['CentOS']:
		print(i['urn'])
		lines.append(i['urn'])
	data2=[]
	try:
		data2 = json.loads(open("azure_credentials.json").read())
	except:
		print("Please provide azure_credentials.json")
	credentials=[]
	for i in data2['azure_credentials']:
		print(i['client_id'])
		credentials.append(i['client_id'])
		
	return render_template("azure.html", title="Azure",opt=lines,credential=credentials)
@app.route("/azure", methods=['POST'])
def azure_post():

	pairs={}
	

	prefix=request.form['vmname']
	pairs['prefix']=prefix
	user=request.form['user']
	pairs['user']=user
	password=request.form['Password']
	#pairs['password']=password
	region=request.form['region']
	pairs['location']=region
	os1=request.form['os']
	#pairs['os']=os
	ami=request.form['ami']
	cred=request.form['cred']
	#pairs['ami']=ami
	sku=""
	publisher=""
	version=""
	try:
		data = json.loads(open("input.json").read())
	except:
		print("Please provide input.json")
		exit(0)
	for i in data['CentOS']:
		if i['urn']==ami:
			pairs['offer']=i['offer']
			pairs['sku']=i['sku']
			pairs['publisher']=i['publisher']
			pairs['image_version']=i['version']
	data2=[]
	try:
		data2 = json.loads(open("azure_credentials.json").read())
	except:
		print("Please provide azure_credentials.json")
	credentials=[]
	for i in data2['azure_credentials']:
		if cred==i['client_id']:
			pairs['subscription_id']=i['subscription_id']
			pairs['tenant_id']=i['tenant_id']
			pairs['client_id']=cred
			
			
			pairs['client_secret']=i['client_secret']
		
    	
	cmd=generateApplyCommand(pairs)
	print(cmd)
	
	os.chdir("azure")
	
	os.system("terraform init")
	os.system (cmd)
	#os.system("terraform state rm \"aws_ami_from_instance.ami\" ")
	#destory =generateApplyCommand(pairs,"destory")
	#os.system(destory)
	return render_template("azure.html", title="Azure")

@app.route("/gcp")
def gcp():
    return render_template("gcp.html",title="GCP")    


@app.route('/getfile', methods=['GET','POST'])
def getfile():
    if request.method == 'POST':

        # for secure filenames. Read the documentation.
        file = request.files['myfile']
        filename = secure_filename(file.filename) 

        # os.path.join is used so that paths work in every operating system
        file.save(filename)
        lines = []
        with open(filename) as f:
        	lines = f.readlines()
        count = 0
        for line in lines:
        	result = line.find('=')
        	print(line[result+1:])      


    else:
        result = request.args.get['myfile']
    return result





if __name__ == '__main__':
   app.run(debug = True ,port=2000)