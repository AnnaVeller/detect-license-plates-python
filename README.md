# detect-license-plates-python
1. [Установка под GPU](#1)
2. [Установка под CPU](#2)
3. [Расположение файлов](#3)
4. [Аргументы командной строки](#4)
5. [Примеры работы](#5)
	1. [Запуск на CPU](#5.1)
	2. [Запуск на GPU](#5.2)
	3. [Пример работы с онлайн камерой](#5.3) 

--------------------------------------

### Установка под GPU <a name='1'></a>
    pip3 install tensorflow-gpu==1.15.2 
    pip3 install Keras==2.2.*
    pip3 install mrcnn
    pip3 install Nomeroff-net-gpu


### Установка под CPU <a name='2'></a>
    pip3 install tensorflow==1.15.2 
    pip3 install Keras==2.2.*
    pip3 install mrcnn
    pip3 install Nomeroff-net

### Расположение файлов <a name='3'></a>
В папке [video](https://github.com/AnnaVeller/detect-license-plates-python/tree/master/video) находятся видео, которые могут быть обработаны. Чтобы их использовать - необходимо указать одно из них в командной строке при запуске скрипта [Runprocess.Py](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/RunProcess.py "Runprocess.Py") *(см. раздел аргументы командной строки)*.

В папке [car_numbers](https://github.com/AnnaVeller/detect-license-plates-python/tree/master/car_numbers) расположены файлы разрешения *txt*, полученные скриптом Runprocess.Py.

### Аргументы командной строки <a name='4'></a>
###### При запуске [Runprocess.Py](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/RunProcess.py "Runprocess.Py") можно указать аргументы:

`--video=test.mp4` *Название файла видео из папки video или ссылка на  онлайн камеру. По умолчанию test.mp4*

`--file=test.txt` *Название файла, куда будет записаны координаты номеров (файлы сохраняются в папку car_numbers). По умолчанию [название__видео].txt*

`--type=v или --type=s`  *Тип того, что было передано в --video. v-видео, s-стрим. По умолчанию видео*

`--sec=0.5` *Количество секунд между захватом кадров для обработки. По умолчанию 0.5 секунд*

`--gpu=False или --gpu=True` *Используется ли GPU. По умолчанию не используется*




### Пример запуска <a name='5'></a>

#### Запуск на CPU: <a name='5.1'></a>
Запустили [Runprocess.Py](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/RunProcess.py "Runprocess.Py") таким образом:

`python3 RunProcess.py --video=multy_mini.MOV --file=multy_mini.txt --type=v --gpu=no`

что было бы аналогично из-за дефолтных настроек этому:

`python3 RunProcess.py --video=multy_mini.MOV`

#### Запуск программы из консоли c использованием GPU <a name='5.2'></a>

`python3 RunProcess.py --video=multy_mini.MOV --sec=0.5 --gpu=True`

![](https://sun9-51.userapi.com/ekPhrW64rUEO0UwE7DIHFVd0wtnorlGbWzypXQ/FkWH7DKZAXg.jpg)
После предупреждений запускается на CPU.


##### Если учесть новые требования с Github [Nomeroff-net](https://github.com/ria-com/nomeroff-net "Nomeroff-net"):

`tensorflow>=2.3.*` 

Библиотеки с изображения выше будут загружаться, но будут возникать новые проблемы. Даже если взять их example



#### Использование онлайн камеры в качестве видео <a name='5.3'></a>

`python3 RunProcess.py --video=[URL на камеру] --file=camera_online.txt --type=s --gpu=no`

Чтобы остановить работу скрипта необходимо нажать Ctrl+c

### [Инструкция к установке Tensorflow](http://tensorflow.org/install/pip)

### Схема работы системы с указанием файлов, к которым принадлежит та или иная функция
![](https://psv4.userapi.com/c856320/u92558681/docs/d8/ee9d7d85596b/Copy_of_Rabochaya_UML_1.png?extra=bR9qblSJH5TAfs3r83yjrPovW5Ka0TQLh6YhncdejFaNcM08-uN5j3IPfPeecyF5b9e7WhxSkululdiPPYhewoiNZNyCsot1NwCG0bGiKoBffnRsn-S4pVgUbOnHzpD7z_QZ62LocKZv0Ez2ov_UHUQ)


##### Полезные команды  

`conda info --envs` - информация по моим виртуальным средам

`conda create --name detect tensorflow keras cudnn=7.6.5=cuda10.1_0`

`conda activate detect`

`conda install пакет`

`conda search пакет`

`conda remove --name myenv --all`

`watch -n 1 nvidia-smi`- будет каждую секунду показывать актуальную загрузку видюхи

`tiv картинка` - показать картинку в терминале

`gitk` - открывает ветки изменения

`git diff <file>` - показывает изменения

`git config --global user.name "John Doe"`

`git config --global user.email johndoe@example.com`

БЕЗ global можно поменять чисто для ТЕКУЩЕГО проекта

`git config user.name "Anna"`

`git config user.email anna.ovsi@mail.com`

ВСЕ НАСТРОЙКИ

`git config --list --show-origin`

`git add .; git commit -m "update"; git push`

`git checkout <file>` - отменить изменения файла пока они не добавлены в add

`mv test.txt test.old` - переименовать

#### Возможно с этими требованиями сработало, но они не совместимы

`conda create --name detect tensorflow-gpu=1.15.0 opencv keras=2.2.* cudnn=*=cuda10.1_0 numpy`


