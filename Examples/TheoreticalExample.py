from methodology.isomorphisms import *
from Utils.owl2tree import expr2tree
from Utils.utils import *


def theoretical_example():
    C1 = "A0 and (r1 some (A1 and (r1 some (A2)) and (r2 some (A3))))"
    C2 = "B0 and (r1 some (B1 and (r1 some (B3)) and (r2 some (B4)))) and (r1 some (B2 and (r2 some (B5))))"

    T1 = expr2tree(C1, 'v')
    T2 = expr2tree(C2, 'w')

    AP = Isomorphisms(T1, T2)

    T1.display()
    T2.display()

    isomorphisms, df = AP.heuristics_subtree_isomorphisms()

    df = df.sort_values(by=['h'], ascending=True)

    print_df(df)
    print_isomorphisms(isomorphisms)
