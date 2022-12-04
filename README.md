# 7seasweb-com-crawler

## 部署方式

安装chrome浏览器：https://www.google.cn/intl/zh-CN/chrome/

打开Chrome浏览器，右上角三个点 -> 关于Chrome，查看一下 Chrome的版本
然后拿着版本号去镜像站下载对应的 chromedriver.exe（假设当前版本为106.0.5249.61）

https://npmmirror.com/mirrors/chromedriver/

点进对应版本号的文件夹，然后下载 ***win32.zip版本的（windows系统就选这个）
如果是 linux 的话就不需要了。
下载完成后，把压缩包里的 chromedriver.exe 放置在项目根目录/bin/(没有就创建一个)里

**chromedriver.exe 和 chrome的版本不一致无法使用！**


## 创建虚拟环境
```bash
python -m venv env
```

## 安装依赖：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 安装Microsoft C++ Build Tools (万一用不了再回头来进行这一步)
https://my.visualstudio.com/

首先登录，接下来，在下载页面搜索build tools，找到左侧的Visual Studio 2015 update 3。
点击Visual Studio 2015 update 3后，下载对应的文件即可，约1.1G，这里需要将格式修改为DVD。
下载完成后，我们得到了文件mu_visual_cpp_build_tools_2015_update_3_x64_dvd_dfd9a39c.iso，解压后，双击VisualCppBuildTools_Full.exe即可自动进行安装。
安装后，即可正常使用pip进行对应包的安装。


## 激活虚拟环境

```bash
.\env\Scripts\activate
```

## 运行项目

如果能用 pycharm的运行更好（不会显示chromedriver的日志）

```bash
python main.py
```





