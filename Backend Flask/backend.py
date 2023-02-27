import os                  # Required for directory traversal
import shutil              # Required for working with temporary directories
import tempfile            # Required for creating temporary directories
import zipfile             # Required for working with zip files
import javalang            # Required for parsing Java source code


def __get_start_end_for_node(node_to_find,tree):
    start = None
    end = None
    for path, node in tree:
        if start is not None and node_to_find not in path:
            end = node.position
            return start, end
        if start is None and node == node_to_find:
            start = node.position
    return start, end


def __get_string(start, end,data):
    if start is None:
        return ""

    # positions are all offset by 1. e.g. first line -> lines[0], start.line = 1
    end_pos = None

    if end is not None:
        end_pos = end.line - 1

    lines = data.splitlines(True)
    string = "".join(lines[start.line:end_pos])
    string = lines[start.line - 1] + string

    # When the method is the last one, it will contain a additional brace
    if end is None:
        left = string.count("{")
        right = string.count("}")
        if right - left == 1:
            p = string.rfind("}")
            string = string[:p]

    return string



# Extract the contents of the zip file to a temporary directory
def extract_zip(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        # Extract the contents of the zip file to the temporary directory
        zip_file.extractall(temp_dir)
        # List the files in the temporary directory
        files_in_temp_dir = os.listdir(temp_dir)
        # Update the temporary directory path to the first extracted directory
        temp_dir = os.path.join(temp_dir, files_in_temp_dir[0])
        # List the files in the updated temporary directory
        files_in_temp_dir = os.listdir(temp_dir)
        # Return the temporary directory path
        return temp_dir

# Load all Java source files in a directory and its subdirectories into memory
def load_files(dir_path):
    files = []
    for root, dirs, filenames in os.walk(dir_path):
        # Traverse the directory tree, and for each file found, add its contents to the `files` list
        for filename in filenames:
            # Check if the file is a Java source file
            if filename.endswith('.java'):
                with open(os.path.join(root, filename), 'r') as f:
                    files.append(f.read())
    # Return the list of Java source files
    return files

# Find all classes that extend the RestController class
def find_classes_and_interfaces(java_sources):
    controllers = {}
    entities={}
    repositories={}
    services={}
    for i in java_sources:
        # Parse the Java source code
        tree = javalang.parse.parse(i)
        for path, node in tree:
            if isinstance(node, javalang.tree.InterfaceDeclaration):
                # Check if the interface extends JpaRepository
                if node.extends is not None:
                    for j in node.extends:
                        if 'JpaRepository' in j.name:
                            start,end=__get_start_end_for_node(node,tree)
                            repositories[node.name]=__get_string(start,end,i)
                # Check if the interface is annotated with @RestController, @Controller or @RequestMapping
                for annotation in node.annotations:
                    if isinstance(annotation, javalang.tree.Annotation):
                        if annotation.name == 'RestController' or annotation.name == 'Controller' or annotation.name == 'RequestMapping':
                            start,end=__get_start_end_for_node(node,tree)
                            controllers[node.name]=__get_string(start,end,i)
                        # Check if the interface is annotated with @Entity
                        if annotation.name == 'Entity':
                            start,end=__get_start_end_for_node(node,tree)
                            entities[node.name]=__get_string(start,end,i)
                        
                        # Check if the interface is annotated with @Service
                        if annotation.name == 'Service':
                            start,end=__get_start_end_for_node(node,tree)
                            services[node.name]=__get_string(start,end,i)
                
            if isinstance(node, javalang.tree.ClassDeclaration):
                # Check if the class is annotated with @RestController, @Controller or @RequestMapping
                for annotation in node.annotations:
                    if isinstance(annotation, javalang.tree.Annotation):
                        if annotation.name == 'RestController' or annotation.name == 'Controller' or annotation.name == 'RequestMapping':
                            start,end=__get_start_end_for_node(node,tree)
                            controllers[node.name]=__get_string(start,end,i)
                        # Check if the class is annotated with @Entity
                        if annotation.name == 'Entity':
                            start,end=__get_start_end_for_node(node,tree)
                            entities[node.name]=__get_string(start,end,i)
                        
                        # Check if the interface is annotated with @Service
                        if annotation.name == 'Service':
                            start,end=__get_start_end_for_node(node,tree)
                            services[node.name]=__get_string(start,end,i)
                    
    # Return a dictionary with the lists of controllers, entities and repositories found
    return {"controllers": controllers, "entities": entities, "repositories": repositories, "services":services}


def zip_to_result(zip_file_path):
    extracted_dir = extract_zip(zip_file_path)      # Extract the contents of the zip file
    java_source = load_files(extracted_dir)  
    # Load all Java source files
    classes_interfaces = find_classes_and_interfaces(java_source)   # Find all controllers that extend RestController
    return classes_interfaces
