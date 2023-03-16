#!/bin/bash

echo "prepare genesis: Run validate-genesis to ensure everything worked and that the genesis file is setup correctly"
./viscad validate-genesis --home /visca

echo "starting visca node $ID in background ..."
./viscad start \
--home /visca \
--keyring-backend test

echo "started visca node"
tail -f /dev/null