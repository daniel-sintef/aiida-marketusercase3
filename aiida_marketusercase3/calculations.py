"""
Calculations provided by aiida_marketusercase3.

Register calculations via the "aiida.calculations" entry point in setup.json.
"""
import json

from aiida.common import datastructures
from aiida.engine import CalcJob
from aiida.orm import ArrayData, Dict, SinglefileData, Str

from aiida_marketusercase3.helpers import *


class MarketPlaceUsercase3Model3Calc(CalcJob):
    """AiiDA calculation plugin for marketplace UC3."""

    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        # yapf: disable
        super().define(spec)

        # new ports
        spec.input('user_inputs', valid_type=Dict, help='User inputs to the plugin')
        # if we want to get fancy, we can create a custom Dict object
        # which can auto-validate the inputs
        spec.input('job_uuid', valid_type=Str, help='A UUID to coordinate file transport.')

        spec.inputs['metadata']['options']['resources'].default = {
                                            'num_machines': 1,
                                            'num_mpiprocs_per_machine': 1,
                                            }
        spec.inputs['metadata']['options']['parser_name'].default = 'marketusercase3'
        #spec.input(
        #    "cas_file", valid_type=SinglefileData, help="Cas file"
        #)
        #spec.input(
        #    "dat_file", valid_type=SinglefileData, help="Dat file"
        #)
        spec.output(
            'output',
            valid_type=ArrayData,
            help='output of marketplace-uc3'
        )

        spec.exit_code(300, 'ERROR_MISSING_OUTPUT_FILES',
                message='Calculation did not produce all expected output files.')

    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files needed by
            the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        codeinfo = datastructures.CodeInfo()
        user_inputs = self.inputs.user_inputs

        input_json ="inputs.json"
        with folder.open(input_json, 'w') as fh:
            json.dump(user_inputs, fh)


        codeinfo = datastructures.CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid
        codeinfo.cmdline_params = ['2ddp', '-g', '-slurm', '-pinfiniband', '-t20', '-i', journal_filename]
        #codeinfo.stdout_name = self.metadata.options.output_filename

        # Prepare a `CalcInfo` to be returned to the engine
        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]

        #calcinfo.local_copy_list = [
        #    (
        #        self.inputs.cas_file.uuid,
        #        self.inputs.cas_file.filename,
        #        self.inputs.cas_file.filename,
        #    ),
        #    (
        #        self.inputs.dat_file.uuid,
        #        self.inputs.dat_file.filename,
        #        self.inputs.dat_file.filename,
        #    ),
        #]

        calcinfo.retrieve_list = ['results.json']

        return calcinfo

#class DiffCalculation(CalcJob):
#    """
#    AiiDA calculation plugin wrapping the diff executable.
#
#    Simple AiiDA plugin wrapper for 'diffing' two files.
#    """
#
#    @classmethod
#    def define(cls, spec):
#        """Define inputs and outputs of the calculation."""
#        super().define(spec)
#
#        # set default values for AiiDA options
#        spec.inputs["metadata"]["options"]["resources"].default = {
#            "num_machines": 1,
#            "num_mpiprocs_per_machine": 1,
#        }
#        spec.inputs["metadata"]["options"]["parser_name"].default = "marketusercase3"
#
#        # new ports
#        spec.input(
#            "metadata.options.output_filename", valid_type=str, default="patch.diff"
#        )
#        spec.input(
#            "parameters",
#            valid_type=DiffParameters,
#            help="Command line parameters for diff",
#        )
#        spec.input(
#            "file1", valid_type=SinglefileData, help="First file to be compared."
#        )
#        spec.input(
#            "file2", valid_type=SinglefileData, help="Second file to be compared."
#        )
#        spec.output(
#            "marketusercase3",
#            valid_type=SinglefileData,
#            help="diff between file1 and file2.",
#        )
#
#        spec.exit_code(
#            300,
#            "ERROR_MISSING_OUTPUT_FILES",
#            message="Calculation did not produce all expected output files.",
#        )
#
#    def prepare_for_submission(self, folder):
#        """
#        Create input files.
#
#        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files
#            needed by the calculation.
#        :return: `aiida.common.datastructures.CalcInfo` instance
#        """
#        codeinfo = datastructures.CodeInfo()
#        codeinfo.cmdline_params = self.inputs.parameters.cmdline_params(
#            file1_name=self.inputs.file1.filename, file2_name=self.inputs.file2.filename
#        )
#        codeinfo.code_uuid = self.inputs.code.uuid
#        codeinfo.stdout_name = self.metadata.options.output_filename
#        codeinfo.withmpi = self.inputs.metadata.options.withmpi
#
#        # Prepare a `CalcInfo` to be returned to the engine
#        calcinfo = datastructures.CalcInfo()
#        calcinfo.codes_info = [codeinfo]
#        calcinfo.local_copy_list = [
#            (
#                self.inputs.file1.uuid,
#                self.inputs.file1.filename,
#                self.inputs.file1.filename,
#            ),
#            (
#                self.inputs.file2.uuid,
#                self.inputs.file2.filename,
#                self.inputs.file2.filename,
#            ),
#        ]
#        calcinfo.retrieve_list = [self.metadata.options.output_filename]
#
#        return calcinfo
#

