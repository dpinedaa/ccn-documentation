import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os 
import socket
import sys
import requests
import shutil
import time

app = Flask(__name__)
CORS(app)

def get_username():
    print("Getting username")
    print(os.getlogin())
    return os.getlogin()


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

print(get_ip_address())

host_ip = get_ip_address()
print(host_ip)

def create_directory(document_name):
    print("Creating documentation for " + document_name)
    
    documentation_path = '../documentation/' + document_name
    try:
        os.makedirs(documentation_path)
        print("Documentation created successfully.")
        return jsonify({"status": "OK", "message": "Documentation created successfully."})
    except Exception as e:
        print(f"Error creating documentation: {str(e)}")
        return jsonify({"status": "Error", "message": f"Error creating documentation: {str(e)}"})


def find_documentation(document_name):
    time.sleep(5)

    print("Finding documentation for " + document_name)
    url = "http://192.168.6.79:3000/document/" + document_name
    print(url)
    #get documentation 
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        print("Documentation found.")
        print(response.json())
        data = response.json()
        full_document_name = data['_id']
        customer_name = full_document_name.split('-')[0]
        print(customer_name)
        document_name = full_document_name.split('-')[1]
        return data['_id'], customer_name, document_name, data['portVue'], data['portFlask'], data['portApache']


def copy_documentation_project(document_name):
    print("Copying documentation for " + document_name)
    source_directory = '../documentation-project/'
    destination_directory = '../documentation/' + document_name
    command = "cp -r " + source_directory + "* " + destination_directory

    try:
        # Run the command in Bash explicitly
        subprocess.run(["bash", "-c", "shopt -s dotglob && " + command + " && shopt -u dotglob"])
        print("Documentation copied successfully.")

    except Exception as e:
        print(f"Error copying documentation: {str(e)}")



def find_and_replace(full_name, customer_name, document_name, portFlask,portApache):
    print("Finding and replacing documentation for " + full_name)
    documentation_path = '../documentation/' + full_name

    
    # command = "find " + documentation_path + " -type f -exec sed -i 's/my-project/" + full_name + "/g' {} +"
    #replace my-project with the full name in package.json and package-lock.json

    command = "sed -i 's/my-project/" + full_name + "/g' " + documentation_path + "/package.json"
    command1 = "sed -i 's/my-project/" + full_name + "/g' " + documentation_path + "/package-lock.json" 
    src_path = documentation_path + "/src"
    command2 = "find " + src_path + " -type f -exec sed -i 's/65000/" + str(portFlask) + "/g' {} +"
    app_path = documentation_path + "/app.py"
    command2_5 = "find " + app_path + " -type f -exec sed -i 's/65000/" + str(portFlask) + "/g' {} +"
    headerComponent = documentation_path + "/src/components/HeaderSection.vue"
    command3 = "find " + headerComponent + " -type f -exec sed -i 's/DOCUMENTNAME/" + document_name + "/g' {} +"
    command4 = "find " + headerComponent + " -type f -exec sed -i 's/CUSTOMERNAME/" + customer_name + "/g' {} +"
    navBar = documentation_path + "/src/components/NavBar.vue"
    command5 = "find " + navBar + " -type f -exec sed -i 's/65555/" + str(portApache) + "/g' {} +"

    try:
        subprocess.run(command, shell=True)
        print("Replace my-project with " + full_name + " successfully.")
        subprocess.run(command1, shell=True)
        print("Replace my-project with " + full_name + " successfully.")
        subprocess.run(command2, shell=True)
        print("Replace PORTFLASK with " + str(portFlask) + " successfully.")
        subprocess.run(command2_5, shell=True)
        print("Replace PORTFLASK with " + str(portFlask) + " successfully.")
        subprocess.run(command3, shell=True)
        print("Replace DOCUMENTNAME with " + document_name + " successfully.")
        subprocess.run(command4, shell=True)
        print("Replace CUSTOMERNAME with " + customer_name + " successfully.")
        subprocess.run(command5, shell=True)
        print("Replace PORTAPACHE with " + str(portApache) + " successfully.")
        

    except Exception as e:
        print(f"Error finding and replacing documentation: {str(e)}")



