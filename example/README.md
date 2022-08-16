## Python 和python -m

### 1、对于普通模块

以“.py”为后缀的文件就是一个模块，在“-m”之后使用时，只需要使用模块名，不需要写出后缀，但前提是该模块名是有效的，且不能是用 C 语言写成的模块。

下面有两个例子，通过不同方式启动同一文件，sys.path属性的值有何不同。

```python
# run.py 内容如下
import sys
print(sys.path)

# 直接启动：python run.py
test_import_project git:(master) ✗ python run.py
['/Users/sx/Documents/note/test_py/test_import_project',  
'/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python27.zip',  
  ...]
# 以模块方式启动：python -m run.py
test_import_project git:(master) ✗ python -m run.py
['',  
'/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python27.zip',
```

#### 在工作场景中有什么用呢？

```markdown
# 目录结构如下
test_import_project/
    /package
        __init__.py
        mod1.py
    /package2
        __init__.py
        run.py  
# run.py 内容如下
import sys
from package import mod1
print(sys.path)
```

#### 如何才能启动run.py文件？

```bash
# 直接启动（失败）
➜  test_import_project git:(master) ✗ python package2/run.py
Traceback (most recent call last):
  File "package2/run.py", line 2, in <module>
    from package import mod1
ImportError: No module named package

# 以模块方式启动（成功）
➜  test_import_project git:(master) ✗ python -m package2.run
['',
'/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python27.zip',
...]
```

当需要启动的py文件引用了一个模块。你需要注意：在启动的时候需要考虑sys.path中有没有你import的模块的路径！
这个时候，到底是使用直接启动，还是以模块的启动？目的就是把import的那个模块的路径放到sys.path中。你是不是明白了呢？

> 官方文档参考： http://www.pythondoc.com/pythontutorial3/modules.html

导入一个叫 mod1 的模块时，解释器先在当前目录中搜索名为 mod1.py 的文件。如果没有找到的话，接着会到 sys.path 变量中给出的目录列表中查找。 sys.path 变量的初始值来自如下：

1. 输入脚本的目录（当前目录）。
2. 环境变量 PYTHONPATH 表示的目录列表中搜索(这和 shell 变量 PATH 具有一样的语法，即一系列目录名的列表)。
3. Python 默认安装路径中搜索。
   实际上，解释器由 sys.path 变量指定的路径目录搜索模块，该变量初始化时默认包含了输入脚本（或者当前目录）， PYTHONPATH 和安装目录。这样就允许 Python程序了解如何修改或替换模块搜索目录。

### 2、对于包内模块

如果“-m”之后要执行的是一个包，那么解释器经过前面提到的查找过程，先定位到该包，然后会去执行它的“__main__”子模块，也就是说，在包目录下需要实现一个“__main__.py”文件。

换句话说，假设有个包的名称是“pname”，那么，**“python -m pname”，其实就等效于“python -m pname.__main__”**
