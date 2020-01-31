# ClassToBook
Scrapy a class from network and transform them to a book

##requirement
srt

selenium
## How to Use
1. Install requirements in `requirements.txt`

2. Change the variable `name` and `courser_url` in main.py, for example
```python
course_url = 'http://open.163.com/special/sp/philosophy-death.html'
name = 'Philosophy-Death'
```
```python
course_url = 'http://open.163.com/newview/movie/' \
              'courseintro?newurl=%2Fspecial%2Fopencourse%2Fpositivepsychology.html'
name = 'HappyClass'
```

3. 

```bash
python main.py
```