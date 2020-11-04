# Детектирование автомобильных номеров на видео

1. [Введение](#1) 
2. [Установка](#2)
3. [Иерархия файлов и папок](#3)
4. [Аргументы командной строки](#4)
5. [Примеры запуска системы распознавания через командную строку](#5)
	1. [Запуск видео на CPU](#5.1)
	2. [Запуск видео на GPU](#5.2)
	3. [Пример работы с онлайн камерой](#5.3)
6. [Описание выходных данных](#6)
	1. [Обработанное видео](#6.1)
	2. [Файл txt со списком номеров](#6.2)
	3. [Кадры с номером](#6.3)
7. [Тестирование](#7)
8. [Определение точности системы](#8)
	1. [AccurancyAsk.py](#8.1)
	2. [AccurancyChecking.py](#8.1)
	3. [AccurancyConclusion.py](#8.1)
9. [Схема работы системы (для понимания логики программы)](#9)
10. [Создание частотной heatmap (тепловой карты) нахождения автомобильных номеров](#10)
11. [Ссылки](#11)
--------------------------------------

###  Введение <a name='1'></a>
Сервис распознает автомобильные номера на видео или с онлайн камер. Достаточно указать это в аргументах при запуске сервиса. Чтобы запускать сервис с использованием видеокарты (GPU) необходимо указать это в аргументах при запуске системы.

Сервис основан на базе [NomeroffNet](https://github.com/ria-com/nomeroff-net "NomeroffNet").

### Установка <a name='2'></a>
Проект [NomeroffNet](https://github.com/ria-com/nomeroff-net "NomeroffNet") находится в постоянной разработке, поэтому советуем уточнять требования для его установки на их [Github](https://github.com/ria-com/nomeroff-net "Github"). Ниже приведены их требования на момент написания этой инструкции.

python >=3.6

[opencv](https://opencv.org/ "opencv") >=3.4

	git clone https://github.com/ria-com/nomeroff-net.git
	cd nomeroff-net
	git clone https://github.com/youngwanLEE/centermask2.git
	pip3 install 'git+https://github.com/facebookresearch/detectron2.git'
	pip3 install -r requirements.txt

Далее необходимо выйти из директории nomeroff-net и произвести установку данной системы:

	cd ..
	git clone https://github.com/AnnaVeller/detect-license-plates-python.git


Обратите внимание, если [текущий проект](https://github.com/AnnaVeller/detect-license-plates-python "текущий проект") будет установлен не в ту же директорию, что и [nomeroff-net](https://github.com/ria-com/nomeroff-net "NomeroffNet"), то необходимо в файле ModelDetect.py указать верный путь к nomeroff-net.

### Иерархия файлов и папок <a name='3'></a>
Все файлы с кодом располагаются в корневом каталоге.

В папке [video](https://github.com/AnnaVeller/detect-license-plates-python/tree/master/video) находятся видео, которые могут быть обработаны. Чтобы их использовать - необходимо указать одно из них в командной строке при запуске скрипта [Runprocess.Py](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/RunProcess.py "Runprocess.Py") *(см. раздел аргументы командной строки)*.

В папку [car_numbers](https://github.com/AnnaVeller/detect-license-plates-python/tree/master/car_numbers) попадают обработанные видео. Там же создается новая папка одноименная с видео, которое было обработано. В неё помещаются*txt*-файлы со списком распознанных номеров на видео, три картинки кадров для каждой машины и с этих же кадров вырезка таблички номера.
```
car_numbers/:
[название видео]_detect.mp4 - обработанное видео

car_numbers/[название_видео]/:
[название видео].txt - список номеров, найденных на видео
[название видео]_[номер в файле txt]_1.jpg - один из первых кадров, где найден номер 
[название видео]_[номер в файле txt]_1_zone.jpg - табличка с номером с кадра выше
[название видео]_[номер в файле txt]_2.jpg - кадр с середины 
[название видео]_[номер в файле txt]_2_zone.jpg
[название видео]_[номер в файле txt]_3.jpg
[название видео]_[номер в файле txt]_3_zone.jpg
```

###### Схематично расположение файлов представлено ниже:
*Структура каталога nomeroff-net представлена кратко. Чтобы показать, какие дополнительные директории необходимо скачать с GitHub (Если вы шли по установке выше - они уже скачаны)*
[![Структура каталогов проекта](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/folder_structure.jpg?raw=true "Структура каталогов проекта")](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/folder_structure.jpg?raw=true "Структура каталогов проекта")

### Аргументы командной строки <a name='4'></a>
###### При запуске [Runprocess.Py](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/RunProcess.py "Runprocess.Py") необходимо указать аргументы:

`--video=test.mp4` *Название файла видео из папки video или ссылка на онлайн камеру. По умолчанию test.mp4*

`--file=test.txt` *Название файла, куда будет записаны координаты номеров (файлы сохраняются в папку car_numbers). По умолчанию [название видео].txt*

`--type=v или --type=s`  *Тип того, что было передано в --video. v-видео, s-стрим. По умолчанию видео*

`--sec=0.5` *Количество секунд между захватом кадров для обработки. По умолчанию 0.5 секунд*

`--gpu=False или --gpu=True` *Используется ли GPU. По умолчанию не используется*


### Пример запуска системы распознавания через командную строку <a name='5'></a>

Основной файл, через который запускается вся система распознавания - это [RunProcess.py](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/RunProcess.py "RunProcess.py").
#### 1. Запуск на CPU: <a name='5.1'></a>

`python3 RunProcess.py --video=multy_mini.MOV --file=multy_mini.txt --type=v --gpu=no`

Это будет аналогично из-за дефолтных настроек этому:

`python3 RunProcess.py --video=multy_mini.MOV`

#### 2. Запуск на GPU <a name='5.2'></a>

`python3 RunProcess.py --video=multy_mini.MOV --sec=0.5 --gpu=True`

#### 3. Использование онлайн камеры в качестве видео <a name='5.3'></a>

`python3 RunProcess.py --video=[URL на камеру] --file=camera_online.txt --type=s --gpu=no`

Чтобы остановить работу скрипта необходимо нажать Ctrl+c



### Описание выходных данных <a name='6'></a>
##### 1. Обработанное видео<a name='6.1'></a>

Это видео, на котором указан номер, найденный на текущем кадре, итоговый номер, регион автомобиля.

Найденный номер на кадре может быть синего и голубого цвета:
 
![blue](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/blue.png?raw=true "blue") ![l-blue](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/light_blue.png?raw=true "l-blue")

Cиний номер означает, что такая комбинация символов может быть номером. Голубой обозначает обратное. 

Синие номера, при помощи несложного алгоритма соединаются в один номер, который называется итоговым и выделен на каждом кадре красным:

![red](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/red.png?raw=true "red")

Соответсвенно, с каждый кадром, накапливается информация по номерам и красный номер может меняться.

Обработанное видео имеет ту же длину, что и исходное. Однако fps (frames per second) отличается и равно 1/sec. Sec - параметр, переданный в командной строке.

Ниже на изображении ещё раз даны комментарии:

![](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/description_frames_smaller.png?raw=true)

##### 2. Файл txt со списком номеров<a name='6.2'></a>

Файл содержит все номера, встреченные в видео. На первой строчке даны характеристики видео. Далее идет порядковый номер автомобильного номера и распознанный итоговый номер:

[Высота] [Ширина] [Название видео] [fps]

[порядковый номер] [автомобильный номер]

[порядковый номер] [автомобильный номер]

...

![](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/txt.png?raw=true)

##### 3. Кадры с номером<a name='6.3'></a>

Для подсчета точности системы нам нужны скриншоты с номерами. Поэтому с каждого распознанного номера мы сохраняем три скриншота: в начале, середине и конце:
![](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/save3frames.png?raw=true)


### Тестирование <a name='7'></a>

Для тестирования были подготовлены видео с КПП и переданы в данную систему. Ниже сделаны скриншоты с видео:
![test](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/tests.png?raw=true "test")

### Определение точности системы <a name='8'></a>

Для определения точности необходима ручная обработка. То есть разметка, что система определила правильно, что нет. Для этого есть три скрипта.

##### 1. Сначала запускается [AccuracyAsk.py](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/AccuracyAsk.py "AccuracyAsk.py")<a name='8.1'></a>

Аргумент `--name`- это имя папки с видео = название видео без разрешения = файл со списком номеров без разрешения
`python3 AccuracyAsk.py --name=multy_mini`

В этом скрипте необходимо на каждый номер из списка выбрать: true/false/unknown:

- `true` (можно также написать t/1/yes/y  ) - номер на картинке совпадает с номером в названии;

- `false` (0/f/no/n) - не совпадает;

- `unknown` (-1/?/unknown/x) - номер плохо различим

Так будут выглядеть картинки:

![](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/accuracy.png?raw=true)


##### 2. Затем можно быстро проверить свои ответы с [AccuracyChecking.py](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/AccuracyChecking.py "AccuracyChecking.py")<a name='8.2'></a>

`python3 AccuracyChecking.py --name=multy_mini`

![check](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/checking.png?raw=true "check")

Этот скрипт сделан исключительно чтобы ПРОСМОТРЕТЬ быстро ответы. Для исправления необходимо открыть этот файл и вручную исправить.

##### 3. Получить точность можно с помощью [AccuracyConclusion.py](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/AccuracyConclusion.py "AccuracyConclusion.py")<a name='8.3'></a>

`python3 AccuracyChecking.py --name=multy_mini`

В итоге в консоль будет выведено:

![conclusion](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/conclusion.png?raw=true "conclusion")

### Схема работы системы с указанием файлов, к которым принадлежит та или иная функция <a name='9'></a>

Данная UML - диаграмма показывает откуда происходит начало (запуск) системы и какие функции в каких файлах задействует. На диаграмме представлены только *основные* функции и файлы.

![](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/UML_schema.png?raw=true)


### Построение частотной heatmap (тепловой карты) нахождения автомобильных номеров на видео или онлайн камерах <a name='10'></a>

Эта задача нужна, чтобы выделить те регионы, где чаще всего встречаются автомобильные номера.
Задача решена в проекте *[heatmap-location-car-plates](https://github.com/AnnaVeller/heatmap-location-car-plates "heatmap-location-car-plates")*. Он устанавливается и запускается отдельно от текущего проекта.

Вот примеры его работы:

![heatmap](https://github.com/AnnaVeller/detect-license-plates-python/blob/master/project_imgs/heatmap.jpg?raw=true "heatmap")

### Ссылки <a name='11'></a>

- [Инструкция к установке Tensorflow](http://tensorflow.org/install/pip)
- [Распознавание номеров. Практическое пособие. Часть 1](https://habr.com/ru/post/432444/ "Распознавание номеров. Практическое пособие. Часть 1")
- [Распознавание номеров. Как мы получили 97% точности для Украинских номеров. Часть 2](https://habr.com/ru/post/439330/ "Распознавание номеров. Как мы получили 97% точности для Украинских номеров. Часть 2")[Репозиторий Nomeroff Net](https://github.com/ria-com/nomeroff-net "Репозиторий Nomeroff Net")
