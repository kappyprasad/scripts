#!/usr/bin/env perl

while (<>) {
    if (/^sending incremental file list$/) {
    }
    elsif (/^skipping non-regular file "([^"]+)"/) {
        #print "~$1\n";
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
