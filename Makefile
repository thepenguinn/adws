default: estimate.md
	pandoc estimate.md --filter pandoc-tablenos -o estimate.pdf && viewpdf estimate.pdf

.PHONY: default
