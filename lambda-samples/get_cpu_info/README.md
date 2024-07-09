# Get Lambda's underlying CPU info

Simple script to get additional information about the underlying Lambda's hardware, /tmp storage, os-release and it's contents in python.

```bash
:12.084Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	Lambda's default working directory:
[INFO]	2024-07-09T03:14:12.084Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	/var/task
[INFO]	2024-07-09T03:14:12.084Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	/tmp contents: []
[INFO]	2024-07-09T03:14:12.084Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	Size of filesystem in MegaBytes: 524.96
[INFO]	2024-07-09T03:14:12.084Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	Actual number of free MegaBytes: 524.95
[INFO]	2024-07-09T03:14:12.084Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	Number of free MegaBytes: 513.39
[INFO]	2024-07-09T03:14:12.084Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	cat /etc/os-release:
[INFO]	2024-07-09T03:14:12.136Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	NAME="Amazon Linux"
VERSION="2023"
ID="amzn"
ID_LIKE="fedora"
VERSION_ID="2023"
PLATFORM_ID="platform:al2023"
PRETTY_NAME="Amazon Linux 2023.4.20240429"
ANSI_COLOR="0;33"
CPE_NAME="cpe:2.3:o:amazon:amazon_linux:2023"
HOME_URL="https://aws.amazon.com/linux/amazon-linux-2023/"
DOCUMENTATION_URL="https://docs.aws.amazon.com/linux/"
SUPPORT_URL="https://aws.amazon.com/premiumsupport/"
BUG_REPORT_URL="https://github.com/amazonlinux/amazon-linux-2023"
VENDOR_NAME="AWS"
VENDOR_URL="https://aws.amazon.com/"
SUPPORT_END="2028-03-15"
VARIANT_ID="202405092144-2023.174.0"

[INFO]	2024-07-09T03:14:12.136Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	uname -a:
[INFO]	2024-07-09T03:14:12.174Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	Linux 169.254.114.61 5.10.216-225.855.amzn2.x86_64 #1 SMP Wed May 8 19:03:05 UTC 2024 x86_64 x86_64 x86_64 GNU/Linux

[INFO]	2024-07-09T03:14:12.174Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	cat /proc/cpuinfo:
[INFO]	2024-07-09T03:14:12.176Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
model		: 63
model name	: Intel(R) Xeon(R) Processor @ 2.50GHz
stepping	: 2
microcode	: 0x1
cpu MHz		: 2499.988
cache size	: 36608 KB
physical id	: 0
siblings	: 2
core id		: 0
cpu cores	: 2
apicid		: 0
initial apicid	: 0
fpu		: yes
fpu_exception	: yes
cpuid level	: 22
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm cpuid_fault invpcid_single ssbd ibrs ibpb stibp ibrs_enhanced fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid smap xsaveopt arat md_clear arch_capabilities
bugs		: spectre_v1 spectre_v2 spec_store_bypass swapgs taa mmio_stale_data eibrs_pbrsb
bogomips	: 4999.97
clflush size	: 64
cache_alignment	: 64
address sizes	: 46 bits physical, 48 bits virtual
power management:

processor	: 1
vendor_id	: GenuineIntel
cpu family	: 6
model		: 63
model name	: Intel(R) Xeon(R) Processor @ 2.50GHz
stepping	: 2
microcode	: 0x1
cpu MHz		: 2499.988
cache size	: 36608 KB
physical id	: 0
siblings	: 2
core id		: 1
cpu cores	: 2
apicid		: 1
initial apicid	: 1
fpu		: yes
fpu_exception	: yes
cpuid level	: 22
wp		: yes
flags		: fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq ssse3 fma cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand hypervisor lahf_lm abm cpuid_fault invpcid_single ssbd ibrs ibpb stibp ibrs_enhanced fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid smap xsaveopt arat md_clear arch_capabilities
bugs		: spectre_v1 spectre_v2 spec_store_bypass swapgs taa mmio_stale_data eibrs_pbrsb
bogomips	: 4999.97
clflush size	: 64
cache_alignment	: 64
address sizes	: 46 bits physical, 48 bits virtual
power management:


[INFO]	2024-07-09T03:14:12.176Z	f33164d9-9741-46c9-869e-e8f2e8eb5048	
END RequestId: f33164d9-9741-46c9-869e-e8f2e8eb5048
REPORT RequestId: f33164d9-9741-46c9-869e-e8f2e8eb5048	Duration: 131.93 ms	Billed Duration: 132 ms	Memory Size: 128 MB	Max Memory Used: 37 MB	Init Duration: 91.03 ms
````