def modify_details(full_name, customer_name, document_name):
    print("Modifying details for " + full_name)
    details_dir = '../documentation/' + full_name + '/public/details'

    #modify the documentauthors.txt
    with open(details_dir + '/documentauthors.txt', 'w') as file:
        text_block = "ccn"
        file.write(text_block)
        print("Document authors modified successfully.")

    with open(details_dir + '/documentclient.txt', 'w') as file:
        text_block = customer_name
        file.write(text_block)
        print("Document client modified successfully.")
    
    with open(details_dir + '/documentissuedate.txt', 'w') as file:
        #today's date in this format yyyy-mm-dd
        text_block = time.strftime("%Y-%m-%d")
        file.write(text_block)
        print("Document date modified successfully.")

    with open(details_dir + '/documentnumber.txt', 'w') as file:
        text_block = "1"
        file.write(text_block)
        print("Document number modified successfully.")

    with open(details_dir + '/documentsecuritystatus.txt', 'w') as file:
        text_block = "Confidential"
        file.write(text_block)
        print("Document security status modified successfully.")
    
    with open(details_dir + '/documentstatus.txt', 'w') as file:
        text_block = "In Progress"
        file.write(text_block)
        print("Document status modified successfully.")

    with open(details_dir + '/documenttitle.txt', 'w') as file:
        text_block = document_name
        file.write(text_block)
        print("Document title modified successfully.")




def add_apache_port(portApache):
    print("Adding apache port " + str(portApache))
    file_path = '/etc/apache2/ports.conf'
    try:
        with open(file_path, 'r') as file:
            existing_content = file.read()

        if f"Listen {portApache}" not in existing_content:
            text_block = f"Listen {portApache}\n"
            with open(file_path, 'a') as file:
                file.write(text_block)
                print("Apache port added successfully.")
        else:
            print("Apache port already exists.")
    except Exception as e:
        print(f"Error adding apache port: {str(e)}")




def create_apache_conf(full_name, portApache, username):
    print("Creating apache conf " + full_name)
    file_path = '/etc/apache2/sites-available/' + full_name + '.conf'
    try:
        with open(file_path, 'w') as file:
            text_block = f"<VirtualHost 192.168.6.79:{portApache}>\n"
            text_block += f"\tServerAdmin webmaster@localhost\n\n"
            #text_block += f"\tDocumentRoot /home/{username}/ccn-documentation/documentation/{full_name}/read-the-docs/build/html/>\n"
            text_block += f"\tDocumentRoot /home/{username}/Documents/GitHub/ccn-documentation/documentation/{full_name}/read-the-docs/build/html/\n\n"
            #text_block += f"<Directory /home/{username}/ccn-documentation/documentation/{full_name}/read-the-docs/build/html/>\n"
            text_block += f"\t<Directory /home/{username}/Documents/GitHub/ccn-documentation/documentation/{full_name}/read-the-docs/build/html/>\n"
            text_block += f"\t\tOptions Indexes FollowSymLinks\n"
            text_block += f"\t\tAllowOverride None\n"
            text_block += f"\t\tRequire all granted\n"
            text_block += f"\t</Directory>\n\n"

            text_block += f"\tErrorLog ${{APACHE_LOG_DIR}}/error.log\n"
            text_block += f"\tCustomLog ${{APACHE_LOG_DIR}}/access.log combined\n"
            text_block += f"</VirtualHost>\n"
            file.write(text_block)
            print("Apache conf created successfully.")
    except Exception as e:
        print(f"Error creating apache conf: {str(e)}")

    # Enable the site
    command = f"sudo a2ensite {full_name}.conf"
    print(command)
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(output)

    # Restart Apache
    command = "sudo systemctl restart apache2"
    print(command)
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(output)




