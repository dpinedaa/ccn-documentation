import os
import re

file_directory = './public'
output_folder = './read-the-docs/source'
section_with_title = []


def extract_title(title):
    title_content = title.read()
    lines = title_content.split("\n")
    for line in lines:
        if line.startswith("Style:"):
            style = line.split(":")[1].strip()
            print(style)
        elif line.startswith("Content:"):
            content_text = line.split(":", 1)[1].strip()
            print(content_text)

    print(title_content)

    return content_text


def gather_titles(file_directory):
    for section_number in range(1, 21):
        print(f"Section {section_number}:")
        section_directory = os.path.join(file_directory, f'section{section_number}')
        for filename in os.listdir(section_directory):
            if filename.endswith("title.txt"):
                # Add section to the array
                section_with_title.append(section_number)
                print(filename)

                # Gather the file content
                title_file_path = os.path.join(section_directory, filename)
                with open(title_file_path, 'r') as title_file:
                    title_content = extract_title(title_file)
                    print(title_content)

                # Create rst file
                rst_file_path = os.path.join(output_folder, f'section{section_number}.rst')
                with open(rst_file_path, 'w') as rst_file:
                    rst_file.write(f"{title_content}\n")
                    rst_file.write("+" * len(title_content) + "\n\n")


def remove_old_rsts(output_folder):
    for filename in os.listdir(output_folder):
        if filename.endswith(".rst") and filename != "index.rst":
            os.remove(os.path.join(output_folder, filename))
            print(f"Removed {filename}")


def extract_text_content_and_style(file_content, filename, section_number):
    style = ""
    content_text = ""
    current_indentation = 0

    lines = file_content.split("\n")
    length = len(lines)

    for line in lines:
        if line.startswith("Style:"):
            style = line.split(":")[1].strip()
            print(style)
        elif line.startswith("Content:"):
            content_text = line.split(":", 1)[1].strip()
            if ".png) --> Element Number" in line:
                break  # Exit the loop, no need to process the rest of the file
            if length > 4 and style == "Code Standalone":
                print(content_text)
                content_text = ""
                # Adjust the indentation in the "Content" block
                indent_level = line.find("{") + 1
                content_text += " " * current_indentation + line.split(":", 1)[1].strip() + "\n"
                if "{" in line:
                    current_indentation += 4
            elif style == "Normal":
                content_text += "\n"
            elif style == "Code Standalone":
                print(content_text)

        elif length > 4:
            if style == "Normal":
                content_text += "\n"

            if line == "}":
                current_indentation = max(0, current_indentation - 4)

            content_text += " " * current_indentation + line.strip() + "\n"

            if "{" in line:
                current_indentation += 4
            elif "}" in line:
                current_indentation = max(0, current_indentation - 4)

    return content_text, style


def write_txt_to_rst(content_text, style, section_number, output_folder, filename):
    rst_file_path = os.path.join(output_folder, f'section{section_number}.rst')

    with open(rst_file_path, 'a', encoding='utf-8') as rst_file:
        if style == "Heading 1":
            rst_file.write(f"{content_text}\n")
            rst_file.write("+" * len(content_text) + "\n\n")
        elif style == "Heading 2":
            rst_file.write(f"{content_text}\n")
            rst_file.write("=" * len(content_text) + "\n\n")
        elif style == "Heading 3":
            rst_file.write(f"{content_text}\n")
            rst_file.write("-" * len(content_text) + "\n\n")
        elif style == "Caption":
            rst_file.write(f"\n\n**{content_text}:**\n\n")
        elif style == "List Paragraph":
            rst_file.write(f"* {content_text}\n\n")
        elif style == "Normal":
            rst_file.write(f"{content_text}\n\n")
        elif style == "Bold":
            rst_file.write(f"\n**{content_text}**\n\n")
        elif style == "Code Standalone":
            codeblock_path = os.path.join('../../public', f'section{section_number}', filename)
            rst_file.write(f".. literalinclude:: {codeblock_path}\n")
            rst_file.write('   :language: bash\n\n')

def process_file_csv( section_number, output_folder, filename):
    rst_file_path = os.path.join(output_folder, f'section{section_number}.rst')

    csv_path = f"../../public/section{section_number}/{filename}    "
    with open(rst_file_path, 'a', encoding='utf-8') as rst_file:
        rst_file.write('.. csv-table:: \n')
        rst_file.write(f'   :file: {csv_path}\n')
        rst_file.write('   :header-rows: 1\n')
        rst_file.write('   :align: center\n\n')
        rst_file.write('\n\n')
        rst_file.write('|')
        rst_file.write('\n\n')



def process_file_png( section_number, output_folder, filename):
    rst_file_path = os.path.join(output_folder, f'section{section_number}.rst')
    image_path = f'../../public/section{section_number}/{filename}'
    
    print("IMAGE PATH: ", image_path)

    with open(rst_file_path, 'a', encoding='utf-8') as rst_file:
        rst_file.write(f".. image:: {image_path}\n")
        rst_file.write('   :height: 350px\n')
        rst_file.write('   :align: center\n\n')
        rst_file.write('\n\n')
        rst_file.write('|')
        rst_file.write('\n\n')



def add_files_to_rst(output_folder):
    for section_number in section_with_title:
        section_directory = os.path.join(file_directory, f'section{section_number}')

        # Use sorted() with a custom sorting key
        for filename in sorted(os.listdir(section_directory), key=lambda x: [int(s) if s.isdigit() else s for s in re.split('(\d+)', x)]):
            print(filename)
            
            # Initialize content_text here
            content_text = ""
            
            if filename.endswith(".txt") and not filename.endswith("title.txt"):
                file_path = os.path.join(section_directory, filename)
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    content_text, style = extract_text_content_and_style(file_content, filename, section_number)
                    write_txt_to_rst(content_text, style, section_number, output_folder, filename)
            
            elif filename.endswith(".csv"):
                process_file_csv( section_number, output_folder, filename)
            
            elif filename.endswith(".png"):
                process_file_png( section_number, output_folder, filename)



# create main
def main():
    remove_old_rsts(output_folder)
    gather_titles(file_directory)
    add_files_to_rst(output_folder)


if __name__ == "__main__":
    main()
