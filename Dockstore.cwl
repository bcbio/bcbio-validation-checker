#!/usr/bin/env cwl-runner

class: CommandLineTool
id: "bcbio-validation-checker"
label: "Compare bcbio validation results against expected baseline"

cwlVersion: v1.0

requirements:
- class: DockerRequirement
  dockerPull: quay.io/bcbio/bcbio-validation-checker

inputs:
  baseline:
    type: File
    inputBinding:
      position: 1

  comparison:
    type: File
    inputBinding:
      position: 2

outputs:
  output:
    type: File
    outputBinding:
      glob: "results.json"

baseCommand: ["python", "/usr/local/bin/bcbio_validation_check.py"]