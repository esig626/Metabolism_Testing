#!/usr/bin/env perl
use strict;
use warnings;
use utf8;

my $cmd = system($^X, 'scripts/build_pilot_screening.pl');
die "screening generator failed\n" if $cmd;
open my $fh, '<:encoding(UTF-8)', 'audit/pilot_screening.csv' or die $!;
my $text = do { local $/; <$fh> };
close $fh;
die "Möllney missing\n" unless index($text, 'Möllney') >= 0;
die "mojibake present\n" if $text =~ /MÃ¶llney|Ã[\x{0080}-\x{00BF}]|â(?:€|€™|€œ|€œ)/;
die "historical unknown encoded as exclusion\n"
  if $text =~ /SCREENED_DECISION_UNRECOVERABLE[^\n]*excluded/i;
die "synthetic query range remains\n"
  if $text =~ /SEARCH-0015;SEARCH-0017-SEARCH-0040/;
my @lines=split /\n/,$text;
die "old combined provenance fields remain\n"
  if $lines[0]=~/(?:^|,)query_identifier(?:,|$)|(?:^|,)provenance_state(?:,|$)/;
die "repair identifiers missing\n" unless $text=~/REPAIR-SEARCH-0001/;
die "original query ID used as repair provenance\n"
  if $text=~/"EXACT_REPAIR_RERUN_MATCH","SEARCH-\d/;
for my $line (@lines[1..$#lines]) {
  next unless $line=~/"HISTORICAL_PROVENANCE_UNRECOVERABLE"/;
  die "unrecoverable historical provenance has query IDs\n"
    unless $line=~/"HISTORICAL_PROVENANCE_UNRECOVERABLE",""/;
}
my $historical_exact=()=$text=~/"EXACT_HISTORICAL_PROVENANCE"/g;
my $historical_unknown=()=$text=~/"HISTORICAL_PROVENANCE_UNRECOVERABLE"/g;
my $repair_exact=()=$text=~/"EXACT_REPAIR_RERUN_MATCH"/g;
my $repair_not_found=()=$text=~/"NOT_FOUND_IN_REPAIR_RERUN"/g;
die "wrong historical provenance counts\n"
  unless $historical_exact==0 && $historical_unknown==226;
die "wrong repair provenance counts\n"
  unless $repair_exact==210 && $repair_not_found==16;
print "ok - split provenance, screening states and UTF-8\n";
