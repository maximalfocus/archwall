"""Who is asking: Verified Launchers, helpers inside apps, Launcher Bundles for unsigned CLIs, scripts and agent tasks.
Drawn from automic-vault/automic-vault at commit d1011a5 (README.md Verified Launchers and Launcher Bundles, docs/architecture.md Identity model and Launcher Packaging, docs/choosing-a-mechanism.md).
Run: python3 launchers.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from archdiagram import Diagram, L, R, GW, T1, H1, T2, H2  # noqa: E402

d = Diagram("Who is asking",
            "1 Verified Launchers: the terminals, IDEs and agent apps you pick; identity is the code signature, "
            "checked live on every request, and Hardened Runtime is required unless the program is an Apple "
            "system binary. Paths and names are not identity. "
            "2 Helpers inside apps: Claude Code's helper is built in, Codex's signed CLI is preselected for your "
            "review, and other helpers count only if you approve them; finding a helper grants nothing. "
            "3 Unsigned CLIs: a Launcher Bundle wraps one unsigned single-file Mach-O CLI, signs it with Hardened "
            "Runtime and rechecks it on every request; a changed or re-signed bundle is denied outright. Scripts "
            "are not supported. "
            "4 Scripts and agent tasks: a Blessed Script is trusted for its exact reviewed contents; a Codex or "
            "Claude Code task ID can narrow a Temporary Access Grant, but software can forge it, so it is not identity.")

d.group(L, 16, GW, H1 + 68, "Verified Launchers", 1)
d.column(L, 16, [("Apps you pick|terminal · IDE · agent app", "coding"),
                 ("Identity|code signature · checked live", "review"),
                 ("Hardened Runtime|required · or an Apple binary", "review")])
d.notes(L, 16, H1 + 68, "Paths and names are not identity", "")

d.group(R, 16, GW, H1 + 68, "Helpers inside apps", 2)
d.column(R, 16, [("Claude Code helper|built in", "coding"),
                 ("Codex CLI|preselected for your review", "coding"),
                 ("Other helpers|only if you approve", "review")])
d.notes(R, 16, H1 + 68, "Finding a helper grants nothing", "")

d.group(R, T2, GW, H2, "Unsigned CLIs", 3)
d.column(R, T2, [("Launcher Bundle|wraps one unsigned CLI", "write"),
                 ("Signed · Hardened Runtime|rechecked every request", "review"),
                 ("Changed or re-signed|denied outright", "review")])
d.notes(R, T2, H2, "Scripts are not supported", "")

d.group(L, T2, GW, H2, "Scripts and agent tasks", 4)
d.column(L, T2, [("Blessed Script|exact reviewed contents", "plan"),
                 ("Agent task ID|Codex or Claude Code session", "data"),
                 ("Task ID can be forged|only narrows a grant", "review")])

d.save(Path(__file__).with_name("launchers.svg"))
