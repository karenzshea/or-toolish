#!/usr/bin/env bash

set -eu
set -o pipefail

usage="Pass version version to download: 5.1 or 6"
version=${1:?"${usage}"}

v_6="https://github.com/google/or-tools/releases/download/v6.0/or-tools_python_examples_v6.0.4217.tar.gz"
v_5="https://github.com/google/or-tools/releases/download/v5.1/or-tools_python_examples_v5.1.4045.tar.gz"

if [ $version == 5.1 ]; then
    dlv="${v_5}"
elif [ $version == 6 ]; then
    dlv="${v_6}"
else
    echo "$usage" && exit 1
fi

curl -L $dlv -o or_tools.tar.gz
tar xzf or_tools.tar.gz

if [ -d ortools_examples ]; then
    pushd ortools_examples
    make install
    popd
else
    echo "err...missing ortools_examples. What directory did the ortools tarball unzip to?" && exit 1
fi

echo "Running python test against ${dlv}"
python crashy.py
