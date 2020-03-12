import configparser
import os
import datetime
import time


#####не забыть поменять пути для линукс
timeout = 15 #тут будет обновляться + в минутах
val1 = "C:\\Users\Agapova.E\\source\\repos\\PythonApplication3\\val1\\"
val2 = "C:\\Users\Agapova.E\\source\\repos\\PythonApplication3\\val2\\"

config = configparser.RawConfigParser()

# *создание папок
#os.mkdir("val2")
#print(os.listdir())

# *создание конфигов

def createConfig(path):
    config.add_section("FileName")
    config.set("FileName","name:file2.txt")
    config.add_section("Logs")
    config.set("Logs", "1")
    config.set("Logs", "signature_one")
    config.set("Logs", "10")
    config.set("Logs", "signature_two")
    config.set("Logs", "25")
    config.set("Logs","signature_three")
    #config.set("Logs", "15")
    #config.set("Logs", "signature_four")
    with open(path, "w") as config_file:
        config.write(config_file) 
#createConfig(val2 + "conf2.cfg")

def createConfigDefault(path):
    config.add_section("Files")
    config.set("Files", "file1.txt")
    config.set("Files", "file8.tar")
    with open(path, "w") as config_file:
        config.write(config_file) 

#createConfigDefault(val2 + "default.cfg")

Files = (os.listdir(val1)) #список файлов из папки val1

# создаём словарь: конфиг:файл из папки val1, который в нем описан, чтобы легче было искать
Dict={}
for file in os.listdir(val2):
    if file != 'default.cfg':
        f = open('C:\\Users\Agapova.E\\source\\repos\\PythonApplication3\\val2\\'+file, mode='r')
        a=f.readline().replace("name:","")
        a=a.replace("\n","")
        Dict[a] = file
        f.close()

print(Dict) #смотрим словарь

# проверяем файлы из папки val1 по условиям из задания
for file in Files:
    with open('C:\\Users\Agapova.E\\source\\repos\\PythonApplication3\\val2\\default.cfg', mode='r') as default:
        flag = False
        for line in default:
            if flag:  #если файл есть в конфиге default
                #проверка, что файл был обновлён в val1 за 15 минут
                lastchange = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(val1 + file))) #время последнего изменения
                print(lastchange)
                print('Файл %s был/не был обновлён за последние 15 минут' % file)
                break
            if file in line:
                flag = True
    if not flag:
        try:
            path = val2+Dict[file] #нашли конфиг файл с именем файла
            print(' Проверка сигнатур для файла %s, содержащихся в конфиге %s:' % (file,Dict[file]))
            f=open(path)
            #проверить, что каждая из указанных в файле сигнатур встречалась в логе за указанное в минутах время
            for line in f:
                if 'сигнатура1' in line:
                   stime=int(a)
                   if stime == 0:
                       stime=timeout
                   #проверяем.что line появлялась в логе за stime
                   print('%s (не) встречалась в логах за %d минут' % (line.replace("\n",""), stime))
                a=line.replace("\n","")
            f.close()
        except KeyError:
            print('Информация о конфигурации файла %s отсутствует' % file)


#- время последнего изменения файла%Y-%m-%d
#lastchange = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(val1 + "\\conf2.cfg")))
#now1 = datetime.datetime.now()
#now2 = time.strftime('%Y-%m-%d %H:%M:%S', datetime.datetime.now())
#delta = now2 - lastchange




# чтение
#config.read(path)
#print (config.get("Sign","Сигнатура1"))
#print (config.get("Sign","Сигнатура2"))
# изменяем/добавляем
#config.set("Sign","Сигнатура2", "signature_five")
#print (config.get("Sign","Сигнатура2"))
# и обязательно сохр изменения
#config.write(open(path, "w"))


