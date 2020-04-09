#!/bin/bash

touch chronicle.log
exec python3 chronicle.py &
exec python3 log_watcher.py