def create_start_script(full_name, portFlask, portVue):
    print("Creating start script " + full_name)
    
    file_path = './scripts/' + full_name + '.sh'

    try:
        with open(file_path, 'w') as file:
            text_block = f"#!/bin/bash \n\n"
            text_block += f"pid=$(lsof -t -i:{portFlask})\n\n"
            text_block += f"if [ -n \"$pid\" ]; then\n"
            text_block += f"\tsudo kill -9 $pid\n"
            text_block += f"fi\n\n"
            text_block += f"pid=$(sudo lsof -t -i:{portVue})\n\n"
            text_block += f"if [ -n \"$pid\" ]; then\n"
            text_block += f"\tsudo kill -9 $pid\n"
            text_block += f"fi\n\n"
            text_block += f"#Start vue project \n"
            text_block += f"cd ../documentation/{full_name}\n"
            text_block += f"sudo PORT={portVue} npm run serve &\n\n"
            text_block += f"#Start flask \n"
            text_block += f"python3 app.py & \n"
            file.write(text_block)
            print("Start script created successfully.")
    except Exception as e:
        print(f"Error creating start script: {str(e)}")

    # Make the script executable
    command = f"sudo chmod +x {file_path}"
    print(command)
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(output)

    





@app.route('/createdocumentation/<document_name>', methods=['POST'])
def create_documentation(document_name):
    create_directory(document_name)
    full_name, customer_name, document_name, portVue, portFlask, portApache = find_documentation(document_name)
    print(full_name, customer_name, document_name, portVue, portFlask, portApache)
    copy_documentation_project(full_name)
    find_and_replace(full_name, customer_name, document_name, portFlask, portApache)
    modify_details(full_name,customer_name, document_name)
    username = get_username()
    add_apache_port(portApache)
    print(username)
    create_apache_conf(full_name, portApache, username)
    create_start_script(full_name, portFlask, portVue)

    return "OK"

    

def delete_doc_project(full_name, portApache, portFlask, portVue):
    print("Deleting documentation project for " + full_name)
    documentation_path = '../documentation/' + full_name
    command = "sudo rm -rf " + documentation_path
    try:
        # Run the command in Bash explicitly
        subprocess.run(["bash", "-c", "shopt -s dotglob && " + command + " && shopt -u dotglob"])
        print("Documentation project deleted successfully.")

    except Exception as e:
        print(f"Error deleting documentation project: {str(e)}")

    # Disable the site
    command = f"sudo a2dissite {full_name}.conf"
    print(command)
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(output)

    # Remove the conf file
    file_path = '/etc/apache2/sites-available/' + full_name + '.conf'
    try:
        os.remove(file_path)
        print("Apache conf deleted successfully.")
    except Exception as e:
        print(f"Error deleting apache conf: {str(e)}")

    # Remove the port from ports.conf
    file_path = '/etc/apache2/ports.conf'
    try:
        with open(file_path, 'r') as file:
            existing_content = file.read()

        if f"Listen {portApache}" in existing_content:
            text_block = f"Listen {portApache}\n"
            with open(file_path, 'w') as file:
                file.write(existing_content.replace(text_block, ""))
                print("Apache port removed successfully.")
        else:
            print("Apache port does not exist.")
    except Exception as e:
        print(f"Error removing apache port: {str(e)}")

    # Restart Apache
    command = "sudo systemctl restart apache2"
    print(command)
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(output)

    # Remove the start script
    file_path = './scripts/' + full_name + '.sh'
    try:
        os.remove(file_path)
        print("Start script deleted successfully.")
    except Exception as e:
        print(f"Error deleting start script: {str(e)}")


    #Kill processes for flask and vue
    command = f"sudo kill -9 $(lsof -t -i:{portFlask})"
    print(command)
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(output)

    command = f"sudo kill -9 $(sudo lsof -t -i:{portVue})"
    print(command)
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(output)

        

    return "OK"


