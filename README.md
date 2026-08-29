# iloader-fedora-copr-ci

[iloader](https://github.com/nab138/iloader) is a user-friendly iOS sideloading companion built with Tauri.

This repo packages iloader for Fedora by rewrapping the upstream prebuilt Linux RPM with a Fedora spec. Currently x86_64 only, matching upstream's prebuilt release artifacts. A GitHub Actions workflow runs daily at 12AM UTC to check the latest release from https://github.com/nab138/iloader and rebuilds COPR only when a new version is published. The downloaded RPM is verified against a recorded SHA256 checksum before submission.

The COPR project repository is available from: https://copr.fedorainfracloud.org/coprs/anudeepd/iloader

## Packaging compliance

This package is distributed via COPR only. It rewraps the upstream prebuilt
binary RPM, so it is **not eligible for the official Fedora repositories**:
the Fedora Packaging Guidelines require all binaries to be built from source
in the Fedora build system, and this repo intentionally ships the upstream
blob as-is (see `specs/iloader.spec`).

Everything else follows the guidelines:

- `ExclusiveArch: x86_64` — matches upstream's prebuilt artifacts.
- `%build` present (empty — nothing to compile) so rpm's build hooks run.
- `%check` runs `desktop-file-validate` and `appstreamcli validate` on the
  packaged files inside the build.
- `rpmlint` runs in CI on the built RPM (spelling false-positives and the
  unstripped prebuilt binary are filtered via `rpmlintrc`); the only remaining
  warning is `no-manual-page-for-binary`, since upstream ships no man page.
- `%doc README.md` ships this file with the package.
- License provenance: `LICENSE` and `LICENSE-BRANDING` are fetched from the
  upstream release tag by `spectool`; a fetch failure fails the build, so the
  packaged license always matches the packaged version. `License: MIT` (SPDX)
  covers the code; branding assets are governed by the shipped
  `LICENSE-BRANDING` notice.
- `%{_bindir}`, `%{_datadir}`, `%{_metainfodir}` macros used in `%files`.
- `%global debug_package %{nil}` with an explicit rationale: the prebuilt
  foreign binary cannot produce debuginfo, and disabling the debug package
  also skips `brp-strip`, which would otherwise rewrite the upstream blob.
- Runtime deps (`usbmuxd`, `hicolor-icon-theme`) declared explicitly; library
  deps auto-detected from `DT_NEEDED`. No network access inside the buildroot.
- The downloaded RPM is verified against a recorded SHA256 checksum before
  submission to COPR.

# Instructions

Enable the COPR repository then install the package.

<pre>
sudo dnf copr enable anudeepd/iloader
sudo dnf install iloader
</pre>

## Credits

Pattern and workflow structure adapted from
[DeltaCopy/waterfox-fedora-copr-ci](https://github.com/DeltaCopy/waterfox-fedora-copr-ci)
— thanks for the clean reference implementation.

<h3> COPR build status </h3>

[![Copr build status](https://copr.fedorainfracloud.org/coprs/anudeepd/iloader/package/iloader/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/anudeepd/iloader/package/iloader/)

<h3> GitHub action workflow status </h3>

[![iloader Fedora COPR CI](https://github.com/anudeepd/iloader-fedora-copr-ci/actions/workflows/iloader-ci.yml/badge.svg)](https://github.com/anudeepd/iloader-fedora-copr-ci/actions/workflows/iloader-ci.yml)

## Latest version
<a href="https://github.com/nab138/iloader/releases">
  <img src="https://img.shields.io/github/v/release/nab138/iloader" alt="iloader latest release">
</a>