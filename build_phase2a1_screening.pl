#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use open qw(:std :encoding(UTF-8));
use Unicode::Normalize qw(NFKC);

# Deterministically consolidate the independently curated Phase 2A.1
# occurrence ledgers.  The source ledgers are inputs and are never rewritten.
# Cross-workstream duplicate detection is deliberately conservative:
# normalized DOI first, then an exact Unicode-normalized title only when both
# records have no DOI and have identical nonblank authors and year.

my @source_specs = (
    {
        code       => 'AC',
        workstream => 'A-C',
        path       => 'audit/phase2a1_screening_AC.csv',
    },
    {
        code       => 'DEF',
        workstream => 'D-F',
        path       => 'audit/phase2a1_screening_DEF.csv',
    },
);
my $output_path = 'audit/phase2a1_screening.csv';

my @source_header = qw(
  phase2a1_record_id query_id search_date search_source title authors year
  doi_or_identifier source_native_id duplicate_group screening_state
  exclusion_reason evidence_depth full_text_access_status evidence_location
  proposed_corpus_record raw_snapshot notes
);

my @output_header = qw(
  phase2a1_record_id workstream_families query_id search_date search_source
  title authors year doi_or_identifier source_native_id duplicate_group
  canonical_record_id deduplication_basis source_ledger source_duplicate_group
  source_screening_state screening_state source_exclusion_reason
  exclusion_reason evidence_depth full_text_access_status evidence_location
  final_record_id corpus_action source_proposed_corpus_record raw_snapshot
  notes
);

my %allowed_state = map { $_ => 1 } qw(
  FULL_TEXT_INCLUDED FULL_TEXT_EXCLUDED FULL_TEXT_UNAVAILABLE DUPLICATE
  FALSE_POSITIVE
);
my %allowed_depth = map { $_ => 1 } qw(
  LEVEL_1_LOAD_BEARING LEVEL_2_SUPPORTING LEVEL_3_DISCOVERY_ONLY
);
my %state_rank = (
    FULL_TEXT_INCLUDED    => 0,
    FULL_TEXT_EXCLUDED    => 1,
    FULL_TEXT_UNAVAILABLE => 2,
    FALSE_POSITIVE        => 3,
    DUPLICATE             => 4,
);

