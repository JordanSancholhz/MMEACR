#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

python AgentCF_train_check.py
python AgentCF_Test_log-.py