#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));
use Test::More;
use File::Temp qw(tempdir);
use File::Copy qw(copy);
use Cwd qw(abs_path);

sub qcsv { my$x=shift//'';$x=~s/"/""/g;qq{"$x"} }
sub parse {
  my$s=shift;chomp$s;my@v;
  while(length$s) {
    if($s=~s/^"((?:[^"]|"")*)"(?:,|$)//){my$x=$1;$x=~s/""/"/g;push@v,$x}
    elsif($s=~s/^([^,]*)(?:,|$)//){push@v,$1}else{die"parse"}
  }@v
}
my@old=qw(record_id full_citation doi url publication_type publication_status
 primary_or_secondary_source scientific_objective biological_domain model_type
 observation_type estimated_or_decided_object experimental_variables_optimised
 uncertainty_represented uncertainty_formulation uncertainty_dependencies
 statistical_criterion statistical_guarantee finite_sample uniform_or_worst_case
 minimax converse_or_impossibility structural_alternatives multiple_experiments
 non_iid sample_size_design replicate_type model_misspecification software
 principal_result authors_stated_limitations reviewer_assessed_limitations
 novelty_claim_affected relevance verification_status evidence_location notes);
push@old,'curator_private_column';
my@row=('')x@old;
my%p=map{$old[$_]=>$_}0..$#old;
$row[$p{record_id}]='P9001';
$row[$p{full_citation}]='Möllney M. Fixture.';
$row[$p{doi}]='10.0000/test';
$row[$p{evidence_location}]='manually changed Section 9';
$row[$p{statistical_guarantee}]='none';
$row[$p{notes}]='curated note';
$row[$p{curator_private_column}]='must survive';

my$dir=tempdir(CLEANUP=>1);
my$input="$dir/input.csv";my$output="$dir/output.csv";my$report="$dir/report.md";
open my$fh,'>:encoding(UTF-8)',$input or die$!;
print$fh join(',',@old),"\n",join(',',map{qcsv($_)}@row),"\n";close$fh;
my$script=abs_path('scripts/rebuild_phase1_corpus.pl');
ok(system($^X,$script,'--input',$input,'--output',$output,'--report',$report)==0,
  'migration succeeds');
open my$got,'<:encoding(UTF-8)',$output or die$!;
my@h=parse(scalar<$got>);my@r=parse(scalar<$got>);close$got;
my%q=map{$h[$_]=>$_}0..$#h;
ok($r[$q{evidence_location}]eq'manually changed Section 9','evidence location survives');
ok($r[$q{statistical_guarantee}]eq'none','downgraded guarantee survives');
ok($r[$q{full_citation}]eq'Möllney M. Fixture.','UTF-8 author survives');
ok($r[$q{curator_private_column}]eq'must survive','unknown column survives');
ok($r[$q{record_id}]eq'P9001','stable ID survives');
ok(@r==@h,'row and column counts are consistent');

# Duplicate stable IDs are a reported conflict and cannot produce output.
my$bad="$dir/bad.csv";my$badout="$dir/bad-output.csv";
open$fh,'>:encoding(UTF-8)',$bad or die$!;
print$fh join(',',@old),"\n";
print$fh join(',',map{qcsv($_)}@row),"\n" for 1..2;close$fh;
ok(system($^X,$script,'--input',$bad,'--output',$badout,
  '--report',"$dir/bad-report.md")!=0,'duplicate-ID conflict refuses migration');
ok(!-e$badout,'conflict creates no migrated output');
ok(-e"$dir/bad-report.md",'conflict report is written');

# A current-schema corpus is a preservation operation: bytes, IDs, row order,
# unknown columns, and UTF-8 must remain unchanged.
my$current="$dir/current.csv";my$currentout="$dir/current-output.csv";
copy('corpus/papers.csv',$current) or die$!;
open my$rawin,'<:raw',$current or die$!;my$before=do{local$/;<$rawin>};close$rawin;
ok(system($^X,$script,'--input',$current,'--output',$currentout,
  '--report',"$dir/current-report.md")==0,'current-schema migration succeeds');
open my$rawout,'<:raw',$currentout or die$!;my$after=do{local$/;<$rawout>};close$rawout;
ok($before eq $after,'valid curated corpus remains byte-for-byte unchanged');
open my$cur,'<:encoding(UTF-8)',$currentout or die$!;
my@ch=parse(scalar<$cur>);my@order;my$has_mollney=0;
while(my$l=<$cur>){my@x=parse($l);push@order,$x[0];$has_mollney=1 if join(' ',@x)=~/Möllney/}
close$cur;
my$total=@order;
ok($total>=29,'existing corpus retains all Phase 1 and later records');
ok(join(';',@order)eq join(';',map{sprintf('P%04d',$_)}1..$total),
  'existing stable IDs remain in the same order');
ok($has_mollney,'Möllney remains correctly encoded');

# An invalid value fails closed even when it belongs to another field's
# vocabulary. It is not moved, normalized, or replaced with a default.
open my$cf,'<:encoding(UTF-8)',$current or die$!;
my@ih=parse(scalar<$cf>);my@ir=parse(scalar<$cf>);close$cf;
my%ip=map{$ih[$_]=>$_}0..$#ih;
$ir[$ip{guarantee_regime}]='T_optimality';
my$invalid="$dir/invalid.csv";my$invalidout="$dir/invalid-output.csv";
open$fh,'>:encoding(UTF-8)',$invalid or die$!;
print$fh join(',',map{qcsv($_)}@ih),"\n",join(',',map{qcsv($_)}@ir),"\n";
close$fh;
open$rawin,'<:raw',$invalid or die$!;my$invalid_before=do{local$/;<$rawin>};close$rawin;
ok(system($^X,$script,'--input',$invalid,'--output',$invalidout,
  '--report',"$dir/invalid-report.md")!=0,
  'invalid guarantee_regime aborts migration');
ok(!-e$invalidout,'validation failure creates no output corpus');
open$rawin,'<:raw',$invalid or die$!;my$invalid_after=do{local$/;<$rawin>};close$rawin;
ok($invalid_before eq $invalid_after,'validation failure does not replace input');
open my$rf,'<:encoding(UTF-8)',"$dir/invalid-report.md" or die$!;
my$rt=do{local$/;<$rf>};close$rf;
ok($rt=~/record_id=P0001/ && $rt=~/field=guarantee_regime/
   && $rt=~/value=`T_optimality`/ && $rt=~/permitted=/,
  'conflict report identifies record, field, value and vocabulary');
ok($rt!~/realigned|moved from guarantee_regime/i,
  'criterion-family value is not moved from guarantee_regime');

done_testing();
