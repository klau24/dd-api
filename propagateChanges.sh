#!/bin/bash

ssh -i /Users/Kenny/.ssh/id_rsa ec2-user@44.240.238.232 'cd /usr/local/dd-api/ && sudo git pull && sudo systemctl restart gunicorn'