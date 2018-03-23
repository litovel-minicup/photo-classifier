# Photo classifier
Toolkit for classification sport photos into classes representing each sport teams.
### Planned classificator schema
```
                                 +-----+
                                 /INPUT|
                                /+---\-+
                               /      -\
   +------------------------+ /         -\
   |                        |/       +--------------------+         +------------------+
   | Object detector (FASA) -        |                    |         |                  |
   |                        |        | Team info provider |         |  Upload, persist |
   +------------|-----------+        |                    |         |                  |
                |                    +----------\---------+         +------------------+
                |                                \                         -/
   +------------|-----------+                     | +------------------+ -/
   |                        |                     \ |                  -/
   | "Average" object color |                      \|  Photo classifier|
   |                        |                       |                  -\
   +------------|-----------+                       +------------------+ --\
                |                                               -/          -\
   +------------|-----------+    +------------------------+   -/          +-------+
   |                        |    |                        | -/            |       |
   |  HSL convert, rescale  -----| Hue bucket selection   -/              |  GUI  |
   |                        |    |                        |               |       |
   +------------------------+    +------------------------+               +-------+
```


### Usage
download testing photos
```
$ make download
```

install and activate env
```
$ make install
$ . .venv/bin/activate
```

and run scripts
```
$ python kit.py data/*
$ python main.py data/*
```
