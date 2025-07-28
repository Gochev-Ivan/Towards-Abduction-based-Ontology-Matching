def generate_subsumption_matches():
    import pandas as pd
    import jpype
    from deeponto.onto import Ontology
    from deeponto.align.mapping import SubsFromEquivMappingGenerator, ReferenceMapping

    # Load the ontologies
    O1_file_path = input("Input the complete path to the first ontology: ")
    O1 = Ontology(O1_file_path)

    O2_file_path = input("Input the complete path to the second ontology: ")
    O2 = Ontology(O2_file_path)

    # Load the equivalence mappings
    # The headings are ["SrcEntity", "TgtEntity", "Score"]
    ref_mappings_file_path = input("Input the complete path to the reference equiv mappings (.tsv file): ")
    O1_2_O2_equiv_mappings = ReferenceMapping.read_table_mappings(ref_mappings_file_path)

    output_file_name = input("Input file in which to save the generated subsumption mappings (.csv): ")

    subs_generator = SubsFromEquivMappingGenerator(
      O1, O2, O1_2_O2_equiv_mappings,
      subs_generation_ratio=1, delete_used_equiv_tgt_class=True
    )

    df = pd.DataFrame(columns=['O1', 'O2', 'rel'])
    for subs in subs_generator.subs_from_equivs:
        print(f"{subs}")
        df.loc[len(df)] = [subs[0], subs[1], subs[2]]

    df.to_csv(output_file_name)
    jpype.shutdownJVM()
