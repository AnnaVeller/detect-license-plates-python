# detect-license-plates-python

### Запуск программы из консоли c использованием GPU

`python3 RunProcess.py --video=multy_mini.MOV --sec=0.5 --gpu=True`

### Требования, nomeroff-net ранее
```
pip3 install tensorflow-gpu==1.15.2
pip3 install Keras==2.2.*
pip3 install mrcnn
pip3 install Nomeroff-net-gpu 
```
```
pip3 install tensorflow==1.15.2
pip3 install Keras==2.2.*
pip3 install mrcnn
pip3 install Nomeroff-net
```

- При запуске c --gpu=True: 
![](https://sun9-51.userapi.com/ekPhrW64rUEO0UwE7DIHFVd0wtnorlGbWzypXQ/FkWH7DKZAXg.jpg)
После предупреждений запускается на CPU.

- Если учесть новые требования с Github [Nomeroff-net](https://github.com/ria-com/nomeroff-net "Nomeroff-net"):

`tensorflow>=2.3.*` 

Библиотеки с изображения выше будут загружаться, но будут возникать новые проблемы.

- Если взять example Nomeroff-net и их текущие требования. То при запуске даже на CPU всё равно появляются проблемы с tensorflow.

### [Инструкция к установке Tensorflow](tensorflow.org/install/pip "Установка Tensorflow")

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


