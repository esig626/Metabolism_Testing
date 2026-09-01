#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));

# Append the separately curated Phase 2A.1 row proposal to papers.csv without
# regenerating or transforming any existing row. The operation is
# deterministic, idempotent, and fails before replacement on any ID, order,
# header, DOI, or row-count conflict.

my $corpus_path   = 'corpus/papers.csv';
my $proposal_path = 'audit/phase2a1_corpus_row_proposals.csv';

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

sub read_csv_lines {
    my ($path) = @_;
    open my $fh, '<:encoding(UTF-8)', $path or die "$path: $!\n";
    my @lines = <$fh>;
    close $fh or die "$path: $!\n";
    die "$path is empty\n" unless @lines;

    my @header = parse_csv_line($lines[0]);
    my %seen_header;
    die "$path has duplicate header fields\n"
      if grep { $seen_header{$_}++ } @header;

    my @rows;
    for my $index (1 .. $#lines) {
        my @values = parse_csv_line($lines[$index]);
        die "$path:" . ($index + 1) . " column count mismatch\n"
          unless @values == @header;
        my %row;
        @row{@header} = @values;
        push @rows, \%row;
    }
    return (\@header, \@rows, \@lines);
}

sub canonical_doi {
    my ($value) = @_;
    $value //= '';
    $value =~ s/^\s+|\s+$//g;
    $value =~ s{^https?://(?:dx\.)?doi\.org/}{}i;
    return '' if $value eq '' || lc($value) eq 'nr';
    return lc $value;
}

my ($corpus_header, $corpus_rows, $corpus_lines) =
  read_csv_lines($corpus_path);
my ($proposal_header, $proposal_rows, $proposal_lines) =
  read_csv_lines($proposal_path);

die "proposal header does not exactly match corpus header\n"
  unless join("\0", @$proposal_header) eq join("\0", @$corpus_header);

my @current_ids = map { $_->{record_id} } @$corpus_rows;
my @expected_existing =
  map { sprintf 'P%04d', $_ } 1 .. scalar(@$corpus_rows);
die "current corpus IDs are not complete and ordered\n"
  unless join("\0", @current_ids) eq join("\0", @expected_existing);

my @proposal_ids = map { $_->{record_id} } @$proposal_rows;
my @expected_proposal = map { sprintf 'P%04d', $_ } 52 .. 74;
die "proposal must contain exactly P0052 through P0074 in order\n"
  unless join("\0", @proposal_ids) eq join("\0", @expected_proposal);

if (@$corpus_rows == 74) {
    my @tail_ids = @current_ids[51 .. 73];
    die "existing Phase 2A.1 tail IDs conflict with proposal\n"
      unless join("\0", @tail_ids) eq join("\0", @proposal_ids);
    for my $offset (0 .. 22) {
        die "existing Phase 2A.1 row P"
          . sprintf('%04d', 52 + $offset)
          . " differs from curated proposal\n"
          unless $corpus_lines->[52 + $offset] eq
                 $proposal_lines->[1 + $offset];
    }
    print "Phase 2A.1 corpus rows already merged; no replacement performed\n";
    exit 0;
}

die "expected 51 existing corpus rows before append; found "
  . scalar(@$corpus_rows) . "\n"
  unless @$corpus_rows == 51;

my %seen_id;
my %seen_doi;
for my $row (@$corpus_rows, @$proposal_rows) {
    my $id = $row->{record_id};
    die "blank record_id\n" unless defined($id) && length($id);
    die "duplicate record_id $id\n" if $seen_id{$id}++;
    my $doi = canonical_doi($row->{doi});
    die "duplicate DOI $doi at $id and $seen_doi{$doi}\n"
      if length($doi) && exists $seen_doi{$doi};
    $seen_doi{$doi} = $id if length $doi;
}

my $temporary = "$corpus_path.tmp.$$";
open my $out, '>:encoding(UTF-8)', $temporary
  or die "$temporary: $!\n";
print {$out} $_ for @$corpus_lines;
print {$out} $proposal_lines->[$_] for 1 .. $#$proposal_lines;
close $out or die "$temporary: $!\n";

my ($check_header, $check_rows, $check_lines) =
  read_csv_lines($temporary);
die "temporary header changed\n"
  unless join("\0", @$check_header) eq join("\0", @$corpus_header);
die "temporary corpus row count is not 74\n"
  unless @$check_rows == 74;
my @check_ids = map { $_->{record_id} } @$check_rows;
my @expected_all = map { sprintf 'P%04d', $_ } 1 .. 74;
die "temporary stable IDs are lost, duplicated, or reordered\n"
  unless join("\0", @check_ids) eq join("\0", @expected_all);
for my $index (0 .. $#$corpus_lines) {
    die "existing corpus byte sequence changed at line " . ($index + 1) . "\n"
      unless $check_lines->[$index] eq $corpus_lines->[$index];
}

rename $temporary, $corpus_path
  or die "rename $temporary -> $corpus_path: $!\n";
print "Appended 23 curated Phase 2A.1 rows; papers.csv now has 74 records\n";