@app.route('/deletedocumentation/<document_name>', methods=['POST'])
def delete_documentation(document_name):
    print("Deleting documentation for " + document_name)
    full_name, customer_name, document_name, portVue, portFlask, portApache = find_documentation(document_name)
    print(full_name, customer_name, document_name, portVue, portFlask, portApache)
    delete_doc_project(full_name,portApache, portFlask, portVue)

    return "OK"


@app.route('/add-word-doc/<document_name>', methods=['POST'])
def add_word_doc(document_name):
    create_directory(document_name)
    print("Adding word doc for " + document_name)
    #Receive word doc from the body of the request
    word_doc = request.files['word_doc']
    print(word_doc)
    #Save the word doc in the documentation folder
    documentation_path = '../documentation/' + document_name
    print(documentation_path)
    word_doc.save(os.path.join(documentation_path, "initial.docx"))
    print("Word doc added successfully.")
    return "OK"

@app.route('/convert/<document_name>', methods=['POST'])
def convert_word(document_name):
    print("Converting word doc for " + document_name)
    #Convert the word doc to html
    documentation_path = '../documentation/' + document_name
    #check if the initial.docx exists
    if os.path.isfile(documentation_path + "/initial.docx"):
        print("File exists")
        command = f"python3 extract.py {document_name}"
        print(command)
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(output)
        print("Word doc converted successfully.")
        return "OK"
    else:
        print("File does not exist")
        return "Error"


#Check if the project is running 
@app.route('/check/<document_name>', methods=['POST'])
def check_project(document_name):
    print("Checking project for " + document_name)
    full_name, customer_name, document_name, portVue, portFlask, portApache = find_documentation(document_name)
    print(full_name, customer_name, document_name, portVue, portFlask, portApache)
    #check if the project is running vue js
    command = f"sudo lsof -t -i:{portVue}"
    print(command)
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(output)
    if output.stdout == "":
        print("Project is not running.")
        return "Not running"
    else:
        print("Project is running.")
        return "Running"
    

@app.route('/delete-customer-projects/<customer_name>/<ID>', methods=['POST'])
def delete_customer_project(customer_name, ID):
    #Find all the projects for the customer
    print("Deleting customer project for " + customer_name)
    url = "http://192.168.6.79:3000/customer/" + ID
    print(url)
    #get documentation
    response = requests.get(url)
    print(response.json())

    for document in response.json()['documents']:
        full_name = document['_id']
        print(full_name)
        delete_doc_project(full_name, document['portApache'], document['portFlask'], document['portVue'])
        print("Project deleted successfully.")
    
    #ensure that all the directories are deleted 
    documentation_path = '../documentation/' 
    command = "sudo rm -rf " + documentation_path + customer_name+"*"
    subprocess.run(command, shell=True)
    print("Directories deleted successfully.")

    return "OK"

# Modify the document name 
@app.route('/modify-document-name/<document_name>', methods=['POST'])
def modify_document_name(document_name): 
    print("Modifying document name for " + document_name)
    #Get the new name from the body of the request
    name = request.get_json()['name']
    print(name)

    document_name0 = document_name.split('-')[0]
    document_name1 = document_name.split('-')[1]
    print(document_name0)
    print(document_name1)

    documentation_dir = '../documentation/' + document_name
    #Find and replace the document name in the documentation folder specific documents 
    file1 = documentation_dir + '/package-lock.json'
    file2 = documentation_dir + '/package.json'
    file3 = documentation_dir + '/public/details/documenttitle.txt'
    file4 = documentation_dir + '/src/components/HeaderSection.vue'
    file5 = "/etc/apache2/sites-available/" + document_name + ".conf"
    file6 = "./scripts/" + document_name + ".sh"

    #Replace the document_name1 with name in the files 
    command = f"sed -i 's/{document_name1}/{name}/g' {file1} {file2} {file3} {file4} {file5} {file6}"
    # command = f"sed -i 's/{document_name1}/{name}/g' {file6}"
    print(command)
    output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(output)

    #Rename the documentation folder
    new_documentation_dir = '../documentation/' + document_name0 + '-' + name
    os.rename(documentation_dir, new_documentation_dir)

    #rename conf file 
    new_file5 = "/etc/apache2/sites-available/" + document_name0 + '-' + name + ".conf"
    os.rename(file5, new_file5)

    #rename start script
    new_file6 = "./scripts/" + document_name0 + '-' + name + ".sh"
    os.rename(file6, new_file6)

    return "OK"


