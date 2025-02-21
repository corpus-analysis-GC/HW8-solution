#!/usr/bin/env python
"""Computes correct usage rate of irregular verbs."""

import collections
import csv
import glob
import os

from lxml import etree


IRREGULARS = "data/irregulars.tsv"
XML_GLOB = "data/*/*.xml"


def main() -> None:
    # Loads verb lexicon.
    cu_verbs = set()
    or_verbs = set()
    with open(IRREGULARS, "r") as source:
        tsv_reader = csv.DictReader(source, delimiter="\t")
        for row in tsv_reader:
            cu_verbs.add(row["VBD"])
            cu_verbs.add(row["VBN"])
            or_verbs.add(row["OR"])
    # Initialize counters.
    cu_counts = collections.Counter()
    or_counts = collections.Counter()
    # Load the XML files and extract counts.
    for path in glob.iglob(XML_GLOB):
        dirname, _ = os.path.split(path)
        _, child = os.path.split(dirname)
        with open(path, "r") as source:
            mytree = etree.parse(source)
            for word in mytree.xpath("//u[@who='CHI']/w/text()"):
                word = word.casefold()
                if word in cu_verbs:
                    cu_counts[child] += 1
                elif word in or_verbs:
                    or_counts[child] += 1
    # Print out the results.
    for child, cu_count in cu_counts.items():
        or_count = or_counts[child]
        cu_rate = 100 * cu_count / (cu_count + or_count)
        print(
            f"{child}: {cu_count:,} CUs, {or_count:,} ORs; "
            f"CUR: {cu_rate:2.2f}%"
        )


if __name__ == "__main__":
    main()
