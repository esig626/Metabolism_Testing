#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use JSON::PP;

sub load_json {
  my $path=shift;
  open my $h,'<:encoding(UTF-8)',$path or die "$path: $!";
  local $/;
  JSON::PP->new->utf8(0)->decode(<$h>)
}
sub csvq { my$v=shift//'';$v=~s/"/""/g;qq{"$v"} }
sub normdoi { my$v=lc(shift//'');$v=~s{^https?://(?:dx\.)?doi\.org/}{};$v }
sub csvrow {
  my $s=shift; chomp$s; my@f;
  while(length$s) {
    $s=~s/^"((?:[^"]|"")*)"(?:,|$)// or die "CSV parse error";
    my$v=$1;$v=~s/""/"/g;push@f,$v
  }
  @f
}

my %query_for;
for my $n (1..6) {
  my $legacy=sprintf('SEARCH-%04d',$n);
  my $repair=sprintf('REPAIR-SEARCH-%04d',$n);
  my $j=load_json("audit/raw_search_results/$legacy-pubmed-esearch.json");
  push @{$query_for{$_}},$repair for @{$j->{esearchresult}{idlist}};
}
my $sum=load_json('audit/raw_search_results/pubmed_unique_esummary.json');

open my $pf,'<:encoding(UTF-8)','corpus/papers.csv' or die$!;
<$pf>; my(%ret,@corpus);
while(my$line=<$pf>) {
  my@f=csvrow($line);
  next unless $f[0] =~ /^P(?:00(?:0[1-9]|1\d|2\d))$/ && $f[0] le 'P0029';
  push@corpus,\@f;
  $ret{normdoi($f[2])}=$f[0] if$f[2] ne'NR';
}
close$pf;

my@rows;
for my$pmid(@{$sum->{result}{uids}}) {
  my$r=$sum->{result}{$pmid};
  my($doi)=map{$_->{value}}grep{($_->{idtype}//'')eq'doi'}@{$r->{articleids}//[]};
  $doi=normdoi($doi);my$pid=$ret{$doi}//'';
  my$authors=join('; ',map{$_->{name}}@{$r->{authors}//[]});
  my($year)=($r->{pubdate}//'')=~/(\d{4})/;
  push@rows,['PubMed','HISTORICAL_PROVENANCE_UNRECOVERABLE','',
    'EXACT_REPAIR_RERUN_MATCH',join(';',@{$query_for{$pmid}}),'2026-07-30',
    'Matched by a 2026-07-30 repair rerun; original record-level discovery query was not preserved.',
    '2026-07-30',$r->{title}//'',$authors,$year//'',$doi||"PMID:$pmid",
    "D-$pmid",$pid?'RETAINED':'SCREENED_DECISION_UNRECOVERABLE',
    $pid?'retained':'unrecoverable','NA',$pid];
}
my%seen=map{normdoi($_->[7])=>1}@rows;
for my$n(11..14) {
  my$legacy=sprintf('SEARCH-%04d',$n);
  my$sid=sprintf('REPAIR-SEARCH-%04d',$n);
  my$j=load_json("audit/raw_search_results/$legacy-openalex.json");
  for my$r(@{$j->{results}//[]}) {
    my$doi=normdoi($r->{doi}//'');next if$doi&&$seen{$doi}++;
    my$authors=join('; ',map{$_->{author}{display_name}}@{$r->{authorships}//[]});
    my$pid=$ret{$doi}//'';
    push@rows,['OpenAlex','HISTORICAL_PROVENANCE_UNRECOVERABLE','',
      'EXACT_REPAIR_RERUN_MATCH',$sid,'2026-07-30',
      'Matched by a 2026-07-30 repair rerun; original record-level discovery query was not preserved.','2026-07-30',
      $r->{title}//'',$authors,$r->{publication_year}//'',$doi||$r->{id},
      'D-OA-'.($r->{id}=~s{.*/}{}r),
      $pid?'RETAINED':'SCREENED_DECISION_UNRECOVERABLE',
      $pid?'retained':'unrecoverable','NA',$pid];
  }
}
my%row_pid=map{($_->[16]||'')=>1}@rows;
for my$f(@corpus) {
  next if$row_pid{$f->[0]};
  my($authors,$year)=($f->[1]=~/^(.*?)\.\s.*?((?:19|20)\d{2})/);
  my$is_repair=$f->[0]eq'P0029';
  push @rows, [($is_repair?'Targeted repair discovery':'Historical supplementary/citation discovery'),
    ($is_repair?'MANUAL_CITATION_DISCOVERY':'HISTORICAL_PROVENANCE_UNRECOVERABLE'),'',
    ($is_repair?'NOT_APPLICABLE':'NOT_FOUND_IN_REPAIR_RERUN'),'',
    ($is_repair?'':'2026-07-30'),
    ($is_repair?'Prospective manual discovery during targeted repair; not an original pilot query match.':
      'Original record-level discovery query was not preserved; record was not found in the stored API reruns.'),
    '2026-07-30',$f->[1],$authors//'',$year//'',
    $f->[2],'D-'.$f->[0],'RETAINED','retained','NA',$f->[0]];
}
@rows=sort{($a->[12]cmp$b->[12])||($a->[4]cmp$b->[4])}@rows;
open my$out,'>:encoding(UTF-8)','audit/pilot_screening.csv' or die$!;
print$out join(',',qw(search_source historical_discovery_provenance_state
  historical_query_ids repair_retrieval_provenance_state repair_query_ids
  repair_rerun_date provenance_notes date title authors year doi_or_identifier
  duplicate_group screening_state
  original_eligibility_disposition exclusion_reason final_paper_id)),"\n";
print$out join(',',map{csvq($_)}@$_),"\n" for@rows;
close$out or die$!;
my%count;$count{$_->[13]}++for@rows;
print"discovered=",scalar(@rows)," retained=",($count{RETAINED}//0),
  " decision_unrecoverable=",($count{SCREENED_DECISION_UNRECOVERABLE}//0),"\n";
