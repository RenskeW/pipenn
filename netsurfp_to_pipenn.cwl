#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

baseCommand: python3

hints:
  DockerRequirement:
    dockerPull: amancevice/pandas:1.3.4-slim # Script needs numpy which is a dependency of pandas
  SoftwareRequirement:
    packages:
      python:
        version: [ 3.8 ] 
      pandas:
        specs: [ https://anaconda.org/conda-forge/pandas ]
        version: [ 1.4.3 ]
      requests:
        specs: [ https://anaconda.org/anaconda/requests ]
        version: [ 2.28.0 ]
inputs:
  script:
    type: File
    inputBinding:
      position: 1
    default:
      class: File
      location: ./netsurfP1-to-PIPENN.py 
      
 outputs:
   output_file:
     type: File
     outputBinding:
       glob: "*.csv"
       
  


