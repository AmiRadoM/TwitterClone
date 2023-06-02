#!/bin/sh
flask db stamp head
flask db migrate
flask db upgrade