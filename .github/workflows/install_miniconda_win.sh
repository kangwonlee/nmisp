exists() {
    folder = $1
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

export MINICONDA_SUB_PATH=$MINICONDA_PATH/Script
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
