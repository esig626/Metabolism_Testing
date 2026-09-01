#!/usr/bin/env perl
use strict;
use warnings;
use utf8;

sub parse {
  my$s=shift;$s=~s/\r?\n\z//;my@v;
  while(length$s) {
    if($s=~s/^"((?:[^"]|"")*)"(?:,|$)//){my$x=$1;$x=~s/""/"/g;push@v,$x}
    elsif($s=~s/^([^,]*)(?:,|$)//){push@v,$1}else{die"CSV parse error\n"}
  }@v
}
sub table {
  my$path=shift;open my$h,'<:encoding(UTF-8)',$path or die$!;
  my@head=parse(scalar<$h>);my@rows;my$line=1;
  while(my$raw=<$h>){++$line;my@r=parse($raw);die"$path line $line column count\n"unless@r==@head;my%x;@x{@head}=@r;push@rows,\%x}
  close$h;(\@head,\@rows)
}

my($ph,$papers)=table('corpus/papers.csv');
my(%pid,%doi);
for my$r(@$papers) {
  die"bad paper ID\n"unless$r->{record_id}=~/^P\d{4}$/;
  die"duplicate paper ID\n"if$pid{$r->{record_id}}++;
  if($r->{doi}ne'NR'){my$d=lc$r->{doi};die"duplicate DOI $d\n"if$doi{$d}++}
}
my($sh,$software)=table('corpus/software.csv');
my%sid;
for my$r(@$software){die"duplicate software ID\n"if$sid{$r->{record_id}}++}
my($lh,$ledger)=table('audit/pilot_screening.csv');
my(%state,%identifier);
for my$r(@$ledger) {
  my$i=lc$r->{doi_or_identifier};
  die"duplicate screening identifier $i\n"if$i ne'NR'&&$identifier{$i}++;
  $state{$r->{screening_state}}++;
  if($r->{screening_state}eq'SCREENED_DECISION_UNRECOVERABLE'){
    die"historical unknown has exclusion\n"unless$r->{original_eligibility_disposition}eq'unrecoverable'&&$r->{exclusion_reason}eq'NA';
  }
  if($r->{historical_discovery_provenance_state}eq'HISTORICAL_PROVENANCE_UNRECOVERABLE'){
    die"fabricated historical provenance\n"unless$r->{historical_query_ids}eq'';
  }
  if($r->{repair_retrieval_provenance_state}eq'EXACT_REPAIR_RERUN_MATCH'){
    die"bad repair provenance\n"unless$r->{repair_query_ids}=~/^REPAIR-SEARCH-\d{4}(?:;REPAIR-SEARCH-\d{4})*$/;
  }
}
die"unexpected genuine exclusions\n"if$state{EXCLUDED_WITH_RECORDED_REASON};
die"wrong historical count\n"unless($state{SCREENED_DECISION_UNRECOVERABLE}//0)==198;
open my$g,'<:encoding(UTF-8)','synthesis/candidate_gaps.md'or die$!;
my$text=do{local$/;<$g>};close$g;
die"UNTESTED gap remains\n"if$text=~/\*\*Pilot status:\*\*\s*UNTESTED/;
die"gap called novel\n"if$text=~/\b(?:is|appears|seems)\s+(?:genuinely\s+)?novel\b/i;
print"ok - CSV structure, IDs, DOI uniqueness, screening semantics and gap statuses\n";
