import xml.dom.minidom
import os
import sys
import json
from shutil import copyfile, rmtree
from pathlib import Path
from operator import itemgetter

global SERVER_PROJECTS_FOLDER_PATH
global XML_PROJECTS_FOLDER
global PROJECT_EXCEPTIONS
# 'D:/Django/implementaciones-ssalud/Implementaciones/project/ProjectsCopy'
SERVER_PROJECTS_FOLDER_PATH = '//p-is-01.ams.red/ssis2017$/02 - Proyectos SSIS'
XML_PROJECTS_FOLDER = 'project/XMLProjects/'
TXT_SQL = 'project/SqlStatement.txt'
PROJECT_EXCEPTIONS = {'Indicadores Estrategicos': 1,
                      'Presupuesto vs Balance': 1,
                      'Trazabilidad de Fichas': 1,
                      'Data Comercial': 1,
                      'Data Ordenes e Internaciones': 2,
                      'Web Centrix': 3}


def main():
    print(get_projects_data())
    # delete_file_resultado_txt()
    # is_input_empty()
    # results()


def resolver_ruta(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath('.'), ruta_relativa)


"""Obtiene los data de todos los proyectos que se encuentran p-is-01/SSIS2017$/02 - Proyectos SSIS"""


def get_projects_data():
    try:
        if not os.path.exists(XML_PROJECTS_FOLDER):
            os.makedirs(XML_PROJECTS_FOLDER)
        else:
            delete_XMLProjects_folder_files()
        projects_list = get_projects_list_from_server()
        if not projects_list:
            print("Error: No existen proyectos en la ruta " +
                  SERVER_PROJECTS_FOLDER_PATH + "\n")
            pass
        else:
            projects = []
            for each_project in projects_list:
                project_name = each_project
                project = {"project_name": project_name, "packages": []}
                files_list = os.listdir(get_project_path_files_from(
                    project_name, SERVER_PROJECTS_FOLDER_PATH))
                project_dtsx_files_list = [
                    each_file for each_file in files_list if each_file[-5:] == ".dtsx"]
                project_files_list = copy_project_dtsx_files_to_XML_folder(
                    project_name, project_dtsx_files_list)
                if project_files_list:
                    for each_package in project_files_list:
                        package_name = each_package[:-4]
                        package_tasks_list = get_package_task_data(
                            project_name, package_name)
                        package = {"package_name": package_name, "tasks": []}
                        for each_task in package_tasks_list:
                            package["tasks"].append({"task_name": each_task})
                        project["packages"].append(package)
                    projects.append(project)
            projects_json = json.dumps(projects)
            return projects_json
    except FileNotFoundError as err:
        print("Error de carpeta: No existe la ruta proporcionada o no tiene permisos"+str(err)+"\n")
        error = json.dumps({"Error"})
        return error


"""Copia los archivos DSTX de cada proyecto a la carpeta local XMLProjects"""


def copy_project_dtsx_files_to_XML_folder(project_name, project_dtsx_files_list=[]):
    create_folder_project(project_name)
    for each_file in project_dtsx_files_list:
        file_src = get_project_path_files_from(
            project_name, SERVER_PROJECTS_FOLDER_PATH)+"/"+each_file
        file_dst = XML_PROJECTS_FOLDER+project_name+"/"+each_file
        copyfile(file_src, file_dst)
    change_extension(get_project_path_files_from(
        project_name, XML_PROJECTS_FOLDER))
    project_files_list = os.listdir(
        get_project_path_files_from(project_name, XML_PROJECTS_FOLDER))
    return project_files_list


"""Crea una carpeta con el nombre del proyecto para ordenar mejor los paquetes"""


def create_folder_project(project_name):
    Path(XML_PROJECTS_FOLDER+project_name).mkdir(parents=True, exist_ok=True)


"""Devuelve la ruta de los archivos DSTX del proyecto dependiendo si se encuentra o no en las excepciones"""


