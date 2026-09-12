# Prebuilt foreign binary: no build-id or debuginfo can be produced, so the
# debug package is disabled. The binary ships as-is from the release RPM.
%global debug_package %{nil}

# NOTE (verified by local rpmbuild of 2.3.1): %%global debug_package %%{nil}
# is what makes the default ELF-rewriting brp hooks run, not what skips them
# — Fedora's %%__os_install_post gates brp-strip / brp-strip-comment-note on
# %%__debug_package being *undefined*. With them in place the payload's ELF
# files get rewritten: brp-strip dropped .symtab/.strtab from
# /usr/bin/iloader (35659024 -> 34534016 bytes) instead of shipping it as
# upstream built it. brp-strip-lto and brp-strip-static-archive are not
# gated at all. Empty all four so the only remaining difference from the
# upstream RPM is the intended curated desktop file. Set them to %%{nil}
# rather than %%undefine'ing them: with rpm 6.0.2 %%undefine does not mask
# brp-strip / brp-strip-comment-note (verified — the hooks still ran, while
# %%undefine on the lto one did take effect).
%global __brp_strip %{nil}
%global __brp_strip_comment_note %{nil}
%global __brp_strip_lto %{nil}
%global __brp_strip_static_archive %{nil}

# add-determinism's brp hook (add-det) would regenerate /usr/lib/.build-id
# links from the payload's ELF build-id notes and otherwise normalize the
# payload. The payload must ship as upstream built it, so unset the hook.
%undefine __brp_add_determinism

Name:           iloader
Version:        2.3.1
Release:        %autorelease
Summary:        User-friendly iOS sideloading companion
License:        MIT
# Branding assets (icons, logos, the "iloader" name) are NOT covered by the
# MIT license; LICENSE-BRANDING states their separate terms and is shipped
# with the package to satisfy the attribution requirements.
URL:            https://github.com/nab138/iloader
ExclusiveArch:  x86_64

Source0:        https://github.com/nab138/iloader/releases/download/v%{version}/iloader-linux-x86_64.rpm
# Upstream prebuilt RPM does not bundle a license file. spectool fetches the
# LICENSE for the exact version being packaged from the release tag; the build
# fails if the fetch fails, so the packaged license always matches the version.
Source1:        https://raw.githubusercontent.com/nab138/iloader/v%{version}/LICENSE
# Curated desktop file: adds URL handling (iloader %u) and the iloader:// scheme.
Source2:        iloader.desktop
# AppStream metadata; upstream RPM ships none.
Source3:        iloader.appdata.xml
# Branding notice fetched from the same release tag, like Source1.
Source4:        https://raw.githubusercontent.com/nab138/iloader/v%{version}/LICENSE-BRANDING
# Repo README shipped as %%doc.
Source5:        README.md

BuildRequires:  desktop-file-utils
BuildRequires:  appstream
BuildRequires:  cpio

# Non-linked runtime deps (not auto-detected by elfdeps)
Requires:       usbmuxd
Requires:       hicolor-icon-theme

# NOTE: library deps (libwebkit2gtk, libgtk, libc, librsvg2, etc.) are added
# automatically by rpmbuild's dependency generator from DT_NEEDED entries.

%description
iloader is a user-friendly iOS sideloading companion built with Tauri.
It lets you install apps like SideStore and import your pairing file
with ease, providing a friendly front-end to isideload on Linux.

%prep
rpm2cpio %{SOURCE0} | cpio -idmu
cp %{SOURCE1} LICENSE
cp %{SOURCE4} LICENSE-BRANDING
cp %{SOURCE5} README.md

%build
# Nothing to compile: the prebuilt upstream binary is unpacked in %%prep.
# The section exists so rpm's build hooks (e.g. macro-injected steps) run.

%install
cp -a usr %{buildroot}/
install -Dm0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/iloader.desktop
install -Dm0644 %{SOURCE3} %{buildroot}%{_metainfodir}/me.nabdev.iloader.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/iloader.desktop
appstreamcli validate --no-net %{buildroot}%{_metainfodir}/me.nabdev.iloader.metainfo.xml

%files
%license LICENSE
%license LICENSE-BRANDING
%doc README.md
%{_bindir}/iloader
%{_datadir}/applications/iloader.desktop
%{_datadir}/icons/hicolor/*/apps/iloader.png
%{_metainfodir}/me.nabdev.iloader.metainfo.xml
# Release is %%autorelease. COPR builds this repo from an uploaded SRPM, where
# rpm's plain %%autorelease fallback applies: the release is a literal 1 plus
# the chroot's dist tag, NOT the changelog entry count (verified against the
# published builds: iloader's 2.3.3-1 was built from a spec with three
# changelog entries, and the only unique NVRs any of these projects ever
# published came from the CI's force_build path). A %%changelog entry therefore
# documents a spec change but does not on its own give an already-built
# upstream version a new NVR — publish it with the force_build workflow input,
# which rewrites Release to %%{autorelease}.f<run_id> (a unique, higher
# release), exactly as the earlier forced builds in these projects did.

%changelog
* Sat Sep 12 2026 Anudeep D <anudeepd2@gmail.com> - 2.3.1-4
- Keep the payload matching upstream outside the curated desktop file: unset
  Fedora's ELF-rewriting brp hooks (brp-strip, brp-strip-comment-note,
  brp-strip-lto, brp-strip-static-archive) which drop .comment from every
  bundled binary

* Sat Aug 29 2026 Anudeep D <anudeepd2@gmail.com> - 2.3.1-3
- Fix CI version gating, rpmlint warnings, and licensing provenance
- Ship LICENSE-BRANDING, AppStream metadata, curated desktop file, and %doc README

* Mon Aug 17 2026 Anudeep D <anudeepd2@gmail.com> - 2.3.1-2
- Package LICENSE and support forced COPR rebuilds

* Mon Aug 17 2026 Anudeep D <anudeepd2@gmail.com> - 2.3.1-1
- Initial Fedora repackaging of upstream prebuilt RPM