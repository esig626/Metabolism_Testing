#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use JSON::PP;

sub load_json {
  my $path=shift;
  # JSON::PP::decode_json expects UTF-8 octets and performs the decode.
  open my $h,'<:raw',$path or die "$path: $!";
  local $/; decode_json(<$h>)
}
sub csvq { my$x=shift//'';$x=~s/"/""/g;qq{"$x"} }
sub doi {
  my$x=lc(shift//'');$x=~s{^https?://(?:dx\.)?doi\.org/}{};$x
}
my @header=qw(discovery_id search_id source search_date title authors year
  doi_or_identifier source_native_id duplicate_group screening_state
  exclusion_reason evidence_level final_corpus_id notes);
my @rows; my %seen; my $n=0;
my %final=(
  '10.1371/journal.pcbi.1009999'=>'P0030',
  '10.1093/bioinformatics/btz500'=>'P0031',
  'arxiv:2605.25079'=>'P0032',
  '10.1016/j.ymben.2012.06.003'=>'P0033',
  '10.3390/metabo12020122'=>'P0034',
  '10.3390/bioengineering4020048'=>'P0035',
);
my %abstract_only = ('P0033' => 1);

my $sum=load_json('audit/phase2_raw_search_results/B/PHASE2-SEARCH-0011-pubmed-esummary.json');
for my $pmid (@{$sum->{result}{uids}}) {
  my$r=$sum->{result}{$pmid};
  my($d)=map{doi($_->{value})}grep{($_->{idtype}//'')eq'doi'}@{$r->{articleids}//[]};
  $d //= '';
  my$key=$d||"pmid:$pmid"; my$dup=$seen{$key}++;
  my$pid=$final{$d}//'';
  my$secondary=($pmid eq '37997613'||$pmid eq '36994165');
  my$state=$dup?'DUPLICATE':$pid&&$abstract_only{$pid}?'TITLE_ABSTRACT_INCLUDED':
    $pid?'FULL_TEXT_INCLUDED':
    $secondary?'TITLE_ABSTRACT_INCLUDED':'TITLE_ABSTRACT_EXCLUDED';
  my$reason=$state eq'DUPLICATE'?'DUPLICATE_OF_EARLIER_PHASE2_OCCURRENCE':
    $state eq'TITLE_ABSTRACT_EXCLUDED'?'SECONDARY_OR_NO_NEW_PRIMARY_METHOD':'NA';
  my$level=$state eq'DUPLICATE'?'LEVEL_3_DISCOVERY_ONLY':
    $pid&&$abstract_only{$pid}?'LEVEL_2_SUPPORTING':
    $pid?'LEVEL_1_LOAD_BEARING':'LEVEL_3_DISCOVERY_ONLY';
  push @rows,[sprintf('ROOT-D%04d',++$n),'PHASE2-SEARCH-0011','PubMed',
    '2026-07-31',$r->{title}//'',join('; ',map{$_->{name}}@{$r->{authors}//[]}),
    (($r->{pubdate}//'')=~/(\d{4})/?$1:''),$d||"PMID:$pmid","PMID:$pmid",
    "ROOT-$key",$state,$reason,$level,$pid,
    'Prospective root workstream screening.'];
}

for my $spec (
  ['PHASE2-SEARCH-0013','B/PHASE2-SEARCH-0013-openalex.json'],
  ['PHASE2-SEARCH-0014','B/PHASE2-SEARCH-0014-openalex.json'],
  ['PHASE2-SEARCH-0038','D/PHASE2-SEARCH-0038-openalex.json']) {
  my($sid,$file)=@$spec;my$j=load_json("audit/phase2_raw_search_results/$file");
  for my$r(@{$j->{results}//[]}) {
    my$d=doi($r->{doi}//'');my$key=$d||lc($r->{id}//'');my$dup=$seen{$key}++;
    my$title=$r->{display_name}//'';my$pid=$final{$d}//'';
    my$relevant=$title=~/(?:13.?C|isotope|metabolic flux).*(?:model|Bayes|uncertain|validat)|(?:model|Bayes|uncertain|validat).*(?:13.?C|isotope|metabolic flux)/i;
    my$state=$dup?'DUPLICATE':$pid&&$abstract_only{$pid}?'TITLE_ABSTRACT_INCLUDED':
      $pid?'FULL_TEXT_INCLUDED':
      $relevant?'TITLE_ABSTRACT_INCLUDED':'TITLE_ABSTRACT_EXCLUDED';
    my$reason=$state eq'DUPLICATE'?'DUPLICATE_OF_EARLIER_PHASE2_OCCURRENCE':
      $state eq'TITLE_ABSTRACT_EXCLUDED'
      ?'OUTSIDE_METABOLIC_MODEL_DISCRIMINATION_SCOPE':'NA';
    my$level=$state eq'DUPLICATE'?'LEVEL_3_DISCOVERY_ONLY':
      $pid&&$abstract_only{$pid}?'LEVEL_2_SUPPORTING':
      $pid?'LEVEL_1_LOAD_BEARING':'LEVEL_3_DISCOVERY_ONLY';
    my$authors=join('; ',map{$_->{author}{display_name}//''}@{$r->{authorships}//[]});
    if($d eq '10.3389/fmicb.2015.00235'){
      # This OpenAlex snapshot contains already-mojibaked display metadata.
      # Normalize this exact DOI in the derived ledger only; preserve the raw
      # response unchanged.
      $title='A review on computational systems biology of pathogen–host interactions';
      $authors='Saliha Durmuş; Tunahan Çakır; Arzucan Özgür; Reinhard Guthke';
    }
    if($d eq '10.3389/fmicb.2015.00104'){
      # This OpenAlex snapshot also contains already-mojibaked author
      # metadata. Normalize only the identified record in the derived ledger;
      # never apply a semantic or encoding guess across curated rows.
      $authors='Kristen M. DeAngelis; Grace Pold; Begüm D. Topçuoğlu; Linda T. A. van Diepen; Rebecca Varney; Jeffrey L. Blanchard; Jerry M. Melillo; Serita D. Frey';
    }
    push @rows,[sprintf('ROOT-D%04d',++$n),$sid,'OpenAlex','2026-07-31',
      $title,$authors,$r->{publication_year}//'',$d||$r->{id},$r->{id},
      "ROOT-$key",$state,$reason,$level,$pid,
      'Prospective root workstream screening; only the preserved result page was screened.'];
  }
}

for my $x (
 ['PHASE2-SEARCH-0015','Publisher/DOI routing','Reversible jump MCMC for multi-model inference in Metabolic Flux Analysis','Theorell A; Nöh K','2020','10.1093/bioinformatics/btz500','P0031','FULL_TEXT_INCLUDED','LEVEL_1_LOAD_BEARING'],
 ['PHASE2-SEARCH-0016','arXiv','Trans-dimensional Bayesian model averaging for 13C-based metabolic flux analysis: Evidence-based flux inference under structural model uncertainty','Jadebeck JF; Stratmann A; Beyß M; Nöh K','2026','arXiv:2605.25079','P0032','FULL_TEXT_INCLUDED','LEVEL_1_LOAD_BEARING'],
 ['PHASE2-SEARCH-0037','PubMed','Parallel labeling experiments with [U-13C]glucose validate E. coli metabolic network model for 13C metabolic flux analysis','Leighty RW; Antoniewicz MR','2012','10.1016/j.ymben.2012.06.003','P0033','TITLE_ABSTRACT_INCLUDED','LEVEL_2_SUPPORTING'],
 ['PHASE2-SEARCH-0040','PMC','MetAMDB: Metabolic Atom Mapping Database','Starke C; Wegner A','2022','10.3390/metabo12020122','P0034','FULL_TEXT_INCLUDED','LEVEL_1_LOAD_BEARING'],
 ['PHASE2-SEARCH-0039','PMC','Assessing and Resolving Model Misspecifications in Metabolic Flux Analysis','Gunawan R; Hutter S; Feng X','2017','10.3390/bioengineering4020048','P0035','FULL_TEXT_INCLUDED','LEVEL_1_LOAD_BEARING']) {
  my($sid,$src,$title,$authors,$year,$id,$pid,$state,$level)=@$x;
  my$key=doi($id);$key=lc$id unless$key;my$dup=$seen{$key}++;
  my$out_state=$dup?'DUPLICATE':$state;
  my$out_reason=$dup?'DUPLICATE_OF_EARLIER_PHASE2_OCCURRENCE':'NA';
  my$out_level=$dup?'LEVEL_3_DISCOVERY_ONLY':$level;
  push @rows,[sprintf('ROOT-D%04d',++$n),$sid,$src,'2026-07-31',$title,
    $authors,$year,$id,$id,"ROOT-$key",$out_state,$out_reason,
    $out_level,$pid,'Prospective supplementary discovery routed to complete primary text.'];
}

open my$out,'>:encoding(UTF-8)','audit/phase2_screening_root.csv' or die$!;
print$out join(',',map{csvq($_)}@header),"\n";
print$out join(',',map{csvq($_)}@$_),"\n" for@rows;
close$out or die$!;
print scalar(@rows)," root discovery occurrences written\n";
