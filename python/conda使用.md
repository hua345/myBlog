# conda

Conda 是一个开源的软件包管理系统和环境管理系统，用于安装多个版本的软件包及其依赖关系，并在它们之间轻松切换。

## 安装conda

conda分为anaconda和miniconda。anaconda是包含一些常用包的版本，miniconda则是精简版，需要啥装啥，所以推荐使用miniconda。

- [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- [https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/](https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/)

## 通过菜单打开`Anaconda Prompt`

```bash
(base) PS C:\Users\Administrator> python --version
Python 3.8.3
(base) PS C:\Users\Administrator> conda --version
conda 4.8.3
# 添加镜像
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
# 更新conda
conda upgrade --all
# 查看当前的编译环境
conda info -e
base                  *  D:\Program File\anaconda
# 查看已经安装的packages 和 pip3 list类似
conda list
```

## 创建环境

```bash

# 现在环境是3.8,创建一个3.6的环境
conda create -n python3.6 python=3.6
done
#
# To activate this environment, use
#
#     $ conda activate python3.6
#
# To deactivate an active environment, use
#
#     $ conda deactivate
# 查看环境列表
conda env list
base                  *  D:\Program File\anaconda
python3.6                D:\Program File\anaconda\envs\python3.6
# 切换环境
conda activate python3.6
python --version
Python 3.6.11
# 退出到默认环境
conda deactivate
python --version
Python 3.8.6
```
