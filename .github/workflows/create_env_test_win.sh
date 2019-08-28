exists() {
    folder=$1
    if [ -d $folder ]; then
        echo "folder $folder exists"
    fi
}

echo "============================================"
echo "Setting environment variables"
echo "============================================"
if [ $CONDA ]; then
    export MINICONDA_PATH=`cygpath --unix $CONDA`
else
    export MINICONDA_PATH=../miniconda
fi
echo "MINICONDA_PATH = $MINICONDA_PATH"
exists $MINICONDA_PATH

if [ -d $MINICONDA_PATH/Script ]; then
    export MINICONDA_SUB_PATH=$MINICONDA_PATH/Scripts
elif [ -d $MINICONDA_PATH/bin ]; then
    export MINICONDA_SUB_PATH=$MINICONDA_PATH/bin
else
    echo "ls $MINICONDA_PATH ========================="
    ls $MINICONDA_PATH
fi
echo "MINICONDA_SUB_PATH = $MINICONDA_SUB_PATH"
exists $MINICONDA_SUB_PATH

export MINICONDA_PATH_WIN=`cygpath --windows $MINICONDA_PATH`;
echo "MINICONDA_PATH_WIN = $MINICONDA_PATH_WIN"
exists $MINICONDA_PATH_WIN

export MINICONDA_LIB_BIN_PATH=$MINICONDA_PATH/Library/bin
echo "MINICONDA_LIB_BIN_PATH = $MINICONDA_LIB_BIN_PATH"
exists $MINICONDA_LIB_BIN_PATH

export MINICONDA_DOWNLOAD=$MINICONDA_PATH/download
echo "MINICONDA_DOWNLOAD = $MINICONDA_DOWNLOAD"

echo "============================================"
echo "PATH = $PATH"
echo "============================================"
echo "init conda ================================="
conda init $SHELL
echo "pwd ========================================"
pwd
echo "~/$BASHRC =================================="
. ~/$BASHRC
echo "hash -r ===================================="
hash -r
echo "============================================"
echo "CONDA_PYTHON = $CONDA_PYTHON ==============="
echo "============================================"
echo "checking python version ===================="
python --version
echo "updating conda ============================="
conda config --set always_yes yes --set changeps1 no;
conda update -q conda;
echo "conda info -a =============================="
conda info -a
echo "create test-environment ===================="
conda env create -n test-environment -f ./tests/environment.${CONDA_PYTHON}.yml
echo "activate test-environment =================="
conda activate test-environment
conda list
py.test --numprocesses=auto tests/
