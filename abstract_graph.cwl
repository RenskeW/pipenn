#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow

hints:
  DockerRequirement:
    dockerPull: amancevice/pandas:1.3.4-slim # Script needs numpy which is a dependency of pandas

inputs:
  fasta_sequence: 
    type: File
  netsurfp_seq_database: Any 
  netsurfp_param2: Any
  avg_prot_length: Any
  std_prot_length: Any

outputs:
  predictions: 
    type: File
    outputSource: pipenn_predict/predictions
  predictions_figures:
    type: File
    outputSource: pipenn_predict/pred_figure


steps:
  run_netsurfp:
    in:
      fasta: fasta_sequence
      database: netsurfp_seq_database # this is the underlying database for netsurfp
      param2: netsurfp_param2 # hypothetical parameter
    out: 
      [ pssm, features ]
    run:
      class: Operation
      inputs:
        fasta: File
        database: Any
        param2: Any
      outputs:
        pssm: File
        features: File
  calculate_length:
    in: 
      fasta: fasta_sequence
      std: std_prot_length
      avg: avg_prot_length
    out:
      [ length_features ]
    run:
    #   label: "Calculates length and normalized length"
      class: Operation
      inputs:
        fasta: File
        std: Any
        avg: Any
      outputs:
        length_features: File 
  combine_inputs:
    in:
      pssm_inputs: run_netsurfp/pssm
      features_inputs: run_netsurfp/features
      hydropathy_inputs: calculate_length/length_features
    out:
      [ combined_inputs ]
    run:
      class: Operation
      inputs:
        pssm_inputs: File
        features_inputs: File
        hydropathy_inputs: File
      outputs:
        combined_inputs: File
  pipenn_predict:
    in: 
      input_features: combine_inputs/combined_inputs
    out:
      [ predictions, pred_figure ]
    run:
      class: Operation
      inputs:
        input_features: File
      outputs: 
        predictions: File # .csv file
        pred_figure: File # figure
    
    
  


