#!/usr/bin/perl

require "$1/libraries.ph" if ($0=~/^(.*)\/[^\/]+$/);

use strict;
use Getopt::Long;

#
# Read and validate command line args
#

my $USAGE = <<EOU;
USAGE: $0 [-qh] <files..s>
Options:
    -q don\'t show titles and totals
    -h this help
EOU

my %OPTIONS;
my $rc = GetOptions(\%OPTIONS,
		    'q',
		    'h');

die $USAGE unless $rc;

die $USAGE if ($OPTIONS{'h'});

die $USAGE unless scalar @ARGV;

my $quiet = $OPTIONS{'q'};

my $usedf;
my $used;
my $name;
my $totalf;
my $total;
my $i;

my $format = "\%15s \%-" . ($ENV{"COLUMNS"}-16) . "s\n";
my $lh = ""; foreach $i (1 .. 15) { $lh .= "-"; }
my $rh = ""; foreach $i (1 .. ($ENV{"COLUMNS"}-16)) { $rh .= "-"; }


$|="1";

$total = 0;

if (! $quiet) {
  print STDOUT sprintf($format, "size(kb)","name");
  print STDOUT sprintf($format, $lh, $rh);
}

my $args = "\"" . join("\" \"", @ARGV) . "\"";
my $cmd = "du -sk $args |";

open (IN, $cmd) || die "Can't run du, $!\n";
while (<IN>) {
  s/[\r\n]//g;
  if (/^(\d+)\s+(\S.*)$/) {
    ($used, $name) = ($1, $2);
    $total+= $used;
    $usedf = &libraries'num2commas($used);
    print STDOUT sprintf($format, $usedf, $name);
  }
}
close(IN);

if ( ! $quiet ) {
  $totalf = sprintf("%12s", &libraries'num2commas($total));
  print STDOUT sprintf($format, $lh, $rh);
  print STDOUT sprintf($format, $totalf, "Total");
}

