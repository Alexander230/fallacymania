Fallacymania: исходники для игровых материалов
=================================================
Текст и картинки карточек псевдоаргументов (a.k.a. fallacies, софизмов). Сделаны участниками московского сообщества LessWrong, с использованием материалов Дэвида Маккандлесса, Джесси Ридчардсона и Александра Образа.

Установка и запуск
------------------

Пререквизиты

0. bash
1. python v3
2. pip
3. pdfrw python module v0.4

На ubuntu/debian пререквизиты устанавливаются следующими командами:

    $ sudo apt-get install python3 python3-pip
    $ sudo pip3 install pdfrw

Скрипт запускается из директории src:

    $ cd src
    $ ./image-generator.sh

Скрипт создает следующие файлы:

*    fallacies-eng.pdf
*    fallacies-rus.pdf
*    stickers/*.pdf
*    tts/*.png

    
Упоминание предшествующих работ
--------------------------------
Основано на работах Дэвида Маккандлесса (David McCandless) [Rhetological fallacies][1], Джесси Ридчардсона (Jesse Richardson) ["your logical fallacy is"][2], с использованием перевода Александра Образа [Логические ошибки][3].

Огромное спасибо Дэвиду за выбранную либеральную лицензию, а Джесси и Александру за любезное разрешение на некоммерческое использование их работ.

###  В оригинальные материалы внесены следующие изменения:
 * выбраны отдельные фрагменты исходных работ (описания избранных псевдоаргументов)
 * переведены и/или отредактированы русские тексты


Лицензия
--------
![Creative Commons][cc-logo]

 Опубликовано под лицензией [CC BY-NC 4.0][4]. Александр Попов, Юрий Баранов, Дмитрий Яхонтов, Алина Горбатова.

 Краткие условия лицензирования [на русском языке][5]:

### Вы можете свободно:

**Делиться (обмениваться)** — копировать и распространять материал на любом носителе и в любом формате

**Адаптировать (создавать производные материалы)** — делать ремиксы, видоизменять, и создавать новое, опираясь на этот материал

Лицензиар не вправе аннулировать эти свободы пока вы выполняете условия лицензии.

### При обязательном соблюдении следующих условий:

![Attribution][by] **«Attribution» («Атрибуция»)** — Вы должны обеспечить **<u>соответствующее указание авторства</u>**, предоставить ссылку на лицензию, и **<u>обозначить изменения, если таковые были сделаны</u>**. Вы можете это делать любым разумным способом, но не таким, который подразумевал бы, что лицензиар одобряет вас или ваш способ использования произведения.

![Non-Commercial][nc] **«NonCommercial» («Некоммерческое использование»)** — Вы не вправе использовать этот материал в **<u>коммерческих целях</u>**.

**Без дополнительных ограничений** — Вы не вправе применять юридические ограничения или **<u>технологические меры</u>**, создающие другим юридические препятствия в выполнении чего-либо из того, что разрешено лицензией.

### Замечания:

 Вы не обязаны действовать согласно условиям лицензии, если конкретная часть материала находится в общественном достоянии или если такое использование вами материала разрешено согласно применимому **<u>исключению или ограничению авторских прав</u>**.

 Вам не даётся никаких гарантий. Лицензия может не включать все разрешения, необходимые вам для использования произведения (материала) по вашему замыслу. Например, иные права, такие как право на **<u>обнародование, неприкосновенность частной жизни или неимущественные права</u>** могут ограничить вашу возможность использовать данный материал.



[1]:  http://www.informationisbeautiful.net/visualizations/rhetological-fallacies/
[2]:  https://yourlogicalfallacyis.com/
[3]:  http://obraz.io/ru/posters/poster_view/1/?back_link=%2Fru%2F&lang=ru&arrow=right
[4]:  https://creativecommons.org/licenses/by-nc/4.0/legalcode
[5]:  https://creativecommons.org/licenses/by-nc-nd/4.0/deed.ru
[cc-logo]: http://mirrors.creativecommons.org/presskit/logos/cc.logo.png
[by]: http://mirrors.creativecommons.org/presskit/icons/by.png
[nc]: http://mirrors.creativecommons.org/presskit/icons/nc.png