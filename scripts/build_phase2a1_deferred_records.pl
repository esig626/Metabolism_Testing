#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));

# One-time, preservation-first construction of the explicit Phase 2A.1
# scoped-disposition ledger.  The output is curated evidence: this utility
# refuses to overwrite it.  In particular, this script never confirms a false
# positive.  A FALSE_POSITIVE_CONFIRMED decision must be entered in the output
# ledger by a curator together with a record-level reason.

my $triage_path = $ENV{PHASE2_TRIAGE_PATH}
  // 'audit/phase2_unresolved_triage.csv';
my $output_path = $ENV{PHASE2_DEFERRED_PATH}
  // 'audit/phase2a1_deferred_records.csv';
my $confirmation_path = $ENV{PHASE2_FALSE_POSITIVE_CONFIRMATIONS_PATH}
  // 'audit/phase2a1_false_positive_confirmations.csv';

die "$output_path already exists; refusing to overwrite curated dispositions\n"
  if -e $output_path;

my @source_paths = (
    'audit/phase2_screening_A.csv',
    'audit/phase2_screening_A_closure.csv',
    'audit/phase2_screening_root.csv',
    'audit/phase2_screening_B_audit.csv',
    'audit/phase2_screening_C.csv',
    'audit/phase2_screening_D_closure.csv',
    'audit/phase2_screening_E.csv',
);

sub parse_csv_line {
    my ($line) = @_;
    $line =~ s/\r?\n\z//;
    my @values;
    pos($line) = 0;
    while (pos($line) < length($line)) {
        if ($line =~ /\G"((?:[^"]|"")*)"(?:,|\z)/gc) {
            my $value = $1;
            $value =~ s/""/"/g;
            push @values, $value;
        }
        elsif ($line =~ /\G([^,]*)(?:,|\z)/gc) {
            push @values, $1;
        }
        else {
            die "CSV parse error near character " . (pos($line) // 0) . "\n";
        }
    }
    push @values, '' if $line =~ /,\z/;
    return @values;
}

sub csv_quote {
    my ($value) = @_;
    $value //= '';
    $value =~ s/"/""/g;
    return qq{"$value"};
}

sub read_csv {
    my ($path) = @_;
    open my $fh, '<:encoding(UTF-8)', $path or die "$path: $!\n";
    my $header_line = <$fh>;
    defined $header_line or die "$path is empty\n";
    my @header = parse_csv_line($header_line);
    my %seen;
    die "$path has a duplicate header field\n" if grep { $seen{$_}++ } @header;
    my @rows;
    my $line_number = 1;
    while (my $line = <$fh>) {
        ++$line_number;
        my @values = parse_csv_line($line);
        die "$path:$line_number column count mismatch\n"
          unless @values == @header;
        my %row;
        @row{@header} = @values;
        push @rows, \%row;
    }
    close $fh or die "$path: $!\n";
    return (\@header, \@rows);
}

sub first_present {
    my ($row, @names) = @_;
    for my $name (@names) {
        return $row->{$name} if exists $row->{$name};
    }
    return '';
}

my %source_by_occurrence;
for my $path (@source_paths) {
    my (undef, $rows) = read_csv($path);
    for my $row (@$rows) {
        my $id = first_present(
            $row, 'phase2_record_id', 'workstream_record_id', 'discovery_id'
        );
        die "$path contains a row without an occurrence ID\n"
          unless length $id;
        die "duplicate source occurrence ID $id\n"
          if exists $source_by_occurrence{$id};
        $source_by_occurrence{$id} = {
            state => first_present($row, 'screening_state'),
            level => first_present($row, 'evidence_level'),
        };
    }
}

