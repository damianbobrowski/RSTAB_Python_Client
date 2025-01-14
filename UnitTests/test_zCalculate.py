import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from RSTAB.enums import OptimizationTargetValueType, AddOn, NodalSupportType, NodalLoadDirection, ActionCategoryType, ObjectTypes
from RSTAB.initModel import Model, client, SetAddonStatus,Calculate_all, CalculateSelectedCases
from RSTAB.Calculate.memberDivision import GetMemberDivisions, MemberDivision
from RSTAB.Calculate.optimizationSettings import OptimizationSettings
from RSTAB.BasicObjects.material import Material
from RSTAB.BasicObjects.section import Section
from RSTAB.BasicObjects.node import Node
from RSTAB.BasicObjects.member import Member
from RSTAB.TypesForNodes.nodalSupport import NodalSupport
from RSTAB.LoadCasesAndCombinations.staticAnalysisSettings import StaticAnalysisSettings
from RSTAB.LoadCasesAndCombinations.loadCase import LoadCase
from RSTAB.LoadCasesAndCombinations.loadCasesAndCombinations import LoadCasesAndCombinations
from RSTAB.Loads.nodalLoad import NodalLoad
import pytest

if Model.clientModel is None:
    Model()

def createmodel():
    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    Material(1, 'S235')

    Section(1, 'IPE 200')

    Node(1, 0.0, 0.0, 0.0)
    Node(2, 5.0, 0.0, 0.0)

    Member(1, 1, 2, 0.0, 1, 1)

    NodalSupport(1, '1', NodalSupportType.FIXED)

    LoadCasesAndCombinations(params = {"current_standard_for_combination_wizard": 6208})
    StaticAnalysisSettings.GeometricallyLinear(1, "Linear")
    LoadCase.StaticAnalysis(1, 'SW', True, 1, ActionCategoryType.ACTION_CATEGORY_PERMANENT_G, [True, 0, 0, 1])
    LoadCase.StaticAnalysis(2, 'SDL', True,  1, ActionCategoryType.ACTION_CATEGORY_PERMANENT_IMPOSED_GQ, [False])

    NodalLoad(1, 1, '2', NodalLoadDirection.LOAD_DIRECTION_GLOBAL_Z_OR_USER_DEFINED_W, 150*1000)
    Model.clientModel.service.finish_modification()

def test_calculate_specific():

    createmodel()
    messages = CalculateSelectedCases([1])

    assert messages
    assert  Model.clientModel.service.has_results(ObjectTypes.E_OBJECT_TYPE_LOAD_CASE.name, 1)
    assert not Model.clientModel.service.has_results(ObjectTypes.E_OBJECT_TYPE_LOAD_CASE.name, 2)

def test_calculate_all():

    createmodel()
    messages = Calculate_all()

    assert messages
    assert Model.clientModel.service.has_results(ObjectTypes.E_OBJECT_TYPE_LOAD_CASE.name, 1)
    assert Model.clientModel.service.has_results(ObjectTypes.E_OBJECT_TYPE_LOAD_CASE.name, 2)

# CAUTION:
# These tests needs to be executed last because they change global settings

@pytest.mark.skip(reason="Function disappeared from RSTAB.")
def test_mesh_settings():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    MemberDivision()

    control_mesh = GetMemberDivisions()
    assert control_mesh.number_of_divisions_for_special_types_of_members == 10

    Model.clientModel.service.finish_modification()

def test_optimization_settings():

    Model.clientModel.service.delete_all()
    Model.clientModel.service.begin_modification()

    SetAddonStatus(Model.clientModel, AddOn.cost_estimation_active)
    OptimizationSettings()

    Model.clientModel.service.finish_modification()

    opt_sett = OptimizationSettings.GetOptimizationSettings(1)

    assert opt_sett.active
    assert opt_sett.number_of_mutations_to_keep == 20
    assert opt_sett.target_value_type == OptimizationTargetValueType.MIN_TOTAL_WEIGHT.name

    # Testing model is closed at the end of the testing session to enable easier and cleaned restart of the unit tests.
    client.service.close_model(0, False)
