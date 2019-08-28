echo "miniconda paths ============================"
export MINICONDA_PATH=$CONDA
export MINICONDA_SUB_PATH=$MINICONDA_PATH/bin
echo "miniconda lib paths ========================"
export MINICONDA_LIB_BIN_PATH=$MINICONDA_PATH/Library/bin

. ./.github/workflows/build_env.sh

. ./.github/workflows/run_test.sh
