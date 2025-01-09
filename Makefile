MRS_URL = "https://developer.arm.com/-/cdn-downloads/permalink/Exploration-Tools-OS-Machine-Readable-Data/AARCHMRS_BSD/AARCHMRS_BSD_A_profile-2024-12.tar.gz"
ISA_URL = "https://developer.arm.com/-/cdn-downloads/permalink/Exploration-Tools-A64-ISA/ISA_A64/ISA_A64_xml_A_profile-2024-12.tar.gz"

.PHONY: aarchmrs
aarchmrs:
	mkdir -p data/aarchmrs
	curl -sL $(MRS_URL) | tar -xz -C data/aarchmrs

.PHONY: isa_a64
isa_a64:
	mkdir -p data/isa_a64
	curl -sL $(ISA_URL) | tar -xz -C data/isa_a64

.PHONY: data
data: aarchmrs isa_a64

.venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install .

run_mrs: .venv
	@. .venv/bin/activate && python3 -m disassegen data/aarchmrs/Instructions.json | less -Sr

run_isa: .venv
	@. .venv/bin/activate && python3 -m disassegen data/isa_a64/ISA_A64_xml_A_profile-2024-12/addg.xml

.PHONY: clean
clean:
	rm -rf data/aarchmrs data/isa_a64
	rm -rf .venv