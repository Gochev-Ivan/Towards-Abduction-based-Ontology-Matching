from Utils.utils import *


def analysis():
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    df_results = pd.DataFrame(columns=["Alignment",
                                       "mean(#E) | median(#E) | max(#E)",
                                       "mean(|E|) | median(|E|) | max(|E|)",
                                       "mean(#A) | median(#A) | max(#A)",
                                       "mean(#C) | median(#C) | max(#C)",
                                       "mean(t[s]) | median(t[s]) | max(t[s])"])

    # "#V(T1)", "#V(T2)", "#E(T1)", "#E(T2)", "BF(T1)", "BF(T2)", "t [s]"
    df_algo_eval = pd.DataFrame(columns=["Alignment",
                                         "mean(#V(T1)) | median(#V(T1)) | max(#V(T1))",
                                         "mean(#V(T2)) | median(#V(T2)) | max(#V(T2))",
                                         "mean(#E(T1)) | median(#E(T1)) | max(#E(T1))",
                                         "mean(#E(T2)) | median(#E(T2)) | max(#E(T2))",
                                         "mean(BF(T1)) | median(BF(T1)) | max(BF(T1))",
                                         "mean(BF(T2)) | median(BF(T2)) | max(BF(T2))",
                                         "mean(t[s]) | median(t[s]) | max(t[s])"])

    """
    eval_results_file = input("Input the file containing the results evaluation (.csv): ")
    eval_results = pd.read_csv(eval_results_file)

    algo_eval_file = input("Input the file containing the algorithm evaluation metrics (.csv): ")
    algo_eval = pd.read_csv(algo_eval_file)

    alignment_ontos = input("Input which ontologies are aligned: ")

    # eval_results_save_file = input("Input the file in which to save the results evaluation (.csv): ")
    # algo_eval_save_file = input("Input the file in which to save the algorithm evaluation (.pdf): ")
    """
    # ==================================================================================================================
    ncit_doid_df = pd.read_csv(r"C:\Users\goche\Desktop\ICKG2025\Implementation\Experiments\Results\ncit-doid_eval_results.csv")
    df_results.loc[len(df_results)] = \
        ["ncit-doid",
         f"{round(ncit_doid_df['#E'].mean(), 2)} | {round(ncit_doid_df['#E'].median(), 2)} | {round(ncit_doid_df['#E'].max(), 2)}",
         f"{round(ncit_doid_df['|E|'].mean(), 2)} | {round(ncit_doid_df['|E|'].median(), 2)} | {round(ncit_doid_df['|E|'].max(), 2)}",
         f"{round(ncit_doid_df['#A'].mean(), 2)} | {round(ncit_doid_df['#A'].median(), 2)} | {round(ncit_doid_df['#A'].max(), 2)}",
         f"{round(ncit_doid_df['#C'].mean(), 2)} | {round(ncit_doid_df['#C'].median(), 2)} | {round(ncit_doid_df['#C'].max(), 2)}",
         f"{round(ncit_doid_df['t[s]'].mean(), 2)} | {round(ncit_doid_df['t[s]'].median(), 2)} | {round(ncit_doid_df['t[s]'].max(), 2)}"]
    # ==================================================================================================================
    omim_ordo_df = pd.read_csv(r"C:\Users\goche\Desktop\ICKG2025\Implementation\Experiments\Results\omim-ordo_eval_results.csv")
    df_results.loc[len(df_results)] = \
        ["omim-ordo",
         f"{round(omim_ordo_df['#E'].mean(), 2)} | {round(omim_ordo_df['#E'].median(), 2)} | {round(omim_ordo_df['#E'].max(), 2)}",
         f"{round(omim_ordo_df['|E|'].mean(), 2)} | {round(omim_ordo_df['|E|'].median(), 2)} | {round(omim_ordo_df['|E|'].max(), 2)}",
         f"{round(omim_ordo_df['#A'].mean(), 2)} | {round(omim_ordo_df['#A'].median(), 2)} | {round(omim_ordo_df['#A'].max(), 2)}",
         f"{round(omim_ordo_df['#C'].mean(), 2)} | {round(omim_ordo_df['#C'].median(), 2)} | {round(omim_ordo_df['#C'].max(), 2)}",
         f"{round(omim_ordo_df['t[s]'].mean(), 2)} | {round(omim_ordo_df['t[s]'].median(), 2)} | {round(omim_ordo_df['t[s]'].max(), 2)}"]
    # ==================================================================================================================
    snomed_fma_body_df = pd.read_csv(r"C:\Users\goche\Desktop\ICKG2025\Implementation\Experiments\Results\snomed_body-fma_body_eval_results.csv")
    df_results.loc[len(df_results)] = \
        ["snomed-fma.body",
         f"{round(snomed_fma_body_df['#E'].mean(), 2)} | {round(snomed_fma_body_df['#E'].median(), 2)} | {round(snomed_fma_body_df['#E'].max(), 2)}",
         f"{round(snomed_fma_body_df['|E|'].mean(), 2)} | {round(snomed_fma_body_df['|E|'].median(), 2)} | {round(snomed_fma_body_df['|E|'].max(), 2)}",
         f"{round(snomed_fma_body_df['#A'].mean(), 2)} | {round(snomed_fma_body_df['#A'].median(), 2)} | {round(snomed_fma_body_df['#A'].max(), 2)}",
         f"{round(snomed_fma_body_df['#C'].mean(), 2)} | {round(snomed_fma_body_df['#C'].median(), 2)} | {round(snomed_fma_body_df['#C'].max(), 2)}",
         f"{round(snomed_fma_body_df['t[s]'].mean(), 2)} | {round(snomed_fma_body_df['t[s]'].median(), 2)} | {round(snomed_fma_body_df['t[s]'].max(), 2)}"]
    # ==================================================================================================================
    snomed_ncit_pharm_df = pd.read_csv(r"C:\Users\goche\Desktop\ICKG2025\Implementation\Experiments\Results\snomed-ncit_pharm_eval_results.csv")
    df_results.loc[len(df_results)] = \
        ["snomed-ncit.pharm",
         f"{round(snomed_ncit_pharm_df['#E'].mean(), 2)} | {round(snomed_ncit_pharm_df['#E'].median(), 2)} | {round(snomed_ncit_pharm_df['#E'].max(), 2)}",
         f"{round(snomed_ncit_pharm_df['|E|'].mean(), 2)} | {round(snomed_ncit_pharm_df['|E|'].median(), 2)} | {round(snomed_ncit_pharm_df['|E|'].max(), 2)}",
         f"{round(snomed_ncit_pharm_df['#A'].mean(), 2)} | {round(snomed_ncit_pharm_df['#A'].median(), 2)} | {round(snomed_ncit_pharm_df['#A'].max(), 2)}",
         f"{round(snomed_ncit_pharm_df['#C'].mean(), 2)} | {round(snomed_ncit_pharm_df['#C'].median(), 2)} | {round(snomed_ncit_pharm_df['#C'].max(), 2)}",
         f"{round(snomed_ncit_pharm_df['t[s]'].mean(), 2)} | {round(snomed_ncit_pharm_df['t[s]'].median(), 2)} | {round(snomed_ncit_pharm_df['t[s]'].max(), 2)}"]
    # ==================================================================================================================

    # df_results.loc[len(df_results)] = \
    #     [alignment_ontos,
    #      f"{round(eval_results['#E'].mean(), 2)} | {round(eval_results['#E'].median(), 2)} | {round(eval_results['#E'].max(), 2)}",
    #      f"{round(eval_results['|E|'].mean(), 2)} | {round(eval_results['|E|'].median(), 2)} | {round(eval_results['|E|'].max(), 2)}",
    #      f"{round(eval_results['#A'].mean(), 2)} | {round(eval_results['#A'].median(), 2)} | {round(eval_results['#A'].max(), 2)}",
    #      f"{round(eval_results['#C'].mean(), 2)} | {round(eval_results['#C'].median(), 2)} | {round(eval_results['#C'].max(), 2)}",
    #      f"{round(eval_results['t[s]'].mean(), 2)} | {round(eval_results['t[s]'].median(), 2)} | {round(eval_results['t[s]'].max(), 2)}"]

    # ==================================================================================================================
    ncit_doid_algo_df = pd.read_csv(r"C:\Users\goche\Desktop\ICKG2025\Implementation\Experiments\Results\ncit-doid_algo_eval.csv")
    df_algo_eval.loc[len(df_algo_eval)] = \
    ["ncit-doid",
     f"{round(ncit_doid_algo_df['#V(T1)'].mean(), 2)} | {round(ncit_doid_algo_df['#V(T1)'].median(), 2)} | {round(ncit_doid_algo_df['#V(T1)'].max(), 2)}",
     f"{round(ncit_doid_algo_df['#V(T2)'].mean(), 2)} | {round(ncit_doid_algo_df['#V(T2)'].median(), 2)} | {round(ncit_doid_algo_df['#V(T2)'].max(), 2)}",
     f"{round(ncit_doid_algo_df['#E(T1)'].mean(), 2)} | {round(ncit_doid_algo_df['#E(T1)'].median(), 2)} | {round(ncit_doid_algo_df['#E(T1)'].max(), 2)}",
     f"{round(ncit_doid_algo_df['#E(T2)'].mean(), 2)} | {round(ncit_doid_algo_df['#E(T2)'].median(), 2)} | {round(ncit_doid_algo_df['#E(T2)'].max(), 2)}",
     f"{round(ncit_doid_algo_df['BF(T1)'].mean(), 2)} | {round(ncit_doid_algo_df['BF(T1)'].median(), 2)} | {round(ncit_doid_algo_df['BF(T1)'].max(), 2)}",
     f"{round(ncit_doid_algo_df['BF(T2)'].mean(), 2)} | {round(ncit_doid_algo_df['BF(T2)'].median(), 2)} | {round(ncit_doid_algo_df['BF(T2)'].max(), 2)}",
     f"{round(ncit_doid_algo_df['t [s]'].mean(), 2)} | {round(ncit_doid_algo_df['t [s]'].median(), 2)} | {round(ncit_doid_algo_df['t [s]'].max(), 2)}"]
    # ==================================================================================================================
    omim_ordo_algo_df = pd.read_csv(r"C:\Users\goche\Desktop\ICKG2025\Implementation\Experiments\Results\omim-ordo_algo_eval.csv")
    df_algo_eval.loc[len(df_algo_eval)] = \
    ["omim-ordo",
     f"{round(omim_ordo_algo_df['#V(T1)'].mean(), 2)} | {round(omim_ordo_algo_df['#V(T1)'].median(), 2)} | {round(omim_ordo_algo_df['#V(T1)'].max(), 2)}",
     f"{round(omim_ordo_algo_df['#V(T2)'].mean(), 2)} | {round(omim_ordo_algo_df['#V(T2)'].median(), 2)} | {round(omim_ordo_algo_df['#V(T2)'].max(), 2)}",
     f"{round(omim_ordo_algo_df['#E(T1)'].mean(), 2)} | {round(omim_ordo_algo_df['#E(T1)'].median(), 2)} | {round(omim_ordo_algo_df['#E(T1)'].max(), 2)}",
     f"{round(omim_ordo_algo_df['#E(T2)'].mean(), 2)} | {round(omim_ordo_algo_df['#E(T2)'].median(), 2)} | {round(omim_ordo_algo_df['#E(T2)'].max(), 2)}",
     f"{round(omim_ordo_algo_df['BF(T1)'].mean(), 2)} | {round(omim_ordo_algo_df['BF(T1)'].median(), 2)} | {round(omim_ordo_algo_df['BF(T1)'].max(), 2)}",
     f"{round(omim_ordo_algo_df['BF(T2)'].mean(), 2)} | {round(omim_ordo_algo_df['BF(T2)'].median(), 2)} | {round(omim_ordo_algo_df['BF(T2)'].max(), 2)}",
     f"{round(omim_ordo_algo_df['t [s]'].mean(), 2)} | {round(omim_ordo_algo_df['t [s]'].median(), 2)} | {round(omim_ordo_algo_df['t [s]'].max(), 2)}"]
    # ==================================================================================================================
    snomed_fma_algo_df = pd.read_csv(r"C:\Users\goche\Desktop\ICKG2025\Implementation\Experiments\Results\snomed_body-fma_body_algo_eval.csv")
    df_algo_eval.loc[len(df_algo_eval)] = \
    ["snomed-fma.body",
     f"{round(snomed_fma_algo_df['#V(T1)'].mean(), 2)} | {round(snomed_fma_algo_df['#V(T1)'].median(), 2)} | {round(snomed_fma_algo_df['#V(T1)'].max(), 2)}",
     f"{round(snomed_fma_algo_df['#V(T2)'].mean(), 2)} | {round(snomed_fma_algo_df['#V(T2)'].median(), 2)} | {round(snomed_fma_algo_df['#V(T2)'].max(), 2)}",
     f"{round(snomed_fma_algo_df['#E(T1)'].mean(), 2)} | {round(snomed_fma_algo_df['#E(T1)'].median(), 2)} | {round(snomed_fma_algo_df['#E(T1)'].max(), 2)}",
     f"{round(snomed_fma_algo_df['#E(T2)'].mean(), 2)} | {round(snomed_fma_algo_df['#E(T2)'].median(), 2)} | {round(snomed_fma_algo_df['#E(T2)'].max(), 2)}",
     f"{round(snomed_fma_algo_df['BF(T1)'].mean(), 2)} | {round(snomed_fma_algo_df['BF(T1)'].median(), 2)} | {round(snomed_fma_algo_df['BF(T1)'].max(), 2)}",
     f"{round(snomed_fma_algo_df['BF(T2)'].mean(), 2)} | {round(snomed_fma_algo_df['BF(T2)'].median(), 2)} | {round(snomed_fma_algo_df['BF(T2)'].max(), 2)}",
     f"{round(snomed_fma_algo_df['t [s]'].mean(), 2)} | {round(snomed_fma_algo_df['t [s]'].median(), 2)} | {round(snomed_fma_algo_df['t [s]'].max(), 2)}"]
    # ==================================================================================================================
    snomed_ncit_algo_df = pd.read_csv(r"C:\Users\goche\Desktop\ICKG2025\Implementation\Experiments\Results\snomed-ncit_pharm_algo_eval.csv")
    df_algo_eval.loc[len(df_algo_eval)] = \
    ["snomed-ncit.pharm",
     f"{round(snomed_ncit_algo_df['#V(T1)'].mean(), 2)} | {round(snomed_ncit_algo_df['#V(T1)'].median(), 2)} | {round(snomed_ncit_algo_df['#V(T1)'].max(), 2)}",
     f"{round(snomed_ncit_algo_df['#V(T2)'].mean(), 2)} | {round(snomed_ncit_algo_df['#V(T2)'].median(), 2)} | {round(snomed_ncit_algo_df['#V(T2)'].max(), 2)}",
     f"{round(snomed_ncit_algo_df['#E(T1)'].mean(), 2)} | {round(snomed_ncit_algo_df['#E(T1)'].median(), 2)} | {round(snomed_ncit_algo_df['#E(T1)'].max(), 2)}",
     f"{round(snomed_ncit_algo_df['#E(T2)'].mean(), 2)} | {round(snomed_ncit_algo_df['#E(T2)'].median(), 2)} | {round(snomed_ncit_algo_df['#E(T2)'].max(), 2)}",
     f"{round(snomed_ncit_algo_df['BF(T1)'].mean(), 2)} | {round(snomed_ncit_algo_df['BF(T1)'].median(), 2)} | {round(snomed_ncit_algo_df['BF(T1)'].max(), 2)}",
     f"{round(snomed_ncit_algo_df['BF(T2)'].mean(), 2)} | {round(snomed_ncit_algo_df['BF(T2)'].median(), 2)} | {round(snomed_ncit_algo_df['BF(T2)'].max(), 2)}",
     f"{round(snomed_ncit_algo_df['t [s]'].mean(), 2)} | {round(snomed_ncit_algo_df['t [s]'].median(), 2)} | {round(snomed_ncit_algo_df['t [s]'].max(), 2)}"]
    # ==================================================================================================================

    # df_algo_eval.loc[len(df_algo_eval)] = [alignment_ontos,
    #                 f"{round(algo_eval['#V(T1)'].mean(), 2)} | {round(algo_eval['#V(T1)'].median(), 2)} | {round(algo_eval['#V(T1)'].max(), 2)}",
    #                 f"{round(algo_eval['#V(T2)'].mean(), 2)} | {round(algo_eval['#V(T2)'].median(), 2)} | {round(algo_eval['#V(T2)'].max(), 2)}",
    #                 f"{round(algo_eval['#E(T1)'].mean(), 2)} | {round(algo_eval['#E(T1)'].median(), 2)} | {round(algo_eval['#E(T1)'].max(), 2)}",
    #                 f"{round(algo_eval['#E(T2)'].mean(), 2)} | {round(algo_eval['#E(T2)'].median(), 2)} | {round(algo_eval['#E(T2)'].max(), 2)}",
    #                 f"{round(algo_eval['BF(T1)'].mean(), 2)} | {round(algo_eval['BF(T1)'].median(), 2)} | {round(algo_eval['BF(T1)'].max(), 2)}",
    #                 f"{round(algo_eval['BF(T2)'].mean(), 2)} | {round(algo_eval['BF(T2)'].median(), 2)} | {round(algo_eval['BF(T2)'].max(), 2)}",
    #                 f"{round(algo_eval['t [s]'].mean(), 2)} | {round(algo_eval['t [s]'].median(), 2)} | {round(algo_eval['t [s]'].max(), 2)}"]

    # fig, axs = plt.subplots(3, 2)
    #
    # sns.lineplot(data=algo_eval, x="#V(T1)", y="t [s]", errorbar=None, ax=axs[0][0])
    # sns.lineplot(data=algo_eval, x="#V(T2)", y="t [s]", errorbar=None, ax=axs[0][1])
    #
    # sns.lineplot(data=algo_eval, x="#E(T1)", y="t [s]", errorbar=None, ax=axs[1][0])
    # sns.lineplot(data=algo_eval, x="#E(T2)", y="t [s]", errorbar=None, ax=axs[1][1])
    #
    # sns.lineplot(data=algo_eval, x="BF(T1)", y="t [s]", errorbar=None, ax=axs[2][0])
    # sns.lineplot(data=algo_eval, x="BF(T2)", y="t [s]", errorbar=None, ax=axs[2][1])
    #
    # plt.show()

    print_df(df_results)
    print_df(df_algo_eval)
