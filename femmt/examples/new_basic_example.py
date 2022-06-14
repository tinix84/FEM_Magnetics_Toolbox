import femmt as fmt
import numpy as np
from femmt.femmt_windings import *
from femmt.femmt_air_gaps import *

geo = fmt.MagneticComponent(component_type="transformer")

geo.core.update(window_h=0.0295, window_w=0.012, core_w=0.015,
                mu_rel=3100, phi_mu_deg=12,
                sigma=0.6)

# Add air gaps
air_gaps = AirGaps(AirGapMethod.Percent)
air_gaps.add_air_gap(AirGapLegPosition.CenterLeg, 50, 0.0005)
geo.air_gaps.update(**air_gaps.get_all_parameters())

# Add windings
windings = Windings()
windings.add_core_isolations(0.001, 0.001, 0.002, 0.001)
windings.add_winding_isolations(0.0002, 0.0002, 0.0005)

winding1 = Winding(10, 0, Conductivity.Copper, WindingType.Primary, WindingScheme.Square)
winding1.set_solid_conductor(0.0011)

winding2 = Winding(0, 10, Conductivity.Copper, WindingType.Secondary, WindingScheme.Square)
winding2.set_litz_conductor(None, 600, 35.5e-6, 0.6)

windings.add_windings([winding1, winding2])
geo.update_conductors(**windings.get_all_parameters())

# Create model
geo.create_model(freq=250000, visualize_before=True)
geo.single_simulation(freq=250000, current=[4.14723021, 14.58960019], phi_deg=[- 1.66257715/np.pi*180, 170])