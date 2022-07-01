#  GenerateImage

## 功能

- 随机生成一行Email邮箱地址图片。
- 效果有两种可选择，一种对整张图片进行透视变换，一种对每个字进行了变换做旧处理后拼成邮箱地址图片。样例图片分别在./data_pic和./raw_data中。

## 运行使用

- 生成处理过的单字：

~~~Shell
python3 generate_letter.py
~~~

- 生成邮箱地址及图片(邮箱地址和图片名存在mysql数据库中)：

~~~shell
./data_pic: python3 generate_email_transform.py
./raw_data: python3 generate_email.py
~~~

- 划分训练集及生成PaddleOCR所需的标签文档(从数据库中获取标签信息)：

~~~Shell
python3 data_reader.py
~~~

## 其它文件说明

- data_pic：存储透视变换后的图片
- raw_data：存储单字图像拼接而成的图片
- train_data：用来存储划分好的训练集和标签文档
- ttf：字体ttf文件
- letters：生成的各种处理过的单字
- email_suffix.txt：存储各种邮箱地址后缀
- label_dict.txt：存储邮箱地址所需的字符的字典

