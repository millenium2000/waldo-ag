# waldo-ag
Solution to "Waldo Photos Engineering Project" <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (https://gist.github.com/pkoz/0b5f8b75a07785430a2e9d2698316b13)

It is implemented in Python3 and the assumption is that you have all the necessary dependancies installed.

Please also look at [results/summary.pdf](subimage/results/summary.pdf) document.


# project sturcture
The `subimage` is the main folder.

Inside there are:
 - `img` - folder which contains some images
 - `src` - obviously, contains the source code
 - `results` - contains some test results as well as a summary document
 - `target` - output folder (everything inside is ignored by git)


# examples
The execution is easy to start, but there may be a slight difference in running on Windows vs. Linux.
On Linux having a `#!/bin/env python` in the beginning of a script file is enough to execute the file as a script, but on Windows it wouldn't work. To overcome this issue I did not use the sha-bang approach and rather execute a script as : `python script.py args`.

Since the main code is in *subimage/src/main/*, you can either give a path to the script from here as: <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`python subimage/src/main/subimage.py` <br/>
or you can <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cd subimage/src/main` <br/>
first and then use <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`python subimage.py`


To get help you run with `-h` flag:
```
D:\Files\waldo-ag\subimage>python src/main/subimage.py -h
usage: subimage.py [-h] [-s FROM_0.0_TO_1.0] [-o FILE_NAME] file1 file2

Tries to find a location of one JPEG image inside another

positional arguments:
  file1                 first input jpeg image file name
  file2                 second input jpeg image file name

optional arguments:
  -h, --help            show this help message and exit
  -s FROM_0.0_TO_1.0, --similarity FROM_0.0_TO_1.0
                        minimum similarity threshold
  -o FILE_NAME, --out FILE_NAME
                        filename of the image to save (with bounding rectangle
                        around found sub-image location)

D:\Files\waldo-ag\subimage>
```

Example of execution
```
D:\Files\waldo-ag\subimage>python src/main/subimage.py img/img-01/img-01-smpl-02-080.jpg img/img-01/img-01-080.jpg
not found

D:\Files\waldo-ag\subimage>python src/main/subimage.py img/img-01/img-01-smpl-02-080.jpg img/img-01/img-01-080.jpg  --similarity 0.9
found 0.9225 similarity at (x,y) = (335,380)

D:\Files\waldo-ag\subimage>python src/main/subimage.py img/img-01/img-01-smpl-02-080.jpg img/img-01/img-01-080.jpg  --similarity 0.9 --out target/location.jpg
found 0.9225 similarity at (x,y) = (335,380)

D:\Files\waldo-ag\subimage>
```

