Summary:	Tools for working with the PinePhone hardware
Name:		pinephone-tools
Version:	1.0
Release:	0.20210524.2
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
Source5:	camera-setup
# udev rules to make sure the LEDs (torch!) can be controlled
Source6:	80-leds.rules
# ALSA configurations
Source10:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/alsa-ucm-pinephone/HiFi.conf
Source11:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/alsa-ucm-pinephone/PinePhone.conf
Source12:	https://raw.githubusercontent.com/dreemurrs-embedded/Pine64-Arch/master/PKGBUILDS/pine64/alsa-ucm-pinephone/VoiceCall.conf
Source14:	asound.state
# PulseAudio configuration
Source15:	pinephone.pa
# NetworkManager configuration
Source20:	MobileData.nmconnection
# Modem firmware
# See https://forum.pine64.org/showthread.php?tid=11815
# https://cnquectel-my.sharepoint.com/:f:/g/personal/europe-fae_quectel_com/EvXsoYRgfANCrMpPTnSZgL4BCDi8fImGZqHT_XFDCpG4vg?e=eSt06u
Source26:	EG25GGBR07A08M2G_01.003.01.003.zip
# TEMPORARY preloaded kwallet to make things easier. Should be replaced
# by patching kwallet to create an empty wallet on first startup to make
# sure we have random seeds
Source30:	kdewallet.kwl
Source31:	kdewallet.salt
ExclusiveArch:	aarch64
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(libxcrypt)
BuildRequires:	unzip
License:	GPLv3+
# Audio driver controls changed in 5.10
Conflicts:	kernel-pinephone < 5.10.0-0

%description
Tool to set up audio routing on the PinePhone

%package debug
Summary:	Debug info for %{name}
Group:		Debugging
Requires:	%{name} = %{EVRD}

%description debug
Debug info for %{name}

%prep

%build
%{__cc} %{optflags} -o pinephone-audio-setup %{S:0}
%{__cc} %{optflags} -o modem-adb-access %{S:2} -lcrypt

%install
mkdir -p %{buildroot}%{_bindir}
cp -a pinephone-audio-setup modem-adb-access %{S:1} %{S:5} %{buildroot}%{_bindir}/

mkdir -p %{buildroot}/lib/udev/rules.d
cp %{S:6} %{buildroot}/lib/udev/rules.d/80-leds.rules

mkdir -p %{buildroot}%{_datadir}/alsa/ucm2/PinePhone/
cp %{S:10} %{S:11} %{S:12} %{buildroot}%{_datadir}/alsa/ucm2/PinePhone/
mkdir -p %{buildroot}%{_localstatedir}/lib/alsa/
cp %{S:14} %{buildroot}%{_localstatedir}/lib/alsa/
mkdir -p %{buildroot}%{_sysconfdir}/pulse/default.pa.d
cp %{S:15} %{buildroot}%{_sysconfdir}/pulse/default.pa.d/pinephone.pa

mkdir -p %{buildroot}/lib/systemd/system
cp %{S:3} %{S:4} %{buildroot}/lib/systemd/system/

mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/system-connections
cp %{S:20} %{buildroot}%{_sysconfdir}/NetworkManager/system-connections/

mkdir -p %{buildroot}%{_sysconfdir}/skel/.local/share/kwalletd
cp %{S:30} %{S:31} %{buildroot}%{_sysconfdir}/skel/.local/share/kwalletd/

chmod +x %{buildroot}%{_bindir}/*

# Known working Modem firmware
mkdir -p %{buildroot}%{_datadir}/modem-fw
cd %{buildroot}%{_datadir}/modem-fw
unzip %{S:26}

%files
%{_bindir}/pinephone-audio-setup
%{_bindir}/camera-setup
%{_bindir}/modem
%{_bindir}/modem-adb-access
/lib/udev/rules.d/80-leds.rules
%{_datadir}/alsa/ucm2/PinePhone
%{_localstatedir}/lib/alsa/asound.state
%{_sysconfdir}/pulse/default.pa.d
/lib/systemd/system/modem.service
/lib/systemd/system/modem-wait-powered.service
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/NetworkManager/system-connections/MobileData.nmconnection
# FIXME remove as soon as kwalletd is patched
%{_sysconfdir}/skel/.local/share/kwalletd/*
%{_datadir}/modem-fw

%files debug
%{_prefix}/lib/debug/.dwz
%{_prefix}/lib/debug%{_bindir}/*.debug
