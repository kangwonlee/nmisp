echo "============================================"
echo "Setting environment variables"
echo "============================================"
if [ $RUNNER_WORKSPACE ]; then
    export MINICONDA_PATH=$RUNNER_WORKSPACE/miniconda
else
    export MINICONDA_PATH=../miniconda
fi

echo "MINICONDA_PATH = $MINICONDA_PATH"
export MINICONDA_SUB_PATH=$MINICONDA_PATH/bin
echo "MINICONDA_SUB_PATH = $MINICONDA_SUB_PATH"

export MINICONDA_PATH_WIN=`cygpath --windows $MINICONDA_PATH`;
echo "MINICONDA_PATH_WIN = $MINICONDA_PATH_WIN"

export MINICONDA_LIB_BIN_PATH=$MINICONDA_PATH/Library/bin
echo "MINICONDA_LIB_BIN_PATH = $MINICONDA_LIB_BIN_PATH"

export MINICONDA_DOWNLOAD=$MINICONDA_PATH/download
echo "MINICONDA_DOWNLOAD = $MINICONDA_DOWNLOAD"

echo "============================================"
echo "Install openssl for Windows"
echo "============================================"
choco install openssl.light;

echo "============================================"
echo "Downloading and Installing Miniconda"
echo "============================================"

choco install miniconda3 --params="'/JustMe /AddToPath:1 /D:$MINICONDA_PATH_WIN'";

echo "============================================"
echo "Finished Installing Miniconda"
echo "============================================"

echo "exporting a new path ======================="
export PATH="$MINICONDA_PATH:$MINICONDA_SUB_PATH:$MINICONDA_LIB_BIN_PATH:$PATH"
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
