import xml.dom.minidom
import os
import sys
from shutil import copyfile, rmtree
from pathlib import Path
import json


def main():
    global SERVER_PROJECTS_FOLDER_PATH
    global XML_PROJECTS_FOLDER
    global PROJECT_EXCEPTIONS
    #PROJECTS_FOLDER_PATH = '//P-IS-01/SSIS2017$/02 - Proyectos SSIS'
    SERVER_PROJECTS_FOLDER_PATH = 'D:/Django/implementaciones-ssalud/Implementaciones/project/ProjectsCopy'
    XML_PROJECTS_FOLDER = 'XMLProjects/'
    PROJECT_EXCEPTIONS = {'Indicadores Estrategicos': 1,
                      'Presupuesto vs Balance': 1,
                      'Trazabilidad de Fichas': 1,
                      'Data Comercial': 1,
                      'Data Ordenes e Internaciones': 2}
    print(get_projects_data())
    #delete_file_resultado_txt()
    #is_input_empty()
    #results()


# global SERVER_PROJECTS_FOLDER_PATH
# global XML_PROJECTS_FOLDER
# global PROJECT_EXCEPTIONS
# SERVER_PROJECTS_FOLDER_PATH = 'D:/Django/implementaciones-ssalud/Implementaciones/project/ProjectsCopy'
# XML_PROJECTS_FOLDER = 'XMLProjects/'
# PROJECT_EXCEPTIONS = {'Indicadores Estrategicos': 1,
#                       'Presupuesto vs Balance': 1,
#                       'Trazabilidad de Fichas': 1,
#                       'Data Comercial': 1,
#                       'Data Ordenes e Internaciones': 2}


class ProjectList:
    def __init__(self, p_name, p_packages={}):
        self.name = p_name
        self.packages = p_packages


def resolver_ruta(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath('.'), ruta_relativa)


"""Obtiene los data de todos los proyectos que se encuentran p-is-01/SSIS2017$/02 - Proyectos SSIS"""
def get_projects_data():
    try:
        delete_XMLProjects_folder_files()
        projects_list = get_projects_list_from_server()
        if not projects_list:
            print("Error: No existen proyectos en la ruta " + SERVER_PROJECTS_FOLDER_PATH + "\n")
            pass
        else:
            i = 0
            projects_data = []
            projects_data_dict = {}
            project_package_dict = {}
            for each_project in projects_list:
                project_name = each_project
                projects_data_dict[i] = {'project_name':project_name}
                files_list = os.listdir(get_project_path_files_from(project_name, SERVER_PROJECTS_FOLDER_PATH))
                project_dtsx_files_list = [each_file for each_file in files_list if each_file[-5:] == ".dtsx"]
                project_files_list = copy_project_dtsx_files_to_XML_folder(project_name, project_dtsx_files_list)
                project = ProjectList(project_name)
                projects_data_dict.append(project_name)
                if project_files_list:
                    for each_package in project_files_list:
                        package_name = each_package[:-4]
                        project_package_tasks_names = get_package_task_data(project_name, package_name)
                    project.packages = project_package_dict
                    projects_data_dict["packages"] = project_package_dict
                    projects_data.append(project)
                else:
                    print("No existen paquetes para el proyecto: "+ project_name +"\n")
                    pass
                i += 1
            return projects_data_dict      
    except FileNotFoundError as err:
        print("Error de carpeta: No existe la ruta proporcionada o no tiene permisos"+str(err)+"\n")
        sys.exit()

"""Copia los archivos DSTX de cada proyecto a la carpeta local XMLProjects"""
def copy_project_dtsx_files_to_XML_folder(project_name, project_dtsx_files_list=[]):
    create_folder_project(project_name)
    for each_file in project_dtsx_files_list:
        file_src = get_project_path_files_from(project_name,SERVER_PROJECTS_FOLDER_PATH)+"/"+each_file
        file_dst = XML_PROJECTS_FOLDER+project_name+"/"+each_file
        copyfile(file_src, file_dst)
    change_extension(get_project_path_files_from(project_name, XML_PROJECTS_FOLDER))
    project_files_list = os.listdir(get_project_path_files_from(project_name, XML_PROJECTS_FOLDER))
    return project_files_list

"""Crea una carpeta con el nombre del proyecto para ordenar mejor los paquetes"""
def create_folder_project(project_name):
    Path(XML_PROJECTS_FOLDER+project_name).mkdir(parents=True, exist_ok=True)

