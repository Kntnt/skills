from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

# Load the executable script directly so the skill needs no packaging
# dependency.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = PROJECT_ROOT / "skills" / "producivity" / "rename-invoices"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))

import rename_invoices as renamer


class RenameInvoicesTest(unittest.TestCase):
    """Verify configuration, locale, planning, and application through the public interface."""

    def setUp(self) -> None:
        """Create an isolated folder for each workflow."""

        # Keep every test side effect inside one automatically removed
        # directory.
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.folder = Path(self.temporary_directory.name)

    def tearDown(self) -> None:
        """Remove the isolated workflow directory."""

        # Release files and configuration created by the current test.
        self.temporary_directory.cleanup()

    def create_pdf(self, name: str, content: bytes | None = None) -> Path:
        """Create one source whose bytes can be integrity-checked."""

        # Injected text extraction makes PDF syntax irrelevant to planner tests.
        path = self.folder / name
        path.write_bytes(content or f"PDF:{name}".encode())

        return path

    def extractor(self, texts: dict[str, str]) -> renamer.TextExtractor:
        """Return deterministic extracted text keyed by source filename."""

        # Preserve the real inventory and hashing path around the injected seam.
        return lambda path: texts[path.name]

    def write_toml(self, name: str, content: str) -> Path:
        """Write one temporary TOML fixture."""

        # Keep declarative examples readable inside their focused tests.
        path = self.folder / name
        path.write_text(content.strip(), encoding="utf-8")

        return path

    def plan(
        self,
        document_type: str,
        texts: dict[str, str],
        *,
        locales: tuple[str, ...] | None = ("en",),
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Build a plan with explicit test locale selection."""

        # Let individual tests replace the locale list or other
        # highest-precedence flags.
        cli_overrides = dict(kwargs.pop("cli_overrides", {}) or {})
        if locales is not None:
            cli_overrides.setdefault("locales", list(locales))

        return renamer.build_plan(
            self.folder,
            document_type,
            use_user_config=False,
            cli_overrides=cli_overrides,
            extractor=self.extractor(texts),
            **kwargs,
        )

    def test_poppler_check_accepts_an_installed_executable(self) -> None:
        """Accept Poppler when pdftotext is available on PATH."""

        # Simulate a conventional installation without opening or generating a
        # PDF.
        with mock.patch(
            "rename_invoices.shutil.which", return_value="/usr/local/bin/pdftotext"
        ):
            status = renamer.check_poppler()

        # Return the resolved dependency for concise diagnostics.
        self.assertEqual(status["status"], "ok")
        self.assertEqual(status["executable"], "/usr/local/bin/pdftotext")

    def test_poppler_check_recommends_homebrew_on_macos(self) -> None:
        """Give an actionable macOS installation instruction when Poppler is missing."""

        # Model a clean macOS host without pdftotext on PATH.
        with (
            mock.patch("rename_invoices.sys.platform", "darwin"),
            mock.patch("rename_invoices.shutil.which", return_value=None),
            self.assertRaisesRegex(renamer.PlanError, "brew install poppler"),
        ):
            renamer.check_poppler()

    def test_production_planning_checks_poppler_before_configuration_and_folder(
        self,
    ) -> None:
        """Fail the production path at its earliest external dependency."""

        # Force the dependency gate before missing locale or folder validation.
        with (
            mock.patch.object(
                renamer,
                "check_poppler",
                side_effect=renamer.PlanError("preflight stopped"),
            ),
            self.assertRaisesRegex(renamer.PlanError, "preflight stopped"),
        ):
            renamer.build_plan(
                self.folder / "missing", "supplier-invoice", use_user_config=False
            )

    def test_locale_selection_is_required_before_folder_access(self) -> None:
        """Reject implicit language selection even when a bundled locale exists."""

        # Omit locale flags and user configuration while targeting a missing
        # folder.
        with self.assertRaisesRegex(renamer.PlanError, "locales must not be empty"):
            renamer.build_plan(
                self.folder / "missing",
                "supplier-invoice",
                use_user_config=False,
                extractor=lambda _: "",
            )

    def test_bundled_settings_and_locale_are_external_files(self) -> None:
        """Require both bundled data files instead of program constants."""

        # Resolve one ordinary configuration entirely from the bundled TOML
        # files.
        configuration = renamer.load_configuration(
            use_user_config=False, locale_names=["en"]
        )
        self.assertEqual(
            configuration.bundled_source,
            (SKILL_ROOT / "config" / "config.toml").resolve(),
        )
        self.assertEqual(
            configuration.locales["en"].source,
            (SKILL_ROOT / "config" / "locales" / "en.toml").resolve(),
        )

        # A missing bundled settings file is a hard packaging error.
        with (
            mock.patch.object(
                renamer,
                "BUNDLED_CONFIG_PATH",
                self.folder / "missing.toml",
            ),
            self.assertRaisesRegex(
                renamer.PlanError, "Bundled configuration file is missing"
            ),
        ):
            renamer.load_configuration(use_user_config=False, locale_names=["en"])

    def test_builtin_type_uses_primary_locale_prefix(self) -> None:
        """Resolve localized standard output text from the first selected locale."""

        # Model one conventional invoice through the English bundled locale.
        self.create_pdf("source.pdf")
        texts = {
            "source.pdf": "Invoice date September 1, 2026\nSeller: Acme Holdings LLC\n",
        }
        plan = self.plan("supplier-invoice", texts)

        # Keep the default settings and linguistic terms independently sourced.
        self.assertEqual(plan["locales"], ["en"])
        self.assertEqual(
            plan["items"][0]["target_name"], "[INVOICE][2026-09-01] Acme Holdings.pdf"
        )

    def test_multiple_locales_process_one_mixed_language_batch(self) -> None:
        """Use every selected locale while preserving one primary output locale."""

        # Combine English and Swedish invoices in one explicitly bilingual
        # batch.
        self.create_pdf("english.pdf")
        self.create_pdf("swedish.pdf")
        texts = {
            "english.pdf": "Invoice date September 2, 2026\nSeller: Acme Ltd\n",
            "swedish.pdf": "Fakturadatum: 3 september 2026\nLeverantör: Exempel AB\n",
        }
        plan = self.plan("supplier-invoice", texts, locales=("en", "sv"))
        items = {item["source_name"]: item for item in plan["items"]}

        # Parse each language and use the first locale's standard prefix for
        # both outputs.
        self.assertEqual(plan["locales"], ["en", "sv"])
        self.assertEqual(
            items["english.pdf"]["target_name"], "[INVOICE][2026-09-02] Acme.pdf"
        )
        self.assertEqual(
            items["swedish.pdf"]["target_name"], "[INVOICE][2026-09-03] Exempel.pdf"
        )

    def test_conflicting_locale_date_interpretations_require_review(self) -> None:
        """Never use locale list order to guess an ambiguous numeric date."""

        # Define two complete test locales whose shared label has opposing
        # numeric orders.
        locale_template = """
version = 1
locale = "{name}"
numeric_date_order = "{order}"
ordinal_suffixes = []
identifier_labels = ["Number"]
issuer_labels = ["Seller"]
recipient_labels = ["Buyer"]
legal_suffixes = ["LLC"]
ignored_counterparty_values = ["Invoice"]

[type_prefixes]
supplier-invoice = "INVOICE"
receipt = "RECEIPT"
customer-invoice = "CUSTOMER INVOICE"
credit-note = "CREDIT NOTE"

[date_labels]
issue = ["Date"]
purchase = ["Purchase date"]
payment = ["Payment date"]
due = ["Due date"]

[months]
"""
        first_locale = self.write_toml(
            "aa.toml", locale_template.format(name="aa", order="dmy")
        )
        second_locale = self.write_toml(
            "bb.toml", locale_template.format(name="bb", order="mdy")
        )
        self.create_pdf("source.pdf")
        texts = {"source.pdf": "Date: 03/04/2026\nSeller: Acme LLC\n"}
        plan = self.plan(
            "supplier-invoice",
            texts,
            locales=("aa", "bb"),
            locale_files=[first_locale, second_locale],
        )

        # Surface the unresolved date rather than preferring the first selected
        # locale.
        self.assertEqual(plan["items"][0]["status"], "needs_review")
        self.assertIn("date", plan["items"][0]["issues"])

    def test_personal_configuration_and_locale_replace_bundled_data(self) -> None:
        """Apply personal files from the fixed kntnt directory before CLI flags."""

        # Create one personal config and a complete replacement English locale.
        personal_root = self.folder / "personal"
        personal_locale = personal_root / "locales" / "en.toml"
        personal_locale.parent.mkdir(parents=True)
        personal_locale.write_text(
            (SKILL_ROOT / "config" / "locales" / "en.toml")
            .read_text(encoding="utf-8")
            .replace(
                'supplier-invoice = "INVOICE"',
                'supplier-invoice = "PERSONAL"',
            ),
            encoding="utf-8",
        )
        (personal_root / "config.toml").write_text(
            """
version = 2
locales = ["en"]

[types.supplier-invoice]
prefix = "CONFIGURED"
""".strip(),
            encoding="utf-8",
        )
        self.create_pdf("source.pdf")
        texts = {"source.pdf": "Invoice date September 4, 2026\nSeller: Acme LLC\n"}

        # Discover both personal files, then let the explicit prefix flag win.
        with mock.patch.object(
            renamer, "user_config_directory", return_value=personal_root
        ):
            configured = renamer.build_plan(
                self.folder,
                "supplier-invoice",
                extractor=self.extractor(texts),
            )
            flagged = renamer.build_plan(
                self.folder,
                "supplier-invoice",
                cli_overrides={"prefix": "FLAGGED"},
                extractor=self.extractor(texts),
            )

        # Preserve complete locale replacement and flag-over-config precedence.
        self.assertEqual(
            configured["locale_sources"]["en"], str(personal_locale.resolve())
        )
        self.assertEqual(
            configured["items"][0]["target_name"], "[CONFIGURED][2026-09-04] Acme.pdf"
        )
        self.assertEqual(
            flagged["items"][0]["target_name"], "[FLAGGED][2026-09-04] Acme.pdf"
        )

    def test_personal_configuration_uses_the_shared_kntnt_directory(self) -> None:
        """Place this Skill's user configuration below the shared Kntnt root."""

        # Assert the convention directly so a later path change cannot fragment
        # it.
        self.assertEqual(
            renamer.user_config_directory(), Path.home() / ".kntnt" / "rename-invoices"
        )

    def test_custom_locale_and_type_require_no_program_changes(self) -> None:
        """Support a contributed language and filename convention through TOML only."""

        # Add one complete German locale and one user-defined type.
        locale_file = self.write_toml(
            "de.toml",
            """
version = 1
locale = "de"
numeric_date_order = "dmy"
ordinal_suffixes = []
identifier_labels = ["Rechnungsnummer"]
issuer_labels = ["Lieferant"]
recipient_labels = ["Kunde"]
legal_suffixes = ["GmbH"]
ignored_counterparty_values = ["Rechnung"]

[type_prefixes]
beleg = "BELEG"

[date_labels]
issue = ["Rechnungsdatum"]

[months]
""",
        )
        config_file = self.write_toml(
            "german-config.toml",
            """
version = 2
locales = ["de"]

[types.beleg]
prefix_key = "beleg"
date_sources = ["issue"]
counterparty_source = "issuer"
identifier_policy = "never"
template = "{date}_{counterparty}_{prefix}.{extension}"
date_format = "%d-%m-%Y"
""",
        )
        self.create_pdf("quelle.pdf")
        texts = {"quelle.pdf": "Rechnungsdatum: 31.08.2026\nLieferant: Beispiel GmbH\n"}
        plan = renamer.build_plan(
            self.folder,
            "beleg",
            config_path=config_file,
            locale_files=[locale_file],
            extractor=self.extractor(texts),
        )

        # Resolve the contributed locale, prefix, and date format from data
        # files.
        self.assertEqual(plan["locales"], ["de"])
        self.assertEqual(
            plan["items"][0]["target_name"], "31-08-2026_Beispiel_BELEG.pdf"
        )

    def test_document_type_is_required_and_never_aliased(self) -> None:
        """Require the exact explicit document type at the command seam."""

        # Parse an otherwise complete invocation without the authoritative type.
        parser = renamer.build_parser()
        with self.assertRaises(SystemExit) as raised:
            parser.parse_args(["plan", "--folder", str(self.folder), "--locale", "en"])
        self.assertEqual(raised.exception.code, 2)

        # Reject a natural-language alias absent from configuration.
        configuration = renamer.load_configuration(
            use_user_config=False, locale_names=["en"]
        )
        with self.assertRaisesRegex(
            renamer.PlanError, "Unknown document type 'invoice'"
        ):
            renamer.resolve_settings(configuration, "invoice")

    def test_unknown_configuration_field_fails_before_folder_access(self) -> None:
        """Reject apparent overrides that contain a misspelled field."""

        # Place one plausible misspelling in an explicit partial configuration.
        config = self.write_toml(
            "invalid.toml",
            """
version = 2
locales = ["en"]

[output]
templat = "{date} {counterparty}.{extension}"
""",
        )
        with self.assertRaisesRegex(renamer.PlanError, "templat"):
            renamer.build_plan(
                self.folder / "missing",
                "supplier-invoice",
                config_path=config,
                extractor=lambda _: "",
            )

    def test_receipt_collisions_use_only_explicit_unique_identifiers(self) -> None:
        """Append identifiers only to otherwise colliding receipt names."""

        # Create two same-day purchases from one provider and one unique
        # purchase.
        for name in ("acme-a.pdf", "acme-b.pdf", "other.pdf"):
            self.create_pdf(name)
        texts = {
            "acme-a.pdf": "Transaction Date: 2026-08-22\nTransaction ID: TX-1001\nSeller: Acme LLC\n",
            "acme-b.pdf": "Transaction Date: 2026-08-22\nTransaction ID: TX-1002\nSeller: Acme LLC\n",
            "other.pdf": "Transaction Date: 2026-08-23\nTransaction ID: TX-2001\nSeller: Other Ltd\n",
        }
        plan = self.plan("receipt", texts)
        items = {item["source_name"]: item for item in plan["items"]}

        # Use identifiers for the collision pair and keep the unique name
        # compact.
        self.assertEqual(
            items["acme-a.pdf"]["target_name"],
            "[RECEIPT][2026-08-22] Acme - TX-1001.pdf",
        )
        self.assertEqual(
            items["acme-b.pdf"]["target_name"],
            "[RECEIPT][2026-08-22] Acme - TX-1002.pdf",
        )
        self.assertEqual(
            items["other.pdf"]["target_name"], "[RECEIPT][2026-08-23] Other.pdf"
        )

    def test_unknown_counterparty_requires_review_until_overridden(self) -> None:
        """Expose uncertainty instead of guessing from the source filename."""

        # Omit both party labels and a complete legal-entity line.
        self.create_pdf("misleading-acme.pdf")
        texts = {
            "misleading-acme.pdf": "Invoice number AC-42\nInvoice date September 5, 2026\n"
        }
        unresolved = self.plan("supplier-invoice", texts)
        self.assertIn("counterparty", unresolved["items"][0]["issues"])

        # Supply only the missing semantic fact through a reviewed override.
        resolved = self.plan(
            "supplier-invoice",
            texts,
            overrides={"misleading-acme.pdf": {"counterparty": "Acme"}},
        )
        self.assertEqual(
            resolved["items"][0]["target_name"], "[INVOICE][2026-09-05] Acme.pdf"
        )

    def test_customer_invoice_uses_recipient_and_requires_identifier(self) -> None:
        """Honor type semantics independently of the document title."""

        # Represent an outgoing invoice whose issuer and recipient are both
        # visible.
        self.create_pdf("customer.pdf")
        texts = {
            "customer.pdf": (
                "Invoice number INV-007\nInvoice date September 6, 2026\n"
                "Seller: My Business LLC\nBill To: Clear Round Ltd\n"
            ),
        }
        plan = self.plan("customer-invoice", texts)

        # Use recipient semantics and always retain the explicit identifier.
        self.assertEqual(
            plan["items"][0]["target_name"],
            "[CUSTOMER INVOICE][2026-09-06] Clear Round - INV-007.pdf",
        )

    def test_apply_rejects_unresolved_edited_and_stale_plans(self) -> None:
        """Keep every apply decision bound to reviewed source bytes."""

        # Reject unresolved work before any filesystem mutation.
        source = self.create_pdf("source.pdf", b"first-version")
        texts = {"source.pdf": "Invoice date September 7, 2026\n"}
        unresolved = self.plan("supplier-invoice", texts)
        with self.assertRaisesRegex(renamer.PlanError, "needs_review"):
            renamer.apply_plan(unresolved)

        # Reject direct plan edits and source changes after a resolved plan.
        resolved = self.plan(
            "supplier-invoice",
            texts,
            overrides={"source.pdf": {"counterparty": "Acme"}},
        )
        edited = dict(resolved)
        edited["items"] = [dict(resolved["items"][0])]
        edited["items"][0]["target_name"] = "edited.pdf"
        with self.assertRaisesRegex(renamer.PlanError, "plan_id"):
            renamer.apply_plan(edited)
        source.write_bytes(b"second-version")
        with self.assertRaisesRegex(renamer.PlanError, "changed since planning"):
            renamer.apply_plan(resolved)

    def test_apply_renames_ready_files_and_preserves_content(self) -> None:
        """Apply a reviewed plan without changing document bytes."""

        # Plan one complete source with distinctive bytes.
        source = self.create_pdf("source.pdf", b"immutable-pdf-content")
        texts = {"source.pdf": "Invoice date September 8, 2026\nSeller: Acme LLC\n"}
        plan = self.plan("supplier-invoice", texts)
        result = renamer.apply_plan(plan)
        target = self.folder / "[INVOICE][2026-09-08] Acme.pdf"

        # Verify the observable rename and byte-for-byte integrity.
        self.assertFalse(source.exists())
        self.assertEqual(target.read_bytes(), b"immutable-pdf-content")
        self.assertEqual(result["renamed_count"], 1)

    def test_matching_canonical_name_is_already_correct(self) -> None:
        """Keep a content-verified canonical name unchanged."""

        # Give one receipt its exact canonical name before planning.
        name = "[RECEIPT][2026-07-12] NodePing.pdf"
        self.create_pdf(name)
        texts = {
            name: "Transaction Date: 2026-07-12\nTransaction ID: abc123\nSeller: NodePing LLC\n"
        }
        plan = self.plan("receipt", texts)

        # Separate verified no-op files from actionable renames.
        self.assertEqual(plan["items"][0]["status"], "already_correct")
        self.assertEqual(
            plan["summary"], {"already_correct": 1, "needs_review": 0, "ready": 0}
        )


if __name__ == "__main__":
    # Run the same suite directly without an additional test-runner dependency.
    unittest.main()
