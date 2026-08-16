# iloader-fedora-copr-ci

[iloader](https://github.com/nab138/iloader) is a user-friendly iOS sideloading companion built with Tauri.

Building from source for Fedora requires the Tauri toolchain (Rust + Bun). A GitHub Actions workflow is scheduled to run daily at 12AM to check the latest version released from https://github.com/nab138/iloader and publish it to COPR.

The COPR project repository is available from: https://copr.fedorainfracloud.org/coprs/anudeepd/iloader

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
  <img src="https://img.shields.io/badge/iloader-v2.3.1-orange" alt="iloader-v2.3.1">
</a>
