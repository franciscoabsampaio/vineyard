#!/bin/bash
cd root
tf init
tf fmt -recursive
tf apply -var-file=../local.tfvars
# Output root resources configuration (will be used downstream)
tf output -json > ../outputs/root.json
cd -