from subprocess import Popen

import sys
import os
import log
import shutil
temp_java = 'java -jar tm-java.jar -sp'
class_path = '-cp'
include_path = '-ip'
log_message = '-print -trace -no-date-check -no-ii -no-dc >'


logger = log.CreateLogger('my')
#1. target 경로와 plugin 경로가 존재하는 경로인가
#                      폴더인가
#                       파일들이 몇개 들어 있는가

#2. target파일들이 plugin 폴더들 비교 후 가져오기
#                       target, plugin 경로에 있는 폴더 리스트가져오기
#                       tartget에 있는 파일이 plugin에 있으면 해당 파일 전체경로 가져오기
#                       현재 작업디렉터리에 plugin 파일 만들기

#                       plugin파일에 붙여넣기

def getWorkingDirectoryPath():
    logger.debug('getWorkingDirectoryPath() called!!')
    return os.getcwd()


def getFileList(absolute_path):
   logger.debug('getFileList() called!!')
   file_list = os.listdir(absolute_path)
   return file_list


def findFolder(absolute_path,file_name):
    # folders = ['plugins','latest_build','coverage','log']
    # temp_file_name = 0
    # for file in folders:
    #     if file_name == file:
    if file_name in os.listdir(absolute_path):
        return os.path.join(absolute_path,file_name)


def makeFolder():
    logger.debug('makeFolder() called!!')
    work_dir = getWorkingDirectoryPath()
    folders = ['plugins','latest_build','coverage','log']
    try:
        for folder_name in folders:
            absolute_path = os.path.join(work_dir, folder_name)
            if not (os.path.isdir(absolute_path)):
                os.makedirs(absolute_path)
                logger.info('created folder: {0}'.format(absolute_path))
        return True
    except OSError as e:
        if e.errno != e.errno.EEXIST:
            print("Failed to create directory!!")
        return False


def makeFullpath(path,file_list):
    logger.debug('makeFullpath() called!!')
    full_path_list = []
    for file in file_list:

        full_path_list.append(os.path.join(path, file))
        logger.debug('make full path: {0}'.format(file))
    return full_path_list


def makeExpandTargetfile(target_folder_list):
    logger.debug('makeExpandTargetfile() called!!')
    expand_file = []
    for file_name in target_folder_list:
        expand_file.append(file_name + '_')
        print(file_name+'_')
    return expand_file

def temtemp(plugin_folder_list, target_folder_list):
    logger.debug('temtemp() called!!')
    file = []
    count = 0
    for plugin_file in plugin_folder_list:
        number = plugin_file.rfind('_')
        temp = plugin_file[:number + 1]

        for target_file in target_folder_list:
            if (target_file == temp):
                file.append(target_file)
    file_temp = []
    for target_file in file:
        file_temp.append(target_file[:-1])
    return file_temp


def compare(plugin_folder_list, target_folder_list):
    logger.debug('compare() called!!')
    file = []
    count = 0
    number = plugin_folder_list[0].rfind('_')

    for plugin_file in plugin_folder_list:
        number = plugin_file.rfind('_')
        temp = plugin_file[:number+1]

        for target_file in target_folder_list:
            if (target_file == temp) :
                file.append(plugin_file)
                logger.info('plugins: {0}'.format(plugin_file))
                logger.info('target: {0}'.format(target_file))


    logger.info('number of file: {0}'.format(len(file)))
    return file


def copy_file(file_list,dst_path):
    number_of_file_list = len(file_list)
    count = 1
    try:
        for file, dst in zip(file_list, dst_path):
            if os.path.isfile(file):
                logger.info('file: {0}\n{1}/{2}'.format(file,count,number_of_file_list))
                shutil.copyfile(file, dst)
                count += 1
            elif os.path.isdir(file):
                logger.info('folder: {0}\n{1}/{2}'.format(file,count,number_of_file_list))
                shutil.copytree(file, dst)
                count += 1
            else:
                logger.debug('file, folder도 아니다')
                continue
        logger.info('file copy success!!')
        return True
    except IOError as e:
        #src가 존재하지 않을 때
        #src가 존재하지만 src에 접근할 수 없을 때
        #dst가 writable하지 않을 때
        logger.info(e)
        return False


