from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, requantification: typing.Optional[bool], identification: typing.Optional[bool], parallel_linking: typing.Optional[bool], ms2_use_feature_ionization: typing.Optional[bool], sirius_sirius_no_recalibration: typing.Optional[bool], sirius_sirius_db: typing.Optional[str], sirius_runpassatutto: typing.Optional[bool], sirius_fingerid_db: typing.Optional[str], sirius_email: typing.Optional[str], sirius_password: typing.Optional[str], sirius_split: typing.Optional[bool], run_ms2query: typing.Optional[bool], sirius_runfid: typing.Optional[bool], run_sirius: typing.Optional[bool], algorithm_metabolitefeaturedeconvolution_intensity_filter_metaboliteadductdecharger_openms: typing.Optional[bool], algorithm_pairfinder_ignore_charge_mapalignerposeclustering_openms: typing.Optional[bool], extract_mz_window_featurefindermetaboident_openms: typing.Optional[float], extract_n_isotopes_featurefindermetaboident_openms: typing.Optional[int], detect_peak_width_featurefindermetaboident_openms: typing.Optional[float], emgscoring_max_iteration_featurefindermetaboident_openms: typing.Optional[int], emgscoring_init_mom_featurefindermetaboident_openms: typing.Optional[bool], algorithm_signal_to_noise_peakpickerhires_openms: typing.Optional[float], algorithm_ffm_mz_scoring_13c_featurefindermetabo_openms: typing.Optional[bool], input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], multiqc_methods_description: typing.Optional[str], polarity: typing.Optional[str], ms2_collection_model: typing.Optional[str], mz_tolerance_pyopenms: typing.Optional[float], rt_tolerance_pyopenms: typing.Optional[float], sirius_sirius_ppm_max: typing.Optional[float], sirius_sirius_ppm_max_ms2: typing.Optional[float], sirius_sirius_profile: typing.Optional[str], sirius_sirius_candidates: typing.Optional[int], sirius_sirius_candidates_per_ion: typing.Optional[int], sirius_sirius_ions_considered: typing.Optional[str], split_consensus_parts: typing.Optional[int], algorithm_metabolitefeaturedeconvolution_charge_min_metaboliteadductdecharger_openms: typing.Optional[int], algorithm_metabolitefeaturedeconvolution_charge_max_metaboliteadductdecharger_openms: typing.Optional[int], algorithm_metabolitefeaturedeconvolution_charge_span_max_metaboliteadductdecharger_openms: typing.Optional[int], algorithm_metabolitefeaturedeconvolution_q_try_metaboliteadductdecharger_openms: typing.Optional[str], algorithm_metabolitefeaturedeconvolution_retention_max_diff_metaboliteadductdecharger_openms: typing.Optional[float], algorithm_metabolitefeaturedeconvolution_retention_max_diff_local_metaboliteadductdecharger_openms: typing.Optional[float], algorithm_metabolitefeaturedeconvolution_mass_max_diff_metaboliteadductdecharger_openms: typing.Optional[float], algorithm_metabolitefeaturedeconvolution_unit_metaboliteadductdecharger_openms: typing.Optional[str], algorithm_metabolitefeaturedeconvolution_max_neutrals_metaboliteadductdecharger_openms: typing.Optional[int], algorithm_metabolitefeaturedeconvolution_use_minority_bound_metaboliteadductdecharger_openms: typing.Optional[bool], algorithm_metabolitefeaturedeconvolution_max_minority_bound_metaboliteadductdecharger_openms: typing.Optional[int], algorithm_metabolitefeaturedeconvolution_min_rt_overlap_metaboliteadductdecharger_openms: typing.Optional[float], adducts_pos: typing.Optional[str], adducts_neg: typing.Optional[str], algorithm_max_num_peaks_considered_mapalignerposeclustering_openms: typing.Optional[int], algorithm_superimposer_mz_pair_max_distance_mapalignerposeclustering_openms: typing.Optional[float], algorithm_superimposer_num_used_points_mapalignerposeclustering_openms: typing.Optional[int], algorithm_pairfinder_distance_rt_max_difference_mapalignerposeclustering_openms: typing.Optional[float], algorithm_pairfinder_distance_mz_max_difference_mapalignerposeclustering_openms: typing.Optional[float], algorithm_pairfinder_distance_mz_unit_mapalignerposeclustering_openms: typing.Optional[str], algorithm_mz_unit_featurelinkerunlabeledkd_openms: typing.Optional[str], algorithm_nr_partitions_featurelinkerunlabeledkd_openms: typing.Optional[int], algorithm_warp_enabled_featurelinkerunlabeledkd_openms: typing.Optional[bool], algorithm_warp_rt_tol_featurelinkerunlabeledkd_openms: typing.Optional[float], algorithm_warp_mz_tol_featurelinkerunlabeledkd_openms: typing.Optional[float], algorithm_link_rt_tol_featurelinkerunlabeledkd_openms: typing.Optional[float], algorithm_link_mz_tol_featurelinkerunlabeledkd_openms: typing.Optional[float], algorithm_link_charge_merging_featurelinkerunlabeledkd_openms: typing.Optional[str], algorithm_link_adduct_merging_featurelinkerunlabeledkd_openms: typing.Optional[str], model_type_featurefindermetaboident_openms: typing.Optional[str], algorithm_common_noise_threshold_int_featurefindermetabo_openms: typing.Optional[float], algorithm_common_chrom_peak_snr_featurefindermetabo_openms: typing.Optional[float], algorithm_common_chrom_fwhm_featurefindermetabo_openms: typing.Optional[float], algorithm_mtd_mass_error_ppm_featurefindermetabo_openms: typing.Optional[float], algorithm_mtd_reestimate_mt_sd_featurefindermetabo_openms: typing.Optional[bool], algorithm_mtd_quant_method_featurefindermetabo_openms: typing.Optional[str], algorithm_epd_enabled_featurefindermetabo_openms: typing.Optional[bool], algorithm_epd_width_filtering_featurefindermetabo_openms: typing.Optional[str], algorithm_ffm_enable_rt_filtering_featurefindermetabo_openms: typing.Optional[bool], algorithm_ffm_isotope_filtering_model_featurefindermetabo_openms: typing.Optional[str]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('requantification', requantification),
                *get_flag('identification', identification),
                *get_flag('polarity', polarity),
                *get_flag('parallel_linking', parallel_linking),
                *get_flag('ms2_collection_model', ms2_collection_model),
                *get_flag('mz_tolerance_pyopenms', mz_tolerance_pyopenms),
                *get_flag('rt_tolerance_pyopenms', rt_tolerance_pyopenms),
                *get_flag('ms2_use_feature_ionization', ms2_use_feature_ionization),
                *get_flag('sirius_sirius_ppm_max', sirius_sirius_ppm_max),
                *get_flag('sirius_sirius_ppm_max_ms2', sirius_sirius_ppm_max_ms2),
                *get_flag('sirius_sirius_no_recalibration', sirius_sirius_no_recalibration),
                *get_flag('sirius_sirius_profile', sirius_sirius_profile),
                *get_flag('sirius_sirius_candidates', sirius_sirius_candidates),
                *get_flag('sirius_sirius_candidates_per_ion', sirius_sirius_candidates_per_ion),
                *get_flag('sirius_sirius_ions_considered', sirius_sirius_ions_considered),
                *get_flag('sirius_sirius_db', sirius_sirius_db),
                *get_flag('sirius_runpassatutto', sirius_runpassatutto),
                *get_flag('sirius_fingerid_db', sirius_fingerid_db),
                *get_flag('sirius_email', sirius_email),
                *get_flag('sirius_password', sirius_password),
                *get_flag('sirius_split', sirius_split),
                *get_flag('split_consensus_parts', split_consensus_parts),
                *get_flag('run_ms2query', run_ms2query),
                *get_flag('sirius_runfid', sirius_runfid),
                *get_flag('run_sirius', run_sirius),
                *get_flag('algorithm_metabolitefeaturedeconvolution_charge_min_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_charge_min_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_charge_max_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_charge_max_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_charge_span_max_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_charge_span_max_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_q_try_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_q_try_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_retention_max_diff_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_retention_max_diff_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_retention_max_diff_local_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_retention_max_diff_local_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_mass_max_diff_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_mass_max_diff_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_unit_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_unit_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_max_neutrals_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_max_neutrals_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_use_minority_bound_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_use_minority_bound_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_max_minority_bound_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_max_minority_bound_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_min_rt_overlap_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_min_rt_overlap_metaboliteadductdecharger_openms),
                *get_flag('algorithm_metabolitefeaturedeconvolution_intensity_filter_metaboliteadductdecharger_openms', algorithm_metabolitefeaturedeconvolution_intensity_filter_metaboliteadductdecharger_openms),
                *get_flag('adducts_pos', adducts_pos),
                *get_flag('adducts_neg', adducts_neg),
                *get_flag('algorithm_max_num_peaks_considered_mapalignerposeclustering_openms', algorithm_max_num_peaks_considered_mapalignerposeclustering_openms),
                *get_flag('algorithm_superimposer_mz_pair_max_distance_mapalignerposeclustering_openms', algorithm_superimposer_mz_pair_max_distance_mapalignerposeclustering_openms),
                *get_flag('algorithm_superimposer_num_used_points_mapalignerposeclustering_openms', algorithm_superimposer_num_used_points_mapalignerposeclustering_openms),
                *get_flag('algorithm_pairfinder_ignore_charge_mapalignerposeclustering_openms', algorithm_pairfinder_ignore_charge_mapalignerposeclustering_openms),
                *get_flag('algorithm_pairfinder_distance_rt_max_difference_mapalignerposeclustering_openms', algorithm_pairfinder_distance_rt_max_difference_mapalignerposeclustering_openms),
                *get_flag('algorithm_pairfinder_distance_mz_max_difference_mapalignerposeclustering_openms', algorithm_pairfinder_distance_mz_max_difference_mapalignerposeclustering_openms),
                *get_flag('algorithm_pairfinder_distance_mz_unit_mapalignerposeclustering_openms', algorithm_pairfinder_distance_mz_unit_mapalignerposeclustering_openms),
                *get_flag('algorithm_mz_unit_featurelinkerunlabeledkd_openms', algorithm_mz_unit_featurelinkerunlabeledkd_openms),
                *get_flag('algorithm_nr_partitions_featurelinkerunlabeledkd_openms', algorithm_nr_partitions_featurelinkerunlabeledkd_openms),
                *get_flag('algorithm_warp_enabled_featurelinkerunlabeledkd_openms', algorithm_warp_enabled_featurelinkerunlabeledkd_openms),
                *get_flag('algorithm_warp_rt_tol_featurelinkerunlabeledkd_openms', algorithm_warp_rt_tol_featurelinkerunlabeledkd_openms),
                *get_flag('algorithm_warp_mz_tol_featurelinkerunlabeledkd_openms', algorithm_warp_mz_tol_featurelinkerunlabeledkd_openms),
                *get_flag('algorithm_link_rt_tol_featurelinkerunlabeledkd_openms', algorithm_link_rt_tol_featurelinkerunlabeledkd_openms),
                *get_flag('algorithm_link_mz_tol_featurelinkerunlabeledkd_openms', algorithm_link_mz_tol_featurelinkerunlabeledkd_openms),
                *get_flag('algorithm_link_charge_merging_featurelinkerunlabeledkd_openms', algorithm_link_charge_merging_featurelinkerunlabeledkd_openms),
                *get_flag('algorithm_link_adduct_merging_featurelinkerunlabeledkd_openms', algorithm_link_adduct_merging_featurelinkerunlabeledkd_openms),
                *get_flag('extract_mz_window_featurefindermetaboident_openms', extract_mz_window_featurefindermetaboident_openms),
                *get_flag('extract_n_isotopes_featurefindermetaboident_openms', extract_n_isotopes_featurefindermetaboident_openms),
                *get_flag('detect_peak_width_featurefindermetaboident_openms', detect_peak_width_featurefindermetaboident_openms),
                *get_flag('model_type_featurefindermetaboident_openms', model_type_featurefindermetaboident_openms),
                *get_flag('emgscoring_max_iteration_featurefindermetaboident_openms', emgscoring_max_iteration_featurefindermetaboident_openms),
                *get_flag('emgscoring_init_mom_featurefindermetaboident_openms', emgscoring_init_mom_featurefindermetaboident_openms),
                *get_flag('algorithm_signal_to_noise_peakpickerhires_openms', algorithm_signal_to_noise_peakpickerhires_openms),
                *get_flag('algorithm_common_noise_threshold_int_featurefindermetabo_openms', algorithm_common_noise_threshold_int_featurefindermetabo_openms),
                *get_flag('algorithm_common_chrom_peak_snr_featurefindermetabo_openms', algorithm_common_chrom_peak_snr_featurefindermetabo_openms),
                *get_flag('algorithm_common_chrom_fwhm_featurefindermetabo_openms', algorithm_common_chrom_fwhm_featurefindermetabo_openms),
                *get_flag('algorithm_mtd_mass_error_ppm_featurefindermetabo_openms', algorithm_mtd_mass_error_ppm_featurefindermetabo_openms),
                *get_flag('algorithm_mtd_reestimate_mt_sd_featurefindermetabo_openms', algorithm_mtd_reestimate_mt_sd_featurefindermetabo_openms),
                *get_flag('algorithm_mtd_quant_method_featurefindermetabo_openms', algorithm_mtd_quant_method_featurefindermetabo_openms),
                *get_flag('algorithm_epd_enabled_featurefindermetabo_openms', algorithm_epd_enabled_featurefindermetabo_openms),
                *get_flag('algorithm_epd_width_filtering_featurefindermetabo_openms', algorithm_epd_width_filtering_featurefindermetabo_openms),
                *get_flag('algorithm_ffm_enable_rt_filtering_featurefindermetabo_openms', algorithm_ffm_enable_rt_filtering_featurefindermetabo_openms),
                *get_flag('algorithm_ffm_isotope_filtering_model_featurefindermetabo_openms', algorithm_ffm_isotope_filtering_model_featurefindermetabo_openms),
                *get_flag('algorithm_ffm_mz_scoring_13c_featurefindermetabo_openms', algorithm_ffm_mz_scoring_13c_featurefindermetabo_openms),
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_metaboigniter", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_metaboigniter(requantification: typing.Optional[bool], identification: typing.Optional[bool], parallel_linking: typing.Optional[bool], ms2_use_feature_ionization: typing.Optional[bool], sirius_sirius_no_recalibration: typing.Optional[bool], sirius_sirius_db: typing.Optional[str], sirius_runpassatutto: typing.Optional[bool], sirius_fingerid_db: typing.Optional[str], sirius_email: typing.Optional[str], sirius_password: typing.Optional[str], sirius_split: typing.Optional[bool], run_ms2query: typing.Optional[bool], sirius_runfid: typing.Optional[bool], run_sirius: typing.Optional[bool], algorithm_metabolitefeaturedeconvolution_intensity_filter_metaboliteadductdecharger_openms: typing.Optional[bool], algorithm_pairfinder_ignore_charge_mapalignerposeclustering_openms: typing.Optional[bool], extract_mz_window_featurefindermetaboident_openms: typing.Optional[float], extract_n_isotopes_featurefindermetaboident_openms: typing.Optional[int], detect_peak_width_featurefindermetaboident_openms: typing.Optional[float], emgscoring_max_iteration_featurefindermetaboident_openms: typing.Optional[int], emgscoring_init_mom_featurefindermetaboident_openms: typing.Optional[bool], algorithm_signal_to_noise_peakpickerhires_openms: typing.Optional[float], algorithm_ffm_mz_scoring_13c_featurefindermetabo_openms: typing.Optional[bool], input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], multiqc_methods_description: typing.Optional[str], polarity: typing.Optional[str] = 'positive', ms2_collection_model: typing.Optional[str] = 'paired', mz_tolerance_pyopenms: typing.Optional[float] = 20, rt_tolerance_pyopenms: typing.Optional[float] = 5, sirius_sirius_ppm_max: typing.Optional[float] = 10, sirius_sirius_ppm_max_ms2: typing.Optional[float] = 10, sirius_sirius_profile: typing.Optional[str] = 'default', sirius_sirius_candidates: typing.Optional[int] = 10, sirius_sirius_candidates_per_ion: typing.Optional[int] = 1, sirius_sirius_ions_considered: typing.Optional[str] = '[M+H]+,[M+K]+,[M+Na]+,[M+H-H2O]+,[M+H-H4O2]+,[M+NH4]+,[M-H]-,[M+Cl]-,[M-H2O-H]-,[M+Br]-', split_consensus_parts: typing.Optional[int] = 20, algorithm_metabolitefeaturedeconvolution_charge_min_metaboliteadductdecharger_openms: typing.Optional[int] = 1, algorithm_metabolitefeaturedeconvolution_charge_max_metaboliteadductdecharger_openms: typing.Optional[int] = 1, algorithm_metabolitefeaturedeconvolution_charge_span_max_metaboliteadductdecharger_openms: typing.Optional[int] = 1, algorithm_metabolitefeaturedeconvolution_q_try_metaboliteadductdecharger_openms: typing.Optional[str] = 'feature', algorithm_metabolitefeaturedeconvolution_retention_max_diff_metaboliteadductdecharger_openms: typing.Optional[float] = 1, algorithm_metabolitefeaturedeconvolution_retention_max_diff_local_metaboliteadductdecharger_openms: typing.Optional[float] = 1, algorithm_metabolitefeaturedeconvolution_mass_max_diff_metaboliteadductdecharger_openms: typing.Optional[float] = 5, algorithm_metabolitefeaturedeconvolution_unit_metaboliteadductdecharger_openms: typing.Optional[str] = 'ppm', algorithm_metabolitefeaturedeconvolution_max_neutrals_metaboliteadductdecharger_openms: typing.Optional[int] = 1, algorithm_metabolitefeaturedeconvolution_use_minority_bound_metaboliteadductdecharger_openms: typing.Optional[bool] = True, algorithm_metabolitefeaturedeconvolution_max_minority_bound_metaboliteadductdecharger_openms: typing.Optional[int] = 1, algorithm_metabolitefeaturedeconvolution_min_rt_overlap_metaboliteadductdecharger_openms: typing.Optional[float] = 0.66, adducts_pos: typing.Optional[str] = 'H:+:0.6 Na:+:0.1 NH4:+:0.1 H-1O-1:+:0.1 H-3O-2:+:0.1', adducts_neg: typing.Optional[str] = 'H-1:-:0.8 H-3O-1:-:0.2', algorithm_max_num_peaks_considered_mapalignerposeclustering_openms: typing.Optional[int] = 1000, algorithm_superimposer_mz_pair_max_distance_mapalignerposeclustering_openms: typing.Optional[float] = 0.5, algorithm_superimposer_num_used_points_mapalignerposeclustering_openms: typing.Optional[int] = 2000, algorithm_pairfinder_distance_rt_max_difference_mapalignerposeclustering_openms: typing.Optional[float] = 100.0, algorithm_pairfinder_distance_mz_max_difference_mapalignerposeclustering_openms: typing.Optional[float] = 0.3, algorithm_pairfinder_distance_mz_unit_mapalignerposeclustering_openms: typing.Optional[str] = 'Da', algorithm_mz_unit_featurelinkerunlabeledkd_openms: typing.Optional[str] = 'ppm', algorithm_nr_partitions_featurelinkerunlabeledkd_openms: typing.Optional[int] = 100, algorithm_warp_enabled_featurelinkerunlabeledkd_openms: typing.Optional[bool] = True, algorithm_warp_rt_tol_featurelinkerunlabeledkd_openms: typing.Optional[float] = 100.0, algorithm_warp_mz_tol_featurelinkerunlabeledkd_openms: typing.Optional[float] = 5.0, algorithm_link_rt_tol_featurelinkerunlabeledkd_openms: typing.Optional[float] = 30, algorithm_link_mz_tol_featurelinkerunlabeledkd_openms: typing.Optional[float] = 10, algorithm_link_charge_merging_featurelinkerunlabeledkd_openms: typing.Optional[str] = 'With_charge_zero', algorithm_link_adduct_merging_featurelinkerunlabeledkd_openms: typing.Optional[str] = 'Any', model_type_featurefindermetaboident_openms: typing.Optional[str] = 'symmetric', algorithm_common_noise_threshold_int_featurefindermetabo_openms: typing.Optional[float] = 10, algorithm_common_chrom_peak_snr_featurefindermetabo_openms: typing.Optional[float] = 3, algorithm_common_chrom_fwhm_featurefindermetabo_openms: typing.Optional[float] = 5, algorithm_mtd_mass_error_ppm_featurefindermetabo_openms: typing.Optional[float] = 20, algorithm_mtd_reestimate_mt_sd_featurefindermetabo_openms: typing.Optional[bool] = True, algorithm_mtd_quant_method_featurefindermetabo_openms: typing.Optional[str] = 'area', algorithm_epd_enabled_featurefindermetabo_openms: typing.Optional[bool] = True, algorithm_epd_width_filtering_featurefindermetabo_openms: typing.Optional[str] = 'fixed', algorithm_ffm_enable_rt_filtering_featurefindermetabo_openms: typing.Optional[bool] = True, algorithm_ffm_isotope_filtering_model_featurefindermetabo_openms: typing.Optional[str] = 'metabolites (5% RMS)') -> None:
    """
    nf-core/metaboigniter

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, requantification=requantification, identification=identification, polarity=polarity, parallel_linking=parallel_linking, ms2_collection_model=ms2_collection_model, mz_tolerance_pyopenms=mz_tolerance_pyopenms, rt_tolerance_pyopenms=rt_tolerance_pyopenms, ms2_use_feature_ionization=ms2_use_feature_ionization, sirius_sirius_ppm_max=sirius_sirius_ppm_max, sirius_sirius_ppm_max_ms2=sirius_sirius_ppm_max_ms2, sirius_sirius_no_recalibration=sirius_sirius_no_recalibration, sirius_sirius_profile=sirius_sirius_profile, sirius_sirius_candidates=sirius_sirius_candidates, sirius_sirius_candidates_per_ion=sirius_sirius_candidates_per_ion, sirius_sirius_ions_considered=sirius_sirius_ions_considered, sirius_sirius_db=sirius_sirius_db, sirius_runpassatutto=sirius_runpassatutto, sirius_fingerid_db=sirius_fingerid_db, sirius_email=sirius_email, sirius_password=sirius_password, sirius_split=sirius_split, split_consensus_parts=split_consensus_parts, run_ms2query=run_ms2query, sirius_runfid=sirius_runfid, run_sirius=run_sirius, algorithm_metabolitefeaturedeconvolution_charge_min_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_charge_min_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_charge_max_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_charge_max_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_charge_span_max_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_charge_span_max_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_q_try_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_q_try_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_retention_max_diff_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_retention_max_diff_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_retention_max_diff_local_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_retention_max_diff_local_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_mass_max_diff_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_mass_max_diff_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_unit_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_unit_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_max_neutrals_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_max_neutrals_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_use_minority_bound_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_use_minority_bound_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_max_minority_bound_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_max_minority_bound_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_min_rt_overlap_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_min_rt_overlap_metaboliteadductdecharger_openms, algorithm_metabolitefeaturedeconvolution_intensity_filter_metaboliteadductdecharger_openms=algorithm_metabolitefeaturedeconvolution_intensity_filter_metaboliteadductdecharger_openms, adducts_pos=adducts_pos, adducts_neg=adducts_neg, algorithm_max_num_peaks_considered_mapalignerposeclustering_openms=algorithm_max_num_peaks_considered_mapalignerposeclustering_openms, algorithm_superimposer_mz_pair_max_distance_mapalignerposeclustering_openms=algorithm_superimposer_mz_pair_max_distance_mapalignerposeclustering_openms, algorithm_superimposer_num_used_points_mapalignerposeclustering_openms=algorithm_superimposer_num_used_points_mapalignerposeclustering_openms, algorithm_pairfinder_ignore_charge_mapalignerposeclustering_openms=algorithm_pairfinder_ignore_charge_mapalignerposeclustering_openms, algorithm_pairfinder_distance_rt_max_difference_mapalignerposeclustering_openms=algorithm_pairfinder_distance_rt_max_difference_mapalignerposeclustering_openms, algorithm_pairfinder_distance_mz_max_difference_mapalignerposeclustering_openms=algorithm_pairfinder_distance_mz_max_difference_mapalignerposeclustering_openms, algorithm_pairfinder_distance_mz_unit_mapalignerposeclustering_openms=algorithm_pairfinder_distance_mz_unit_mapalignerposeclustering_openms, algorithm_mz_unit_featurelinkerunlabeledkd_openms=algorithm_mz_unit_featurelinkerunlabeledkd_openms, algorithm_nr_partitions_featurelinkerunlabeledkd_openms=algorithm_nr_partitions_featurelinkerunlabeledkd_openms, algorithm_warp_enabled_featurelinkerunlabeledkd_openms=algorithm_warp_enabled_featurelinkerunlabeledkd_openms, algorithm_warp_rt_tol_featurelinkerunlabeledkd_openms=algorithm_warp_rt_tol_featurelinkerunlabeledkd_openms, algorithm_warp_mz_tol_featurelinkerunlabeledkd_openms=algorithm_warp_mz_tol_featurelinkerunlabeledkd_openms, algorithm_link_rt_tol_featurelinkerunlabeledkd_openms=algorithm_link_rt_tol_featurelinkerunlabeledkd_openms, algorithm_link_mz_tol_featurelinkerunlabeledkd_openms=algorithm_link_mz_tol_featurelinkerunlabeledkd_openms, algorithm_link_charge_merging_featurelinkerunlabeledkd_openms=algorithm_link_charge_merging_featurelinkerunlabeledkd_openms, algorithm_link_adduct_merging_featurelinkerunlabeledkd_openms=algorithm_link_adduct_merging_featurelinkerunlabeledkd_openms, extract_mz_window_featurefindermetaboident_openms=extract_mz_window_featurefindermetaboident_openms, extract_n_isotopes_featurefindermetaboident_openms=extract_n_isotopes_featurefindermetaboident_openms, detect_peak_width_featurefindermetaboident_openms=detect_peak_width_featurefindermetaboident_openms, model_type_featurefindermetaboident_openms=model_type_featurefindermetaboident_openms, emgscoring_max_iteration_featurefindermetaboident_openms=emgscoring_max_iteration_featurefindermetaboident_openms, emgscoring_init_mom_featurefindermetaboident_openms=emgscoring_init_mom_featurefindermetaboident_openms, algorithm_signal_to_noise_peakpickerhires_openms=algorithm_signal_to_noise_peakpickerhires_openms, algorithm_common_noise_threshold_int_featurefindermetabo_openms=algorithm_common_noise_threshold_int_featurefindermetabo_openms, algorithm_common_chrom_peak_snr_featurefindermetabo_openms=algorithm_common_chrom_peak_snr_featurefindermetabo_openms, algorithm_common_chrom_fwhm_featurefindermetabo_openms=algorithm_common_chrom_fwhm_featurefindermetabo_openms, algorithm_mtd_mass_error_ppm_featurefindermetabo_openms=algorithm_mtd_mass_error_ppm_featurefindermetabo_openms, algorithm_mtd_reestimate_mt_sd_featurefindermetabo_openms=algorithm_mtd_reestimate_mt_sd_featurefindermetabo_openms, algorithm_mtd_quant_method_featurefindermetabo_openms=algorithm_mtd_quant_method_featurefindermetabo_openms, algorithm_epd_enabled_featurefindermetabo_openms=algorithm_epd_enabled_featurefindermetabo_openms, algorithm_epd_width_filtering_featurefindermetabo_openms=algorithm_epd_width_filtering_featurefindermetabo_openms, algorithm_ffm_enable_rt_filtering_featurefindermetabo_openms=algorithm_ffm_enable_rt_filtering_featurefindermetabo_openms, algorithm_ffm_isotope_filtering_model_featurefindermetabo_openms=algorithm_ffm_isotope_filtering_model_featurefindermetabo_openms, algorithm_ffm_mz_scoring_13c_featurefindermetabo_openms=algorithm_ffm_mz_scoring_13c_featurefindermetabo_openms, input=input, outdir=outdir, email=email, multiqc_title=multiqc_title, multiqc_methods_description=multiqc_methods_description)

