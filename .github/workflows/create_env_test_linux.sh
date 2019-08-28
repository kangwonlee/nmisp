echo "============================================"
echo "Setting environment variables"
echo "============================================"
export MINICONDA_PATH=$CONDA
echo "MINICONDA_PATH = $MINICONDA_PATH"
export MINICONDA_SUB_PATH=$MINICONDA_PATH/bin
echo "MINICONDA_SUB_PATH = $MINICONDA_SUB_PATH"

. ./.github/workflows/build_env.sh

. ./.github/workflows/run_test.sh
