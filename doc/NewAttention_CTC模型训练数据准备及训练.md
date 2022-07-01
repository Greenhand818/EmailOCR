# NewAttention_CTC模型训练数据准备及训练

## 功能

- 使用不同字体生成一行email图片
- 保存标签数据到mysql
- 转换标签数据成PaddlePaddle提供的NewAttention_CTC模型所需要的数据格式

## 运行

- 生成email图片、划分数据集、按要求的数据格式获得标签文档：

~~~shell
python3 Generate_Data.py
~~~

- 将模型标签文档退回成email：

~~~shell
python3 data_reader.py
~~~

- 将图片按要求的文件路径格式传输到模型训练项目文件夹中：

~~~ shell
python3 pic.py
~~~

需要用到的字典文档chinese_ch_dict.txt来自于PaddleOCR自带的字典集，具体路径为PaddleOCR/ppocr/utils/dict/chinese_ch_dict.txt

## 参考资料及注意事项：

__NewAttention_CTC模型训练的整个过程和训练数据标签格式请参见：https://github.com/PaddlePaddle/models/tree/develop/PaddleCV/ocr_recognition__

需要注意的是，该项目使用的paddlepaddle版本较老，运行出错时需考虑版本是否匹配。