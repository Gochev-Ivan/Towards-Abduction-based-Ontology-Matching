from owlready2 import *
from methodology.isomorphisms import *


def experiments():
    from OWLUtils.Ontologies import Ontology, OntologyClass
    from Utils.PythonOWL2expr import POWL2expr
    from Utils.owl2tree import expr2tree, signature
    from Utils.utils import clean_expr, print_df
    import time

    prefixes = []

    O1_folder_path = input("Input the folder of the first ontology: ")
    O1_file_path = input("Input the name of the first ontology (.owl): ")
    O1 = Ontology(O1_folder_path, O1_file_path)

    print(f"O1 = {O1}")

    O2_folder_path = input("Input the folder of the second ontology: ")
    O2_file_path = input("Input the name of the second ontology (.owl): ")
    O2 = Ontology(O2_folder_path, O2_file_path)

    print(f"O2 = {O2}")

    sub_mappings_file = input("Input the file of the generated subsumption mappings (.csv): ")
    df_sub_mappings = pd.read_csv(sub_mappings_file)

    results_file = input("Input the file in which to save the results (.csv): ")

    algorithm_eval_file = input("Input the file in which to save the results from the algorithm evaluation (.csv): ")

    prefixes.extend([O1_folder_path, O2_folder_path])

    results = pd.DataFrame(columns=["#E", "|E|", "#A", "#C", "t[s]"])

    algorithm_eval = pd.DataFrame(columns=["#V(T1)", "#V(T2)", "#E(T1)", "#E(T2)", "BF(T1)", "BF(T2)", "t [s]"])

    for i in range(len(df_sub_mappings)):
        row = df_sub_mappings.iloc[i]
        print(f"{[*row]=}")
        C1 = OntologyClass(iri=row['O1'], cls=IRIS[row['O1']])
        C2 = OntologyClass(iri=row['O2'], cls=IRIS[row['O2']])

        num_E, card_E, num_A, num_R, time_s = 0, [], 0, 0, 0

        for definition_1 in set(C1.get_equivalentToClasses() + C1.get_supClasses(direct=False)):
            for definition_2 in set(C2.get_equivalentToClasses() + C2.get_supClasses(direct=False)):

                if definition_1 == Thing or definition_2 == Thing:
                    continue

                def_1 = POWL2expr(clean_expr(definition_1, prefixes))
                def_2 = POWL2expr(clean_expr(definition_2, prefixes))

                try:
                    T1 = expr2tree(def_1, inputted_vertex_notation='v')
                    T2 = expr2tree(def_2, inputted_vertex_notation='w')
                except IndexError:
                    print("Index error while generating trees.")
                    continue

                AP = Isomorphisms(T1=T1, T2=T2)

                start_time = time.time()

                algo_time_start = time.time()
                _, _ = AP.heuristics_subtree_isomorphisms()
                algo_time_end = time.time() - algo_time_start

                time_s += time.time() - start_time

                for num, h in enumerate(AP.construct_hypotheses()):
                    for axiom in h:
                        lhs, rhs = axiom.split("SubClassOf")
                        classes_1, properties_1 = signature(lhs)
                        classes_2, properties_2 = signature(rhs)
                        num_A = len(classes_1) + len(classes_2)
                        num_R = len(properties_1) + len(properties_2)
                    card_E.append(len(h))
                    num_E += 1

                card_V1 = len(T1.V)
                card_V2 = len(T2.V)

                card_E1 = len(T1.E)
                card_E2 = len(T2.E)

                bf1_arr = [deg for _, deg in T1.deg().items() if deg != 0]
                bf2_arr = [deg for _, deg in T2.deg().items() if deg != 0]

                bf1 = sum(bf1_arr) / len(bf1_arr) if len(bf1_arr) != 0 else 0
                bf2 = sum(bf2_arr) / len(bf2_arr) if len(bf2_arr) != 0 else 0

                algorithm_eval.loc[len(algorithm_eval)] = [card_V1, card_V2, card_E1, card_E2, bf1, bf2, algo_time_end]

        results.loc[len(results)] = [num_E, sum(card_E) / len(card_E), num_A, num_R, time_s]

    print_df(results)
    print_df(algorithm_eval)
    results.to_csv(results_file)
    algorithm_eval.to_csv(algorithm_eval_file)
