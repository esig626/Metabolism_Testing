#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));

# Audit-only validator and summary for the prospective Phase 2 screening
# ledgers. It does not modify any input.

my @allowed_states = qw(
  DISCOVERED_NOT_SCREENED
  TITLE_ABSTRACT_INCLUDED
  TITLE_ABSTRACT_EXCLUDED
  FULL_TEXT_INCLUDED
  FULL_TEXT_EXCLUDED
  DUPLICATE
  FULL_TEXT_UNAVAILABLE
  AWAITING_VERIFICATION
  FALSE_POSITIVE
  DEFERRED_RELEVANT_SUPPORTING
  DEFERRED_RELEVANT_ADJACENT
  OUT_OF_SCOPE_FOR_PHASE2A1
  FALSE_POSITIVE_CONFIRMED
);
my %allowed_state = map { $_ => 1 } @allowed_states;
my @allowed_levels = qw(
  LEVEL_1_LOAD_BEARING
  LEVEL_2_SUPPORTING
  LEVEL_3_DISCOVERY_ONLY
);
my %allowed_level = map { $_ => 1 } @allowed_levels;

my @specs = (
  [A      => 'audit/phase2_screening_A.csv'],
  [A      => 'audit/phase2_screening_A_closure.csv'],
  [ROOT   => 'audit/phase2_screening_root.csv'],
  [B      => 'audit/phase2_screening_B_audit.csv'],
  [C      => 'audit/phase2_screening_C.csv'],
  [D      => 'audit/phase2_screening_D_closure.csv'],
  [E      => 'audit/phase2_screening_E.csv'],
  [MERGED => 'audit/phase2_screening.csv'],
);

sub parse_csv {
    my ($line) = @_;
    $line =~ s/\r?\n\z//;
    my @values;
    while (length $line) {
        if ($line =~ s/^"((?:[^"]|"")*)"(?:,|\z)//) {
            my $value = $1;
            $value =~ s/""/"/g;
            push @values, $value;
        }
        elsif ($line =~ s/^([^,]*)(?:,|\z)//) {
            push @values, $1;
        }
        else {
            die "CSV parse error near: $line\n";
        }
    }
    return @values;
}

sub first_present {
    my ($row, @names) = @_;
    for my $name (@names) {
        return $row->{$name} if exists $row->{$name};
    }
    return '';
}

my $errors = 0;
for my $spec (@specs) {
    my ($label, $path) = @$spec;
    next unless -e $path;
    open my $fh, '<:encoding(UTF-8)', $path or die "$path: $!\n";
    my @header = parse_csv(scalar <$fh>);
    my %state_count;
    my %level_count;
    my %query_count;
    my %workstream_count;
    my %groups;
    my %row_ids;
    my $rows = 0;
    my $ungrouped = 0;
    while (my $line = <$fh>) {
        $rows++;
        my @values = parse_csv($line);
        if (@values != @header) {
            warn "$path row $rows: expected " . scalar(@header)
              . " columns, found " . scalar(@values) . "\n";
            $errors++;
            next;
        }
        my %row;
        @row{@header} = @values;
        my $state = first_present(\%row, 'screening_state');
        my $level = first_present(\%row, 'evidence_level');
        my $query = first_present(\%row, 'query_id', 'search_id');
        my $reason = first_present(\%row, 'exclusion_reason');
        my $group = first_present(\%row, 'duplicate_group');
        my $id = first_present(
            \%row, 'phase2_record_id', 'workstream_record_id', 'discovery_id'
        );
        my $workstream = first_present(\%row, 'workstream');

        $state_count{$state}++;
        $level_count{$level}++;
        $query_count{$query}++;
        $workstream_count{$workstream}++ if length $workstream;
        if (length $group) {
            $groups{$group}++;
        }
        else {
            $ungrouped++;
        }
        if (length $id && $row_ids{$id}++) {
            warn "$path row $rows: duplicate occurrence ID $id\n";
            $errors++;
        }
        unless ($allowed_state{$state}) {
            warn "$path row $rows: invalid screening_state '$state'\n";
            $errors++;
        }
        unless ($allowed_level{$level}) {
            warn "$path row $rows: invalid evidence_level '$level'\n";
            $errors++;
        }
        unless ($query =~ /^PHASE2-SEARCH-\d{4}$/) {
            warn "$path row $rows: invalid or missing query ID '$query'\n";
            $errors++;
        }
        if (($state eq 'TITLE_ABSTRACT_EXCLUDED'
                || $state eq 'FULL_TEXT_EXCLUDED'
                || $state eq 'FULL_TEXT_UNAVAILABLE'
                || $state eq 'FALSE_POSITIVE'
                || $state eq 'FALSE_POSITIVE_CONFIRMED')
            && (!length($reason) || $reason eq 'NA')) {
            warn "$path row $rows: prospective exclusion lacks a reason\n";
            $errors++;
        }
        if (($state eq 'DEFERRED_RELEVANT_SUPPORTING'
                || $state eq 'DEFERRED_RELEVANT_ADJACENT'
                || $state eq 'OUT_OF_SCOPE_FOR_PHASE2A1')
            && (!length($reason) || $reason eq 'NA')) {
            warn "$path row $rows: scoped disposition lacks a reason\n";
            $errors++;
        }
        if ($state eq 'DUPLICATE'
            && (!length($reason) || $reason eq 'NA')) {
            warn "$path row $rows: duplicate lacks a reason\n";
            $errors++;
        }
        if ($line =~ /(?:Ã|Â|ÄŸ|â€|â€™|â€“|ï¿½|\x{FFFD})/) {
            warn "$path row $rows: possible UTF-8 mojibake\n";
            $errors++;
        }
    }
    close $fh or die "$path: $!\n";

    print "$label\t$path\trows=$rows"
      . "\tgroups=" . scalar(keys %groups)
      . "\tungrouped=$ungrouped\n";
    print "  states "
      . join(' ', map { "$_=$state_count{$_}" } sort keys %state_count)
      . "\n";
    print "  levels "
      . join(' ', map { "$_=$level_count{$_}" } sort keys %level_count)
      . "\n";
    print "  queries "
      . join(' ', map { "$_=$query_count{$_}" } sort keys %query_count)
      . "\n";
    if (%workstream_count) {
        print "  workstreams "
          . join(' ', map { "$_=$workstream_count{$_}" }
              sort keys %workstream_count)
          . "\n";
    }
}

die "Phase 2 audit validation failed with $errors error(s)\n" if $errors;
print "Phase 2 audit validation passed\n";
