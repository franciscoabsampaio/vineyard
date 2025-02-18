#!/bin/bash
cd env
tf init
tf fmt -recursive
TF_VAR_env=$1
tf apply -var-file=../local.tfvars -var="env=$1"
cd -