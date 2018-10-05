#!/bin/sh

BASEDIR=`dirname $0`
DB_NAME=wms-demo-pyconfr-2018
if [ "$1" != "" ]; then
    echo "Exécutez sans arguments !"
    echo
    echo "Ceci installe le code du projet de démo sous $(realpath $BASEDIR)"
    echo "et initialise une base de donnée appelée $DB_NAME"
    exit 1
fi

python3 -m venv $BASEDIR/venv
BINDIR=$BASEDIR/venv/bin

$BINDIR/pip install -e git+https://github.com/gracinet/anyblok_wms_base@pyconfr-2018#egg=anyblok_wms_base
$BINDIR/pip install -e wms_demo
$BINDIR/anyblok_createdb -c $BASEDIR/demo.cfg

