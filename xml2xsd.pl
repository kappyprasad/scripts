#!/usr/bin/perl

# $Date: 2014-06-19 08:24:58 +1000 (Thu, 19 Jun 2014) $
# $Revision: 4728 $
# $Author: dedson $
# $HeadURL: https://slither/svn/repository/trunk/DavidEdson/Software/perl/xml2xsd.pl $
# $Id: xml2xsd.pl 4728 2014-06-18 22:24:58Z dedson $




use strict;
use Getopt::Long;
use XML::DOM;

my $USAGE = <<EOU;
USAGE: $0 [-a] <xml> <xsd>
Options:
    -h this help document
    -a fill in attribute enumerations
EOU

my %OPTIONS;
my $rc = GetOptions(\%OPTIONS, 'a', 'h');

die $USAGE if ($OPTIONS{'h'});

my %elements;   # $elements(parent, child) = sequence order, size == 1 links self
my %attributes; # $attributes(parent, attr-name) = @attvalues

my @sorter;

my $key;
my $element;
my $name;
my $unbound;

if ($#ARGV != 1) {
  die $USAGE;
}

my $parser = new XML::DOM::Parser;
my $doc = $parser->parsefile (shift(@ARGV));

my $xsd = shift(@ARGV);

open (OUT, ">$xsd") || die "Can't create $xsd, $!\n";

print OUT <<EOF;
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified" attributeFormDefault="unqualified">
EOF

my $root = $doc->getLastChild();

&acquire($root, "/");

$elements{$root->getNodeName()}{"-"} = -2; # to mark annotation

foreach $key (sort(keys(%elements))) {
  #print "element=$key\n";

  my $hasChildren = keys(%{ $elements{$key} }) > 1;
  my $hasAttributes = keys(%{ $attributes{$key} }) > 0;

  print OUT "  <xs:element name=\"" . $key . "\"";
  if (! $hasChildren && ! $hasAttributes) {
    print OUT " type=\"xs:string\"";
  }
  print OUT ">\n";

  if ($elements{$key}{"-"} == -2) {
    print OUT <<EOF;
    <xs:annotation>
      <xs:documentation>root</xs:documentation>
    </xs:annotation>
EOF
  }

  if ($hasChildren  || $hasAttributes ) {
    print OUT "    <xs:complexType>\n";
  }

  undef(@sorter);
  undef($unbound);

  foreach $element (keys(%{ $elements{$key} })) {
    if ($element ne "-") {
      #print "\tref=$element\n";
      $sorter[$elements{$key}{$element}] = $element;
      if ( ($key eq ( $element . "s")) ) {
        #print "$key, $element, len=" . length(%{ $elements{$key} }) . "\n";
        $unbound = 1;
      }
    }
  }

  if ($hasChildren ) {
    print OUT "      <xs:sequence";
    if ($unbound == 1) {
      print OUT " maxOccurs=\"unbounded\"";
    }
    print OUT ">\n";
  }

  foreach $element (@sorter) {
    if ($element ne "") {
      #ignore text elemements, WARNING forcing order.
      print OUT "        <xs:element ref=\"" . $element . "\"/>\n";
    }
  }

  if ($hasChildren) {
    print OUT "      </xs:sequence>\n";
  }

  foreach $name (sort(keys(%{ $attributes{$key} }))) {
    #print "\t\tattr=$name, value=$attributes{$key}{$name}\n";
    my @atts = @{ $attributes{$key}{$name} };
    if (!defined($OPTIONS{'a'})) {
      print OUT "      <xs:attribute name=\"" . $name . "\" type=\"xs:string\"/>\n";
    }
    else {
      print OUT "      <xs:attribute name=\"" . $name . "\">\n";
      print OUT "        <xs:simpleType>\n";
      print OUT "          <xs:restriction base=\"xs:string\">\n";
      foreach my $att (@atts) {
        print OUT "            <xs:enumeration value=\"$att\"/>\n";
      }
			print OUT "          </xs:restriction>\n";
			print OUT "        </xs:simpleType>\n";
      print OUT "      </xs:attribute>\n";
    }
  }

  if ($hasChildren || $hasAttributes) {
    print OUT "    </xs:complexType>\n";
  }

  print OUT "  </xs:element>\n";

}

print OUT <<EOF;
</xs:schema>
EOF

$doc->dispose;

close(OUT);

exit 0;

sub acquire {
  my $parent = shift(@_);
  my $leader = shift(@_);

  if ($parent->getNodeType() == ELEMENT_NODE) {

    my $nodes = $parent->getChildNodes();
    my $n = $nodes->getLength();

    my $atts = $parent->getAttributes();
    my $ac = $atts->getLength();

    $elements{$parent->getNodeName()}{"-"} = -1;

    for (my $i = 0; $i < $n; $i++) {
      my $node = $nodes->item ($i);
      my $href = $node->getNodeName();
      if ($node->getNodeType() == ELEMENT_NODE) {
        #putting order into sequence
        $elements{$parent->getNodeName()}{$node->getNodeName()} = $i;
        #print $leader . "/" . $parent->getNodeName() . "/" . $node->getNodeName() . "\n";

      }
      &acquire($node,$leader . "/" . $parent->getNodeName());
    }

    for (my $a=0; $a<$ac; $a++) {
      my $att = $atts->item($a);
      if ($att->getName() ne "xmlns:xsi" && $att->getName() ne "xsi:noNamespaceSchemaLocation") {
        # ignore namespace attributes
        push(@{ $attributes{$parent->getNodeName()}{$att->getName()} }, $att->getValue());
      }
    }

  }

}