def copy_target_file(path):
    pass


def make_empty_batch_file(plugins_list_path,latest_build_list_path,coverage_file_path,log_file_path):
    logger.debug('make_empty_batch_file() called!!')
    temp_file_name = os.path.join(getWorkingDirectoryPath(), 'coverage_build.bat')
    with open(temp_file_name,'w') as file:
        logger.info('make batch file: {0}'.format(temp_file_name))
        for plugins_file, target_file, coverage_file in zip(plugins_list_path, latest_build_list_path, coverage_file_path):
            temp_string = temp_java +' "'+target_file+'\src" '+ class_path+' "' + plugins_file+'" ' + include_path +' "'+ coverage_file +'" '+ log_message+' "' +log_file_path+'\\temp.txt"'+'\n'
            file.write(temp_string)
    return temp_file_name


def remove_lockfile(absolute_coverage_path):
    file_list = getFileList(absolute_coverage_path)
    lock = '.lock'

    for file_name in file_list:
       if lock in file_name:
           temp = os.path.join(absolute_coverage_path, file_name)
           print(temp)
           if os.path.isfile(temp):
               os.remove(temp)
               logger.info('remove .lock file: {0}'.format(temp))
           elif os.path.isdir(temp):
               os.rmdir(temp)
               logger.info('remove .lock folder: {0}'.format(temp))
           else:
               logger.info('삭제할 수 없습니다.')



def main(plugin_absolute_path, target_absolute_path):
    logger.debug('main() called!!')
    if not makeFolder():

        return False
    plugin_folder_list = getFileList(plugin_absolute_path)
    target_folder_list = getFileList(target_absolute_path)
    logger.info('number of Plugin file: {0}\n number of Target file: {1}'.format(len(plugin_folder_list),len(target_folder_list)))
    if len(target_folder_list) == 0:
        logger.info('Target file의 개수가 0개 입니다.')
        return False
    elif len(plugin_folder_list) == 0:
        logger.info('Plugin file의 개수가 0개 입니다.')
        return False
    temp = makeExpandTargetfile(target_folder_list)
    original_plugin_list = compare(plugin_folder_list,temp)
    original_target_list = temtemp(plugin_folder_list,temp)

    makeFullpath(plugin_absolute_path, original_plugin_list)

    target_path = os.path.join(getWorkingDirectoryPath(),'latest_build')
    plugins_path = os.path.join(getWorkingDirectoryPath(),'plugins')
    log_path = os.path.join(getWorkingDirectoryPath(),'log')
    coverage_path = os.path.join(getWorkingDirectoryPath(),'coverage')
    plugins_list_path = []
    target_list_path = []
    coverage_list_path = []

    for plugin_file, target_file in zip(original_plugin_list, original_target_list):
        plugins_list_path.append(os.path.join(plugins_path, plugin_file))
        target_list_path.append(os.path.join(target_path, target_file))
        coverage_list_path.append(os.path.join(coverage_path, plugin_file))

    if not copy_file(makeFullpath(plugin_absolute_path, original_plugin_list), plugins_list_path):
        log.info('파일/폴더에 문제가 있어 프로그램을 종료합니다..')
        return False
    if not copy_file(makeFullpath (target_absolute_path, original_target_list), target_list_path):
        log.info('파일/폴더에 문제가 있어 프로그램을 종료합니다..')
        return False

    bat_path = make_empty_batch_file(plugins_list_path, target_list_path, coverage_list_path, log_path)

    p = Popen(bat_path)
    stdout, stderr = p.communicate()
    logger.info('excute batch file: {0}'.format(bat_path))

    remove_lockfile(coverage_path)
    return True


if __name__ == '__main__':
    pass