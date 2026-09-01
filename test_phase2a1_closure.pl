#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));
use Test::More;

sub parse_csv_row {
    my ($text) = @_;
    $text =~ s/\r?\n\z//;
    my @values;
    while (length $text) {
        if ($text =~ s/^"((?:[^"]|"")*)"(?:,|\z)//) {
            my $value = $1;
            $value =~ s/""/"/g;
            push @values, $value;
        }
        elsif ($text =~ s/^([^,]*)(?:,|\z)//) {
            push @values, $1;
        }
        else {
            die "CSV parse failure near: $text\n";
        }
    }
    return @values;
}

sub read_csv {
    my ($path) = @_;
    open my $fh, '<:encoding(UTF-8)', $path or die "$path: $!\n";
    my @header = parse_csv_row(scalar <$fh>);
    my @rows;
    my $line_number = 1;
    while (my $line = <$fh>) {
        ++$line_number;
        my @values = parse_csv_row($line);
        die "$path:$line_number column count mismatch\n"
          unless @values == @header;
        my %row;
        @row{@header} = @values;
        push @rows, \%row;
    }
    close $fh or die "$path: $!\n";
    return (\@header, \@rows);
}

my (undef, $papers) = read_csv('corpus/papers.csv');
is(scalar(@$papers), 74, 'paper corpus contains 74 stable rows');
is_deeply(
    [map { $_->{record_id} } @$papers],
    [map { sprintf 'P%04d', $_ } 1 .. 74],
    'P0001-P0074 remain complete and ordered'
);
my %paper = map { $_->{record_id} => $_ } @$papers;

my (undef, $triage) = read_csv('audit/phase2_unresolved_triage.csv');
is(scalar(@$triage), 241, '264 occurrences normalize to 241 unique records');
my %triage_id;
my %triage_state;
my $source_occurrences = 0;
for my $row (@$triage) {
    ok(!$triage_id{$row->{unique_record_id}}++,
       "unique triage ID $row->{unique_record_id}");
    $source_occurrences += $row->{source_occurrence_count};
    ++$triage_state{$row->{final_disposition}};
    isnt($row->{final_disposition}, 'UNRESOLVED',
          "$row->{unique_record_id} has a final disposition");
    if ($row->{final_disposition} eq 'FULL_TEXT_INCLUDED') {
        like($row->{notes}, qr/(?:Existing corpus ID\(s\)|Final corpus ID)=P\d{4}/,
             "$row->{unique_record_id} inclusion names a stable corpus ID");
        ok(length($row->{evidence_location}) > 20,
           "$row->{unique_record_id} inclusion has an exact location");
    }
    if ($row->{final_disposition} ne 'FULL_TEXT_INCLUDED') {
        ok(length($row->{exclusion_reason})
             && $row->{exclusion_reason} ne 'NA',
           "$row->{unique_record_id} non-inclusion has a reason");
    }
}
is($source_occurrences, 264, 'triage preserves all 264 source occurrences');
is_deeply(
    \%triage_state,
    {
        DEFERRED_RELEVANT_ADJACENT   => 95,
        DEFERRED_RELEVANT_SUPPORTING => 60,
        FALSE_POSITIVE_CONFIRMED     => 2,
        FULL_TEXT_EXCLUDED           => 2,
        FULL_TEXT_INCLUDED           => 12,
        FULL_TEXT_UNAVAILABLE        => 11,
        OUT_OF_SCOPE_FOR_PHASE2A1    => 59,
    },
    'paper-level final disposition counts are exact'
);

my (undef, $main) = read_csv('audit/phase2_screening.csv');
is(scalar(@$main), 1937, 'Phase 2 occurrence ledger row count is preserved');
my %main_state;
++ $main_state{$_->{screening_state}} for @$main;
is_deeply(
    \%main_state,
    {
        AWAITING_VERIFICATION         => 1,
        DEFERRED_RELEVANT_ADJACENT    => 95,
        DEFERRED_RELEVANT_SUPPORTING  => 60,
        DUPLICATE                     => 360,
        FALSE_POSITIVE_CONFIRMED      => 2,
        FULL_TEXT_EXCLUDED            => 2,
        FULL_TEXT_INCLUDED            => 51,
        FULL_TEXT_UNAVAILABLE         => 13,
        OUT_OF_SCOPE_FOR_PHASE2A1     => 59,
        TITLE_ABSTRACT_EXCLUDED => 1294,
    },
    'Phase 2 final occurrence-state counts are exact'
);
is($main_state{TITLE_ABSTRACT_INCLUDED} // 0, 0,
   'no title/abstract-included occurrence remains');

for my $row (@$main) {
    if ($row->{screening_state} eq 'FULL_TEXT_INCLUDED') {
        like($row->{final_record_id}, qr/^[PS]\d{4}$/,
             "$row->{phase2_record_id} inclusion maps to a stable corpus ID");
    }
    if ($row->{screening_state} eq 'FALSE_POSITIVE_CONFIRMED'
        || $row->{screening_state} eq 'FULL_TEXT_EXCLUDED'
        || $row->{screening_state} eq 'FULL_TEXT_UNAVAILABLE'
        || $row->{screening_state} eq 'DUPLICATE') {
        ok(length($row->{exclusion_reason})
             && $row->{exclusion_reason} ne 'NA',
           "$row->{phase2_record_id} final non-inclusion has a reason");
    }
}

