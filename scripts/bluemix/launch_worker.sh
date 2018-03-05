#!/bin/bash

celery worker -A application -l info --events