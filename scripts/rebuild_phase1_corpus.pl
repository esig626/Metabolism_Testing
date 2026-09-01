#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use Getopt::Long qw(GetOptions);
use POSIX qw(strftime);
use File::Copy qw(copy);
use File::Basename qw(dirname);
use File::Path qw(make_path);

my ($input, $output, $report, $apply) =
  ('corpus/papers.csv', undef, 'audit/migration_report.md', 0);
GetOptions('input=s'=>\$input, 'output=s'=>\$output, 'report=s'=>\$report,
  'apply!'=>\$apply) or die "invalid options\n";
die "--apply cannot be combined with --output\n" if $apply && defined $output;

my @old = qw(record_id full_citation doi url publication_type
  publication_status primary_or_secondary_source scientific_objective
  biological_domain model_type observation_type estimated_or_decided_object
  experimental_variables_optimised uncertainty_represented
  uncertainty_formulation uncertainty_dependencies statistical_criterion
  statistical_guarantee finite_sample uniform_or_worst_case minimax
  converse_or_impossibility structural_alternatives multiple_experiments
  non_iid sample_size_design replicate_type model_misspecification software
  principal_result authors_stated_limitations reviewer_assessed_limitations
  novelty_claim_affected relevance verification_status evidence_location notes);
my @new = qw(criterion_family guarantee_regime robustness_scope converse_type
  stopping_rule structural_alternative_subtype parameter_sharing
  retrieval_status access_status full_text_inspected screening_disposition
  exclusion_reason);
my %default = (
  criterion_family=>'unclear', guarantee_regime=>'unclear',
  robustness_scope=>'none', converse_type=>'none',
  stopping_rule=>'unspecified', structural_alternative_subtype=>'other',
  parameter_sharing=>'unspecified', retrieval_status=>'unclear',
  access_status=>'unclear', full_text_inspected=>'no',
  screening_disposition=>'retained', exclusion_reason=>'NA',
);
my %allowed = (
  criterion_family=>[qw(D_optimality T_optimality KL_optimality Bayesian_discrimination Chernoff Fisher_information likelihood posterior other NR unclear)],
  guarantee_regime=>[qw(none heuristic simulation_based local_asymptotic global_asymptotic non_asymptotic exact_finite_sample unclear)],
  robustness_scope=>[qw(none local_neighbourhood sampled_flux_maps finite_scenario_set continuous_parameter_set structural_uncertainty_set distributional_uncertainty model_misspecification unclear)],
  converse_type=>[qw(none identifiability_obstruction rank_obstruction lower_bound error_exponent_converse sample_complexity_converse other unclear)],
  stopping_rule=>[qw(fixed_sample sequential adaptive unspecified NA)],
  structural_alternative_subtype=>[qw(reaction_presence_absence pathway_alternative compartment_structure atom_mapping kinetic_mechanism mechanism_class other NA unclear)],
  parameter_sharing=>[qw(shared_across_conditions condition_specific partially_shared unspecified NA)],
  retrieval_status=>[qw(not_attempted metadata_retrieved abstract_retrieved retrieved_full_text retrieval_failed unclear)],
  access_status=>[qw(open_access author_manuscript user_supplied paywalled_or_inaccessible not_retrieved unclear)],
  full_text_inspected=>[qw(yes no partial unclear)],
  screening_disposition=>[qw(retained excluded duplicate pending unclear)],
);
my %permitted = map { $_ => join(';', @{$allowed{$_}}) } keys %allowed;
for my $field (keys %allowed) {
  my %values = map { $_=>1 } @{$allowed{$field}};
  $allowed{$field} = \%values;
}

