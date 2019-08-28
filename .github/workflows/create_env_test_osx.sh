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

. ./.github/workflows/wget_install_miniconda.sh

. ./.github/workflows/build_env.sh

. ./.github/workflows/run_test.sh
