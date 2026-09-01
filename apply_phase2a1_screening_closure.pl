#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));

# Apply explicit paper-level Phase 2A.1 decisions to the occurrence ledger.
#
# Fail-closed rules:
# - no disposition is inferred from priority, workstream, or value semantics;
# - deferred/false-positive decisions must be supplied in the scoped ledger;
# - an unmapped unresolved record remains unchanged;
# - a mapped record in an unexpected curated state aborts before replacement;
# - every actual transition is recorded in the change log;
# - repeated execution is idempotent.

my $screening_path = $ENV{PHASE2_SCREENING_PATH}
  // 'audit/phase2_screening.csv';
my $triage_path = $ENV{PHASE2_TRIAGE_PATH}
  // 'audit/phase2_unresolved_triage.csv';
my $deferred_path = $ENV{PHASE2_DEFERRED_PATH}
  // 'audit/phase2a1_deferred_records.csv';
my $change_log_path = $ENV{PHASE2_CLOSURE_CHANGE_LOG_PATH}
  // 'audit/phase2a1_closure_change_log.csv';
my $papers_path = $ENV{PHASE2_PAPERS_PATH}
  // 'corpus/papers.csv';
my $expected_triage_rows = $ENV{PHASE2_EXPECTED_TRIAGE_ROWS} // 241;
my $expected_triage_occurrences =
  $ENV{PHASE2_EXPECTED_TRIAGE_OCCURRENCES} // 264;
my $expected_deferred_rows =
  $ENV{PHASE2_EXPECTED_DEFERRED_ROWS} // 229;
my $change_date = $ENV{PHASE2_CLOSURE_CHANGE_DATE} // '2026-07-31';

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
    my %seen_header;
    die "$path has a duplicate header field\n"
      if grep { $seen_header{$_}++ } @header;
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

sub require_fields {
    my ($path, $header, @required) = @_;
    my %present = map { $_ => 1 } @$header;
    my @missing = grep { !$present{$_} } @required;
    die "$path is missing required fields: @missing\n" if @missing;
}

sub write_csv_temporary {
    my ($path, $header, $rows) = @_;
    my $temporary = "$path.tmp.$$";
    open my $out, '>:encoding(UTF-8)', $temporary
      or die "$temporary: $!\n";
    print {$out} join(',', map { csv_quote($_) } @$header), "\n";
    for my $row (@$rows) {
        print {$out}
          join(',', map { csv_quote($row->{$_}) } @$header), "\n";
    }
    close $out or die "$temporary: $!\n";

    my ($check_header, $check_rows) = read_csv($temporary);
    die "$temporary header changed\n"
      unless join("\0", @$check_header) eq join("\0", @$header);
    die "$temporary row count changed\n"
      unless @$check_rows == @$rows;
    return ($temporary, $check_rows);
}