sub parse_csv {
  my ($s)=@_; $s =~ s/\r?\n\z//; my @v;
  while (length $s) {
    if ($s =~ s/^"((?:[^"]|"")*)"(?:,|\z)//) {
      my $x=$1; $x =~ s/""/"/g; push @v,$x;
    } elsif ($s =~ s/^([^,]*)(?:,|\z)//) { push @v,$1 }
    else { die "CSV parse error\n" }
  }
  @v
}
sub quote_csv { my $x=shift//''; $x =~ s/"/""/g; qq{"$x"} }
sub write_report {
  my ($path,$text)=@_; make_path(dirname($path)) unless -d dirname($path);
  open my $h,'>:encoding(UTF-8)',$path or die "$path: $!"; print $h $text;
  close $h or die "$path: $!";
}
sub allowed_value {
  my ($field,$value)=@_;
  return 1 unless exists $allowed{$field};
  my @parts=split/;/,$value,-1;
  return !grep{!$allowed{$field}{$_}}@parts;
}

open my $in,'<:encoding(UTF-8)',$input or die "$input: $!";
my @header=parse_csv(scalar <$in>);
my %pos;
for my $i (0..$#header) {
  die "duplicate column $header[$i]\n" if exists $pos{$header[$i]};
  $pos{$header[$i]}=$i;
}
for my $i (0..$#old) {
  die "previous-schema mismatch at column ".($i+1)."\n"
    unless defined $header[$i] && $header[$i] eq $old[$i];
}
my (@rows,@ids,%seen,@conflicts);
my $line=1;
while (my $raw=<$in>) {
  ++$line; my @row=parse_csv($raw);
  die "column-count mismatch at line $line\n" unless @row==@header;
  my $id=$row[$pos{record_id}]; push @ids,$id;
  push @conflicts,"duplicate stable ID $id" if $seen{$id}++;
  for my $f (@new) {
    next unless exists $pos{$f} && exists $allowed{$f};
    my $v=$row[$pos{$f}];
    unless (allowed_value($f,$v)) {
      push @conflicts,
        "record_id=$id; field=$f; value=`$v`; permitted=`$permitted{$f}`";
    }
  }
  push @rows,\@row;
}
close $in;
if (@conflicts) {
  write_report($report,"# Phase 1 Corpus Migration Report\n\n"
    ."- Input: `$input`\n- Replacement performed: no\n"
    ."- Validation conflicts:\n".join("\n",map{"- $_"}@conflicts)."\n"
    ."- Curated values moved or normalized: no\n");
  die "validation conflicts detected; no output or replacement written: "
    .join('; ',@conflicts)."\n";
}
my @added;
for my $f (@new) {
  next if exists $pos{$f};
  $pos{$f}=@header; push @header,$f; push @added,$f;
  push @$_,$default{$f} for @rows;
}
die "stable IDs lost or duplicated\n" unless @ids==@rows && keys(%seen)==@rows;

my $stamp=strftime('%Y%m%dT%H%M%SZ',gmtime);
my $tmp=$apply ? "$input.migration.tmp" : ($output // "$input.migrated");
open my $out,'>:encoding(UTF-8)',$tmp or die "$tmp: $!";
print $out join(',',map{quote_csv($_)}@header),"\n";
print $out join(',',map{quote_csv($_)}@$_),"\n" for @rows;
close $out or die "$tmp: $!";

my $backup='not created (fixture/output mode)';
if ($apply) {
  my $dir='audit/migrations/backups'; make_path($dir);
  $backup="$dir/papers.$stamp.csv";
  my $suffix=1;
  $backup="$dir/papers.$stamp.$suffix.csv",++$suffix while -e $backup;
  copy($input,$backup) or die "backup failed: $!";
  # The output was built in input order; re-check its IDs before replacement.
  open my $check,'<:encoding(UTF-8)',$tmp or die $!;
  my @h2=parse_csv(scalar <$check>); my @ids2;
  while (my $raw=<$check>) {
    my @r=parse_csv($raw); push @ids2,$r[$pos{record_id}];
  }
  close $check;
  die "row count or order changed; no replacement\n"
    unless @ids2==@ids && join("\0",@ids2) eq join("\0",@ids);
  rename $tmp,$input or die "replacement failed: $!";
}
my $fields=@added ? join(', ',map{"`$_`"}@added) : 'None';
my $defaults=@added
  ? join("\n",map{"- `$_`: `$default{$_}` inserted in ".scalar(@rows)." rows"}@added)
  : '- None; target fields already existed.';
my $unchanged=scalar(@rows);
write_report($report,<<"REPORT");
# Phase 1 Corpus Migration Report

- Timestamp (UTC): $stamp
- Input: `$input`
- Rows before/after: @{[scalar @rows]} / @{[scalar @rows]}
- Stable IDs and row order preserved: yes
- Backup: `$backup`
- Fields added: $fields
- Fields transformed:
- None; curated values are never semantically realigned or normalized.
- Defaults inserted:
$defaults
- Conflicts: None.
- Records unchanged: $unchanged
- Records requiring manual review:
- None.
- Unknown columns: preserved in their original order.
REPORT
print "migrated ".scalar(@rows)." rows; added ".scalar(@added)." fields; backup=$backup\n";
