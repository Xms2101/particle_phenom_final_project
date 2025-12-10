import uproot
import awkward as ak
import numpy as np
import os

# ------------------------------------------------------------
# 1. Select branches to keep
# ------------------------------------------------------------
BRANCHES_TO_KEEP_MC = [
    "gamma1_E", "gamma2_E", "mc_vtx", "MasterAnaDev_vtx",
    "MasterAnaDev_muon_E","MasterAnaDev_muon_P","MasterAnaDev_muon_Px","MasterAnaDev_muon_Py","MasterAnaDev_muon_Pz","MasterAnaDev_muon_theta",
    "MasterAnaDev_pion_E","MasterAnaDev_pion_P","MasterAnaDev_pion_Px","MasterAnaDev_pion_Py","MasterAnaDev_pion_Pz","MasterAnaDev_pion_theta",
    "MasterAnaDev_minos_trk_qp", "MasterAnaDev_proton_score",
    "mc_incomingE", "pi0_E", "truth_muon_E", "truth_pi_E"]

BRANCHES_TO_KEEP_D = [
    "gamma1_E", "gamma2_E", "MasterAnaDev_vtx",
    "MasterAnaDev_muon_E","MasterAnaDev_muon_P","MasterAnaDev_muon_Px","MasterAnaDev_muon_Py","MasterAnaDev_muon_Pz","MasterAnaDev_muon_theta",
    "MasterAnaDev_pion_E","MasterAnaDev_pion_P","MasterAnaDev_pion_Px","MasterAnaDev_pion_Py","MasterAnaDev_pion_Pz","MasterAnaDev_pion_theta",
    "MasterAnaDev_minos_trk_qp", "MasterAnaDev_proton_score", "MasterAnaDev_pion_score", "MasterAnaDev_pion_score1", "MasterAnaDev_pion_score2", 
    "muon_track_cluster_ID_sz"]

# ------------------------------------------------------------
# 2. Slim a single file
# ------------------------------------------------------------
def slim_file(input_path, output_path, branches):
    print(f"Opening: {input_path}")

    with uproot.open(input_path) as f:
        # Find the tree automatically
        tree_name = "MasterAnaDev"   # Usually "tree" or "ana"
        tree = f[tree_name]

        # Check which requested branches exist
        available = [b for b in branches if b in tree.keys()]
        missing   = [b for b in branches if b not in tree.keys()]

        if missing:
            print("WARNING: Some branches not found:", missing)

        # Read the available branches
        print("Reading branches...")
        arr = tree.arrays(available, how=dict)

        # Convert to awkward array for writing
        ak_arr = ak.Array(arr)

        # Save the new slimmed tree
        print(f"Writing slimmed file → {output_path}")
        with uproot.recreate(output_path) as fout:
            fout[tree_name] = ak_arr

    print("Done!\n")



#slim_file("data/1p_data_24.root", "data/reconstructed/1p_data_snip_24.root", BRANCHES_TO_KEEP_D)


slim_file("data/1p_mc_7.root", "data/monte_carlo/1p_mc_snip_7.root", BRANCHES_TO_KEEP_MC)
