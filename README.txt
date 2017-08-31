To run the application:
Windows & Ubutu commands provided:
#Provide a blob 
C:\temp\pyexamples>C:\Users\admin\AppData\Local\Programs\Python\Python35\python.exe frontend.py --data "hello|world|123"
vagrant@vagrant:/tmp/pyexample$python3.5 frontend.py --data "hello|world|123"
Top 10 words...
10 - Count: 1 Words: ['world']
9 - Count: 1 Words: ['hello']

C:\temp\pyexamples>C:\Users\admin\AppData\Local\Programs\Python\Python35\python.exe frontend.py --data "hello world's this is life """test""" 'life's are carzy workd! life test life live live live live 93"
vagrant@vagrant:/tmp/pyexample$python3.5 frontend.py --data "hello world's this is life """test""" 'life's are carzy workd! life test life live live live live 93"
Top 10 words...
10 - Count: 4 Words: ['live']
9 - Count: 3 Words: ['life']
8 - Count: 2 Words: ['test']
7 - Count: 1 Words: ["life's"]
6 - Count: 1 Words: ['this']
5 - Count: 1 Words: ['is']
4 - Count: 1 Words: ['are']
3 - Count: 1 Words: ['hello']
2 - Count: 1 Words: ["world's", 'workd']
1 - Count: 1 Words: ['carzy']

#Provide a filename downloaded from http://www.gutenberg.org/
C:\temp\pyexamples>C:\Users\admin\AppData\Local\Programs\Python\Python35\python.exe frontend.py --files "C:\temp\pyexamples\55458-0.txt"
vagrant@vagrant:/tmp/pyexample$ python3.5 frontend.py --files "/tmp/pyexample/55458-0.txt"
Top 10 words...
10 - Count: 3137 Words: ['the']
9 - Count: 1793 Words: ['of']
8 - Count: 1287 Words: ['and']
7 - Count: 877 Words: ['to']
6 - Count: 746 Words: ['in']
5 - Count: 725 Words: ['a']
4 - Count: 495 Words: ['his']
3 - Count: 476 Words: ['The']
2 - Count: 448 Words: ['with']
1 - Count: 406 Words: ['is']


#Provide directory with the files downloaded from http://www.gutenberg.org/
# PLEASE NOTE NOT TRAILING SPACE IN THE DIRECTORY PATH
C:\Users\admin\AppData\Local\Programs\Python\Python35\python.exe frontend.py --dir "C:\\temp\pyexamples\data"
vagrant@vagrant:/tmp/pyexample$ python3.5 frontend.py --dir "/tmp/pyexample/data"
Top 10 words...
10 - Count: 20483 Words: ['the']
9 - Count: 13809 Words: ['of']
8 - Count: 8588 Words: ['and']
7 - Count: 6858 Words: ['in']
6 - Count: 6305 Words: ['to']
5 - Count: 5720 Words: ['is']
4 - Count: 4590 Words: ['a']
3 - Count: 3622 Words: ['that']
2 - Count: 3192 Words: ['as']
1 - Count: 3082 Words: ['which']