sub canonical_doi {
    my ($value) = @_;
    $value //= '';
    $value =~ s/^\s+|\s+$//g;
    $value =~ s{^https?://(?:dx\.)?doi\.org/}{}i;
    return '' if $value eq '' || lc($value) eq 'nr';
    return lc $value;
}

my %scoped_state = map { $_ => 1 } qw(
  DEFERRED_RELEVANT_SUPPORTING
  DEFERRED_RELEVANT_ADJACENT
  OUT_OF_SCOPE_FOR_PHASE2A1
  FALSE_POSITIVE_CONFIRMED
);
my %final_state = map { $_ => 1 } (
    keys(%scoped_state),
    qw(FULL_TEXT_INCLUDED FULL_TEXT_EXCLUDED FULL_TEXT_UNAVAILABLE DUPLICATE),
);
my %evidence_level = map { $_ => 1 } qw(
  LEVEL_1_LOAD_BEARING LEVEL_2_SUPPORTING LEVEL_3_DISCOVERY_ONLY
);

my ($screen_header, $screen_rows) = read_csv($screening_path);
require_fields(
    $screening_path, $screen_header,
    qw(phase2_record_id screening_state exclusion_reason evidence_level
       final_record_id notes)
);
my ($triage_header, $triage_rows) = read_csv($triage_path);
require_fields(
    $triage_path, $triage_header,
    qw(unique_record_id title authors year doi_or_identifier
       source_occurrence_count workstream candidate_gap_affected
       methodological_family likely_load_bearing current_evidence_depth
       full_text_access_status final_disposition exclusion_reason
       evidence_location notes)
);
my ($deferred_header, $deferred_rows) = read_csv($deferred_path);
require_fields(
    $deferred_path, $deferred_header,
    qw(unique_record_id title authors year doi_or_identifier
       source_occurrence_ids source_occurrence_count
       original_phase2_screening_state original_phase2_evidence_level
       phase2a1_scoped_disposition broader_review_relevance
       disposition_reason eligible_for_later_synthesis
       current_evidence_depth full_text_access_status likely_load_bearing
       methodological_family candidate_gap_affected evidence_location notes)
);

die "triage row count " . scalar(@$triage_rows)
  . " != expected $expected_triage_rows\n"
  unless @$triage_rows == $expected_triage_rows;
die "deferred-ledger row count " . scalar(@$deferred_rows)
  . " != expected $expected_deferred_rows\n"
  unless @$deferred_rows == $expected_deferred_rows;

my %screen_by_id;
my @screen_order;
for my $row (@$screen_rows) {
    my $id = $row->{phase2_record_id};
    die "blank phase2_record_id\n" unless length $id;
    die "duplicate phase2_record_id $id\n" if exists $screen_by_id{$id};
    $screen_by_id{$id} = $row;
    push @screen_order, $id;
}

my %mapping_for;
for my $row (@$deferred_rows) {
    my $uid = $row->{unique_record_id} // '';
    die "$deferred_path contains a blank unique_record_id\n"
      unless length $uid;
    die "$deferred_path repeats $uid\n" if exists $mapping_for{$uid};
    my $target = $row->{phase2a1_scoped_disposition} // '';
    die "$deferred_path:$uid has invalid scoped disposition '$target'\n"
      unless $scoped_state{$target}
          || $target eq 'FULL_TEXT_EXCLUDED'
          || $target eq 'FULL_TEXT_UNAVAILABLE';
    die "$deferred_path:$uid does not preserve the original "
      . "TITLE_ABSTRACT_INCLUDED state\n"
      unless ($row->{original_phase2_screening_state} // '')
          eq 'TITLE_ABSTRACT_INCLUDED';
    die "$deferred_path:$uid has an invalid original evidence level\n"
      unless $evidence_level{$row->{original_phase2_evidence_level} // ''};
    my $reason = $row->{disposition_reason} // '';
    die "$deferred_path:$uid lacks an explicit scoped-disposition reason\n"
      unless length($reason) && $reason ne 'NA';
    if ($target eq 'FALSE_POSITIVE_CONFIRMED') {
        die "$deferred_path:$uid has no record-level false-positive reason\n"
          unless length($reason) > 80
              && ($row->{broader_review_relevance} // '')
                    eq 'NOT_RELEVANT_TO_ANY_REVIEW_QUESTION'
              && ($row->{eligible_for_later_synthesis} // '') eq 'no';
    }
    elsif ($scoped_state{$target}) {
        die "$deferred_path:$uid incorrectly excludes a deferred record "
          . "from later qualified synthesis\n"
          unless ($row->{eligible_for_later_synthesis} // '')
                    eq 'yes_qualified_only';
    }
    $mapping_for{$uid} = $row;
}

my (undef, $paper_rows) = read_csv($papers_path);
my %paper_for_doi;
for my $paper (@$paper_rows) {
    my $doi = canonical_doi($paper->{doi});
    next unless length $doi;
    die "duplicate paper DOI $doi\n" if exists $paper_for_doi{$doi};
    $paper_for_doi{$doi} = $paper->{record_id};
}

my %triage_for;
my %group_for_occurrence;
my $triage_occurrence_total = 0;
my @triage_order;
my @triage_transitions;
for my $row (@$triage_rows) {
    my $uid = $row->{unique_record_id} // '';
    die "blank unique_record_id in $triage_path\n" unless length $uid;
    die "duplicate unique_record_id $uid\n" if exists $triage_for{$uid};
    $triage_for{$uid} = $row;
    push @triage_order, $uid;

    my ($occurrence_text) = ($row->{notes} // '') =~ /Occurrences=([^.]+)\./;
    die "$uid lacks an exact Occurrences=... note\n"
      unless defined $occurrence_text && length $occurrence_text;
    my @occurrences = split /;/, $occurrence_text;
    die "$uid occurrence count mismatch\n"
      unless ($row->{source_occurrence_count} // '') =~ /^\d+$/
          && $row->{source_occurrence_count} == @occurrences;
    $triage_occurrence_total += @occurrences;

    my $mapping = $mapping_for{$uid};
    if ($mapping) {
        for my $field (qw(
          title authors year doi_or_identifier source_occurrence_count
          current_evidence_depth full_text_access_status likely_load_bearing
          methodological_family candidate_gap_affected evidence_location
        )) {
            my $left = $row->{$field} // '';
            my $right = $mapping->{$field} // '';
            die "$uid mapping conflict for $field: triage='$left' "
              . "mapping='$right'\n"
              unless $left eq $right;
        }
        die "$uid mapping occurrence IDs do not match triage\n"
          unless ($mapping->{source_occurrence_ids} // '')
              eq join(';', @occurrences);
    }

    my $current = $row->{final_disposition} // '';
    my $desired;
    if ($mapping) {
        $desired = $mapping->{phase2a1_scoped_disposition};
        if ($current ne $desired) {
            die "$uid has unexpected curated triage disposition '$current'; "
              . "expected legacy FALSE_POSITIVE or '$desired'\n"
              unless $current eq 'FALSE_POSITIVE';
            push @triage_transitions, {
                uid => $uid,
                previous => $current,
                desired => $desired,
            };
            $row->{final_disposition} = $desired;
            $row->{exclusion_reason} = $mapping->{disposition_reason};
            my $marker =
              "Phase 2A.1 scoped-repair correction ($change_date): "
              . "automatic FALSE_POSITIVE closure superseded by "
              . "$desired; original broader-review relevance preserved.";
            $row->{notes} = length($row->{notes} // '')
              ? "$row->{notes} $marker"
              : $marker;
        }
        else {
            die "$uid scoped disposition reason conflicts with its "
              . "explicit mapping\n"
              unless ($row->{exclusion_reason} // '')
                  eq ($mapping->{disposition_reason} // '');
        }
    }
    elsif ($current eq 'FULL_TEXT_INCLUDED') {
        # Existing primary full-text decisions are explicit triage decisions,
        # not inferred closure states.
        $desired = $current;
    }
    elsif ($current eq 'UNRESOLVED') {
        # No explicit mapping means no change.
        next;
    }
    elsif ($current eq 'FALSE_POSITIVE') {
        die "$uid has a legacy FALSE_POSITIVE but no explicit scoped mapping\n";
    }
    else {
        # Other unmapped states are left unchanged by rule.
        next;
    }

    die "$uid has invalid explicit target '$desired'\n"
      unless $final_state{$desired};
    $row->{_desired} = $desired;
    $row->{_mapping} = $mapping;

    if ($desired eq 'FULL_TEXT_INCLUDED') {
        my ($corpus_id) = ($row->{notes} // '') =~
          /(?:Existing corpus ID\(s\)|Final corpus ID)=([PS]\d{4})/;
        if (!defined $corpus_id) {
            my $doi = canonical_doi($row->{doi_or_identifier});
            die "$uid is FULL_TEXT_INCLUDED without a canonical DOI\n"
              unless length $doi;
            $corpus_id = $paper_for_doi{$doi};
            die "$uid is FULL_TEXT_INCLUDED but DOI $doi is absent from "
              . "$papers_path\n"
              unless defined $corpus_id;
        }
        $row->{_corpus_id} = $corpus_id;
    }

    for my $index (0 .. $#occurrences) {
        my $occurrence = $occurrences[$index];
        die "$uid names unknown occurrence $occurrence\n"
          unless exists $screen_by_id{$occurrence};
        die "occurrence $occurrence is assigned to two triage records\n"
          if exists $group_for_occurrence{$occurrence};
        $group_for_occurrence{$occurrence} = {
            uid => $uid,
            index => $index,
            canonical => $occurrences[0],
            triage => $row,
        };
    }
}

die "triage occurrence count $triage_occurrence_total "
  . "!= expected $expected_triage_occurrences\n"
  unless $triage_occurrence_total == $expected_triage_occurrences;
for my $uid (sort keys %mapping_for) {
    die "$deferred_path names unknown triage record $uid\n"
      unless exists $triage_for{$uid};
}

my @screen_transitions;
for my $occurrence (@screen_order) {
    my $entry = $group_for_occurrence{$occurrence} or next;
    my $row = $screen_by_id{$occurrence};
    my $triage = $entry->{triage};
    my $desired = $entry->{index} > 0 ? 'DUPLICATE' : $triage->{_desired};
    my $current = $row->{screening_state} // '';
    next if !defined $desired;

    if ($current eq $desired) {
        if ($entry->{index} == 0 && $triage->{_mapping}) {
            my $mapping = $triage->{_mapping};
            die "$occurrence evidence level conflicts with explicit mapping\n"
              unless ($desired eq 'FALSE_POSITIVE_CONFIRMED'
                  ? $row->{evidence_level} eq 'LEVEL_3_DISCOVERY_ONLY'
                  : $row->{evidence_level}
                      eq $mapping->{original_phase2_evidence_level});
            die "$occurrence reason conflicts with explicit mapping\n"
              unless ($row->{exclusion_reason} // '')
                  eq ($mapping->{disposition_reason} // '');
        }
        next;
    }

    my $allowed_transition =
         $current eq 'TITLE_ABSTRACT_INCLUDED'
      || ($entry->{index} == 0
          && $current eq 'FALSE_POSITIVE'
          && $triage->{_mapping}
          && $scoped_state{$desired});
    die "$occurrence has unexpected curated state '$current'; "
      . "refusing transition to '$desired'\n"
      unless $allowed_transition;

    my $previous = $current;
    $row->{screening_state} = $desired;
    if ($desired eq 'DUPLICATE') {
        $row->{exclusion_reason} =
          "DUPLICATE_PHASE2A1_OCCURRENCE_OF_$entry->{canonical}";
        $row->{evidence_level} = 'LEVEL_3_DISCOVERY_ONLY';
        $row->{final_record_id} = '';
    }
    elsif ($desired eq 'FULL_TEXT_INCLUDED') {
        $row->{exclusion_reason} = '';
        $row->{evidence_level} =
          ($triage->{likely_load_bearing} // '') =~
            /^(?:LOAD_BEARING|POTENTIALLY_LOAD_BEARING)$/
          ? 'LEVEL_1_LOAD_BEARING'
          : 'LEVEL_2_SUPPORTING';
        $row->{final_record_id} = $triage->{_corpus_id};
    }
    elsif ($desired eq 'FULL_TEXT_EXCLUDED'
           || $desired eq 'FULL_TEXT_UNAVAILABLE') {
        my $reason = $triage->{exclusion_reason} // '';
        die "$entry->{uid} $desired lacks an explicit reason\n"
          unless length($reason) && $reason ne 'NA';
        $row->{exclusion_reason} = $reason;
        $row->{evidence_level} = 'LEVEL_3_DISCOVERY_ONLY';
        $row->{final_record_id} = '';
    }
    elsif ($scoped_state{$desired}) {
        my $mapping = $triage->{_mapping};
        die "$entry->{uid} has no explicit mapping for $desired\n"
          unless $mapping;
        $row->{exclusion_reason} = $mapping->{disposition_reason};
        $row->{evidence_level} =
          $desired eq 'FALSE_POSITIVE_CONFIRMED'
          ? 'LEVEL_3_DISCOVERY_ONLY'
          : $mapping->{original_phase2_evidence_level};
        $row->{final_record_id} = '';
    }
    else {
        die "unsupported explicit transition target $desired\n";
    }

    my $marker = "Phase 2A.1 scoped repair ($change_date): "
      . "unique_record_id=$entry->{uid}; "
      . "state=$desired; no priority-based inference.";
    $row->{notes} = length($row->{notes} // '')
      ? "$row->{notes} $marker"
      : $marker;
    push @screen_transitions, {
        uid => $entry->{uid},
        occurrence => $occurrence,
        previous => $previous,
        desired => $desired,
        reason => $row->{exclusion_reason},
    };
}

my @after_screen_order = map { $_->{phase2_record_id} } @$screen_rows;
die "screening stable-ID order changed before write\n"
  unless join("\0", @after_screen_order) eq join("\0", @screen_order);
my @after_triage_order = map { $_->{unique_record_id} } @$triage_rows;
die "triage stable-ID order changed before write\n"
  unless join("\0", @after_triage_order) eq join("\0", @triage_order);

my @change_header = qw(
  change_id change_date unique_record_id phase2_record_id artifacts_changed
  previous_state new_state reason mapping_source status
);
my ($existing_change_header, $change_rows);
if (-e $change_log_path) {
    ($existing_change_header, $change_rows) = read_csv($change_log_path);
    die "$change_log_path header is incompatible\n"
      unless join("\0", @$existing_change_header) eq join("\0", @change_header);
}
else {
    $existing_change_header = \@change_header;
    $change_rows = [];
}
my %logged_transition;
my $max_change = 0;
for my $row (@$change_rows) {
    my $id = $row->{change_id} // '';
    die "$change_log_path has invalid change ID '$id'\n"
      unless $id =~ /^P2A1-CLOSURE-(\d{4})$/;
    $max_change = $1 if $1 > $max_change;
    my $key = join("\0",
        $row->{phase2_record_id} // '',
        $row->{previous_state} // '',
        $row->{new_state} // '');
    die "$change_log_path repeats a transition for "
      . ($row->{phase2_record_id} // '') . "\n"
      if exists $logged_transition{$key};
    $logged_transition{$key} = 1;
}

my %triage_changed_for =
  map { $_->{uid} => 1 } @triage_transitions;
my $new_log_rows = 0;
for my $transition (@screen_transitions) {
    my $key = join("\0",
        $transition->{occurrence},
        $transition->{previous},
        $transition->{desired});
    next if $logged_transition{$key};
    push @$change_rows, {
        change_id => sprintf('P2A1-CLOSURE-%04d', ++$max_change),
        change_date => $change_date,
        unique_record_id => $transition->{uid},
        phase2_record_id => $transition->{occurrence},
        artifacts_changed =>
          $triage_changed_for{$transition->{uid}}
          ? 'audit/phase2_screening.csv;audit/phase2_unresolved_triage.csv'
          : 'audit/phase2_screening.csv',
        previous_state => $transition->{previous},
        new_state => $transition->{desired},
        reason => $transition->{reason},
        mapping_source => $deferred_path,
        status => 'APPLIED',
    };
    $logged_transition{$key} = 1;
    ++$new_log_rows;
}

# A triage transition normally has a matching canonical occurrence
# transition. Refuse to leave an unlogged triage-only mutation.
my %screen_changed_for = map { $_->{uid} => 1 } @screen_transitions;
for my $transition (@triage_transitions) {
    die "$transition->{uid} triage transition has no screening transition\n"
      unless $screen_changed_for{$transition->{uid}};
}

my $changes = @screen_transitions + @triage_transitions;
if (!$changes) {
    print "Phase 2A.1 scoped closure already applied; no files changed\n";
    exit 0;
}

# All conflicts have been checked. Write and validate every temporary before
# replacing either curated ledger.
my ($screen_temporary, $screen_check_rows) =
  write_csv_temporary($screening_path, $screen_header, $screen_rows);
my ($triage_temporary, $triage_check_rows) =
  write_csv_temporary($triage_path, $triage_header, $triage_rows);
my ($log_temporary, $log_check_rows) =
  write_csv_temporary($change_log_path, \@change_header, $change_rows);

my @screen_check_order =
  map { $_->{phase2_record_id} } @$screen_check_rows;
die "temporary screening stable-ID order changed\n"
  unless join("\0", @screen_check_order) eq join("\0", @screen_order);
my @triage_check_order =
  map { $_->{unique_record_id} } @$triage_check_rows;
die "temporary triage stable-ID order changed\n"
  unless join("\0", @triage_check_order) eq join("\0", @triage_order);

rename $screen_temporary, $screening_path
  or die "rename $screen_temporary -> $screening_path: $!\n";
rename $triage_temporary, $triage_path
  or die "rename $triage_temporary -> $triage_path: $!\n";
rename $log_temporary, $change_log_path
  or die "rename $log_temporary -> $change_log_path: $!\n";

my %state_count;
$state_count{$_->{screening_state}}++ for @$screen_rows;
print "Phase 2A.1 explicit scoped closure applied: "
  . "screening_transitions=" . scalar(@screen_transitions)
  . " triage_transitions=" . scalar(@triage_transitions)
  . " new_change_log_rows=$new_log_rows\n";
print "states ",
  join(' ', map { "$_=$state_count{$_}" } sort keys %state_count), "\n";
