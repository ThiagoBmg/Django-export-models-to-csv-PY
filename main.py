
from genericpath import isdir, isfile
from os import listdir, system, terminal_size
from posixpath import join
import logging 

log = logging.getLogger(__name__)
logging.basicConfig(filename='service.log')

MODELS = list() 
"""

TODO:

"""
def extract_values(text:str):  
    #TODO: MELHORA
    try:
        
        text_ = text.split(' = models.')
        if len(text_) == 1:
            text_ = text.split('=models.')
        if len(text_) == 1:
            text_ = text.split(' =  models.')

        fild_name = text_[0]
        text_ = text_[1].split('(')
        fild_type  = text_[0]
        fild_description = text_[1].replace(')', '')
        fild_description = fild_description if len(fild_description) != 1  else '-'
        return fild_name, fild_type, fild_description
    except Exception as exc:
        #print(text.split(' = models.')[0])
        return '', '', ''
    
def extract_values2(text:str):
    try:
        text = text.split('= ')
        text_ = text[1].split('models.')
        fild_name = text[0]
        return [fild_name , (text_[1].split('('))[0]]
    except Exception as exc:
        return list('None')

def run2(FILE_NAME:str):
    t = list()
    qtd_models = 0 
    qtd_filds = 0

    with open(FILE_NAME,  'r') as file: 
        lines = file.readlines()
        for line in lines:
            try:
                if 'class' in line and 'models.Model' in line:
                    table_name = (line.split("class")[1]).split("(")[0]
                    qtd_models += 1
                elif 'models.' in line \
                    and not ('models.Model') in line \
                    and '=' in line \
                    and not 'Index' in line:

                    qtd_filds += 1

                    if '(' in line and ')' in line:
                        f_name, res, desc = extract_values(line)
                        t.append({
                            "table_name": table_name.replace(" ",""),
                            "fild_name":f_name.replace(" ",""),
                            "fild_type":res.replace(" ",""),
                            "desc":desc.replace("\n","")
                        }) if f_name.replace(" ","") != 'N' else ...
                    else:
                        d  = extract_values2(line)
                        if d:
                            t.append({
                                "table_name": table_name.replace(" ",""),
                                "fild_name":d[0].replace(" ",""),
                                "fild_type":d[1].replace(" ",""),
                                "desc":'-'.replace("\n","")
                            }) if d[0].replace("","") != 'N' else ...
            except Exception as exc:
                log.error(f'{FILE_NAME} - [ERRO AO FORMATAR CAMPO] {exc} - line: {line}')
            
    with open(FILE_NAME.replace('txt', 'csv')\
        .replace("extract_doc","extract_doc/csv"), 'w') as file:
        for i in t:
            file.writelines(f'{i.get("table_name")};')
            file.writelines(f'{i.get("fild_name")};')
            file.writelines(f'{i.get("fild_type")};')
            file.writelines(f'{i.get("desc")}\n')
    log.warning(f'{FILE_NAME} - Quantidade de Tabelas localizadas {qtd_models}')
    log.warning(f'{FILE_NAME} - Quantidade de campos localizados {qtd_filds}')

"""

TODO:

"""
def get_files_from_dir(dir:str):
    files = [file for file in listdir(f'../{dir}') 
        if isfile(join(f'../{dir}',file))]
    dirs = [file for file in listdir(f'../{dir}') 
        if isdir(join(f'../{dir}',file))]
    return files , dirs

def get_model_files_from_list(dir:str, list:str):
    for file in list:
        if file == 'models.py':
            MODELS.append((dir,file))
    pass

def run():
    IGNORE_DIRS = ['.venv', '.git']
    THIS_PATH = [dir for dir in listdir('..') \
        if isdir(join('..',dir)) \
        and dir not in IGNORE_DIRS ]

    print('Qual projeto deseja escanear... ', end="\n")
    index = 1
    
    for file_or_dir in THIS_PATH:
        print(f'{index} - {file_or_dir}' ,end="\n")
        index = index + 1

    PROJETO_PATH = int(input(''))

    files, dirs = get_files_from_dir(THIS_PATH[PROJETO_PATH-1])
    get_model_files_from_list(THIS_PATH[PROJETO_PATH-1],files)

    for d in dirs:
        files = [file for file in listdir(f'../{THIS_PATH[PROJETO_PATH-1]}/{d}')
            if isfile(f'../{THIS_PATH[PROJETO_PATH-1]}/{d}/{file}')]

        get_model_files_from_list(f'../{THIS_PATH[PROJETO_PATH-1]}/{d}', files)
    
    return MODELS

def main():
    """

    TODO:

    """
    system(' mkdir extract_doc ')
    system(' mkdir ./extract_doc/csv ')

    step01_ = run()
    list_ = list()
    for i in step01_:
        with open(f'{i[0]}/{i[1]}', 'r') as file:
            data = file.read()
        
        list_.append(f'./extract_doc/{i[0].replace("/","-").replace(".","")}.txt')

        with open(f'./extract_doc/{i[0].replace("/","-").replace(".","")}.txt', 'w') as n_file:
            n_file.write(data)
    system('clear')
    for i in list_:
        try:
            run2(i)
        except Exception as exc: 
            print(f'ERRO -> {exc}\n')
            pass

if __name__ == "__main__":
    main()