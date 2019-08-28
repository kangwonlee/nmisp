echo "miniconda paths ============================"
export MINICONDA_PATH=$CONDA
export MINICONDA_SUB_PATH=$MINICONDA_PATH/bin
echo "miniconda lib paths ========================"
export MINICONDA_LIB_BIN_PATH=$MINICONDA_PATH/Library/bin
echo "exporting a new path ======================="
export PATH="$MINICONDA_PATH:$MINICONDA_SUB_PATH:$MINICONDA_LIB_BIN_PATH:$PATH"
echo "init conda ================================="
conda init bash
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

. run_test.sh
