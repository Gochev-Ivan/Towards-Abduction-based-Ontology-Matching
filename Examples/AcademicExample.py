from methodology.isomorphisms import *
from Utils.owl2tree import expr2tree
from Utils.utils import *


def academic_example():
    concepts_O1 = {"ConferencePaper": "Paper and (publishedIn some (Conference))",
                   "Researcher": "T and (writes some (Paper))",
                   "ProjectAssociate": "T and (writes some (Paper)) and (worksOn some (Project))"}

    concepts_O2 = {"SymposiumPublication": "Publication and (publishedIn some (Symposium))",
                   "Scholar": "T and (writes some (Publication))",
                   "AssociateScholar": "Scholar and (worksOn some (Initiative))"}

    for C1, C1_def in concepts_O1.items():
        for C2, C2_def in concepts_O2.items():

            print(C1, C2)

            T1 = expr2tree(C1_def, 'v')
            T2 = expr2tree(C2_def, 'w')

            AP = Isomorphisms(T1, T2)

            isomorphisms, df = AP.heuristics_subtree_isomorphisms()

            df = df.sort_values(by=['h'], ascending=True)

            print_df(df)
            print_isomorphisms(isomorphisms)

            print()
        print()
