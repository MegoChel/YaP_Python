# YaP_Python
Лабораторная работа написана с помощью фреймворка Flask.
Скрипт имеет доступ только к папкам и файлам, лежащим в папке с ним.
Для получения доступа к корневой папке достаточно перейти на http://127.0.0.1:5000/ .
Все запросы, за исключением создания папки, пожно выполнить с помощью url ссылок (например, для скачивания файла нажать на [dwnld], для удаления - [del]).
Чтобы создать папку, нужно послать запрос вида http://127.0.0.1:5000/createDir/"путь_до_новой_папки"
