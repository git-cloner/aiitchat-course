# aiitchat-course程序部署

## 1、创建python虚拟环境

```bash
conda create -n course python=3.10 -y
```

## 2、安装依赖包

```bash
conda activate course
pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn
```

## 3、运行模型服务

```bash
python model_stream.py
```

## 4、运行API服务

```bash
python api_stream.py
```

## 5、运行客户端

```bash
npm start
```

## 6、测试

http://localhost:3000