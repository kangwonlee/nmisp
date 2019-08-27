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
