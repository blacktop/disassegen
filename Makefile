SPEC_URL = https://developer.arm.com/-/media/developer/products/architecture/a-profile/exploration-tools/os-machine-readable-data/aarchmrs_bsd/aarchmrs_bsd_a_profile-2024-12.tar.gz

.PHONY: aarchmrs
aarchmrs:
	curl -sL $(SPEC_URL) | tar -xz -C aarchmrs