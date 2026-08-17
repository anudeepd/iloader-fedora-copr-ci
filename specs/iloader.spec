%global debug_package %{nil}

Name:           iloader
Version:        2.3.1
Release:        %autorelease
Summary:        User-friendly iOS sideloading companion
License:        MIT
URL:            https://github.com/nab138/iloader

Source0:        https://github.com/nab138/iloader/releases/download/v%{version}/iloader-linux-x86_64.rpm
# Upstream prebuilt RPM does not bundle a license file. The build fetches the
# LICENSE for the exact version being packaged (see the CI workflows) and falls
# back to this vendored copy if that fetch fails.
Source1:        LICENSE

BuildRequires:  cpio

# Non-linked runtime deps (not auto-detected by elfdeps)
Requires:       usbmuxd
Requires:       hicolor-icon-theme
Requires:       librsvg2

# NOTE: library deps (libwebkit2gtk, libgtk, libc, etc.) are added
# automatically by rpmbuild's dependency generator from DT_NEEDED entries.

%description
iloader is a user-friendly iOS sideloading companion built with Tauri.
It lets you install apps like SideStore and import your pairing file
with ease, providing a friendly front-end to isideload on Linux.

%prep
rpm2cpio %{SOURCE0} | cpio -idmu
cp %{SOURCE1} LICENSE

%install
cp -a usr %{buildroot}/

%files
%license LICENSE
%attr(0755, root, root) /usr/bin/iloader
/usr/share/applications/iloader.desktop
/usr/share/icons/hicolor/*/apps/iloader.png