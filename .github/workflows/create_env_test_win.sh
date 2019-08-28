echo "============================================"
echo "Setting environment variables"
echo "============================================"
if [ $CONDA ]; then
    export MINICONDA_PATH=`cygpath --unix $CONDA`
else
    export MINICONDA_PATH=../miniconda
fi
echo "MINICONDA_PATH = $MINICONDA_PATH"

export MINICONDA_SUB_PATH=$MINICONDA_PATH/Scripts
echo "MINICONDA_SUB_PATH = $MINICONDA_SUB_PATH"

. ./.github/workflows/build_env.sh

. ./.github/workflows/run_test.sh