def modify_apache_conf(customer_name, name):
    print("Modifying apache conf for " + customer_name)
    sites_available_dir = "/etc/apache2/sites-available/"
    files = []
    #Find all the conf files for the customer
    for filename in os.listdir(sites_available_dir):
        if filename.startswith(customer_name):
            print(filename)
            files.append(filename)

    
    for file in files:
        file_path = sites_available_dir + file
        print(file_path)
        #Replace the customer name in the conf file
        command = f"sed -i 's/{customer_name}/{name}/g' {file_path}"
        print(command)
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(output)
        #Rename the conf file
        filename0 = file.split('-')[0]
        filename1 = file.split('-')[1]
        new_file_path = sites_available_dir + name + '-' + filename1
        print(new_file_path)
        os.rename(file_path, new_file_path)

        command = f"sudo a2ensite {name}-{filename1}"
        print(command)
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(output)

        #Restart apache
        command = "sudo systemctl reload apache2"
        print(command)
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(output)


        
    


def modify_scripts(customer_name, name):
    print("Modifying scripts for " + customer_name)
    scripts_dir = "./scripts/"
    files = []
    #Find all the scripts for the customer
    for filename in os.listdir(scripts_dir):
        if filename.startswith(customer_name):
            print(filename)
            files.append(filename)

    
    for file in files:
        file_path = scripts_dir + file
        print(file_path)
        #Replace the customer name in the script
        command = f"sed -i 's/{customer_name}/{name}/g' {file_path}"
        print(command)
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(output)
        #Rename the script
        filename0 = file.split('-')[0]
        filename1 = file.split('-')[1]
        new_file_path = scripts_dir + name + '-' + filename1
        print(new_file_path)
        os.rename(file_path, new_file_path)

    

def modify_directories(customer_name, name):
    print("Modifying directories for " + customer_name)
    documentation_dir = "../documentation/"
    directories = []
    #Find all the directories for the customer
    for filename in os.listdir(documentation_dir):
        if filename.startswith(customer_name):
            #print(filename)
            directories.append(filename)

    for directory in directories:
        print(directory)
        file1 = documentation_dir + directory + '/package-lock.json'
        file2 = documentation_dir + directory + '/package.json'
        file3 = documentation_dir + directory + '/public/details/documentclient.txt'
        file4 = documentation_dir + 'src/components/HeaderSection.vue'

        #Replace the customer name in the files
        command = f"sed -i 's/{customer_name}/{name}/g' {file1} {file2} {file3} {file4}"
        print(command)
        output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(output)
        #Rename the directory
        filename0 = directory.split('-')[0]
        filename1 = directory.split('-')[1]
        new_directory = documentation_dir + name + '-' + filename1
        print(new_directory)
        os.rename(documentation_dir + directory, new_directory)




   

    
    
# Modify the customer name in all files 
@app.route('/modify-customer-name/<customer_name>', methods=['POST'])
def modify_customer_name(customer_name): 
    print("Modifying customer name for " + customer_name)
    #Get the new name from the body of the request
    name = request.get_json()['name']
    print(name)
    
    modify_scripts(customer_name, name) 
    modify_directories(customer_name, name)
    modify_apache_conf(customer_name, name)

    
    return "OK"




if __name__ == '__main__':
    app.run(debug=True, host=host_ip, port=2001)
