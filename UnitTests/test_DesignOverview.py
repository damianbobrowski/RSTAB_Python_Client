import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__),
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from RSTAB.enums import AddOn
from RSTAB.initModel import Model, SetAddonStatus, openFile,closeModel
from RSTAB.Results.designOverview import GetDesignOverview, GetPartialDesignOverview
from RSTAB.Reports.partsList import GetPartsListAllByMaterial, GetPartsListMemberRepresentativesByMaterial
from RSTAB.Reports.partsList import GetPartsListMemberSetsByMaterial, GetPartsListMembersByMaterial

if Model.clientModel is None:
    Model()

def test_designOverview():

    dirname = os.path.join(os.getcwd(), os.path.dirname(__file__))
    openFile(os.path.join(dirname, 'src', 'printout.rs9'))

    SetAddonStatus(Model.clientModel, AddOn.steel_design_active)
    Model.clientModel.service.calculate_all(False)

    designOverview = GetDesignOverview()

    assert round(designOverview[0][0].row['design_ratio']) == 0
    assert designOverview[0][0].row['design_check_type'] == 'SP4100.03'

    partialDesignOverview = GetPartialDesignOverview(False)
    assert len(partialDesignOverview) == 0

    partialDesignOverview = GetPartialDesignOverview(True)
    assert len(partialDesignOverview) == 3

    a = GetPartsListAllByMaterial()
    assert len(a[0]) == 3

    b = GetPartsListMemberRepresentativesByMaterial()
    assert b == ''

    c = GetPartsListMemberSetsByMaterial()
    assert c == ''

    d = GetPartsListMembersByMaterial()
    assert len(d[0][0].row) == 13
    assert d[0][0].row['members_no'] == '1'

    closeModel(1)
