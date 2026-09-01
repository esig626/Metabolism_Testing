#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));

sub parse {
  my$s=shift;$s=~s/\r?\n\z//;my@v;
  while(length$s){
    if($s=~s/^"((?:[^"]|"")*)"(?:,|\z)//){my$x=$1;$x=~s/""/"/g;push@v,$x}
    elsif($s=~s/^([^,]*)(?:,|\z)//){push@v,$1}
    else{die"CSV parse error\n"}
  }@v
}
sub csvq{my$x=shift//'';$x=~s/"/""/g;qq{"$x"}}
my %allowed_state=map{$_=>1}qw(
  DISCOVERED_NOT_SCREENED TITLE_ABSTRACT_INCLUDED TITLE_ABSTRACT_EXCLUDED
  FULL_TEXT_INCLUDED FULL_TEXT_EXCLUDED DUPLICATE FULL_TEXT_UNAVAILABLE
  AWAITING_VERIFICATION FALSE_POSITIVE
  DEFERRED_RELEVANT_SUPPORTING DEFERRED_RELEVANT_ADJACENT
  OUT_OF_SCOPE_FOR_PHASE2A1 FALSE_POSITIVE_CONFIRMED
);
my %allowed_level=map{$_=>1}qw(
  LEVEL_1_LOAD_BEARING LEVEL_2_SUPPORTING LEVEL_3_DISCOVERY_ONLY
);
my @out=qw(phase2_record_id workstream search_source query_id date title
  authors year doi_or_identifier source_native_id duplicate_group
  screening_state exclusion_reason evidence_level final_record_id notes);
my @sources=(
 ['A','audit/phase2_screening_A.csv'],
 ['A','audit/phase2_screening_A_closure.csv'],
 ['AUTO','audit/phase2_screening_root.csv'],
 ['B','audit/phase2_screening_B_audit.csv'],
 ['C','audit/phase2_screening_C.csv'],
 ['D','audit/phase2_screening_D_closure.csv'],
 ['E','audit/phase2_screening_E.csv'],
);
my @rows;my$serial=0;my%seen_id;
for my$spec(@sources){
  my($ws,$path)=@$spec;open my$h,'<:encoding(UTF-8)',$path or die"$path: $!";
  my@head=parse(scalar<$h>);my%p;@p{@head}=0..$#head;
  my$line_number=1;
  while(my$line=<$h>){
    $line_number++;
    my@r=parse($line);die"$path column mismatch\n"unless@r==@head;
    my$get=sub{for(@_){return$r[$p{$_}]if exists$p{$_}}return''};
    my$id=$get->('phase2_record_id','workstream_record_id','discovery_id');
    $id=sprintf('PHASE2-D%05d',++$serial) unless length$id;
    die "$path:$line_number duplicate occurrence ID $id\n" if $seen_id{$id}++;
    my$source=$get->('search_source','source');
    my$qid=$get->('query_id','search_id');
    my$date=$get->('search_date','date');
    my$native=$get->('source_native_id','url');
    my$dup=$get->('duplicate_group');
    my$final=$get->('final_corpus_id','final_record_id');
    my$state=$get->('screening_state');
    my$reason=$get->('exclusion_reason');
    my$level=$get->('evidence_level');
    die "$path:$line_number invalid query ID '$qid'\n"
      unless$qid=~/^PHASE2-SEARCH-\d{4}$/;
    die "$path:$line_number invalid screening state '$state'\n"
      unless$allowed_state{$state};
    die "$path:$line_number invalid evidence level '$level'\n"
      unless$allowed_level{$level};
    die "$path:$line_number missing duplicate group\n" unless length$dup;
    if($state eq'TITLE_ABSTRACT_EXCLUDED'||$state eq'FULL_TEXT_EXCLUDED'){
      die "$path:$line_number missing prospective exclusion reason\n"
        unless length($reason)&&$reason ne'NA';
    }
    if($state eq'DUPLICATE'){
      die "$path:$line_number missing duplicate reason\n"
        unless length($reason)&&$reason ne'NA';
    }
    my$resolved_ws=$ws;
    if($ws eq 'AUTO'){
      $resolved_ws = $qid =~ /^PHASE2-SEARCH-(?:001[1-6])$/ ? 'B' :
                     $qid =~ /^PHASE2-SEARCH-(?:003[6-9]|0040)$/ ? 'D' :
                     die "Cannot infer workstream for $qid in $path\n";
    }
    push@rows,[$id,$resolved_ws,$source,$qid,$date,$get->('title'),$get->('authors'),
      $get->('year'),$get->('doi_or_identifier'),$native,$dup,
      $state,$reason,$level,$final,$get->('notes','raw_result_file')];
  }close$h;
}
my$out_path='audit/phase2_screening.csv';
my$tmp_path="$out_path.tmp.$$";
open my$o,'>:encoding(UTF-8)',$tmp_path or die$!;
print$o join(',',map{csvq($_)}@out),"\n";
print$o join(',',map{csvq($_)}@$_),"\n"for@rows;
close$o or die$!;

# Reapply the separately curated Phase 2A.1 paper-level closure after every
# deterministic rebuild. Apply it to the temporary base ledger so a closure
# conflict cannot replace the authoritative curated ledger. The throwaway
# closure log describes only transformations of this temporary rebuild; the
# authoritative correction history remains in the repository audit log.
if (-e 'audit/phase2_unresolved_triage.csv') {
  my $temporary_closure_log = "$tmp_path.closure-log";
  local $ENV{PHASE2_SCREENING_PATH} = $tmp_path;
  local $ENV{PHASE2_CLOSURE_CHANGE_LOG_PATH} = $temporary_closure_log;
  my $status = system(
    $^X, 'scripts/apply_phase2a1_screening_closure.pl'
  );
  if ($status != 0) {
    unlink $tmp_path if -e $tmp_path;
    unlink $temporary_closure_log if -e $temporary_closure_log;
    die "Phase 2A.1 screening closure failed (status=$status); "
      . "authoritative ledger was not replaced\n";
  }
  if (-e $temporary_closure_log) {
    unlink $temporary_closure_log
      or die "cannot remove temporary closure log "
        . "$temporary_closure_log: $!\n";
  }
}

if (-e $out_path) {
  open my $existing, '<:raw', $out_path or die "$out_path: $!";
  local $/;
  my $existing_bytes = <$existing>;
  close $existing or die "$out_path: $!";
  open my $candidate, '<:raw', $tmp_path or die "$tmp_path: $!";
  my $candidate_bytes = <$candidate>;
  close $candidate or die "$tmp_path: $!";
  if ($existing_bytes ne $candidate_bytes) {
    unlink $tmp_path if -e $tmp_path;
    die "rebuild candidate differs from curated $out_path; refusing "
      . "replacement and requiring an explicit record-level merge\n";
  }
  unlink $tmp_path
    or die "cannot remove identical rebuild candidate $tmp_path: $!\n";
}
else {
  rename $tmp_path, $out_path
    or die "rename $tmp_path -> $out_path: $!";
}

# Report the post-closure authoritative states, not the transient base states.
open my $final, '<:encoding(UTF-8)', $out_path
  or die "$out_path: $!";
my @final_head = parse(scalar <$final>);
my %fp;
@fp{@final_head} = 0 .. $#final_head;
my (%state, %level, %workstream);
my $final_rows = 0;
while (my $line = <$final>) {
  my @r = parse($line);
  die "$out_path column mismatch\n" unless @r == @final_head;
  $final_rows++;
  $workstream{$r[$fp{workstream}]}++;
  $state{$r[$fp{screening_state}]}++;
  $level{$r[$fp{evidence_level}]}++;
}
close $final or die "$out_path: $!";
print "occurrences=$final_rows\n";
print "workstreams ",
  join(' ', map { "$_=$workstream{$_}" } sort keys %workstream), "\n";
print "states ",
  join(' ', map { "$_=$state{$_}" } sort keys %state), "\n";
print "levels ",
  join(' ', map { "$_=$level{$_}" } sort keys %level), "\n";
