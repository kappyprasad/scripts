#!/usr/bin/env perl

require "$1/libraries.ph" if ($0=~/^(.*)\/[^\/]+$/);

if ($#ARGV >= 0) {
  $char = shift(@ARGV);
}
else {
  $char = "_";
}

&libraries'doHorizontal($char);

