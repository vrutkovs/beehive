#!/bin/sh

# Usage:
# *in* the "beehive" working directory, run "tools/runtests.sh"

# NOTE!!
# This script will do some setup work for you but you will NEED to:
# 1. set up a tools/virtualenvs directory.
# 2. ensure that each of your Python versions has pip, distribute and
#    virtualenv installed.
# That last step can be tricky! Make sure, for example, that jython
# *actually has pip etc. installed* and it's not just trying to use
# whatever's in /usr/local/bin
# I needed to run "/usr/local/jython2.5.2/bin/pip install virtualenv"
# manually to get virtualenv installed properly.

# Even then jython can be a little tricky and you may need to help it along
# with some manual installation...


if [ x"$BEEHIVE_DIR" != x"" ]; then
    beehive_dir=$BEEHIVE_DIR
	venv_dir=$beehive_dir/tools/virtualenvs
else
    case "`dirname $0`" in
    tools)
        beehive_dir="."
        venv_dir="tools/virtualenvs"
        ;;
    .)
        beehive_dir=".."
        venv_dir="virtualenvs"
        ;;
    "")
        beehive_dir=".."
        venv_dir="virtualenvs"
        ;;
    *)
        echo "Must be run from beehive directory or provide BEEHIVE_DIR env var"
        exit 1
        ;;
    esac
fi

beehive_dir=`cd $beehive_dir; pwd`
venv_dir=`cd $venv_dir; pwd`

function check_venv {
    if [ ! -d $venv_dir ]; then
        mkdir -p $venv_dir
        mkdir -p $venv_dir/cache
    fi

    case $1 in
    pypy*)
        python=`which pypy`
        ;;
    py*)
        python=`echo $1 | sed -e s/py/python/`
        python=`which $python`
        ;;
    jy2.5)
        python=`which jython`
        ;;
    esac

    if [ ! -d $venv_dir/beehive$1 ]; then
        echo "===================== $1 CREATING VIRTUALENV ====================="
        $python `which virtualenv` --no-site-packages --python=$python $venv_dir/beehive$1
    fi

    echo "===================== $1 CHECKING PACKAGES ====================="

    $venv_dir/beehive$1/bin/pip -q install --download-cache=$venv_dir/cache nose mock parse

    case $1 in
    py2.5)
        $venv_dir/beehive$1/bin/pip -q install --download-cache=$venv_dir/cache argparse simplejson
        ;;
    py2.6)
        $venv_dir/beehive$1/bin/pip -q install --download-cache=$venv_dir/cache argparse
        ;;
    jy2.5)
        $venv_dir/beehive$1/bin/pip -q install --download-cache=$venv_dir/cache argparse simplejson
        ;;
    esac
}

failed=""

function test_version {
    case $1 in
    pypy)
        python=pypy
        ;;
    py*)
        python=python
        ;;
    jy*)
        python=jython
        ;;
    esac

    echo
    echo "===================== $1 ====================="
    source $venv_dir/beehive$1/bin/activate
    cd $beehive_dir
    rm -rf build
    #echo "Running: $python setup.py build 2>&1 > build.log"
    #$python setup.py build 2>&1 > build.log
    $python setup.py build
    cp -r tools/test-features build/lib/
    cd build/lib/
    echo "--------------------- $1 UNIT TESTS --------------------------"
    $venv_dir/beehive$1/bin/nosetests || failed="$failed $1"
    echo "--------------------- $1 TEST FEATURES --------------------------"
    $python -m beehive.__main__ -v test-features
    cd ../../
    echo "--------------------- $1 DONE --------------------------"
    echo
}

if [ x"$*" != x"" ]; then
    versions="$*"
else
    versions="py2.5 py2.6 py2.7 py3.2 pypy1.7 jy2.5"
fi

for version in $versions; do
    check_venv $version
    test_version $version
done

if [ x"$failed" != x"" ]; then
    echo "Versions failed:$failed"
fi