"""Devuelve la ruta de los archivos DSTX del proyecto dependiendo si se encuentra o no en las excepciones"""
def get_project_path_files_from(project_name,folder=None):
    if folder == XML_PROJECTS_FOLDER:
        project_files_path = folder+"/"+project_name
    else:
        if project_name in PROJECT_EXCEPTIONS:
            if PROJECT_EXCEPTIONS[project_name] == 1:
                project_files_path = folder+"/"+project_name
            elif PROJECT_EXCEPTIONS[project_name] == 2:
                project_files_path = folder+"/Data Ordenes e Internaciones Vigente"
        else:
            project_files_path = folder +'/'+ project_name +'/'+ project_name
    return project_files_path

"""Borra archivos de la carpeta XMLProjects"""
def delete_XMLProjects_folder_files():
    for filename in os.listdir(XML_PROJECTS_FOLDER):
        file_path = os.path.join(XML_PROJECTS_FOLDER, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                rmtree(file_path)
        except Exception as e:
            print('Error al borrar %s. Motivo: %s' % (file_path, e))


"""Devuelve listas con las task pertenecientes al package"""
def get_package_task_data(project_name, package_name):
    # project_package_tasks_names = []
    project_package_tasks_names_dict = {}
    doc = xml.dom.minidom.parse(XML_PROJECTS_FOLDER+project_name+"/"+package_name+".xml")
    dts_padre = doc.getElementsByTagName("DTS:Executables")
    for pprop in dts_padre:
        dts_hijo = pprop.getElementsByTagName("DTS:Executable")
        for hprop in dts_hijo:
            task = hprop.attributes._attrs['DTS:ObjectName'].nodeValue
            # project_package_tasks_names.append(task)
            project_package_tasks_names_dict["task_name"].append(task)
            
    return project_package_tasks_names


"""Verifica si existe la carpeta XML. De lo contrario el programa termina"""
def is_folder_empty():
    try:
        if os.listdir(XML_PROJECTS_FOLDER):
            return False
        else:
            return True
    except FileNotFoundError:
        print("Error de carpeta: No existe la carpeta XML en la raiz del programa\n")
        sys.exit()

"""Obtiene listado de proyectos que se encuentran en el servidor P-IS-01"""
def get_projects_list_from_server():
    projects_list = os.listdir(SERVER_PROJECTS_FOLDER_PATH)
    return projects_list

"""Obtiene el listado de proyectos que se encuentran en la carpeta local XMLProjects"""
def get_projects_list_from_local():
    projects_list = os.listdir(XML_PROJECTS_FOLDER)
    return projects_list


"""Cambia la extension de los archivos de DTSX a XML"""
def change_extension(folder):
    for filename in os.listdir(folder):
        if filename[-5:] == ".dtsx":
            infilename = os.path.join(folder,filename)
            if not os.path.isfile(infilename): continue
            oldbase = os.path.splitext(filename)
            newname = infilename.replace('.dtsx', '.xml')
            output = os.rename(infilename, newname)


"""Busca el codigo SQL, Nombre del paquete y Tarea dentro del XML"""
def find_xml(filename, string_search):
    doc = xml.dom.minidom.parse(XML_PROJECTS_FOLDER+filename)
    
    package = filename[:-4]

    dts_padre = doc.getElementsByTagName("DTS:Executables")
    for pprop in dts_padre:
        dts_hijo = pprop.getElementsByTagName("DTS:Executable")
        for hprop in dts_hijo:
            task = hprop.attributes._attrs['DTS:ObjectName'].nodeValue
            SQL = hprop.getElementsByTagName("SQLTask:SqlTaskData")
            for prop in SQL:
                sql_script = prop.getAttribute("SQLTask:SqlStatementSource")
                write_sql_scrip_on_txt(sql_script, package, task, string_search)


"""Copia el script SQL de la tarea en el txt SqlStatement.txt"""
def write_sql_scrip_on_txt(sql_script, package, task, string_search):

    nombre_archivo = resolver_ruta("SqlStatement.txt")

    f=open(nombre_archivo, "a+")
    f.truncate(0)
    f.write(sql_script)
    f.close()

    find_in_txt(string_search, package, task)


"""Recorre el SqlStatement en busqueda del texto ingresado en el inicio 
y guarda en que linea se encontró, el nombre del paquete y de la tarea"""
def find_in_txt(string_search, package, task):
    nombre_archivo = resolver_ruta("SqlStatement.txt")
    archivo_resultado = resolver_ruta("resultado.txt")


    f=open(archivo_resultado, "a+")

    with open(nombre_archivo) as myFile:
        for num, line in enumerate(myFile, 1):
            if string_search in line:
                f.write("#########################################################\n")
                f.write("Codigo buscado: "+string_search+'\n')
                f.write('Encontrado en linea: '+str(num)+'\n')
                f.write(line+"\n")
                f.write('Paquete: ' + str(package) + '\n')
                f.write('Tarea: ' + str(task) + '\n')
                f.write("_________________________________________________________\n")
                f.write("\n")
                f.write("\n")
    f.close()


if __name__ == "__main__":
    main()