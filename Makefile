# Makefile for source rpm: star
# $Id$
NAME := star
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
