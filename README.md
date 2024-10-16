# QUESTIONNAIRE

基于kivy+buildozer开发的用于调查焦虑评分APP，数据记录在<external_storage_path>\quest文件夹下，以json格式存储，仅供学习使用。

## 开发环境准备（windows）

1. Clone仓库，建立虚拟环境（过程省略），安装依赖：

    ```
    git clone https://github.com/vzionv/QUESTIONNAIRE.git
    cd QUESTIONNAIRE
    pip install -r requirements.txt
    ```

2. 运行

    ```
    python.exe <Project Path>\main.py 
    ```


------

## 编译环境准备（Linux）

### 自行配置制作编译环境

1. Centos软件升级更新

    ```
    curl -o /etc/yum.repos.d/CentOS-Linux-Base.repo http://mirrors.aliyun.com/repo/Centos-8.repo
    yum -y upgrade
    ```
    
2. 安装依赖

    ```
    # 安装系统工具
    yum -y install vim make wget tar unzip zip bzip2 patch autoconf automake libtool lld
    # 安装基础依赖
    yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc gcc-c++ make libffi-devel
    # java依赖安装
    yum -y install java java-devel git 
    ```

3. Python 安装 （过程省略）

4. 安装第三方Python包

    ```
    pip3 install cython
    pip3 install kivy buildozer
    pip3 install android-toast
    ```

    

### 直接使用配置好的虚拟机

下载链接： [Centos_kivy.ova](https://pan.baidu.com/s/19tqiAGFdEQhc0uyn-74urA)

提取码：kivy
登录账户：root
账户密码：kivy2021

------

## 项目编译

将项目clone到虚拟机，随后在项目目录下运行命令：

```shell
buildozer -v android debug
 # 首次编译时会自动下载 android sdk、apache ant、android ndk等组件
 # 如果延迟过高可以修改buildozer的源代码android.py（/usr/local/python3/lib/python3.8/site-packages/buildozer/targets/android.py ），将代码中用到的https://github全部替换成https://gitee即可
```

编译成功后，会在当前目录下创建一个新的**bin**目录，并在该目录下生成一个apk文件

------

## Acknowledgement

[Kivy](https://github.com/kivy/kivy)

[KivyMD](https://github.com/kivymd/KivyMD)

[kivy-toaster](https://github.com/knappador/kivy-toaster)

https://blog.csdn.net/qq_38872258/article/details/117458881



