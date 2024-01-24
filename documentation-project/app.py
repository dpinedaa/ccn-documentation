import subprocess
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os 
import socket
import base64
import csv
import re



app = Flask(__name__)
CORS(app)

username = os.getlogin()
home_dir="/home"

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

print(get_ip_address())

host_ip = get_ip_address()

@app.route('/get_title/<section_number>', methods=['GET'])
def get_title(section_number):
    print("section_number: ", section_number)
    file_path = f"./public/section{section_number}/section{section_number}title.txt"
    print(file_path)
    with open(file_path, 'r') as f:
        title = f.read()
        # Find the index of "Content:"
        content_index = title.find("Content:")
        # Extract the text after "Content:"
        content = title[content_index + len("Content:"):].strip()

    print("Title:", title)
    print(content)
       
    return content


@app.route('/update_title/<section_number>', methods=['POST'])
def update_title(section_number):
    print("section_number: ", section_number)
    file_path = f"./public/section{section_number}/section{section_number}title.txt"
    print(file_path)

    #check if the file exists and if does not 
    if os.path.exists(file_path):
        print("File exists")
            # Read the existing content from the file
        with open(file_path, 'r') as f:
            existing_content = f.read()
        # Find the index of "Content: "
        content_index = existing_content.find("Content: ")

        if content_index != -1:
            # Update the content after "Content: "
            updated_content = existing_content[:content_index + len("Content: ")]

            # Read the new content from the request body
            #new_content = request.data.decode('utf-8')
            new_content = request.json.get('content', '')
            updated_content += new_content

            # Open the file and update its content
            with open(file_path, 'w') as f:
                f.write(updated_content)

            return "Success"
    else:
        with open(file_path, 'w') as f:
            new_content = request.json.get('content', '')
            body = f"Style: Heading 1\nContent: {new_content}"
            f.write(body)
        return "Success"
    

