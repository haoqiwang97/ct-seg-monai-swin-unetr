import pathlib
from zipfile import ZipFile
import monai.deploy.core as md
from monai.deploy.core import DataPath, ExecutionContext, Image, InputContext, IOType, Operator, OutputContext
from monai.deploy.operators.monai_seg_inference_operator import InMemImageReader, MonaiSegInferenceOperator
@md.input("zip_archive", DataPath, IOType.DISK)
@md.output("unzip_folder", DataPath, IOType.DISK)
class UnzipOperator(Operator):
    """This operator unzip a zip archive."""

    def compute(
        self,
        op_input: InputContext,
        op_output: OutputContext,
        context: ExecutionContext,
    ):
        """Performs computation for this operator and handlesI/O."""

        input_path = pathlib.Path(op_input.get().path)
        print(input_path)
        zfile_path = next(input_path.glob("*.zip"))  # take the first file
        print(zfile_path)
        if ZipFile(zfile_path).testzip() is not None:
            raise ValueError("input_path is corrupted or is not a zip file.")

        # Input path of the zip file is:
        # /flywheel/v0/input/input-file/AP Detector_1.zip'
        # Output path of the unzipped file is:
        # /flywheel/v0/input/input-file/AP Detector_1/dicom_file.dcm
        # the code below generates the folder path of the unzipped file

        with ZipFile(zfile_path, "r") as zip_file:
            zip_file.extractall(input_path)
        unzip_folder = zfile_path.parent / zfile_path.stem
        op_output.set(DataPath(unzip_folder), "unzip_folder")