class DummyMarketPlaceUsercase3Model3Calc(CalcJob):
    """Dummy calculation that dumps and receives json files to be used by other plugins"""

    @classmethod
    def define(cls, spec):
        """Define inputs and outputs of the calculation."""
        # yapf: disable
        super().define(spec)
        #super(MarketPlaceUsercase3Model3Calc, cls).define(spec)

        # new ports
        spec.input('user_inputs', valid_type=Dict, help='User inputs to the plugin')
        # if we want to get fancy, we can create a custom Dict object
        # which can auto-validate the inputs
        spec.input('job_uuid', valid_type=Str, help='User inputs to the plugin')

        spec.inputs['metadata']['options']['resources'].default = {
                                            'num_machines': 1,
                                            'num_mpiprocs_per_machine': 1,
                                            }
        spec.inputs['metadata']['options']['parser_name'].default = 'dummy_marketuc3'
        #spec.input(
        #    "cas_file", valid_type=SinglefileData, help="Cas file"
        #)
        #spec.input(
        #    "dat_file", valid_type=SinglefileData, help="Dat file"
        #)
        spec.output(
            'output',
            valid_type=ArrayData,
            help='output of marketplace-uc3'
        )

        spec.exit_code(300, 'ERROR_MISSING_OUTPUT_FILES',
                message='Calculation did not produce all expected output files.')

    def prepare_for_submission(self, folder):
        """
        Create input files.

        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files needed by
            the calculation.
        :return: `aiida.common.datastructures.CalcInfo` instance
        """
        codeinfo = datastructures.CodeInfo()
        user_inputs = self.inputs.user_inputs
        with folder.open('inputs.json', 'w') as fh:
            json.dump(dict(user_inputs), fh)

        job_uuid = self.inputs.job_uuid
        job_uuid_file = "JOB_UUID"
        with folder.open(job_uuid_file, 'w') as fh:
            fh.write(job_uuid.value)
            #json.dump(str(job_uuid.value.replace('"','')), fh)



        codeinfo = datastructures.CodeInfo()
        codeinfo.code_uuid = self.inputs.code.uuid

        calcinfo = datastructures.CalcInfo()
        calcinfo.codes_info = [codeinfo]

        calcinfo.retrieve_list = [('results.json')]

        return calcinfo

#class DiffCalculation(CalcJob):
#    """
#    AiiDA calculation plugin wrapping the diff executable.
#
#    Simple AiiDA plugin wrapper for 'diffing' two files.
#    """
#
#    @classmethod
#    def define(cls, spec):
#        """Define inputs and outputs of the calculation."""
#        super().define(spec)
#
#        # set default values for AiiDA options
#        spec.inputs["metadata"]["options"]["resources"].default = {
#            "num_machines": 1,
#            "num_mpiprocs_per_machine": 1,
#        }
#        spec.inputs["metadata"]["options"]["parser_name"].default = "marketusercase3"
#
#        # new ports
#        spec.input(
#            "metadata.options.output_filename", valid_type=str, default="patch.diff"
#        )
#        spec.input(
#            "parameters",
#            valid_type=DiffParameters,
#            help="Command line parameters for diff",
#        )
#        spec.input(
#            "file1", valid_type=SinglefileData, help="First file to be compared."
#        )
#        spec.input(
#            "file2", valid_type=SinglefileData, help="Second file to be compared."
#        )
#        spec.output(
#            "marketusercase3",
#            valid_type=SinglefileData,
#            help="diff between file1 and file2.",
#        )
#
#        spec.exit_code(
#            300,
#            "ERROR_MISSING_OUTPUT_FILES",
#            message="Calculation did not produce all expected output files.",
#        )
#
#    def prepare_for_submission(self, folder):
#        """
#        Create input files.
#
#        :param folder: an `aiida.common.folders.Folder` where the plugin should temporarily place all files
#            needed by the calculation.
#        :return: `aiida.common.datastructures.CalcInfo` instance
#        """
#        codeinfo = datastructures.CodeInfo()
#        codeinfo.cmdline_params = self.inputs.parameters.cmdline_params(
#            file1_name=self.inputs.file1.filename, file2_name=self.inputs.file2.filename
#        )
#        codeinfo.code_uuid = self.inputs.code.uuid
#        codeinfo.stdout_name = self.metadata.options.output_filename
#        codeinfo.withmpi = self.inputs.metadata.options.withmpi
#
#        # Prepare a `CalcInfo` to be returned to the engine
#        calcinfo = datastructures.CalcInfo()
#        calcinfo.codes_info = [codeinfo]
#        calcinfo.local_copy_list = [
#            (
#                self.inputs.file1.uuid,
#                self.inputs.file1.filename,
#                self.inputs.file1.filename,
#            ),
#            (
#                self.inputs.file2.uuid,
#                self.inputs.file2.filename,
#                self.inputs.file2.filename,
#            ),
#        ]
#        calcinfo.retrieve_list = [self.metadata.options.output_filename]
#
#        return calcinfo
#
