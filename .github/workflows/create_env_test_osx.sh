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

echo "============================================"
echo "Downloading and Installing Miniconda"
echo "============================================"

export MINICONDA_DOWNLOAD=$MINICONDA_PATH/download
echo "MINICONDA_DOWNLOAD = $MINICONDA_DOWNLOAD"

mkdir -p $MINICONDA_DOWNLOAD;
echo "downloading miniconda.sh for osx ==========="
wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O $MINICONDA_DOWNLOAD/miniconda.sh;

echo "installing miniconda ======================="
bash $MINICONDA_DOWNLOAD/miniconda.sh -b -u -p $MINICONDA_PATH;

echo "============================================"
echo "Finished Installing Miniconda"
echo "============================================"

. ./.github/workflows/build_env.sh

. ./.github/workflows/run_test.sh
