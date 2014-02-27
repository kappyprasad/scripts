#!/usr/bin/perl

require "$1/libraries.ph" if ($0=~/^(.*)\/[^\/]+$/);

$|=1;

$cg=$libraries'colour{'Green'};
$co=$libraries'colour{'Orange'};
$cb=$libraries'colour{'Blue'};
$ct=$libraries'colour{'Teal'};
$cr=$libraries'colour{'Red'};
$cx=$libraries'colour{'Off'};

open (IN, "mvn @ARGV 2>&1 |") || die "Can't start ant, $!\n";

while (<IN>) {
  if (/\-{5}/) {
    &libraries'doHorizontal("-");
  }
  else {
    s/(\-{3}\s.*\s\-{3})/$ct$1$cx/g;
    s/\[(debug|INFO)\]/\[$cb$1$cx\]/g;
    s/\[(WARNING)\]/\[$co$1$cx\]/g;
    s/\[(ERROR)\]/\[$cr$1$cx\]/g;
    s/(SUCCESSFUL|SUCCESS)/$cg$1$cx/g;
    s/(FAILURE|FAILED)/$cr$1$cx/g;
    if (/Reactor Summary:/) {
      &libraries'doHorizontal("=");
    }
    print;
  }
}

