#!/bin/bash
cd root
tf init
tf fmt -recursive
tf apply -var-file=../local.tfvars
cd -