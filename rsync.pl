#!/usr/bin/env perl

while (<>) {
    if (/^sending incremental file list$/) {
    }
    elsif (/^sent\s[0-9\,]+\s.*$/) {
    }
    elsif (/^total size is [0-9\,]+\s.*$/) {
    }
    elsif (/^\.\/$/) {
    }
    elsif (/^\s+$/) {
    }
    else {
        print "+$_";
    }
}
