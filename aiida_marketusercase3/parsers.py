"""
Parsers provided by aiida_marketusercase3.

Register parsers via the "aiida.parsers" entry point in setup.json.
"""
from aiida.common import exceptions
from aiida.engine import ExitCode
from aiida.orm import SinglefileData, ArrayData
from aiida.parsers.parser import Parser
from aiida.plugins import CalculationFactory
import pandas as pd
import numpy as np

UserCase3Calc = CalculationFactory("marketusercase3")

class UserCase3Parser(Parser):
    """
    Parser class for parsing output of calculation.
    """

    def __init__(self, node):
        """
        Initialize Parser instance

        Checks that the ProcessNode being passed was produced by a DiffCalculation.

        :param node: ProcessNode of calculation
        :param type node: :class:`aiida.orm.nodes.process.process.ProcessNode`
        """
        super().__init__(node)
        if not issubclass(node.process_class, UserCase3Calc):
            raise exceptions.ParsingError("Can only parse UserCase3 calculations")

    def parse(self, **kwargs):
        """
        Parse outputs, store results in database.

        :returns: an exit code, if parsing fails (or nothing if parsing succeeds)
        """
        
        # For now we don't do any output verification 
        #output_filename = self.node.get_option("output_filename")
        particle_area_file = "FSP-Lurederra_alumina-particle_area_flux.srp"
        particle_volume_file = "FSP-Lurederra_alumina-particle_volume_flux.srp"

        # Check that folder content is as expected
        files_retrieved = self.retrieved.list_object_names()
        files_expected = [particle_area_file, particle_volume_file]
        # Note: set(A) <= set(B) checks whether A is a subset of B
        if not set(files_expected) <= set(files_retrieved):
            self.logger.error(
                f"Found files '{files_retrieved}', expected to find '{files_expected}'"
            )
            return self.exit_codes.ERROR_MISSING_OUTPUT_FILES

        # # add output file
        # self.logger.info(f"Parsing '{output_filename}'")
        # with self.retrieved.open(output_filename, "rb") as handle:
        #     output_node = SinglefileData(file=handle)
        # self.out("marketusercase3", output_node)

        with self.retrieved.open(particle_area_file) as fh:
            area_file_data = pd.read_csv(fh,skiprows = 5, delim_whitespace = True)
        with self.retrieved.open(volume_file_data) as fh:
            volume_file_data = pd.read_csv(fh,skiprows = 5, delim_whitespace = True)
        volume_value = float(volume_file_data.columns[1])
        area_value = float(area_file_data.columns[1])
        particle_size = 6.0*1e9*volume_value/area_value


        #with self.retrieved.open("Monitor_progress-FSP-Lurederra_alumina.out") as fh:
        #    monitor_results = pd.read_csv(fh,
        #                      delim_whitespace=True,
        #                      skiprows=3,
        #                      usecols=[2,3],
        #                      header=None)
        #monitor_results.columns=['particle_area_flow',
        #                         'particle_volume_flow']
        #monitor_results['final_result'] = 6*1e9*monitor_results['particle_volume_flow'] / \
        #                                        monitor_results['particle_area_flow']
        
        results = ArrayData()
        #results.set_array('final_result', monitor_results.final_result.to_numpy())
        #results.set_array('particle_volume_flow', monitor_results.particle_volume_flow.to_numpy())
        #results.set_array('particle_area_flow', monitor_results.particle_area_flow.to_numpy())
        results.set_array('volume_flux', np.array(volume_value))
        results.set_array('area_flux', np.array(area_value))
        results.set_array('particle_size', np.array(particle_size))
        self.out("output", results)

        return ExitCode(0)
