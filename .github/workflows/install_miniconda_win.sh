echo "============================================"
echo "Setting environment variables"
echo "============================================"
if [ $CONDA ]; then
    export MINICONDA_PATH=`cygpath --unix $CONDA`
else
    export MINICONDA_PATH=../miniconda
fi

echo "MINICONDA_PATH = $MINICONDA_PATH"
export MINICONDA_SUB_PATH=$MINICONDA_PATH/Script
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
