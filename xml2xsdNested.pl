#!/usr/bin/perl

# $Date: 2014-06-19 08:24:58 +1000 (Thu, 19 Jun 2014) $
# $Revision: 4728 $
# $Author: dedson $
# $HeadURL: https://slither/svn/repository/trunk/DavidEdson/Software/perl/xml2xsdNested.pl $
# $Id: xml2xsdNested.pl 4728 2014-06-18 22:24:58Z dedson $



use XML::DOM;

my $parser = new XML::DOM::Parser;
my $doc = $parser->parsefile (shift(@ARGV));

print <<EOF;
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified" attributeFormDefault="unqualified">
EOF

my $root = $doc->getLastChild();
&process($root, "  ");

print <<EOF;
</xs:schema>
EOF

$doc->dispose;

exit 0;

sub process {
  my $parent = shift(@_);
  my $leader = shift(@_);

  if ($parent->getNodeType() == ELEMENT_NODE) {

    my $tag = $parent->getTagName();
    $tag =~ s/^[^:]*://;

    my $nodes = $parent->getChildNodes();
    my $n = $nodes->getLength();

    if (count($parent) > 0) {
      print "$leader<xs:element name=\"$tag\">\n";
      print "${leader}  <xs:complexType>\n";
      print "${leader}    <xs:sequence>\n";

      for (my $i = 0; $i < $n; $i++) {
        my $node = $nodes->item ($i);
        my $href = $node->getNodeName();
        &process($node, "${leader}      ");
      }

      print "${leader}    </xs:sequence>\n";

      my $atts = $parent->getAttributes();
      my $ac = $atts->getLength();
      for (my $a=0; $a<$ac; $a++) {
        my $att = $atts->item($a);
	my $an = $att->getName();
	$an =~ s/^[^:]*://;
        print "${leader}    <xs:attribute name=\"$an\" type=\"xs:string\"/>\n";
      }

      print "${leader}  </xs:complexType>\n";
      print "$leader</xs:element>\n";

    }
    else {
	print "${leader}  <xs:element name=\"$tag\" type=\"xs:string\"/>\n";
    }

  }

}

sub count {
  my $node = shift(@_);
  my $ret = 0;
  my $nodes = $node->getChildNodes();
  my $n = $nodes->getLength();
  for (my $i=0; $i< $n; $i++) {
    my $n = $nodes->item($i);
    if ($n->getNodeType() == ELEMENT_NODE) {
      $ret++;
    }
  }
  return $ret;
}
