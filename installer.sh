#!/bin/bash

VIRTUALENV_SCRIPT=virtualenv.py
VIRTUALENV_DOWNLOAD_URL=https://raw.github.com/pypa/virtualenv/master/virtualenv.py
VIRTUALENV_PATH=cyclope_workenv
DEBIAN_OS_DEPENDENCIES="mercurial git-core python-imaging"
PYTHON=
CYCLOPE_PACKAGE=http://forja.codigosur.org/hg/cyclope/archive/tip.tar.bz2

get_python_version() {
    if python2 --version >/dev/null 2>&1; then
      PYTHON=python2;
    else PYTHON=python;
    fi
    echo "using python binary:"; 
    which $PYTHON;
}

install_dependencies() {
    if apt-get >/dev/null 2>&1; then 
        sudo apt-get install -y $DEBIAN_OS_DEPENDENCIES || { echo -e >&2 "\n\nplease install $DEBIAN_OS_DEPENDENCIES and. Aborting."; exit 1; }
    else
        git --version >/dev/null 2>&1 || { echo -e >&2 "\n\ngit not found. Please install git package and retry.  Aborting."; exit 1; }
        hg --version >/dev/null 2>&1 || { echo -e >&2 "\n\nmercurial not found. Please install mercurial package and retry.  Aborting."; exit 1; }
        $PYTHON -c "import PIL" 2>&1 || { echo -e >&2 "\n\nPIL not found. Please install python-imaging or PIL package and retry.  Aborting."; exit 1; }
    fi
}

bootstrap_virtualenv() {
    echo "Downloading virtualenv";
    
    #try to download with curl and wget
    curl -o $VIRTUALENV_SCRIPT -O $VIRTUALENV_DOWNLOAD_URL || wget -O $VIRTUALENV_SCRIPT $VIRTUALENV_DOWNLOAD_URL || { echo -e >&2 "\n\nPlease install curl or wget and retry.  Aborting."; exit 1; }
    
    $PYTHON $VIRTUALENV_SCRIPT --system-site-packages $VIRTUALENV_PATH;
}

activate_virtualenv() {
    . $1/bin/activate;
}

install_cyclope() {
    pip install --use-mirrors --timeout=50 $CYCLOPE_PACKAGE;
}

post_install_message() {
    echo -e "\n\nCyclope3 installed."
    echo "run 'source cyclope_workenv/bin/activate' to activate virtualenv and then"
    echo "run 'cyclopeproject project_name' to create an empty project OR"
    echo "run 'cyclopedemo demo' to create a demo project with some content"
    
}

# deactivate if inside virtualenv
deactivate >/dev/null 2>&1;

get_python_version;
install_dependencies;
bootstrap_virtualenv;
activate_virtualenv $VIRTUALENV_PATH;
install_cyclope;
post_install_message;
