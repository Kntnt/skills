"""Historical contract provenance for two limits on a review of web copy.

These assertions read the frozen held source; they do not qualify runtime delivery.

On `web-copy-clean`, in about six runs of ten across #397, #398 and #402,
Redline reported the page's form as missing and asked for a link or a location,
because the web-copy review half said a reference to a form needs an included
or explicitly specified form. It also copied a reply time from a subheading
into the sentence under it, because the time stood only in the heading. The
frozen row, *Short headings … work*, is right on both points: a form is
interface and never part of the copy, and a heading may carry a fact its
section does not repeat. What stays a finding is copy that places or describes
an interface element differently from what the artifact shows, and a body that
needs its heading to be understood (issue #432).

Both are limits on findings, which a writer has no use for, so they live in the
review halves and no base half changes.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EDITORIAL = REPO_ROOT / "docs" / "evaluation" / "held-source-28330ae1" / "editorial"
WEBCOPY_REVIEW = EDITORIAL / "genres" / "webcopy.review.md"
BASE_REVIEW = EDITORIAL / "base.review.md"

# The sentence that made every web page naming its own form a finding.
FORM_NEEDS_INCLUSION = "needs an included or explicitly specified form"

# The interface limit, the case #345 filed that stays a finding, and the case
# the limit takes out.
INTERFACE_FINDING_ONLY_WHERE = (
    "is a finding only where the copy places or describes it differently from"
    " what the artifact shows"
)
FORM_BELOW_OVER_A_LINK = "*the form below* where the artifact holds only a link"
OWN_FORM_IS_NO_FINDING = (
    "where the artifact carries no interface markup at all, is not a finding"
)

# The heading limit, and what is a finding instead.
HEADING_MAY_CARRY_A_FACT = (
    "A heading may carry a fact that the section under it does not repeat"
)
BODY_NEEDS_THE_HEADING = (
    "a pronoun, a definite form or an ellipsis that only the heading completes"
)


def test_a_reference_to_the_pages_own_form_is_not_a_finding() -> None:
    """A form, button or link reference is a finding only where copy and artifact differ.

    The sentence written for #345's "the form below" over a link fired, read
    literally, on every page that names its own form, so Redline asked for a
    link or a location on a complete information page (issue #432).
    """

    review = WEBCOPY_REVIEW.read_text(encoding="utf-8")

    assert FORM_NEEDS_INCLUSION not in review, (
        f"{WEBCOPY_REVIEW}: still says a reference to a form needs an included"
        f" or explicitly specified form, which makes every page that names its"
        f" own form a finding (issue #432)."
    )
    assert INTERFACE_FINDING_ONLY_WHERE in review, (
        f"{WEBCOPY_REVIEW}: does not say that a form, button or link reference"
        f" is a finding only where the copy places or describes it differently"
        f" from the artifact (issue #432)."
    )
    assert FORM_BELOW_OVER_A_LINK in review, (
        f"{WEBCOPY_REVIEW}: no longer names #345's case, *the form below* over"
        f" what is only a link, as a finding (issue #432)."
    )
    assert OWN_FORM_IS_NO_FINDING in review, (
        f"{WEBCOPY_REVIEW}: does not say that copy naming the page's own form,"
        f" with no interface markup in the artifact, is not a finding"
        f" (issue #432)."
    )


def test_a_heading_may_carry_a_fact_its_section_does_not_repeat() -> None:
    """A fact only a heading states is not missing from the body under it.

    The base contract's rule that a section stays intelligible without treating
    its subheading as its opening sentence is about grammar and referents, and
    a review read it as asking for every fact in a heading to be said again
    (issue #432).
    """

    review = BASE_REVIEW.read_text(encoding="utf-8")

    assert HEADING_MAY_CARRY_A_FACT in review, (
        f"{BASE_REVIEW}: does not say that a heading may carry a fact its"
        f" section does not repeat, so a reply time stated only in a subheading"
        f" is copied into the body as a repair (issue #432)."
    )
    assert BODY_NEEDS_THE_HEADING in review, (
        f"{BASE_REVIEW}: does not name what is a finding instead — a body that"
        f" needs its heading to be understood (issue #432)."
    )
