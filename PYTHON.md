## Python
### Content
1. [Hello world](#1-hello-world)
2. [Cú pháp](#2-c%C3%BA-ph%C3%A1p)
<!-- 3. [Phân chia module](#3) -->
3. [Class](#4)

### 1. Hello world
```Python
print 'Hello world'
```
Run
```bash
$ python helloworld.py
```
### 2. Cú pháp

#### 2.1. Biến số
Khai báo giá trị.
```python
a = 1
```
hoặc
```python
a = 1
b = 'hello world'
c = [1, 2, 3]
d = [1.2, 'Hello', 'W', 2]
```

#### 2.2. Toán tử số học
- Cộng `+`
- Trừ `-`
- Nhân `*`
- Chia `/`
- Chia lấy dư `%`

#### 2.3. Toán tử logic
##### Boolean
- Đúng `True`
- Sai `False`
- `not` đảo giá trị `!`
- `and` logic và `&&`
- `or` logic hoặc `||`

##### Toán tử logic
- So sánh các giá trị `>`, `<`, `>=`, `<=`, `!=`/`<>`, `==`
- Trong một tập hơp `in`


##### Ví dụ
```Python
x = 2
x < 1 #False
x >= 2 #True
0 < x < 3 #False
x != 2 #False
```
```python
lst = [1, 2, 3, 4]
print 3 in lst
#True
```
```python
gst = [1.2, 'Hello', 'W', 2]
print 'W' not in gst
#False
```
```python
stri = 'Hi there!'
print 'Hi' in stri
#True
```

#### 2.4. Cấu trúc điều khiển
##### 2.4.1. Cấu trúc `if.. else`
```python
if condition1:
 doSomething_1()
elif condition2:
 doSomething_2()
else:
 doSomething_3()
```
**Ví dụ**
```python
x = 8
m = 3

if x == 10:
 m += 1
else:
 m -= 3
# Kết quả : m = 0
```
*Một cách viết gọn: *
```python
x = 8
m = 3
m += 1 if x == 10 else 3
```
Trong python không có `switch.. case`
##### 2.4.2. Cấu trúc `For.. in`
```python
for iterating_var in sequence:
 statements(s)
```
**Ví dụ**
```python
for letter in 'Python':
 print 'Current Letter : ', letter

# Kết quả
# Current Letter : P
# Current Letter : y
# Current Letter : t
# Current Letter : h
# Current Letter : o
# Current Letter : n
```
```python
fruits = ['banana', 'apple', 'mango']
for fruit in fruits:
 print 'Current fruit :', fruit
print "Good bye!"

# Kết quả
# Current fruit : banana
# Current fruit : apple
# Current fruit : mango
# Good bye!
```
##### 2.4.3. Cấu trúc `while ..`
```python
while expression:
 statement(s)
```
**Ví dụ**
```python
count = 0
while (count < 9):
 print 'The count is: ', count
 count = count + 1
print "Good bye!"

# Kết quả
# The count is: 0
# The count is: 1
# The count is: 2
# The count is: 3
# The count is: 4
# The count is: 5
# The count is: 6
# The count is: 7
# The count is: 8
# Good bye!
```
#### 2.5. Hàm
```python
def functionname(param, param2,..):
 statements(s)
```
**Ví dụ**
```python
# Khai báo
def sum(a, b):
 return a + b

# Sử dụng
s = sum(2, 3)
print s

# Kết quả : 5
```
**Hàm có hỗ trợ giá trị mặc định cho tham số khi không truyền vào.**
```python
def add_ten(a, b=10):
 return a+b
print add_ten(2)

# Kết quả 12
```
#### 2.6. Xử lý chuỗi
```python
str1 = "Hello"
str2 = 'world'

# Nối chuỗi
str = str1 + str2
print str

# Lấy ký tự trong chuỗi
print str[0]
print str[2]

# Trích xuất chuỗi
print str[0:4] # (Hiển thị "Hell")
print str[:4] # (Hiển thị "Hell")
print str[-3:] # (Hiển thị "rld")
print str[6:-3] # (Hiển thị "wo")

# Lấy độ dài
count = len("Hello world") # (count có giá trị 11)
```
**Tìm & thay thế nội dung**
*Biểu thức * `replace(search, replace[, max]) `
```python
str = 'Hello world'
newstr = str.replace('Hello', 'Bye')
print newstr
# (Sẽ hiển thị chuỗi "Bye world" trên màn hình)
```
**Tìm vị trí chuỗi con**
*Biểu thức * `find(str, beg=0, end=len(string))`
```python
str = 'Hello world'
print str.find('world') # (hiển thị 6)
print str.find('Bye') # (hiển thị -1)
```
- `find()` tìm lần lượt từ trái qua phải
- `rfind()` tìm ngược lại

**Tách chuỗi**

*Biểu thức * `split(str="", num=string.count(str))`
```python
str = 'Hello world'
print str.split(' ')
# (Trả về một mảng có 2 phần tử là 2 chuỗi "Hello" và "world")
# ['Hello', 'world']
```
**Trim ký tự khoảng trắng**
- `strip([chars])`: loại bỏ trước và sau chuỗi
- `lstrip([chars])`: loại bỏ phía trước chuỗi
- `rstrip([chars])`: loại bỏ phía sau chuỗi

**Một số hàm xử lý chuỗi**
- `isnumeric()` : Kiểm tra một chuỗi có phải là chuỗi số
- `lower()` : Chuyển chuỗi hết thành chữ thường
- `upper()` : Chuyển chuỗi hết thành chữ HOA

#### 2.7. List
**Khai báo**
```python
numbers = [1, 2, 3, 4, 5]
names = ['Marry', 'Peter']
```
**Truy xuất từng phần tử của mảng**
```python
print numbers[0]
# (Hiển thị 1)

print numbers[-3]
# (Hiển thị 3)

print names[1]
# (Hiển thị 'Peter')```
Lấy độ dài list dùng `len(array)`
```python
print len(names)
# (Hiển thị '2')
```

**Để kiểm tra một giá trị** có `tồn tại` / `không tồn tại` trong mảng hay không thì có thể sử dụng toán tử `in` / `not in`

```python
mylist = ['a', 'b', 'c']

print 'a' in mylist
# (Hiển thị True)

print 'b' not in mylist
# (Hiển thị False)
```

**Trích xuất mảng con**

```python
numbers = ['a', 'b', 'c', 'd']

print numbers[:2]
# (Hiển thị ['a', 'b'])

print numbers[-2:]
# (Hiển thị ['c', 'd'])```

**Xóa phần tử của mảng**

Có thể xóa một phần tử thông qua toán tử `del`
```python
numbers = [1, 2, 3, 4, 5]
del numbers[0]
print numbers
# (Hiển thị [2, 3, 4, 5])
```

Xóa một khoản dựa vào toán tử lấy khoản `[start:end] `
```python
numbers = [1, 2, 3, 4, 5, 6, 7]
del numbers[2:4]
print numbers
# (Hiển thị [1, 2, 5, 6, 7])
```

**Nối 2 mảng**

```python
a = [1, 2]
b = [1, 3]

print a + b
# (Hiển thị [1, 2, 1, 3])
```

**Thêm phần tử vào mảng**

```python
numbers = [1, 2, 3]
numbers.append(4)
print numbers
(Hiển thị [1, 2, 3, 4]```

**Lấy phần tử cuối ra khỏi mảng**
```python
numbers = [1, 2, 3]
mynumber = numbers.pop()
print mynumber
# (Hiển thị 3)

print numbers
# (Hiển thị [1, 2])```

**Tìm vị trí một giá trị trong mảng**

```python
aList = [123, 'xyz', 'zara', 'abc'];
print "Index for xyz : ", aList.index('xyz')
print "Index for zara : ", aList.index('zara')```
Kết quả
```
Index for xyz : 1
Index for zara : 2 ```

**Đảo ngược giá trị của mảng**

```python
numbers = [1, 2, 3, 4]
numbers.reverse()
print numbers
(Hiển thị [4, 3, 2, 1])```

**Sắp xếp giá trị các phần tử**
```python
aList = [123, 'xyz', 'zara', 'abc', 'xyz']
aList.sort()
print "List : ", aList
(Hiển thị List : [123, 'abc', 'xyz', 'xyz', 'zara'])```


#### 2.8. Tuple
- `Tuple` cũng là một cấu trúc mảng, tương tự như cấu trúc `List`.
- Một số điểm khác nhau cơ bản là khai báo `Tuple` sử dụng cặp dấu ngoặc `(...)`
- Một `tuple` đã được khai báo rồi thì không thay đổi được giá trị
- Không hỗ trợ các phương thức như `append()` , ` pop()` , ...

```python
mytuple = ('x', 'y', 'z')
print mytuple
# (Hiển thị ('x', 'y', 'z'))
```

#### 2.9. Dictionary

- `Dictionary` cũng là một cấu trúc mảng, nhưng các phần tử bao gồm `key` và `value`.
- Nếu bạn có biết JSON thì cấu trúc `Dictionary` tương tự như một object json.
- Một `Dictionary` được khai báo bằng cặp dấu ngoặc `{...}` .

```python
point = {'x': 1, 'y': 2}```
hoặc
```python
point = {'x': 3, 'y': 6, 'z' : 9}
print point['x']
# (Hiển thị 3)```

**Thêm một phần tử**

Để thêm một phần tử vào đối tượng đã khai báo, sử dụng cấu trúc `dict[key] = value` .

```python
user = {'name': 'Jone', 'age': 30}
user['country'] = 'Vietnam'
print user
# (Hiển thị {'country': 'Vietnam', 'age': 30, 'name': 'Jone'})```

**Một số hàm, phương thức thông dụng**

- `dict.clear()` : Xóa toàn bộ dữ liệu bên trong đối
tượng
- `dict.copy()` : Trả về một bản copy của đối tượng
- `dict.fromkeys(seq[, value])` : Tạo một đối tượng với danh sách key từ seq và nếu có truyền value thì lấy đó làm giá trị cho các phần tử.
- `dict.has_key(key)` : kiểm tra một key có tồn tại trong đối tượng hay không.
- `dict.keys()` : Trả về một List chứa các key
- `dict.values()` : Trả về một List chứa các value


```python
seq = ('name', 'age', 'sex')
dict = dict.fromkeys(seq)
print "New Dictionary : %s" % str(dict)

dict = dict.fromkeys(seq, 10)
print "New Dictionary : %s" % str(dict)```

Kết quả

```
New Dictionary : {'age': None, 'name': None, 'sex': None}
New Dictionary : {'age': 10, 'name': 10, 'sex': 10}```

Xong 2 chương đầu!

<!-- ### 3. Phân chia module -->



### 3. Class

**Khai báo một Class**

```python
class myclass([parentclass]):
    assignments
    def __init__(self):
        statements
    def method():
        statements
    def method2():
        statements
```

**Ví dụ một class:**
```python
class animal():
    name = ''
    name = ''
    age = 0
    def __init__(self, name = '', age = 0):
        self.name = name
        self.age = age
    def show(self):
        print 'My name is ', self.name
    def run(self):
        print 'Animal is running...'
    def go(self):
        print 'Animal is going...'


class dog(animal):
    def run(self):
        print 'Dog is running...'

myanimal = animal()
myanimal.show()
myanimal.run()
myanimal.go()

mydog = dog('Lucy')
mydog.show()
mydog.run()
mydog.go()
```

Sau khi thực thi sẽ cho ra kết quả:
```
My Name is
Animal is running...
Animal is going...
My Name is Lucy
Dog is running...
Animal is going...
```

Trong ví dụ trên thì:
- `animal`  và  `dog`  là 2 class. Trong đó class  dog  kế thừa
từ class cha là  `animal`  nên sẽ có các phương thức của
class  `animal` .
- `name`  và  `age`  là thuộc tính (Attribute) của class.
- Phương thức ` __init__(self)`  là hàm tạo của class.
- Hàm này sẽ được gọi mỗi khi có một object mới được
tạo (từ một class), gọi là quá trình tạo instance.
`show()` ,  `run()`  và  `go()`  là 2 phương thức của 2 class.
- Khi khai báo phương thức có kèm tham số  `self`  dùng
để truy cập ngược lại object đang gọi. Lúc gọi phương
thức thì không cần truyền tham số này.
- Phương thức  `run()`  của class  `dog`  gọi là  override
của phương thức  `run()`  của class  `animal` .
