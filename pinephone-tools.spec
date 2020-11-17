Summary:	Tools for working with the PinePhone hardware
Name:		pinephone-tools
Version:	1.0
Release:	0.20201114.1
Url:		https://xnux.eu/devices/feature/audio-pp.html
# Tools to drive PinePhone hardware...
# Audio routing
Source0:	https://xnux.eu/devices/feature/call-audio.c
# Modem
# See https://xnux.eu/devices/feature/modem-pp.html#toc-modem-power-driver
# for documentation on the driver
Source1:	modem
# Unlock adb access to the modem
Source2:	https://xnux.eu/devices/feature/qadbkey-unlock.c
# Systemd integration for the modem...
Source3:	modem.service
Source4:	modem-wait-powered.service
# Camera setup/test script
Source5:	camera
# ALSA configurations
Source10:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/alsa-ucm-pinephone/HiFi.conf
Source11:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/alsa-ucm-pinephone/PinePhone.conf
Source12:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/alsa-ucm-pinephone/VoiceCall.conf
Source13:	99-dmix.conf
Source14:	asound.state
# NetworkManager configuration
Source20:	MobileData.nmconnection
# Modem firmware
# See https://forum.pine64.org/showthread.php?tid=11815
Source25:	https://universe2.us/collector/qfirehose_good.tar.zst
Source26:	https://universe2.us/collector/newfw.tar.zst
# TEMPORARY preloaded kwallet to make things easier. Should be replaced
# by patching kwallet to create an empty wallet on first startup to make
# sure we have random seeds
Source30:	kdewallet.kwl
Source31:	kdewallet.salt
ExclusiveArch:	aarch64
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libxcrypt)
License:	GPLv3+
# Audio driver controls changed in 5.10
Conflicts:	kernel-pinephone < 5.10.0-0

%description
Tool to set up audio routing on the PinePhone

%prep

%build
%{__cc} %{optflags} -o pinephone-audio-setup %{S:0}
%{__cc} %{optflags} -o modem-adb-access %{S:2} -lcrypt
tar xf %{S:25}
# Modem firmware flash tool
cd qfirehose_good
make clean
%make_build cflags="%{optflags}" CC="%{__cc}"

%install
mkdir -p %{buildroot}%{_bindir}
cp -a pinephone-audio-setup modem-adb-access %{S:1} %{S:5} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}%{_datadir}/alsa/ucm2/PinePhone/
cp %{S:10} %{S:11} %{S:12} %{buildroot}%{_datadir}/alsa/ucm2/PinePhone/
mkdir -p %{buildroot}%{_sysconfdir}/alsa/conf.d/
cp %{S:13} %{buildroot}%{_sysconfdir}/alsa/conf.d/
mkdir -p %{buildroot}%{_localstatedir}/lib/alsa/
cp %{S:14} %{buildroot}%{_localstatedir}/lib/alsa/

mkdir -p %{buildroot}/lib/systemd/system
cp %{S:3} %{S:4} %{buildroot}/lib/systemd/system/

mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/system-connections
cp %{S:20} %{buildroot}%{_sysconfdir}/NetworkManager/system-connections/

mkdir -p %{buildroot}%{_sysconfdir}/skel/.local/share/kwalletd
cp %{S:30} %{S:31} %{buildroot}%{_sysconfdir}/skel/.local/share/kwalletd/

cp qfirehose_good/QFirehose %{buildroot}%{_bindir}

chmod +x %{buildroot}%{_bindir}/*

# Known working Modem firmware
mkdir -p %{buildroot}%{_datadir}/modem-fw
cd %{buildroot}%{_datadir}/modem-fw
tar x --strip-components=1 -f %{S:26}

%files
%{_bindir}/pinephone-audio-setup
%{_bindir}/camera
%{_bindir}/modem
%{_bindir}/modem-adb-access
%{_bindir}/QFirehose
%{_datadir}/alsa/ucm2/PinePhone
%{_localstatedir}/lib/alsa/asound.state
/lib/systemd/system/modem.service
/lib/systemd/system/modem-wait-powered.service
%config %{_sysconfdir}/alsa/conf.d/99-dmix.conf
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/NetworkManager/system-connections/MobileData.nmconnection
# FIXME remove as soon as kwalletd is patched
%{_sysconfdir}/skel/.local/share/kwalletd/*
%{_datadir}/modem-fw
