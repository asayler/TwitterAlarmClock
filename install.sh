#!/bin/bash

echo "Installing CGI Scripts"
chmod 755 cgi/*
cp cgi/* /usr/lib/cgi-bin/