ALLOWED_EXTENSIONS = {'txt', 'png', 'jpeg', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Get All files in the folder
@app.route('/files/<section_number>')
def get_files(section_number):
    print("section_number: ", section_number)
    section_path = f'section{section_number}'
    public_folder  = "./public/" + section_path
    print("public_folder: ", public_folder)
    print(public_folder)

    

    try:
        files = []
        #Print the files in the folder

        for filename in sorted(os.listdir(public_folder), key=lambda x: [int(s) if s.isdigit() else s for s in re.split('(\d+)', x)]):
            print(filename)
            if allowed_file(filename):
                file_path = os.path.join(public_folder, filename)
                with open(file_path, 'rb') as file:
                    if filename.endswith(('.png', '.jpeg')):
                        content = base64.b64encode(file.read()).decode('utf-8')

                    elif filename.endswith('.csv'):
                        csv_file_name = os.path.join(public_folder, filename)

                        with open(csv_file_name, "r") as csv_file:
                            csv_reader = csv.reader(csv_file)
                            rows = []

                            for row in csv_reader:
                                modified_row = []

                                for cell in row:
                                    if cell.startswith('"') and cell.endswith('"'):
                                        modified_cell = cell[1:-1].replace(',', ' ')
                                    else:
                                        modified_cell = cell

                                    modified_row.append(modified_cell)

                                rows.append(','.join(modified_row))

                            content = '\n'.join(rows)

                    else:
                        content = file.read().decode('utf-8')

                files.append({'name': filename, 'content': content})

        return jsonify(files)

    except Exception as e:
        print(f'Error reading files: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    


@app.route('/files/<section_number>/<filename>')
def get_file(section_number, filename):
    print("section_number: ", section_number)
    print("filename: ", filename)
    public_folder  = "./public/section" + section_number

    try:
        file_path = os.path.join(public_folder, filename)
        return send_file(file_path)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


@app.route('/update_file/<section_number>/<filename>', methods=['PUT'])
def update_file(section_number, filename):
    public_folder  = "./public/section" + section_number
    try:
        file_path = os.path.join(public_folder, filename)

        if filename.endswith(('.png', '.jpeg')):
            base64_data = request.form.get('base64Data')
            with open(file_path, 'wb') as file:
                file.write(base64.b64decode(base64_data))
        else:
            new_content = request.data.decode('utf-8')

            if filename.endswith('.txt'):
                with open(file_path, 'r+', encoding='utf-8') as file:
                    content = file.read()
                    index = content.find('Content: ')
                    if index != -1:
                        content = content[:index + 9] + new_content
                        file.seek(0)
                        file.write(content)
                        file.truncate()
            elif filename.endswith('.csv'):
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)
            else:
                return jsonify({'error': 'Invalid file type'}), 400

        return jsonify({'message': 'File updated successfully'})
    except Exception as e:
        print(f'Error updating file: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500






@app.route('/delete_file/<section_number>/<filename>', methods=['DELETE'])
def delete_file(section_number, filename):
    print("section_number: ", section_number)
    print("filename: ", filename)
    public_folder  = "./public/section" + section_number

    try:
        # if not filename.endswith('.txt'):
        #     return jsonify({'error': 'Invalid file type'}), 400

        file_path = os.path.join(public_folder, filename)
        os.remove(file_path)

        return jsonify({'message': 'File deleted successfully'})
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        print(f'Error deleting file: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    

@app.route('/save_text/<section_number>', methods=['POST'])
def save_text(section_number):
    folder_path = f"./public/section{section_number}"
    
    # Find the latest file number in the folder (regardless of type)
    latest_file_number = 0
    for filename in os.listdir(folder_path):
        match = re.match(rf"section{section_number}_(\d+)_output_.*", filename)
        if match:
            file_number = int(match.group(1))
            latest_file_number = max(latest_file_number, file_number)

    # Increment the latest file number
    new_file_number = latest_file_number + 1

    # Construct the new file name
    new_file_name = f"section{section_number}_{new_file_number}_output_text.txt"
    
    # Construct the full file path
    file_path = os.path.join(folder_path, new_file_name)

    # Get style and text content from JSON
    style = request.json.get('style', '')
    content = request.json.get('text', '')

    # Save the text to the new file in the specified format
    text_content = f"Style: {style}\nContent: {content}"
    with open(file_path, 'w') as f:
        f.write(text_content)

    return "Success"


@app.route('/save_csv/<section_number>', methods=['POST'])
def save_csv(section_number):
    folder_path = f"./public/section{section_number}"
    
    # Find the latest file number in the folder (regardless of type)
    latest_file_number = 0
    for filename in os.listdir(folder_path):
        match = re.match(rf"section{section_number}_(\d+)_output_.*", filename)
        
        if match:
            file_number = int(match.group(1))
            latest_file_number = max(latest_file_number, file_number)

    # Increment the latest file number
    new_file_number = latest_file_number + 1

    # Construct the new file name
    new_file_name = f"section{section_number}_{new_file_number}_output_csv.csv"
    
    # Construct the full file path
    file_path = os.path.join(folder_path, new_file_name)

    # Extract headers and data from the request
    headers = request.json.get('headers', [])
    data = request.json.get('data', [])

    # Save the CSV content to the new file using the csv module
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(headers)
        csv_writer.writerows(data)

    return "Success"

@app.route('/save_image/<section_number>', methods=['POST'])
def save_image(section_number):
    folder_path = f"./public/section{section_number}"

    # Find the latest file number in the folder (regardless of type)
    latest_file_number = 0
    for filename in os.listdir(folder_path):
        match = re.match(rf"section{section_number}_(\d+)_output_.*", filename)
        if match:
            file_number = int(match.group(1))
            latest_file_number = max(latest_file_number, file_number)

    # Increment the latest file number
    new_file_number = latest_file_number + 1

    # Construct the new file name
    new_file_name = f"section{section_number}_{new_file_number}_output_image.png"

    # Construct the full file path
    file_path = os.path.join(folder_path, new_file_name)

    # Save the image to the new file
    with open(file_path, 'wb') as f:
        f.write(request.files['image'].read())

    return "Success"


#Move down the file in the file list 

# Move file down in the file list
@app.route('/move_down/<section_number>/<filename>', methods=['PUT'])
def move_down(section_number, filename):
    section_path = f'section{section_number}'
    public_folder = "./public/" + section_path

    try:
        files = sorted(os.listdir(public_folder), key=lambda x: [int(s) if s.isdigit() else s for s in re.split('(\d+)', x)])
        print("Current files order:", files)

        # Find the index of the target file
        index = next((i for i, file in enumerate(files) if file == filename), None)

        # Ensure that the file is not already at the top
        if index is not None and index < len(files) - 1:
            # Swap file positions
            filename_down = files[index + 1]

            # Use the code for swapping file names
            file_name = filename.split("_")
            file_name_down = filename_down.split("_")

            new_filename = file_name[0] + "_" + file_name_down[1] + "_" + file_name[2] + "_" + file_name[3]
            new_filename_down = file_name_down[0] + "_" + file_name[1] + "_" + file_name_down[2] + "_" + file_name_down[3]

            # Print information for debugging
            print("Swapping files:")
            print("  - Original Filename to be changed:", filename)
            print("  - Original Filename to swap with:", filename_down)
            print("  - New Filename for the changed file:", new_filename)
            print("  - New Filename for the swapped file:", new_filename_down)

            # Rename the files
            os.rename(os.path.join(public_folder, filename_down), os.path.join(public_folder, "temp"))
            os.rename(os.path.join(public_folder, filename), os.path.join(public_folder, new_filename))
            os.rename(os.path.join(public_folder, "temp"), os.path.join(public_folder, new_filename_down))

            # Print updated files order
            files = sorted(os.listdir(public_folder), key=lambda x: [int(s) if s.isdigit() else s for s in re.split('(\d+)', x)])
            print("Updated files order:", files)

            return jsonify({'message': 'Files moved down successfully', 'new_filename_down': new_filename_down, 'new_filename': new_filename})

        else:
            return jsonify({'message': 'File is already at the bottom'})

    except FileNotFoundError:
        return jsonify({'error': 'Section not found'})

    except Exception as e:
        return jsonify({'error': str(e)})



# Move file UP in the file list
@app.route('/move_up/<section_number>/<filename>', methods=['PUT'])
def move_up(section_number, filename):
    section_path = f'section{section_number}'
    public_folder = "./public/" + section_path

    try:
        files = sorted(os.listdir(public_folder), key=lambda x: [int(s) if s.isdigit() else s for s in re.split('(\d+)', x)])
        print("Current files order:", files)

        # Find the index of the target file
        index = next((i for i, file in enumerate(files) if file == filename), None)

        # Ensure that the file is not already at the top
        if index is not None and index > 0:
            # Swap file positions
            
            filename=files[index]
            filename_up = files[index - 1]
            print("filename: ", filename)
            print("filename_up: ", filename_up)


            # Use the code for swapping file names
            file_name = filename.split("_")
            file_name_up = filename_up.split("_")

            new_filename = file_name[0] + "_" + file_name_up[1] + "_" + file_name[2] + "_" + file_name[3]
            new_filename_up = file_name_up[0] + "_" + file_name[1] + "_" + file_name_up[2] + "_" + file_name_up[3]
            

            # Print information for debugging
            print("Swapping files:")
            print("  - Original Filename to be changed:", filename)
            print("  - Original Filename to swap with:", filename_up)
            print("  - New Filename for the changed file:", new_filename_up)
            print("  - New Filename for the swapped file:", new_filename)

            # Rename the files
            os.rename(os.path.join(public_folder, filename_up), os.path.join(public_folder, "temp"))
            os.rename(os.path.join(public_folder, filename), os.path.join(public_folder, new_filename))
            os.rename(os.path.join(public_folder, "temp"), os.path.join(public_folder, new_filename_up))

            # Print updated files order
            files = sorted(os.listdir(public_folder), key=lambda x: [int(s) if s.isdigit() else s for s in re.split('(\d+)', x)])
            print("Updated files order:", files)

            return jsonify({'message': 'Files moved up successfully', 'new_filename_up': new_filename_up, 'new_filename': new_filename})

        else:
            return jsonify({'message': 'File is already at the top'})

    except FileNotFoundError:
        return jsonify({'error': 'Section not found'})

    except Exception as e:
        return jsonify({'error': str(e)})



@app.route('/add_csv/<section_number>', methods=['POST'])
def add_csv(section_number):
    # Define the folder path where the CSV file will be saved
    folder_path = f"./public/section{section_number}"
    latest_file_number = 0
    # Check if the folder exists, create it if not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        # Check if the request contains a file
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        # Check if the file has a valid filename
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the file to the specified folder
        #print("file.filename: ", file.filename)
        filename = file.filename
        for filename in os.listdir(folder_path):
            match = re.match(rf"section{section_number}_(\d+)_output_.*", filename)
            
            if match:
                file_number = int(match.group(1))
                latest_file_number = max(latest_file_number, file_number)

        # Increment the latest file number
        new_file_number = latest_file_number + 1

        # Construct the new file name
        new_file_name = f"section{section_number}_{new_file_number}_output_csv.csv"
        file_path = os.path.join(folder_path, new_file_name)
        file.save(file_path)

        return jsonify({'message': 'File uploaded successfully'}), 200

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    

#Create Rst files method 

def create_rst_files():
    print("Creating RST files")
    subprocess.run(["python3", "scripts/createrst.py"])

#Create Rst files method
@app.route('/update', methods=['POST'])
def update():
    print("Updating RST files")
    create_rst_files()

    #change directory to read-the-docs
    os.chdir("read-the-docs")

    #Build the html files and show the output in the terminal
    
    subprocess.run(["make", "html"])

    #change directory to the main folder
    os.chdir("..")

    return "Success"





#Add document details in the details folder 
@app.route('/document_details/<document_name>', methods=['POST'])  
def add_document_details(document_name):
    directory_file_path = f"./public/details/{document_name}.txt"
    print("directory_file_path: ", directory_file_path)
    
    new_content = request.json.get('content', '')
    print("new_content: ", new_content)

    #Rewrite the file with the new content
    with open(directory_file_path, 'w') as f:
        f.write(new_content)

    return "Success"


#Get all the document details from the details folder
@app.route('/document_details/', methods=['GET'])
def get_all_details():
    print("Getting all the details")
    directory_file_path = f"./public/details/"
    print("directory_file_path: ", directory_file_path)

    try:
        files = []
        #Print the files in the folder

        for filename in sorted(os.listdir(directory_file_path), key=lambda x: [int(s) if s.isdigit() else s for s in re.split('(\d+)', x)]):
            print(filename)
            if allowed_file(filename):
                file_path = os.path.join(directory_file_path, filename)
                with open(file_path, 'rb') as file:
                    content = file.read().decode('utf-8')

                files.append({'name': filename, 'content': content})

        return jsonify(files)

    except Exception as e:
        print(f'Error reading files: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500
    

#Update multiple details files from the detail folder at once 
@app.route('/update_details/', methods=['POST'])
def update_multiple_details():
    print("Updating multiple details")
    directory_file_path = f"./public/details/"
    print("directory_file_path: ", directory_file_path)

    try:
        #Get the data from the request
        data = request.json.get('data', [])
        print("data: ", data)

        for file in data:
            print("file: ", file)
            file_name = file['name']
            print("file_name: ", file_name)
            file_content = file['content']
            print("file_content: ", file_content)

            #Rewrite the file with the new content
            with open(directory_file_path + file_name, 'w') as f:
                f.write(file_content)

        return "Success"

    except Exception as e:
        print(f'Error updating files: {e}')
        return jsonify({'error': 'Internal Server Error'}), 500








if __name__ == '__main__':
    app.run(debug=True, host=host_ip, port=65000)