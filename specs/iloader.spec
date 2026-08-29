# Prebuilt foreign binary: no build-id or debuginfo can be produced, and
# disabling the debug package also skips brp-strip, which would otherwise
# rewrite the upstream blob. The binary ships as-is from the release RPM.
%global debug_package %{nil}

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
# Release is %%autorelease: COPR's rpmautospec sets it to the changelog entry
# count. To rebuild the same upstream version with a spec change, append a new
# %%changelog entry — Release bumps automatically and the NVR stays unique.

%changelog
* Sat Aug 29 2026 Anudeep D <anudeepd2@gmail.com> - 2.3.1-3
- Fix CI version gating, rpmlint warnings, and licensing provenance
- Ship LICENSE-BRANDING, AppStream metadata, curated desktop file, and %doc README

* Mon Aug 17 2026 Anudeep D <anudeepd2@gmail.com> - 2.3.1-2
- Package LICENSE and support forced COPR rebuilds

* Mon Aug 17 2026 Anudeep D <anudeepd2@gmail.com> - 2.3.1-1
- Initial Fedora repackaging of upstream prebuilt RPM