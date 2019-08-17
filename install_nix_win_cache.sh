  # Install miniconda
if [[ "$TRAVIS_OS_NAME" != "windows" ]]; then
    if [[ -d $MINICONDA_SUB_PATH ]]; then
        echo "miniconda for posix already available";
    else
        echo "installing miniconda for posix";
        bash $HOME/download/miniconda.sh -b -u -p $MINICONDA_PATH;
    fi;
elif  [[ "$TRAVIS_OS_NAME" == "windows" ]]; then
    echo "checking if folder $MINICONDA_SUB_PATH exists"
    if [[ -d $MINICONDA_SUB_PATH ]]; then
        echo "folder $MINICONDA_SUB_PATH exists"
        echo "miniconda for Windows already installed";
    else
        echo "folder $MINICONDA_SUB_PATH does not exist"
        echo "installing miniconda for windows";
        choco install miniconda3 --params="'/JustMe /AddToPath:1 /D:$MINICONDA_PATH_WIN'";
    fi;
fi;
export PATH="$MINICONDA_PATH:$MINICONDA_SUB_PATH:$MINICONDA_LIB_BIN_PATH:$PATH";
# begin checking miniconda existance
echo "checking if folder $MINICONDA_SUB_PATH exists"
if [[ -d $MINICONDA_SUB_PATH ]]; then
    echo "folder $MINICONDA_SUB_PATH exists"
else
    echo "folder $MINICONDA_SUB_PATH does not exist"
fi;
# end checking miniconda existance
source $MINICONDA_PATH/etc/profile.d/conda.sh;
hash -r;
echo $TRAVIS_OS_NAME
echo $CONDA_PYTHON
python --version
conda config --set always_yes yes --set changeps1 no;
conda update -q conda;
# Useful for debugging any issues with conda
conda info -a
# See if test-environment already available
# As necessary, apply python module recipies
if [[ ! -d $MINICONDA_PATH/envs/test-environment ]]; then
    echo "create test-environment";
    conda env create -n test-environment -f ./tests/environment.${CONDA_PYTHON}.yml;
else
    echo "update test-environment";
    conda env update -n test-environment -f ./tests/environment.${CONDA_PYTHON}.yml;
fi;
conda activate test-environment
conda list

# python 3.7.4 linux h265db76_0 might have cython filename issue

if [[ $(conda list | grep ^python.*3.7.4.*h265db76_0) ]]; then
    conda install python=3.7.4;
fi;
