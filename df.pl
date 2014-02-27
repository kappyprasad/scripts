#!/usr/bin/perl

require "$1/libraries.ph" if ($0=~/^(.*)\/[^\/]+$/);

use strict;
use Getopt::Long;

my $USAGE = <<EOU;
USAGE: $0 [-hv] [<-d drive:>] [target]
Options:
    -v show all drives
    -q don't show titles
    -d <last local drive>
    -h this help
EOU

my %OPTIONS;
my $rc = GetOptions(\%OPTIONS,
    'q',
    'h');

die $USAGE unless $rc;

die $USAGE if ($OPTIONS{'h'});

my $quiet = $OPTIONS{'q'};

#die $USAGE unless scalar @ARGV;

my %st;

open(SUBST, "subst |") || die "Can't run subst, $!\n";
while (<SUBST>) {
  if (/^(\S:)(.*)$/) {
    $st{$1}=$2;
  }
}
close(SUBST);

#for my $d (sort(keys(%st))) {
#  print "\$st[$d]=$st{$d}\n";
#}

my $bits = join(" ", @ARGV);

my $drive;
my $size;
my $sizef;
my $used;
my $usedf;
my $percent;
my $avail;
my $availf;

format PsList =
@< @>>>>>>>>>>>> @>>>>>>>>>>>> @>>>>>>>>>>>> @>>>
$drive, $sizef, $usedf, $availf, $percent
.

$~ = "PsList";

if (! $quiet) {
  print "?:    size(kb)      used(kb)     avail(kb)   used\n";
  print "-- ------------- ------------- ------------- ----\n";
}

open (IN, "df -t ntfs -t vfat -k $bits |") || die "Can't run df, $!\n";
while (<IN>) {
  s/[\r\n]//g;
  if (/^([a-z]:)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+\%)\s+/i) {
    ($drive, $size, $used, $avail, $percent) = ($1, $2, $3, $4, $5);
    $sizef = &libraries'num2commas($size);
    $usedf = &libraries'num2commas($used);
    $availf = &libraries'num2commas($avail);
    if (! defined($st{$drive})) {
      write;
    }
  }
}
close(IN);

