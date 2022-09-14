from RSTAB.initModel import Model, clearAtributes
from RSTAB.enums import ModalNumberOfModes, ModalSolutionMethod, ModalMassConversionType, ModalMassMatrixType, ModalNeglectMasses

class ModalAnalysisSettings():

    def __init__(self,
                 no: int = 1,
                 name: str = 'Modal Analysis Sett',
                 number_of_modes_method = ModalNumberOfModes.NUMBER_OF_MODES_METHOD_USER_DEFINED,
                 number_of_modes : int = 4,
                 solution_method = ModalSolutionMethod.SOLUTION_METHOD_SHIFTED_INVERSE_POWER_METHOD,
                 find_modes_beyond_frequency: bool = False,
                 frequency_f: float = 10,
                 maxmimum_natural_frequency: float = 1700,
                 effective_modal_mass_factor: float = 0.85,
                 mass_matrix_type = ModalMassMatrixType.MASS_MATRIX_TYPE_CONSISTENT,
                 mass_conversion_type = ModalMassConversionType.MASS_CONVERSION_TYPE_Z_COMPONENTS_OF_LOADS,
                 acting_masses: list = None,
                 neglect_masses = ModalNeglectMasses.E_NEGLECT_MASSES_NO_NEGLECTION,
                 comment: str = '',
                 params: dict = None,
                 model = Model):
        """
        Args:
            no (int): Setting Tag
            name (str): Setting Name
            solution_method (enum): Modal Solution Method Enumeration
            mass_conversion_type (enum): Modal Mass Conversion Type Enumeration
            mass_matrix_type (enum): Modal Mass Matrix Type Enumeration
            number_of_modes (int): Number of Modes
            acting_masses (list): Acting Masses Directions List
            neglect_masses (enum): Modal Neglect Masses Enumeration
            comment (str, optional): Comment
            params (dict, optional): Any WS Parameter relevant to the object and its value in form of a dictionary
            model (RSTAB Class, optional): Model to be edited
        """
        # Client model | Surface
        clientObject = model.clientModel.factory.create('ns0:modal_analysis_settings')

        # Clears object atributes | Sets all atributes to None
        clearAtributes(clientObject)

        # Static Analysis Settings No.
        clientObject.no = no

        # Method for Dertermining the Number of Nodes
        clientObject.number_of_modes_method = number_of_modes_method.name

        # Analysis Type
        clientObject.solution_method = solution_method.name

        # Modes beyond frequency
        if number_of_modes_method == ModalNumberOfModes.NUMBER_OF_MODES_METHOD_USER_DEFINED:
            clientObject.number_of_modes = number_of_modes
            clientObject.find_eigenvectors_beyond_frequency = find_modes_beyond_frequency
            if find_modes_beyond_frequency:
                clientObject.frequency = frequency_f
        elif number_of_modes_method == ModalNumberOfModes.NUMBER_OF_MODES_METHOD_EFFECTIVE_MASS_FACTORS:
            clientObject.effective_modal_mass_factor = effective_modal_mass_factor
        elif number_of_modes_method == ModalNumberOfModes.NUMBER_OF_MODES_METHOD_MAXIMUM_FREQUENCY:
            clientObject.maxmimum_natural_frequency = maxmimum_natural_frequency
            clientObject.find_eigenvectors_beyond_frequency = find_modes_beyond_frequency
            if find_modes_beyond_frequency:
                clientObject.frequency = frequency_f

        # Acting Masses
        if len(acting_masses) == 6:
            clientObject.acting_masses_about_axis_x_enabled = acting_masses[0]
            clientObject.acting_masses_about_axis_y_enabled = acting_masses[1]
            clientObject.acting_masses_about_axis_z_enabled = acting_masses[2]
            clientObject.acting_masses_in_direction_x_enabled = acting_masses[3]
            clientObject.acting_masses_in_direction_y_enabled = acting_masses[4]
            clientObject.acting_masses_in_direction_z_enabled = acting_masses[5]
        else:
            raise Exception('WARNING: The acting masses array needs to be of length 6. Kindly check list inputs for completeness and correctness.')

        # Name
        if name:
            clientObject.user_defined_name_enabled = True
            clientObject.name = name

        # Mass Conversion Type
        clientObject.mass_conversion_type = mass_conversion_type.name

        # Mass Matrix Type
        clientObject.mass_matrix_type = mass_matrix_type.name

        # Neglect Masses
        clientObject.neglect_masses = neglect_masses.name

        # Comment
        clientObject.comment = comment

        # Adding optional parameters via dictionary
        if params:
            for key in params:
                clientObject[key] = params[key]

        # Add Static Analysis Settings to client model
        model.clientModel.service.set_modal_analysis_settings(clientObject)
