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

#    lo1 = pd.read_csv("outputmodel3/Monitor-Catalyst-LO1_7.out", delim_whitespace=True, skiprows=3, usecols=[2,4], header=None)
#    lo2 = pd.read_csv("outputmodel3/Monitor-Catalyst-LO2_7.out", delim_whitespace=True, skiprows=3, usecols=[2,4], header=None)
#    lo3 = pd.read_csv("outputmodel3/Monitor-Catalyst-LO3_7.out", delim_whitespace=True, skiprows=3, usecols=[2,4], header=None)
#    lo1.columns=['t','ch4']
#    lo2.columns=['t','ch4']
#    lo3.columns=['t','ch4']
#    outputs['Lightoff1Temperature'].set(lo1.t.to_numpy(),'K')
#    outputs['Lightoff1MethaneMassFraction'].set(lo1.ch4.to_numpy(),'-')
#    outputs['Lightoff2Temperature'].set(lo2.t.to_numpy(),'K')
#    outputs['Lightoff2MethaneMassFraction'].set(lo2.ch4.to_numpy(),'-')
#    outputs['Lightoff3Temperature'].set(lo3.t.to_numpy(),'K')
#    outputs['Lightoff3MethaneMassFraction'].set(lo3.ch4.to_numpy(),'-')

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

         # Check that folder content is as expected
        files_retrieved = self.retrieved.list_object_names()
        files_expected = ["Monitor-Catalyst-LO1_7.out",
                          "Monitor-Catalyst-LO2_7.out",
                          "Monitor-Catalyst-LO2_7.out" ]
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


        with self.retrieved.open("Monitor-Catalyst-LO1_7.out") as fh:
            lo1 = pd.read_csv(fh,
                              delim_whitespace=True,
                              skiprows=3,
                              usecols=[2,4],
                              header=None)
        with self.retrieved.open("Monitor-Catalyst-LO2_7.out") as fh:
            lo2 = pd.read_csv(fh,
                              delim_whitespace=True,
                              skiprows=3,
                              usecols=[2,4],
                              header=None)
        with self.retrieved.open("Monitor-Catalyst-LO3_7.out") as fh:
            lo3 = pd.read_csv(fh,
                              delim_whitespace=True,
                              skiprows=3,
                              usecols=[2,4],
                              header=None)
        lo1.columns=['t','ch4']
        lo2.columns=['t','ch4']
        lo3.columns=['t','ch4']
        
        results = ArrayData()
        
        results.set_array('Lightoff1Temperature', lo1.t.to_numpy())
        results.set_array('Lightoff1MethaneMassFraction', lo1.ch4.to_numpy())
        results.set_array('Lightoff2Temperature', lo2.t.to_numpy())
        results.set_array('Lightoff2MethaneMassFraction', lo2.ch4.to_numpy())
        results.set_array('Lightoff3Temperature', lo3.t.to_numpy())
        results.set_array('Lightoff3MethaneMassFraction', lo3.ch4.to_numpy())
        self.out("output", results)

        return ExitCode(0)