def get_project_path_files_from(project_name, folder=None):
    if folder == XML_PROJECTS_FOLDER:
        project_files_path = folder+project_name
    else:
        if project_name in PROJECT_EXCEPTIONS:
            if PROJECT_EXCEPTIONS[project_name] == 1:
                project_files_path = folder+"/"+project_name
            elif PROJECT_EXCEPTIONS[project_name] == 2:
                project_files_path = folder + \
                    "/Data Ordenes e Internaciones/Data Ordenes e Internaciones Vigente"
            elif PROJECT_EXCEPTIONS[project_name] == 3:
                project_files_path = folder+"/Web Centrix/WebCentrix"
        else:
            project_files_path = folder + '/' + project_name + '/' + project_name
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
    project_package_tasks_names = []
    doc = xml.dom.minidom.parse(
        XML_PROJECTS_FOLDER+project_name+"/"+package_name+".xml")
    dts_padre = doc.getElementsByTagName("DTS:Executables")
    for pprop in dts_padre:
        dts_hijo = pprop.getElementsByTagName("DTS:Executable")
        for hprop in dts_hijo:
            task = hprop.attributes._attrs['DTS:ObjectName'].nodeValue
            project_package_tasks_names.append(task)
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
    #projects_list = os.listdir(SERVER_PROJECTS_FOLDER_PATH)
    projects_list = [name for name in os.listdir(SERVER_PROJECTS_FOLDER_PATH) if os.path.isdir(
        os.path.join(SERVER_PROJECTS_FOLDER_PATH, name))]
    return projects_list


"""Obtiene el listado de proyectos que se encuentran en la carpeta local XMLProjects"""


def get_projects_list_from_local():
    projects_list = os.listdir(XML_PROJECTS_FOLDER)
    return projects_list


"""Cambia la extension de los archivos de DTSX a XML"""


def change_extension(folder):
    for filename in os.listdir(folder):
        if filename[-5:] == ".dtsx":
            infilename = os.path.join(folder, filename)
            if not os.path.isfile(infilename):
                continue
            oldbase = os.path.splitext(filename)
            newname = infilename.replace('.dtsx', '.xml')
            output = os.rename(infilename, newname)


def get_sql_search(string_search):

    result = {'result': []}

    projects_list = get_projects_list_from_local()
    if not projects_list:
        print("Error: No existen proyectos en la ruta \n")
        pass
    else:
        for each_project in projects_list:
            project_name = each_project
            files_list = os.listdir(get_project_path_files_from(
                project_name, XML_PROJECTS_FOLDER))
            for each_file in files_list:
                json_list = find_xml(project_name, each_file, string_search)
                for json_item in json_list:
                    result['result'].append(json_item)
    return result


"""Busca el codigo SQL, Nombre del paquete y Tarea dentro del XML"""


def find_xml(project_name, filename, string_search):
    path = get_project_path_files_from(project_name, XML_PROJECTS_FOLDER)
    doc = xml.dom.minidom.parse(path+"/"+filename)

    nombre_archivo = TXT_SQL

    json_result = []

    package = filename[:-4]

    dts_padre = doc.getElementsByTagName("DTS:Executables")
    for pprop in dts_padre:
        dts_hijo = pprop.getElementsByTagName("DTS:Executable")
        for hprop in dts_hijo:
            task = hprop.attributes._attrs['DTS:ObjectName'].nodeValue
            SQL = hprop.getElementsByTagName("SQLTask:SqlTaskData")
            for prop in SQL:
                sql_script = prop.getAttribute("SQLTask:SqlStatementSource")
                write_sql_scrip_on_txt(sql_script, project_name, package, task)

                # Copia el script SQL completo
                f = open(nombre_archivo, 'r')
                script_completo = f.read()
                cant_lineas = len(script_completo.splitlines())
                f.close()

                # Crea json con la linea y numero del txt donde se encuentra el valor buscado
                with open(nombre_archivo) as myFile:
                    numeracion = enumerate(myFile, 1)
                    for num, line in numeracion:
                        if string_search.lower() in line.lower():
                            json_result.append({'n_line': str(num), 'line': str(line), 'project': str(project_name), 'package': str(
                                package), 'task': str(task), 'script': str(script_completo), 'cant_lineas': str(cant_lineas)})
                            # json_result.append({'n_line':str(num), 'line':str(line), 'project': str(project_name), 'package': str(package), 'task':str(task)})

    return json_result


"""Copia el script SQL de la tarea en el txt SqlStatement.txt"""


def write_sql_scrip_on_txt(sql_script, project_name, package, task):
    nombre_archivo = TXT_SQL
    f = open(nombre_archivo, "a+")
    f.truncate(0)
    f.write(sql_script)
    f.close()


if __name__ == "__main__":
    main()
