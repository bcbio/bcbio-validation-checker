# Check bcbio validation runs

Compare validation outputs from [bcbio](http://bcb.io) against existing
truth sets. Designed for the GA4GH-DREAM Tool Execution Challenge, this provides
a Docker container and [CWL](http://www.commonwl.org/) wrapper for verifying
that a bcbio validation is correct. bcbio itself runs alignment, variantcalling
and validation against known truth sets from [Genome in a Bottle](http://jimb.stanford.edu/giab)
reporting sensitivity and specificity for samples and methods. This look takes
these outputs and ensures they match previous results.
