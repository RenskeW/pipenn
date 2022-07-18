#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

baseCommand: python3

hints:
  DockerRequirement:
    dockerPull: amancevice/pandas:1.3.4-slim # Script needs numpy which is a dependency of pandas

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
       
  


