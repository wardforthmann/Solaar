#!/bin/sh

cd "`dirname "$0"`/.."
python -m cProfile -o $TMPDIR/solaar.profile bin/solaar "$@"
