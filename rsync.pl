#!/usr/bin/env perl

while (<>) {
    if ( ! /^(sending incremental file list|sent\s[0-9\,]+\s.*|total size is [0-9\,]+\s.*|\.\/|\s+)$/) {
        print "+$_";
    }
}