my (undef, $deferred) =
  read_csv('audit/phase2a1_deferred_records.csv');
is(scalar(@$deferred), 229,
   'scoped ledger preserves all non-included/deferred unique records');
my %deferred_state;
my %deferred_id;
for my $row (@$deferred) {
    ok(!$deferred_id{$row->{unique_record_id}}++,
       "$row->{unique_record_id} occurs once in scoped ledger");
    ++$deferred_state{$row->{phase2a1_scoped_disposition}};
    is($row->{original_phase2_screening_state},
       'TITLE_ABSTRACT_INCLUDED',
       "$row->{unique_record_id} preserves its original Phase 2 state");
    if ($row->{phase2a1_scoped_disposition}
          eq 'FALSE_POSITIVE_CONFIRMED') {
        is($row->{broader_review_relevance},
           'NOT_RELEVANT_TO_ANY_REVIEW_QUESTION',
           "$row->{unique_record_id} has an explicit whole-review scope decision");
        ok(length($row->{disposition_reason}) > 80,
           "$row->{unique_record_id} has a record-level false-positive reason");
    }
    elsif ($row->{phase2a1_scoped_disposition} =~
             /^(?:DEFERRED_RELEVANT_|OUT_OF_SCOPE_FOR_PHASE2A1)/) {
        is($row->{eligible_for_later_synthesis}, 'yes_qualified_only',
           "$row->{unique_record_id} remains eligible for qualified synthesis");
    }
}
is_deeply(
    \%deferred_state,
    {
        DEFERRED_RELEVANT_ADJACENT    => 95,
        DEFERRED_RELEVANT_SUPPORTING  => 60,
        FALSE_POSITIVE_CONFIRMED      => 2,
        FULL_TEXT_EXCLUDED            => 2,
        FULL_TEXT_UNAVAILABLE         => 11,
        OUT_OF_SCOPE_FOR_PHASE2A1     => 59,
    },
    'scoped ledger disposition counts are exact'
);

my (undef, $change_log) =
  read_csv('audit/phase2a1_closure_change_log.csv');
is(scalar(@$change_log), 216,
   'every reversed automatic closure has one audit-log row');
my %changed_occurrence;
for my $row (@$change_log) {
    ok(!$changed_occurrence{$row->{phase2_record_id}}++,
       "$row->{phase2_record_id} has one correction entry");
    is($row->{previous_state}, 'FALSE_POSITIVE',
       "$row->{phase2_record_id} records the defective prior state");
    isnt($row->{new_state}, 'FALSE_POSITIVE',
          "$row->{phase2_record_id} is not automatically false-positive");
}

my (undef, $a1) = read_csv('audit/phase2a1_screening.csv');
is(scalar(@$a1), 959, 'Phase 2A.1 retains all prospective occurrences');
my %a1_state;
my $a1_inclusions = 0;
for my $row (@$a1) {
    ++$a1_state{$row->{screening_state}};
    unlike($row->{screening_state},
           qr/^(?:DISCOVERED_NOT_SCREENED|TITLE_ABSTRACT_INCLUDED|AWAITING_VERIFICATION)$/,
           "$row->{phase2a1_record_id} has a final state");
    if ($row->{screening_state} eq 'FULL_TEXT_INCLUDED') {
        ++$a1_inclusions;
        like($row->{final_record_id}, qr/^P\d{4}$/,
             "$row->{phase2a1_record_id} maps to the paper corpus");
        is($paper{$row->{final_record_id}}{full_text_inspected}, 'yes',
           "$row->{phase2a1_record_id} mapped paper is full-text inspected");
        ok(length($row->{evidence_location}) > 20,
           "$row->{phase2a1_record_id} retains an exact evidence location");
    }
}
is($a1_inclusions, 22, '22 unique foundational inclusions are mapped');
is_deeply(
    \%a1_state,
    {
        DUPLICATE             => 180,
        FALSE_POSITIVE        => 727,
        FULL_TEXT_INCLUDED    => 22,
        FULL_TEXT_UNAVAILABLE => 30,
    },
    'Phase 2A.1 occurrence-state counts are exact'
);

for my $path (
    'analyses/fixed_sample_composite_testing_foundations.md',
    'analyses/gap01_component_assessment.md',
    'analyses/gap03_converse_assessment.md',
) {
    open my $fh, '<:encoding(UTF-8)', $path or die "$path: $!\n";
    local $/;
    my $text = <$fh>;
    close $fh;
    unlike($text, qr/stable corpus ID assigned during root integration/i,
           "$path contains no unassigned-ID placeholder");
}

open my $gaps, '<:encoding(UTF-8)', 'synthesis/candidate_gaps.md'
  or die $!;
local $/;
my $gap_text = <$gaps>;
close $gaps;
like($gap_text, qr/GAP-01[\s\S]*?\*\*Status:\*\* \*\*WEAKENED\*\*/,
     'GAP-01 is weakened');
like($gap_text, qr/GAP-03[\s\S]*?\*\*Status:\*\* \*\*WEAKENED\*\*/,
     'GAP-03 is weakened');
unlike($gap_text, qr/\*\*SURVIVES FULL REVIEW\*\*/,
       'no full-review survival claim remains');

done_testing();