my (undef, $triage_rows) = read_csv($triage_path);
my ($confirmation_header, $confirmation_rows) = read_csv($confirmation_path);
my %confirmation_field = map { $_ => 1 } @$confirmation_header;
for my $required (qw(unique_record_id record_level_reason status)) {
    die "$confirmation_path is missing required field $required\n"
      unless $confirmation_field{$required};
}
my %confirmation_for;
for my $row (@$confirmation_rows) {
    my $uid = $row->{unique_record_id} // '';
    die "$confirmation_path has a blank unique_record_id\n"
      unless length $uid;
    die "$confirmation_path repeats $uid\n"
      if exists $confirmation_for{$uid};
    die "$confirmation_path:$uid has invalid status '$row->{status}'\n"
      unless ($row->{status} // '') eq 'FALSE_POSITIVE_CONFIRMED';
    my $reason = $row->{record_level_reason} // '';
    die "$confirmation_path:$uid lacks a record-level reason\n"
      unless length($reason) > 40;
    $confirmation_for{$uid} = $row;
}
my @output_header = qw(
  unique_record_id title authors year doi_or_identifier source_occurrence_ids
  source_occurrence_count original_phase2_screening_state
  original_phase2_evidence_level phase2a1_scoped_disposition
  broader_review_relevance disposition_reason eligible_for_later_synthesis
  current_evidence_depth full_text_access_status likely_load_bearing
  methodological_family candidate_gap_affected evidence_location notes
);

my @output_rows;
my %uid_seen;
for my $row (@$triage_rows) {
    my $uid = $row->{unique_record_id} // '';
    die "blank unique_record_id in $triage_path\n" unless length $uid;
    die "duplicate unique_record_id $uid\n" if $uid_seen{$uid}++;

    my ($occurrence_text) = ($row->{notes} // '') =~ /Occurrences=([^.]+)\./;
    die "$uid lacks an exact Occurrences=... note\n"
      unless defined $occurrence_text && length $occurrence_text;
    my @occurrences = split /;/, $occurrence_text;
    die "$uid occurrence count mismatch\n"
      unless ($row->{source_occurrence_count} // '') =~ /^\d+$/
          && $row->{source_occurrence_count} == @occurrences;

    my %states;
    my %levels;
    my @source_levels;
    for my $occurrence (@occurrences) {
        my $source = $source_by_occurrence{$occurrence}
          or die "$uid refers to unknown source occurrence $occurrence\n";
        $states{$source->{state}}++;
        $levels{$source->{level}}++;
        push @source_levels, $source->{level};
    }
    die "$uid source occurrences do not all preserve "
      . "TITLE_ABSTRACT_INCLUDED\n"
      unless keys(%states) == 1 && exists $states{TITLE_ABSTRACT_INCLUDED};
    my $original_level = $source_levels[0];
    die "$uid canonical source occurrence has no evidence level\n"
      unless defined($original_level) && length($original_level);
    my $level_note = keys(%levels) == 1
      ? "All source occurrences preserved $original_level."
      : 'Source occurrence evidence levels were mixed ('
          . join(';', @source_levels)
          . "); the canonical occurrence's original level is preserved.";

    my $current = $row->{final_disposition} // '';
    next if $current eq 'FULL_TEXT_INCLUDED';

    my ($scoped, $broader, $reason, $eligible);
    if ($current eq 'FULL_TEXT_EXCLUDED') {
        $scoped = 'FULL_TEXT_EXCLUDED';
        $broader = 'ASSESSED_AND_EXCLUDED_AT_FULL_TEXT';
        $reason = $row->{exclusion_reason};
        $eligible = 'no';
    }
    elsif ($current eq 'FULL_TEXT_UNAVAILABLE') {
        $scoped = 'FULL_TEXT_UNAVAILABLE';
        $broader = 'RELEVANT_BUT_FULL_TEXT_UNAVAILABLE';
        $reason = $row->{exclusion_reason};
        $eligible = 'conditional_on_full_text';
    }
    elsif ($current eq 'FALSE_POSITIVE'
           || $current eq 'DEFERRED_RELEVANT_SUPPORTING'
           || $current eq 'DEFERRED_RELEVANT_ADJACENT'
           || $current eq 'OUT_OF_SCOPE_FOR_PHASE2A1'
           || $current eq 'FALSE_POSITIVE_CONFIRMED') {
        # The current FALSE_POSITIVE value is the known automatic closure
        # defect.  Restore relevance conservatively.  Confirmation of a true
        # false positive is deliberately impossible here.
        if (exists $confirmation_for{$uid}) {
            $scoped = 'FALSE_POSITIVE_CONFIRMED';
        }
        elsif ($current ne 'FALSE_POSITIVE') {
            $scoped = $current;
        }
        elsif (($row->{workstream} // '') =~ /(?:^|;)C(?:;|$)/) {
            $scoped = 'DEFERRED_RELEVANT_ADJACENT';
        }
        elsif (($row->{likely_load_bearing} // '') eq 'SUPPORTING') {
            $scoped = 'DEFERRED_RELEVANT_SUPPORTING';
        }
        else {
            $scoped = 'OUT_OF_SCOPE_FOR_PHASE2A1';
        }

        if ($scoped eq 'DEFERRED_RELEVANT_SUPPORTING') {
            $broader = 'RELEVANT_SUPPORTING';
            $reason =
              'DEFERRED_FROM_NARROW_GAP01_GAP03_REPAIR; '
              . 'ORIGINAL_BROADER_PHASE2_RELEVANCE_PRESERVED';
            $eligible = 'yes_qualified_only';
        }
        elsif ($scoped eq 'DEFERRED_RELEVANT_ADJACENT') {
            $broader = 'RELEVANT_ADJACENT';
            $reason =
              'ADJACENT_TO_BROADER_REVIEW_BUT_NOT_FULL_TEXT_PRIORITISED_FOR_'
              . 'NARROW_GAP01_GAP03_REPAIR';
            $eligible = 'yes_qualified_only';
        }
        elsif ($scoped eq 'OUT_OF_SCOPE_FOR_PHASE2A1') {
            $broader = 'RELEVANT_OUTSIDE_NARROW_REPAIR';
            $reason =
              'OUTSIDE_NARROW_GAP01_GAP03_REPAIR; '
              . 'NOT_EXCLUDED_FROM_BROADER_PHASE2_REVIEW';
            $eligible = 'yes_qualified_only';
        }
        elsif ($scoped eq 'FALSE_POSITIVE_CONFIRMED') {
            my $confirmation = $confirmation_for{$uid}
              or die "$uid is FALSE_POSITIVE_CONFIRMED without an explicit "
                . "confirmation record\n";
            $broader = 'NOT_RELEVANT_TO_ANY_REVIEW_QUESTION';
            $reason = $confirmation->{record_level_reason};
            $eligible = 'no';
        }
    }
    else {
        die "$uid has unexpected disposition '$current'\n";
    }

    die "$uid has no scoped disposition\n" unless defined $scoped;
    die "$uid has no record-level disposition reason\n"
      unless defined($reason) && length($reason) && $reason ne 'NA';

    my $scope_note = $scoped eq 'FALSE_POSITIVE_CONFIRMED'
      ? 'FALSE_POSITIVE_CONFIRMED is based on the separately preserved '
          . 'record-level scope decision and not on screening priority.'
      : 'Deferred records may provide qualified family-level context but '
          . 'cannot support definitive synthesis until full text is verified.';
    push @output_rows, {
        unique_record_id => $uid,
        title => $row->{title},
        authors => $row->{authors},
        year => $row->{year},
        doi_or_identifier => $row->{doi_or_identifier},
        source_occurrence_ids => join(';', @occurrences),
        source_occurrence_count => scalar(@occurrences),
        original_phase2_screening_state => 'TITLE_ABSTRACT_INCLUDED',
        original_phase2_evidence_level => $original_level,
        phase2a1_scoped_disposition => $scoped,
        broader_review_relevance => $broader,
        disposition_reason => $reason,
        eligible_for_later_synthesis => $eligible,
        current_evidence_depth => $row->{current_evidence_depth},
        full_text_access_status => $row->{full_text_access_status},
        likely_load_bearing => $row->{likely_load_bearing},
        methodological_family => $row->{methodological_family},
        candidate_gap_affected => $row->{candidate_gap_affected},
        evidence_location => $row->{evidence_location},
        notes =>
          'Explicit Phase 2A.1 scoped-disposition record. The original '
          . 'Phase 2 title/abstract relevance decision remains preserved. '
          . "$level_note "
          . $scope_note,
    };
}

for my $uid (sort keys %confirmation_for) {
    die "$confirmation_path names unknown or ineligible record $uid\n"
      unless $uid_seen{$uid};
}

die "expected 229 deferred/non-included records; found "
  . scalar(@output_rows) . "\n"
  unless @output_rows == 229;

my $temporary = "$output_path.tmp.$$";
open my $out, '>:encoding(UTF-8)', $temporary
  or die "$temporary: $!\n";
print {$out} join(',', map { csv_quote($_) } @output_header), "\n";
for my $row (@output_rows) {
    print {$out}
      join(',', map { csv_quote($row->{$_}) } @output_header), "\n";
}
close $out or die "$temporary: $!\n";

my (undef, $check_rows) = read_csv($temporary);
die "temporary deferred-ledger row count changed\n"
  unless @$check_rows == @output_rows;
rename $temporary, $output_path
  or die "rename $temporary -> $output_path: $!\n";

my %count;
$count{$_->{phase2a1_scoped_disposition}}++ for @output_rows;
print "created $output_path rows=", scalar(@output_rows), "\n";
print "states ",
  join(' ', map { "$_=$count{$_}" } sort keys %count), "\n";
