import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os 
import socket
import sys
import requests
import shutil

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



def find_and_replace(full_name, customer_name, document_name, portFlask):
    print("Finding and replacing documentation for " + full_name)
    documentation_path = '../documentation/' + full_name
    command = "find " + documentation_path + " -type f -exec sed -i 's/my-project/" + full_name + "/g' {} +"
    command2 = "find " + documentation_path + " -type f -exec sed -i 's/PORTFLASK/" + str(portFlask) + "/g' {} +"
    command3 = "find " + documentation_path + " -type f -exec sed -i 's/DOCUMENTNAME/" + document_name + "/g' {} +"
    command4 = "find " + documentation_path + " -type f -exec sed -i 's/CUSTOMERNAME/" + customer_name + "/g' {} +"

    try:
        subprocess.run(command, shell=True)
        print("Replace my-project with " + full_name + " successfully.")
        subprocess.run(command2, shell=True)
        print("Replace PORTFLASK with " + str(portFlask) + " successfully.")
        subprocess.run(command3, shell=True)
        print("Replace DOCUMENTNAME with " + document_name + " successfully.")
        subprocess.run(command4, shell=True)
        print("Replace CUSTOMERNAME with " + customer_name + " successfully.")

    except Exception as e:
        print(f"Error finding and replacing documentation: {str(e)}")

    
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


# def create_start_script(full_name, portFlask, portVue):
#     print("Creating start script " + full_name)
#     file_path = '/scripts/start-' + full_name + '.sh'

#     try:
#         with open(file_path, 'w') as file:
#             text_block = f"#!/bin/bash\n"
#             text_block += f"cd /home/{username}/Documents/GitHub/ccn-documentation/documentation/{full_name}/\n"
#             text_block += f"nohup python3 -m http.server {portVue} &\n"
#             text_block += f"nohup python3 -m flask run --port={portFlask} &\n"
#             file.write(text_block)
#             print("Start script created successfully.")


@app.route('/createdocumentation/<document_name>', methods=['POST'])
def create_documentation(document_name):
    create_directory(document_name)
    full_name, customer_name, document_name, portVue, portFlask, portApache = find_documentation(document_name)
    print(full_name, customer_name, document_name, portVue, portFlask, portApache)
    copy_documentation_project(full_name)
    find_and_replace(full_name, customer_name, document_name, portFlask)
    username = get_username()
    add_apache_port(portApache)
    print(username)
    create_apache_conf(full_name, portApache, username)
    # create_start_script(full_name, portFlask, portVue)



    return "OK"

    





if __name__ == '__main__':
    app.run(debug=True, host=host_ip, port=2001)
