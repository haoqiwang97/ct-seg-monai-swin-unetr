#!/usr/bin/env python
"""The run script"""
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_ct_total_segmentator.parser import parse_config

log = logging.getLogger(__name__)


def main(context: GearToolkitContext) -> None:  # pragma: no cover
    """Parses config and run"""

    # Call parse_config to extract the args, kwargs from the context
    # (e.g. config.json).
#     input_file, use_fast, use_multilabel, compute_statistics, debug = parse_config(
#         context
#     )
    
    use_multilabel, debug = parse_config(
        context
    )
        

    # log.debug(f"input-file: {input_file}")
    # log.debug(f"use-fast:{use_fast}")
    log.debug(f"use-multilabel:{use_multilabel}")
    # log.debug(f"compute-statitics:{compute_statistics}")

    output_path = context.output_dir

#     additional_flags = []
#     if use_fast == True:
#         additional_flags.append("--fast")

    if use_multilabel == True:
        additional_flags.append("--ml")

#     if compute_statistics == True:
#         additional_flags.append("--statistics")

    cmd = [
        "python",
        "-i",
        "/var/monai/input",
        "-o",
        "/flywheel/v0/output,
        "-m /opt/monai/app/best_metric_model_gpu.ts",
    ]
    
    for flag in additional_flags:
        cmd.append(flag)

    log.info(f"Calling...\n{' '.join(cmd)}")

    process = subprocess.Popen(
        cmd, cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    # Stream the output from p.communicate so the user can monitor the progress continuously.
    # This approach is taken from:
    # https://gitlab.com/flywheel-io/flywheel-apps/nifti-to-dicom/-/blob/0.1.0/fw_gear_nifti_to_dicom/pixelmed.py
    while True:
        time.sleep(5)
        if process.poll() is None:
            output, _ = process.communicate()
            print(output.decode("utf-8").strip() + "\n")
        else:
            if process.returncode != 0:
                log.error(
                    f"Swin UNETR failed with exit_code: {process.returncode}"
                )
                raise SystemExit(1)
            else:
                log.info("Swin UNETR completed")
                # move combined segmentation to the output directory
                if use_multilabel == True:
                    seg_path = os.path.join(output_path, "combined_seg_output.nii")
                    cmd = ["mv", "/flywheel/v0/output.nii", seg_path]
                    subprocess.call(cmd)
                sys.exit(process.returncode)


# Only execute if file is run as main, not when imported by another module
if __name__ == "__main__":  # pragma: no cover
    # Get access to gear config, inputs, and sdk client if enabled.
    with GearToolkitContext() as gear_context:
        # Initialize logging, set logging level based on `debug` configuration
        # key in gear config.
        gear_context.init_logging()

        # Pass the gear context into main function defined above.
        main(gear_context)
