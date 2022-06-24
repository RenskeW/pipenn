#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow

inputs:
  fasta_sequence: 
    type: File
  netsurfp_param1: Any
  netsurfp_param2: Any
  h1: Any
  h2: Any

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
      param1: netsurfp_param1
      param2: netsurfp_param2
    out: 
      [ pssm, features ]
    run:
      class: Operation
      inputs:
        fasta: File
        param1: Any
        param2: Any
      outputs:
        pssm: File
        features: File
  calculate_length:
    in: 
      fasta: fasta_sequence
      std: h1
      avg: h2
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
    
    
  