sub parse_csv_row {
    my ($text) = @_;
    defined $text or die "Unexpected end of CSV\n";
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

sub csv_quote {
    my ($value) = @_;
    $value //= '';
    $value =~ s/"/""/g;
    return qq{"$value"};
}

sub normalize_doi {
    my ($value) = @_;
    $value //= '';
    $value = lc NFKC($value);
    $value =~ s/^\s+|\s+$//g;
    $value =~ s{^https?://(?:dx\.)?doi\.org/}{};
    # arXiv's stable identifier and its DataCite DOI identify the same
    # primary preprint. This explicit normalization is syntactic, not an
    # inferred title match.
    return "10.48550/arxiv.$1"
      if $value =~ /^arxiv:(\d{4}\.\d{4,5})(?:v\d+)?$/;
    return $value =~ /^10\.\d{4,9}\// ? $value : '';
}

sub normalize_exact_text {
    my ($value) = @_;
    $value //= '';
    $value = lc NFKC($value);
    $value =~ s/\s+/ /g;
    $value =~ s/^\s+|\s+$//g;
    return $value;
}

sub title_key_is_safe {
    my ($row) = @_;
    return 0 if normalize_doi($row->{doi_or_identifier}) ne '';
    my $title = normalize_exact_text($row->{title});
    my $authors = normalize_exact_text($row->{authors});
    my $year = normalize_exact_text($row->{year});
    return 0 if length($title) < 30;
    return 0 if scalar(grep { length } split / /, $title) < 4;
    return 0 if $authors eq '' || $year !~ /^\d{4}$/;
    return 1;
}

sub find_root {
    my ($parent, $index) = @_;
    my $root = $index;
    $root = $parent->[$root] while $parent->[$root] != $root;
    while ($parent->[$index] != $index) {
        my $next = $parent->[$index];
        $parent->[$index] = $root;
        $index = $next;
    }
    return $root;
}

sub union_sets {
    my ($parent, $rank, $a, $b) = @_;
    my $ra = find_root($parent, $a);
    my $rb = find_root($parent, $b);
    return if $ra == $rb;
    if ($rank->[$ra] < $rank->[$rb]) {
        $parent->[$ra] = $rb;
    }
    elsif ($rank->[$ra] > $rank->[$rb]) {
        $parent->[$rb] = $ra;
    }
    else {
        $parent->[$rb] = $ra;
        ++$rank->[$ra];
    }
}

my (%corpus_id, %corpus_doi, %corpus_citation);
{
    my $path = 'corpus/papers.csv';
    open my $fh, '<:encoding(UTF-8)', $path or die "$path: $!\n";
    my @header = parse_csv_row(scalar <$fh>);
    my %position;
    @position{@header} = 0 .. $#header;
    die "$path: missing record_id, full_citation or doi\n"
      unless exists $position{record_id}
      && exists $position{full_citation}
      && exists $position{doi};
    my $line_number = 1;
    while (my $line = <$fh>) {
        ++$line_number;
        my @values = parse_csv_row($line);
        die "$path:$line_number column mismatch\n"
          unless @values == @header;
        my $id = $values[$position{record_id}];
        die "$path:$line_number invalid paper ID '$id'\n"
          unless $id =~ /^P\d{4}$/;
        die "$path:$line_number duplicate paper ID '$id'\n"
          if $corpus_id{$id}++;
        $corpus_citation{$id} =
          normalize_exact_text($values[$position{full_citation}]);
        my $doi = normalize_doi($values[$position{doi}]);
        if ($doi ne '') {
            die "$path:$line_number duplicate corpus DOI '$doi'\n"
              if exists $corpus_doi{$doi};
            $corpus_doi{$doi} = $id;
        }
    }
    close $fh or die "$path: $!\n";
}

# Preserve a curator-assigned stable ID from an existing consolidated output.
# It must already exist in the paper corpus.  No other derived field is read
# back, so stale classifications cannot influence the deterministic rebuild.
my %preserved_final_record_id;
if (-e $output_path) {
    open my $fh, '<:encoding(UTF-8)', $output_path
      or die "$output_path: $!\n";
    my @header = parse_csv_row(scalar <$fh>);
    my %position;
    @position{@header} = 0 .. $#header;
    if (exists $position{phase2a1_record_id}
        && exists $position{final_record_id}) {
        my $line_number = 1;
        while (my $line = <$fh>) {
            ++$line_number;
            my @values = parse_csv_row($line);
            die "$output_path:$line_number column mismatch\n"
              unless @values == @header;
            my $id = $values[$position{phase2a1_record_id}];
            my $final = $values[$position{final_record_id}];
            next if $final eq '';
            die "$output_path:$line_number invalid final_record_id '$final'\n"
              unless $final =~ /^P\d{4}$/;
            die "$output_path:$line_number final_record_id '$final' "
              . "is absent from corpus/papers.csv\n"
              unless $corpus_id{$final};
            die "$output_path:$line_number conflicting repeated mapping for "
              . "$id\n"
              if exists $preserved_final_record_id{$id}
              && $preserved_final_record_id{$id} ne $final;
            $preserved_final_record_id{$id} = $final;
        }
    }
    close $fh or die "$output_path: $!\n";
}

my @rows;
my %occurrence_id;
for my $spec (@source_specs) {
    open my $fh, '<:encoding(UTF-8)', $spec->{path}
      or die "$spec->{path}: $!\n";
    my @header = parse_csv_row(scalar <$fh>);
    die "$spec->{path}: unexpected header\n"
      unless "@header" eq "@source_header";
    my $line_number = 1;
    while (my $line = <$fh>) {
        ++$line_number;
        my @values = parse_csv_row($line);
        die "$spec->{path}:$line_number column mismatch\n"
          unless @values == @header;
        my %row;
        @row{@header} = @values;
        $row{_source_ledger} = $spec->{code};
        $row{_workstream_families} = $spec->{workstream};
        $row{_source_order} = scalar @rows;

        die "$spec->{path}:$line_number duplicate occurrence ID "
          . "$row{phase2a1_record_id}\n"
          if $occurrence_id{$row{phase2a1_record_id}}++;
        die "$spec->{path}:$line_number invalid query ID '$row{query_id}'\n"
          unless $row{query_id} =~ /^PHASE2A1-SEARCH-\d{4}$/;
        die "$spec->{path}:$line_number invalid search date "
          . "'$row{search_date}'\n"
          unless $row{search_date} =~ /^\d{4}-\d{2}-\d{2}$/;
        die "$spec->{path}:$line_number invalid final screening state "
          . "'$row{screening_state}'\n"
          unless $allowed_state{$row{screening_state}};

        # DEF used this older spelling before consolidation.  This is a
        # declared schema-label normalization, not an evidence reclassification.
        $row{evidence_depth} = 'LEVEL_3_DISCOVERY_ONLY'
          if $row{evidence_depth} eq 'LEVEL_3_DISCOVERY';
        die "$spec->{path}:$line_number invalid evidence depth "
          . "'$row{evidence_depth}'\n"
          unless $allowed_depth{$row{evidence_depth}};

        if ($row{screening_state} =~
            /^(?:FULL_TEXT_EXCLUDED|FULL_TEXT_UNAVAILABLE|DUPLICATE|FALSE_POSITIVE)$/) {
            die "$spec->{path}:$line_number final disposition lacks reason\n"
              if $row{exclusion_reason} eq ''
              || $row{exclusion_reason} eq 'NA';
        }
        if ($row{screening_state} eq 'FULL_TEXT_INCLUDED') {
            die "$spec->{path}:$line_number inclusion lacks evidence location\n"
              if $row{evidence_location} eq '';
            die "$spec->{path}:$line_number discovery-only inclusion\n"
              if $row{evidence_depth} eq 'LEVEL_3_DISCOVERY_ONLY';
        }
        die "$spec->{path}:$line_number lacks raw snapshot provenance\n"
          if $row{raw_snapshot} eq '';
        die "$spec->{path}:$line_number raw snapshot does not exist: "
          . "$row{raw_snapshot}\n"
          unless -e $row{raw_snapshot};
        die "$spec->{path}:$line_number lacks source duplicate group\n"
          if $row{duplicate_group} eq '';

        push @rows, \%row;
    }
    close $fh or die "$spec->{path}: $!\n";
}

my @parent = (0 .. $#rows);
my @union_rank = (0) x scalar(@rows);
my %source_groups;
for my $index (0 .. $#rows) {
    my $row = $rows[$index];
    push @{$source_groups{
      "$row->{_source_ledger}\0$row->{duplicate_group}"
    }}, $index;
}
for my $indices (values %source_groups) {
    union_sets(\@parent, \@union_rank, $indices->[0], $_)
      for @$indices[1 .. $#$indices];
}

# Cross-workstream DOI joins.
my %doi_groups;
for my $index (0 .. $#rows) {
    my $doi = normalize_doi($rows[$index]{doi_or_identifier});
    push @{$doi_groups{$doi}}, $index if $doi ne '';
}
for my $indices (values %doi_groups) {
    my %ledgers = map { $rows[$_]{_source_ledger} => 1 } @$indices;
    next unless keys(%ledgers) > 1;
    union_sets(\@parent, \@union_rank, $indices->[0], $_)
      for @$indices[1 .. $#$indices];
}

# Cross-workstream exact-title joins.  The author and year restrictions avoid
# merging generic or reused titles, and DOI-bearing versions are deliberately
# kept distinct.
my %title_groups;
for my $index (0 .. $#rows) {
    next unless title_key_is_safe($rows[$index]);
    my $key = join "\0",
      normalize_exact_text($rows[$index]{title}),
      normalize_exact_text($rows[$index]{authors}),
      normalize_exact_text($rows[$index]{year});
    push @{$title_groups{$key}}, $index;
}
for my $indices (values %title_groups) {
    my %ledgers = map { $rows[$_]{_source_ledger} => 1 } @$indices;
    next unless keys(%ledgers) > 1;
    union_sets(\@parent, \@union_rank, $indices->[0], $_)
      for @$indices[1 .. $#$indices];
}

my %members;
push @{$members{find_root(\@parent, $_)}}, $_ for 0 .. $#rows;

# Stable global group ordering follows first occurrence order.  The canonical
# row is the strongest source disposition, then the first source occurrence.
my @roots = sort {
    $members{$a}[0] <=> $members{$b}[0]
} keys %members;
my (%group_id, %canonical, %basis);
my $group_serial = 0;
for my $root (@roots) {
    my @indices = @{$members{$root}};
    $group_id{$root} = sprintf 'A1-DUP-%04d', ++$group_serial;
    my ($best) = sort {
        my $rank_a =
          $rows[$a]{proposed_corpus_record} =~ /^P\d{4}$/
          ? -1
          : $state_rank{$rows[$a]{screening_state}};
        my $rank_b =
          $rows[$b]{proposed_corpus_record} =~ /^P\d{4}$/
          ? -1
          : $state_rank{$rows[$b]{screening_state}};
        $rank_a <=> $rank_b
          || $rows[$a]{_source_order} <=> $rows[$b]{_source_order}
    } @indices;
    $canonical{$root} = $best;

    my %ledger = map { $rows[$_]{_source_ledger} => 1 } @indices;
    my %doi = map {
        my $d = normalize_doi($rows[$_]{doi_or_identifier});
        $d ne '' ? ($d => 1) : ()
    } @indices;
    my %source_group = map {
        join("\0",
          $rows[$_]{_source_ledger},
          $rows[$_]{duplicate_group}) => 1
    } @indices;
    my @why;
    push @why, 'SOURCE_LEDGER_GROUP' if keys(%source_group) < @indices;
    push @why, 'NORMALIZED_DOI'
      if keys(%ledger) > 1 && keys(%doi) == 1 && keys(%doi) > 0;
    if (keys(%ledger) > 1 && !keys(%doi)) {
        my %safe_title = map {
            title_key_is_safe($rows[$_])
              ? (join("\0",
                    normalize_exact_text($rows[$_]{title}),
                    normalize_exact_text($rows[$_]{authors}),
                    normalize_exact_text($rows[$_]{year})) => 1)
              : ()
        } @indices;
        push @why, 'EXACT_TITLE_AUTHOR_YEAR_NO_DOI'
          if keys(%safe_title) == 1 && keys(%safe_title) > 0;
    }
    $basis{$root} = @why ? join(';', @why) : 'UNIQUE_OCCURRENCE';
}

my @output_rows;
for my $index (0 .. $#rows) {
    my $row = $rows[$index];
    my $root = find_root(\@parent, $index);
    my $canonical_index = $canonical{$root};
    my $state = $row->{screening_state};
    my $reason = $row->{exclusion_reason};
    my %group_ledgers = map {
        $rows[$_]{_source_ledger} => 1
    } @{$members{$root}};

    # Only cross-ledger noncanonical representatives are re-labelled here.
    # Their original disposition and exact full-text evidence remain in
    # source_screening_state/source_exclusion_reason/evidence_location.
    if ($index != $canonical_index
        && keys(%group_ledgers) > 1
        && $state ne 'DUPLICATE') {
        $state = 'DUPLICATE';
        $reason = 'CROSS_WORKSTREAM_DUPLICATE_OF='
          . $rows[$canonical_index]{phase2a1_record_id}
          . ';MATCH_BASIS=' . $basis{$root}
          . ';SOURCE_DISPOSITION=' . $row->{screening_state};
    }
    my $is_representative_inclusion =
      $index == $canonical_index && $state eq 'FULL_TEXT_INCLUDED';
    my $source_final_record_id =
      $row->{proposed_corpus_record} =~ /^P\d{4}$/
      ? $row->{proposed_corpus_record}
      : '';
    my $doi = normalize_doi($row->{doi_or_identifier});
    my $doi_final_record_id =
      $doi ne '' && exists $corpus_doi{$doi} ? $corpus_doi{$doi} : '';
    my $title_final_record_id = '';
    if ($is_representative_inclusion && $doi_final_record_id eq '') {
        my $title = normalize_exact_text($row->{title});
        my @matches = sort grep {
            index($corpus_citation{$_}, $title) >= 0
        } keys %corpus_citation;
        die "$row->{phase2a1_record_id}: title is too short or generic for "
          . "safe corpus matching\n"
          if @matches
          && (length($title) < 30
              || scalar(grep { length } split / /, $title) < 4);
        die "$row->{phase2a1_record_id}: exact title matches multiple corpus "
          . "rows: " . join(', ', @matches) . "\n"
          if @matches > 1;
        $title_final_record_id = $matches[0] // '';
    }
    my $preserved_final_record_id =
      $preserved_final_record_id{$row->{phase2a1_record_id}} // '';
    my %mapped_id = map { $_ => 1 }
      grep { $_ ne '' }
      ($source_final_record_id, $doi_final_record_id, $title_final_record_id,
       $preserved_final_record_id);
    die "$row->{phase2a1_record_id}: conflicting corpus mappings: "
      . join(', ', sort keys %mapped_id) . "\n"
      if keys(%mapped_id) > 1;
    my ($mapped_record_id) = keys %mapped_id;
    $mapped_record_id //= '';
    my $final_record_id =
      $is_representative_inclusion ? $mapped_record_id : '';
    my $corpus_action =
        $is_representative_inclusion && $final_record_id ne ''
      ? 'EXISTING_CORPUS_RECORD'
      : $is_representative_inclusion
        && $row->{proposed_corpus_record} eq 'NEW_CORPUS_CANDIDATE'
      ? 'NEW_CORPUS_CANDIDATE'
      : $state eq 'DUPLICATE' && $mapped_record_id ne ''
      ? 'DUPLICATE_OF_EXISTING_CORPUS'
      : $state eq 'DUPLICATE'
        && $row->{proposed_corpus_record} eq 'NEW_CORPUS_CANDIDATE'
      ? 'DUPLICATE_OF_NEW_CORPUS_CANDIDATE'
      : 'NONE';
    push @output_rows, {
        phase2a1_record_id      => $row->{phase2a1_record_id},
        workstream_families     => $row->{_workstream_families},
        query_id                => $row->{query_id},
        search_date             => $row->{search_date},
        search_source           => $row->{search_source},
        title                   => $row->{title},
        authors                 => $row->{authors},
        year                    => $row->{year},
        doi_or_identifier       => $row->{doi_or_identifier},
        source_native_id        => $row->{source_native_id},
        duplicate_group         => $group_id{$root},
        canonical_record_id     =>
          $rows[$canonical_index]{phase2a1_record_id},
        deduplication_basis      => $basis{$root},
        source_ledger            => $row->{_source_ledger},
        source_duplicate_group   => $row->{duplicate_group},
        source_screening_state   => $row->{screening_state},
        screening_state          => $state,
        source_exclusion_reason  => $row->{exclusion_reason},
        exclusion_reason         => $reason,
        evidence_depth           => $row->{evidence_depth},
        full_text_access_status  => $row->{full_text_access_status},
        evidence_location        => $row->{evidence_location},
        final_record_id          => $final_record_id,
        corpus_action            => $corpus_action,
        source_proposed_corpus_record =>
          $row->{proposed_corpus_record},
        raw_snapshot             => $row->{raw_snapshot},
        notes                    => $row->{notes},
    };
}

my $temporary_path = "$output_path.tmp.$$";
open my $out, '>:encoding(UTF-8)', $temporary_path
  or die "$temporary_path: $!\n";
print {$out} join(',', map { csv_quote($_) } @output_header), "\n";
for my $row (@output_rows) {
    print {$out} join(',', map { csv_quote($row->{$_}) } @output_header), "\n";
}
close $out or die "$temporary_path: $!\n";
rename $temporary_path, $output_path
  or die "rename $temporary_path -> $output_path: $!\n";

my (%state_count, %source_count, %basis_count);
for my $row (@output_rows) {
    ++$state_count{$row->{screening_state}};
    ++$source_count{$row->{source_ledger}};
}
++ $basis_count{$basis{$_}} for @roots;

print "occurrences=", scalar(@output_rows), "\n";
print "deduplicated_groups=", scalar(@roots), "\n";
print "source_rows=",
  join(' ', map { "$_=$source_count{$_}" } sort keys %source_count), "\n";
print "states=",
  join(' ', map { "$_=$state_count{$_}" } sort keys %state_count), "\n";
print "group_bases=",
  join(' ', map { "$_=$basis_count{$_}" } sort keys %basis_count), "\n";
