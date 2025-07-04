from owlready2 import *
import pandas as pd

from Utils.PythonOWL2expr import POWL2expr
from Utils.utils import clean_expr
from Utils.owl2tree import signature


class OntologyClass:
    def __init__(self, iri, cls):
        self.iri = iri
        self.cls = cls

    def __str__(self):
        return f"{self.cls.name}"

    # ==================================================================================================================
    def hierarchy(self):
        def dfs(current, path):
            if not current.is_a:
                all_paths.append(path)
                return
            for parent in current.is_a:
                if parent not in path:
                    dfs(parent, path + [parent])

        all_paths = []
        dfs(self.cls, [self.cls])

        all_paths.append(self.get_equivalentToClasses())

        return all_paths
    # ==================================================================================================================

    def get_annotations(self):
        return rdfs.label[self.cls]

    def get_equivalentToClasses(self, direct=True):
        if direct:
            if self.cls.equivalent_to:
                # return [self.cls] + [eq for eq in self.cls.equivalent_to]
                return [self.cls] + self.cls.equivalent_to
            return []

        # TODO: This part needs to be finalized - for each class in an expression in the set of equivalent_to
        #       classes, find all equivalent_to expressions and construct a hierarchy of these. This can be
        #       implemented recursively.
        return []

    def get_supClasses(self, direct=True):
        if direct:
            return [self.cls] + self.cls.is_a

        return [*set(self.cls.is_a + [*self.cls.ancestors()])]

    def get_subClasses(self, direct=True):
        if direct:
            direct_subclasses = [c for c in self.cls.subclasses() if isinstance(c, ThingClass)]
            restrictions = []
            for subclass in direct_subclasses:
                restrictions.extend([r for r in subclass.is_a])
            return [*set(direct_subclasses + restrictions)]
        else:
            def get_descendants(sc, level=0):
                subclasses = [c for c in sc.subclasses() if isinstance(c, ThingClass)]
                for sub_class in subclasses:
                    restrictions.extend([r for r in sub_class.is_a])
                    return get_descendants(sub_class, level + 1)

            restrictions = []

            return [*set([*self.cls.descendants()] + restrictions)]


class Ontology:

    def __init__(self, file_path, onto_file_name):
        self.ontology = get_ontology(file_path + onto_file_name).load()

    def get_equivalentTo_axioms(self, prefixes):
        equivalentTo_axioms = pd.DataFrame(columns=['Class Name',
                                                    'Class', 'Definitions',
                                                    'Class Labels', 'Definitions Labels'])
        class_and_property_labels = {}
        for cls in self.ontology.classes():
            onto_class = OntologyClass(iri=cls.iri, cls=cls)
            if cls.equivalent_to:
                cls_label = onto_class.get_annotations()
                labels = []
                for d in cls.equivalent_to:
                    labeled_expr = POWL2expr(clean_expr(d, prefixes))
                    classes_1, properties_1 = signature(labeled_expr)
                    for el in classes_1.union(properties_1):
                        if el in class_and_property_labels:
                            labeled_expr = labeled_expr.replace(el, class_and_property_labels[el])
                        else:
                            class_and_property_labels[el] = rdfs.label[self.ontology.search(iri=f"*{el}")[0]][0]
                            labeled_expr = labeled_expr.replace(el, class_and_property_labels[el])
                    labels.append(labeled_expr)
                equivalentTo_axioms.loc[len(equivalentTo_axioms)] = [cls.name, cls, cls.equivalent_to,
                                                                     cls_label[0], labels]
        return equivalentTo_axioms

    def get_expr_labels(self, expr):
        expr_with_labels = expr
        classes, properties = signature(expr)
        for el in classes.union(properties):
            if el == 'T':
                expr_with_labels = expr_with_labels.replace('T', "Thing")
            expr_with_labels = expr_with_labels.replace(el, rdfs.label[self.ontology.search(iri=f"*{el}")[0]][0])
        return expr_with_labels

    def __str__(self):
        return f"ontology={self.ontology}"
