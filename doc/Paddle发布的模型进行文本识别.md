# Paddle发布的模型进行文本识别

## 功能

- 可以使用paddleocr中PaddleOCR类创建模型，并使用该模型进行文本识别。
- 使用paddlehub中Module类选择创建模型，并使用该模型进行文本识别。



## 运行

​	由于编写时，本人Python编写能力较弱，如果需要修改图片路径，请在相应脚本文件中的最后修改函数的参数；如果需要修改mysql的登录连接信息，请在相应脚本文件中修改pymysql.connect中的参数。

- 使用PaddleOCR类创建模型：

~~~shell
python3 Paddle_rec.py
~~~

- 使用PaddleHub中Module类选择创建模型(目前使用的是PaddleHub中的multi_languages_ocr_db_crnn模型)：

~~~shell
python3 OCR_raw.py
~~~

- 计算文本识别的准确率：

~~~shell
python3 accuracy.py
~~~

- 图片预处理(对文字左右两侧进行padding使其宽高保持一致，效果见两个图片文件夹)：

~~~shell
python3 image.py
~~~

## 其它文件说明

- ocr验证集：有真实数据标签，有小概率标签有错
- result.xlsx：使用PaddleOCR类进行了检测和识别的模型预测结果
- paddle_rec_result.xlsx：使用PaddleOCR类对预处理后的图片进行了检测和识别的模型预测结果
- img：原数据集
- image：预处理后的数据集
